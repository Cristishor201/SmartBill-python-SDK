from database import Database
import pdfplumber, re

class Process:
    def __init__(self, db_path, db_cache, db_language):
        self.__database = Database(db_path, db_cache, db_language)
        self.__re_invoice = {
            "seller_name": re.compile(r"\w+:\s(.+)\s{FACTURA}".format(FACTURA=self.__database.get_myLanguage().the_invoice)),
            "buyer_name": re.compile(r"{FACTURA}\s\w+:\s(.*)".format(FACTURA=self.__database.get_myLanguage().the_invoice)),
            "reg": (re.compile(r"([A-Z0-9]{3}/\d{2,5}/\d{4})(.*)"), re.compile(r"[A-Z0-9]{3}/\d{2,5}/\d{4}"))
        }

    def get_database(self):
        return self.__database

    def get_pdf_to_json(self, name, pdf_binary=None): #invoice
        #TODO - can i open binary directly ?
        path = self.__database.get_database_filepath()

        seller = {} ; buyer = {} ; final = {}
        iter_re_invoice = iter(self.__re_invoice.keys())
        re_item = next(iter_re_invoice)
        duplex = {
            "reg": 0
        }

        with pdfplumber.open(path + "/" + name) as pdf:
            pages = pdf.pages
            for page in pages:
                text = page.extract_text()
                for line in text.split("\n"):
                    print(line)
                    if re_item == "seller_name":
                        res = self.__re_invoice[re_item].search(line)
                        seller["name"] = res.group(1)
                        re_item = next(iter_re_invoice)
                    if re_item == "buyer_name":
                        res = self.__re_invoice[re_item].search(line)
                        buyer["name"] = res.group(1)
                        re_item = next(iter_re_invoice)
                    if re_item == "reg":
                        res = self.__re_invoice[re_item][0].findall(line) # first search reg + (something)
                        if len(res) == 1: #if found a match
                            if duplex[re_item] == 0:
                                seller[re_item] = res[0][0]
                                duplex[re_item] += 1 # 1
                                res2 = self.__re_invoice[re_item][1].search(res[0][1]) # search in (something)
                                if res2 != None: #if found second match on the same line
                                    buyer[re_item] = res2.group(0)
                                    duplex[re_item] += 1 # 2
                                    # re_item = next(iter_re_invoice)
                                else: # is the name sub-part
                                    buyer["name"] += res[0][1]
                            elif duplex[re_item] == 1: # if second reg is on another line
                                buyer[re_item] = res[0][0]
                                duplex[re_item] += 1 # 2
                                # re_item = next(iter_re_invoice)
                            else:
                                print("------Error ---- More than 2 Reg")
                    if re_item == "cif":
                        pass #TODO - cautat cif-uri

            final["seller"] = seller
            final["buyer"] = buyer


        return final

from database import Database
import pdfplumber, re

class Process:
    def __init__(self, db_path, db_cache, db_language, series):
        self.__database = Database(db_path, db_cache, db_language)
        invoice = self.__database.get_myLanguage().the_invoice
        cif = self.__database.get_myLanguage().cif
        address = self.__database.get_myLanguage().address

        self.__re_invoice = {
            "seller_name": re.compile(r"\w+:\s(.+)\s{FACTURA}".format(FACTURA=invoice)),
            "buyer_name": re.compile(r"{FACTURA}\s\w+:\s(.*)".format(FACTURA=invoice)),
            "reg": re.compile(r"[A-Z\d]{3}/\d{2,5}/\d{4}"),
            "cif": re.compile(r":\s?([a-zA-Z]{2}\d{6,8})\s"),
            "series": series,
            "address": (re.compile(r"{ADDRESS}:\s(.*),?\s{CIF}".format(ADDRESS=address, CIF=cif)),
                        re.compile(r"{ADDRESS}:\s(.*),?\s{ADDRESS}:\s(.*)".format(ADDRESS=address)),
                        address),
            "date": re.compile(r"\s(\d{2}/\d{2}/\d{4})"),
            "TVA": None, #TODO - TVA procent
            "iban": None, #TODO - ibanuri
            "bank": None, #TODO - banks
            "website": None, #TODO - website
            "phone": None, #TODO - phones seller
            "email": None, #TODO - mail seller + capital(tradus)
        }

    def get_database(self):
        return self.__database

    #DEPRECATED
    def __searching_dublicated(self, seller, buyer, duplex, re_item, line, _duplicate=None): #_duplicate is the name var for what is left from (something)
        res = self.__re_invoice[re_item][0].findall(line)  # first search reg/cif + (something)
        if len(res) == 1:  # if found a match
            #TODO - atentie atunci cand astept intre 2 dubluri, si mai am un camp de preluat
            if duplex[re_item] == 0:
                seller[re_item] = res[0][0]
                duplex[re_item] += 1  # 1
                res2 = self.__re_invoice[re_item][1].search(res[0][1])  # search in (something)
                if res2 != None:  # if found second match on the same line
                    buyer[re_item] = res2.group(0)
                    duplex[re_item] += 1  # 2
                    re_item = next(self.iter_re_invoice)
                else:  # is the name sub-part
                    if _duplicate != None:
                        buyer[_duplicate] += res[0][1]
            elif duplex[re_item] == 1:  # if second reg is on another line
                buyer[re_item] = res[0][0]
                duplex[re_item] += 1  # 2
                re_item = next(self.iter_re_invoice)
            else:
                print("------Error ---- More than 2 {0}".format(re_item))
        return [seller, buyer, duplex, re_item]

    def __extract_left_pattern(self, pattern, text):
        r = re.compile(r"(.*)\s({PATTERN})".format(PATTERN=pattern))
        result = r.search(text).group(1)
        return result

    def __extract_right_pattern(self, pattern, text):
        r = re.compile(r"{PATTERN}(.*)".format(PATTERN=pattern))
        r2 = re.compile(r"{PATTERN}".format(PATTERN=pattern))
        result = r.search(text).group(1)
        res = r2.search(result)
        if res is None: # double-check after another pattern on right
            return result
        else:
            return ""

    def get_pdf_to_json(self, name, id, pdf_binary=None): #invoice
        #TODO - can i open binary directly ?
        path = self.__database.get_database_filepath()

        seller = {} ; buyer = {} ; final = {}
        self.iter_re_invoice = iter(self.__re_invoice.keys())
        re_item = next(self.iter_re_invoice)
        duplex = {} ; is_next_address = False
        myTables = []

        with pdfplumber.open(path + "/" + name) as pdf:
            pages = pdf.pages
            for page in pages:
                # TODO - extras de fiecare data tabelul pt a extrage din el lista cumparaturi
                table2 = page.find_tables(table_settings={
                    "edge_min_length": 3,
                })[0].extract()
                print(table2)
                print(page.find_tables(table_settings={
                    "horizontal_strategy": "text",
                    "snap_y_tolerance": 5,
                    "keep_blank_chars": True,
                })[0]) #TODO - IMPOSIBIL sa separ liniile invizibile la lista cumparaturi -------------------!!


                #TODO - facut sa extraga aceste date doar 1 singura data in prima pagina (nu si in a doua)
                """
                myTable = list(table2[0].bbox)
                first_column_ext = 10 ; x1 = myTable[2]
                myTable[-1] = myTable[1] ; myTable[1] = 0 ; myTable[2] = myTable[2] / 3 + first_column_ext # first column
                myTables.append(myTable)

                myTable[0] = myTable[2] + first_column_ext ; myTable[2] = (myTable[2] - first_column_ext)*2 # second_column
                myTables.append(myTable)

                myTable[0] = myTable[2] + first_column_ext ; myTable[2] = x1 # third column
                myTables.append(myTable)
                print(myTable)
                text = page.crop(bbox=myTable).extract_text()
                print(text)
                """


                """
                text = page.extract_text()
                for line in text.split("\n"):
                    print("----------")
                    print(line)
                    if re_item == "seller_name":
                        res = self.__re_invoice[re_item].search(line)
                        seller["name"] = res.group(1)
                        re_item = next(self.iter_re_invoice)

                    if re_item == "buyer_name":
                        res = self.__re_invoice[re_item].search(line)
                        buyer["name"] = res.group(1)
                        re_item = next(self.iter_re_invoice)

                    if re_item == "reg":
                        res = self.__re_invoice[re_item].search(line) # filtering for the first Reg line
                        if res is not None:
                            res = self.__re_invoice[re_item].findall(text)
                            seller[re_item] = res[0]
                            buyer[re_item] = res[1]
                            buyer["name"] += self.__extract_right_pattern(pattern=self.__re_invoice[re_item].pattern, text=line)
                            re_item = next(self.iter_re_invoice)

                    if re_item == "cif":
                        res = self.__re_invoice[re_item].findall(text)
                        if len(res) == 2:
                            seller[re_item] = res[0]
                            buyer[re_item] = res[1]
                            re_item = next(self.iter_re_invoice)

                    if re_item == "series":
                        final[re_item] = (self.__re_invoice[re_item], id)
                        re_item = next(self.iter_re_invoice)

                    if re_item == "address":
                        res = self.__re_invoice[re_item][0].search(line) # Address + CIF on same line
                        if res is not None:
                            seller[re_item] = res.group(1)
                            re_item = next(self.iter_re_invoice)
                        else:
                            res = self.__re_invoice[re_item][1].search(line) # Address + Address on same line
                            if res is not None:
                                seller[re_item] = res.group(1)
                                buyer[re_item] = res.group(2)
                                re_item = next(self.iter_re_invoice)

                    if re_item == "date":
                        res = self.__re_invoice[re_item].search(line)  # filtering the line
                        if res is not None:
                            res = self.__re_invoice[re_item].findall(text)
                            final["date"] = res[0]
                            final["due_date"] = res[1]
                            re_item = next(self.iter_re_invoice)
                            is_next_address = True # very next line is the address
                            continue

                    if is_next_address == True:
                        address = self.__re_invoice["address"][2]
                        text = line.split(" {Address}: ".format(Address=address)) #TODO - modificarile ca sa folosesc split in loc de regex
                        seller["address"] += " " + text[0]
                        if len(text) == 2:
                            buyer["addss"] = text[1]
                        print(text)
                        is_next_address = False
                        #TODO - ? a doua adresa


                        #TODO - sa nu uit sa adaug a doua bucata pt ambele adrese
                """

            final["seller"] = seller
            final["buyer"] = buyer

        return final



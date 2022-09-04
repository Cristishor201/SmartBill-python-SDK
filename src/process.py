from database import Database

class Process:
    def __init__(self, db_path, db_cache):
        self.__database = Database(db_path, db_cache)

    def get_pdf_to_json(self, name, pdf_binary):
        self.__database.save_to_pdf("{filename}.pdf".format(filename=name), pdf_binary)
        return {} #return pdf to json

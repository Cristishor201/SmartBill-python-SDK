from database import Database

class Process:
    def __init__(self, db_name, db_path):
        self.__database = Database(db_name, db_path)

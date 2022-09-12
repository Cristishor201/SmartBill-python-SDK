import os
from datetime import datetime

class Database:
    def __init__(self, cache_path="_cache", keep_cache_days=30, myLanguage=[]):
        self.__path_input = cache_path
        self.__keep_cache_days = keep_cache_days
        self.__myLanguage = myLanguage #object
        self.delete_cache()

    def get_database_filepath(self):
        return self.__path_input

    def get_myLanguage(self):
        return self.__myLanguage

    def save_to_pdf(self, name, obj_binary):
        if self.__keep_cache_days != 0: # if cache_days is zero, don't save them
            url = "{0}/{1}".format(self.__path_input, name)
            with open(url, "wb") as file:
                file.write(obj_binary)

    def save_to_json(self, name, text):
        #TODO - mai multe jscon calls cu un rand spatiu / zi
        # exception FileNotFoundError: <if not exist>
        pass

    def is_filename(self, filename):
        files = os.listdir((self.__path_input))
        if filename in files:
            return True
        else:
            return False

    def delete_cache(self):
        if self.__keep_cache_days == -1:
            pass # never delete cache
        else:
            files = os.listdir((self.__path_input))
            for file in files:
                creation = datetime.fromtimestamp(os.path.getctime("{folder}/{file}".format(folder=self.__path_input, file=file)))
                right_now = datetime.now()
                delta = (right_now - creation).days
                if delta > self.__keep_cache_days:
                    os.remove("{path}/{file}".format(path=self.__path_input, file=file))
                    print("Eliberating cache...")

class Language():
    def __init__(self, the_invoice):
        self.the_invoice = the_invoice.upper() # translation for invoice
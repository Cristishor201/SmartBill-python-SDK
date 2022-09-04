import os
from datetime import datetime

class Database:
    def __init__(self, cache_path="_cache", keep_cache_days=30):
        self.__path_input = cache_path
        self.__keep_cache_days = keep_cache_days
        self.delete_cache()

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
        pass
    #TODO - daca fisiserul exista - true, altfel false
    #TODO - si-l fac sa fie accesibil din server, inainte de request

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
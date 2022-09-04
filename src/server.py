import json, requests
from requests.auth import HTTPBasicAuth
from process import Process
from os import environ

class Server:
    __credentials = {}
    def __init__(self, series, cache_path, keep_cache_days):
        #self.__headers = {"Content-Type": "application/json"} # for other operations
        self.__base_url = "https://ws.smartbill.ro/SBORO/api"

        self.__credentials["CUI"] = environ.get("CUI")
        self.__credentials["MAIL"] = environ.get("MAIL")
        self.__credentials["PASS"] = environ.get("TOKEN")

        self.series = series
        self.__process = Process(cache_path, keep_cache_days)
        self.__session = requests.Session()
        self.__session.auth = HTTPBasicAuth(self.__credentials["MAIL"], self.__credentials["PASS"])
        #self.__session.headers.update(self.__headers)

    def get_invoice(self, invoice_id): #factura n1
        headers = {"Accept": "application/octet-stream"}  # for view invoice
        url = "{base}/invoice/pdf?cif={cif}&seriesname={seriesname}&number={number}".format(base=self.__base_url, cif=self.__credentials["CUI"], seriesname=self.series, number=invoice_id)

        response = self.__session.get(url, headers=headers, timeout=10)
        return self.__process.get_pdf_to_json(name=self.series + str(invoice_id), pdf_binary=response.content) # pdf binary

    def __del__(self):
        self.__session.close()

"""
    @staticmethod
    def loadJson(name):
        with open(name, 'r') as file:
            data = json.loads(file.read())
        return data
"""
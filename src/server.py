import json, requests
from process import Process
from os import environ

class Server:
    def __init__(self, series, db_name, db_path):
        print(environ)
        self.__CUI = environ.get("CUI")
        self.__MAIL = environ.get("MAIL")
        self.__TOKEN = environ.get("TOKEN")
        self.series = series
        self.__process = Process(db_name, db_path)
        self.session = requests.Session()
        self.session.headers.update({'Authorization': "Bearer {}".format(self.__TOKEN)})

    def get_invoice(self, invoice_id): #factura n1
        url = "https://ws.smartbill.ro/SBORO/api/invoice/pdf?cif={cif}&seriesname={seriesname}&number={number}".format(cif=self.__CUI, seriesname=self.series, number=invoice_id)
        response = requests.get(url)
        print(response)


    @staticmethod
    def loadJson(name):
        with open(name, 'r') as file:
            data = json.loads(file.read())
        return data

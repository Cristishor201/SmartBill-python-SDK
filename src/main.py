# examples of using it
from server import Server
from database import Language
import os, json
from dotenv import load_dotenv

if __name__ == "__main__":
    #load_dotenv()
    mylanguage = Language(the_invoice="Factura", address="Adresa", cif="cif")

    mySmartBill = Server("ALL", cache_path="_cache", keep_cache_days=30, myLanguage=mylanguage) # replace path starting from src
    print(json.dumps(mySmartBill.get_invoice(26284), indent=4))
    #print("==============================================")
    #print(mySmartBill.get_invoice(26222))
    # 26284 - 2 pages

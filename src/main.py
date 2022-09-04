# examples of using it
from server import Server
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    #load_dotenv()
    mySmartBill = Server("ALL", cache_path="_cache", keep_cache_days=30) # replace path starting from src
    #print(mySmartBill.get_invoice(26221))

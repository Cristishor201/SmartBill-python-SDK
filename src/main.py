# examples of using it
from server import Server
import os
from dotenv import load_dotenv

#load_dotenv()
mySmartBill = Server("ALL", "db", "/")
print(mySmartBill.get_invoice(1))

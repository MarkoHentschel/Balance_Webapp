import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv("keyholder.env")
print (os.getenv("DETA_KEY"))
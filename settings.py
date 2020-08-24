import os
from dotenv import load_dotenv, find_dotenv  # for using .env file

load_dotenv(find_dotenv())

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

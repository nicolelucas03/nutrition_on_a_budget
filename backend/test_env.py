from dotenv import load_dotenv
import os

#THIS IS TO TEST IF THE API KEY IS LOADED
load_dotenv()
print(f"API Key loaded: {os.getenv('ANTRHOPIC_API_KEY')}")
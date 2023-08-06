import requests
import asyncio
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
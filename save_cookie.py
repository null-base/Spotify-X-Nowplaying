import asyncio
import os

from dotenv import load_dotenv
from twikit import Client

load_dotenv()

client = Client(language="ja",user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36')

async def main():
    # アカウントにログイン
    await client.login(
        auth_info_1=os.getenv("AUTH_INFO_1"),
        auth_info_2=os.getenv("AUTH_INFO_2"),
        password=os.getenv("PASSWORD"),
    )
    client.save_cookies("cookies.json")


asyncio.run(main())

import yfinance as yf
import pandas as pd
import requests
import apimoex
import asyncio
import asyncio

import aiohttp

import aiomoex
import pandas as pd


async def main():
    request_url = "https://iss.moex.com/iss/engines/stock/" "markets/shares/boards/TQBR/securities.json"
    arguments = {"securities.columns": ("SECID," "REGNUMBER," "LOTSIZE," "SHORTNAME")}

    async with aiohttp.ClientSession() as session:
        iss = aiomoex.ISSClient(session, request_url, arguments)
        data = await iss.get()
        df = pd.DataFrame(data["securities"])
        df.set_index("SECID", inplace=True)
        print(df.head(), "\n")
        print(df.tail(), "\n")
        df.info()


asyncio.run(main())





import re
import requests

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import currencies, CBU_URL

message_router = Router()

@message_router.message(F.text.isdigit())
async def exchange_handler(message: Message):
    print(message.text, message.from_user.username, message.from_user.first_name)
    x = int(message.text)
    s = f"{x} sums: \n"
    s += f"\t- {x / int(currencies['USD']['rate']): .2f} US dollars\n"
    s += f"\t- {x / int(currencies['EUR']['rate']): .2f} Euros\n"
    s += f"\t- {x / int(currencies['RUB']['rate']): .2f} Russian rubles\n\n"
    s += f"Cuurency rates fetched from <a href = '{CBU_URL}'>CBU API</a>"
    await message.reply(
        text=s,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text = 'Source',
                        url = CBU_URL
                    ),
                    InlineKeyboardButton(
                        text = 'Source',
                        url = CBU_URL
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='Author',
                        url = "https://imrasulovsanjar.com"
                    ),
                ]
            ]
        )
    )

@message_router.message(F.text)
async def usd_handler(message: Message):
    print(message.text, message.from_user.username, message.from_user.first_name)
    
    date_pattern = r'\b\d{4}-\d{2}-\d{2}\b'
    
    match1 = re.search(date_pattern, message.text)
    match2 = re.search(r'(\d+)', message.text)  
    if match1:
        date = match1.group()
        if 'dollar' or 'USD' in message.text:
            response = requests.get(f"{CBU_URL}USD/{date}/")
            res  = response.json()[0]
            s = f"In {date}:\n"
            s += f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
        if 'euro' in message.text:
            response = requests.get(f"{CBU_URL}EUR/{date}/")
            res  = response.json()[0]
            s = f"In {date}:\n"
            s += f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
        if 'ruble' in message.text:
            response = requests.get(f"{CBU_URL}RUB/{date}/")
            res  = response.json()[0]
            s = f"In {date}:\n"
            s += f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
    elif match2:
        amount = int(match2.group(1))
        if 'dollar' in message.text.lower() or '$' in message.text:
            s = f"{amount} dollars: \n"
            s += f"\t- {amount * int(currencies['USD']['rate']): .2f} uzbek sums\n"
        elif 'euro' in message.text.lower():
            s = f"{amount} euros: \n"
            s += f"\t- {amount * int(currencies['EUR']['rate']): .2f} uzbek sums\n"
        elif 'ruble' in message.text.lower():
            s = f"{amount} rubles: \n"
            s += f"\t- {amount * int(currencies['RUB']['rate']): .2f} uzbek sums\n"

    await message.reply(s)
    

    
    

    
    
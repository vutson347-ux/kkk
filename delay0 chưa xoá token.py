import asyncio
import aiohttp
import time
import os
import sys
import requests
from bs4 import BeautifulSoup
from pystyle import Colorate, Colors

def get_keys_from_anotepad():
    try:
        url = 'https://anotepad.com/notes/gfqyfhtw'  
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            note_content = soup.find('div', {'class': 'plaintext'})
            if note_content:
                keys = [line.strip() for line in note_content.get_text().strip().split('\n') if line.strip()]
                return keys
            else:
                print(' | Không có nội dung!')
                return []
        else:
            print(f' | Yêu cầu thất bại! : {response.status_code}')
            return []
    except Exception as e:
        print(f' | Lỗi khi lấy key: {e}')
        return []

async def get_channel_name(channel_id, token):
    url = f"https://discord.com/api/v9/channels/{channel_id}"
    headers = {
        "Authorization": token
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("name", "Unknown")
            else:
                return "Unknown"

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_info(msg): 
    print(Colorate.Horizontal(Colors.rainbow, f"[SYSTEM] {msg}"))

def log_success(msg): 
    print(Colorate.Horizontal(Colors.rainbow, f"[SYSTEM] {msg}"))

def log_warning(msg): 
    print(Colorate.Horizontal(Colors.rainbow, f"[SYSTEM] {msg}"))

def log_input(msg): 
    return input(Colorate.Horizontal(Colors.rainbow, f"[INPUT] {msg}"))

BANNER = """


██████╗░░█████╗░░█████╗░
██╔══██╗██╔══██╗██╔══██╗
██████╦╝███████║██║░░██║
██╔══██╗██╔══██║██║░░██║
██████╦╝██║░░██║╚█████╔╝
╚═════╝░╚═╝░░╚═╝░╚════╝░

██████╗░░█████╗░░█████╗░
██╔══██╗██╔══██╗██╔══██╗
██████╦╝███████║██║░░██║
██╔══██╗██╔══██║██║░░██║
██████╦╝██║░░██║╚█████╔╝
╚═════╝░╚═╝░░╚═╝░╚════╝░

Tool Spam Discord By CNB
"""

def mask_token(token):
    token = token.strip()
    if len(token) <= 10:
        return token
    return f"{token[:5]} *** {token[-5:]}"

async def mem_pool(token, link, id_channel, content, n_spam, n_delay, namechannel):
    token = str(token).strip()
    masked_token = mask_token(token)
    header_data = {
        "Authorization": token,
    }

    message_data = {
        "content": content,
        "tts": False
    }
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=header_data) as ses:
        while True:
            try:
                log_success(f" | Token {masked_token} | Send successfully [{namechannel}] - [{id_channel}]")
                for _ in range(n_spam):
                    try:
                        async with ses.post(url=f"https://discord.com/api/v9/channels/{str(id_channel)}/messages", data=message_data) as resp:
                            if 200 <= resp.status < 350:
                                pass
                    except:
                        log_warning(f" | Có lỗi xảy ra!")
            finally:
                await asyncio.sleep(n_delay)

async def action_pool(tokens, link, id_channel, content, n_spam, n_delay):
    print()
    log_info("Start")
    print()
    tasks = []
    
    first_token = tokens[0].strip()
    name_channel = await get_channel_name(id_channel, first_token)
    for token in tokens:
        token_str = token.strip()
        tasks.append(asyncio.create_task(mem_pool(token_str, link, id_channel, content, n_spam, n_delay, name_channel)))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    cls()
    print(Colorate.Horizontal(Colors.rainbow, BANNER))

    keys = get_keys_from_anotepad()
    if not keys:
        log_warning(" | Không thể lấy key bảo mật!")
        exit()

    user_key = log_input(" | Nhập Key : ").strip()
    if user_key not in keys:
        log_warning(" | Key không đúng!")
        exit()
    
    ID_CHANNEL = log_input(" | Nhập id channel : ")
    TXT_TOKEN = log_input(" | Nhập tokens.txt : ")
    TXT_CONTENT = log_input(" | Nhập content.txt : ")

    
    N_DELAY = float(log_input(" | Nhập delay : "))
    if N_DELAY == 0:
        log_warning(" | Spam siêu tốc!")
        N_DELAY = 1

    CONTENT = None
    TOKENS = None

    try:
        with open(TXT_TOKEN, "r", encoding="utf-8") as f:
            TOKENS = f.readlines()
    except Exception as e:
        log_warning(f"File {TXT_TOKEN} lỗi (TOKEN): {e}")
        time.sleep(10)
        sys.exit(0)       

    try:
        with open(TXT_CONTENT, "r", encoding="utf-8") as f2:
            CONTENT = f2.read().strip()
    except Exception as e:
        log_warning(f"File {TXT_CONTENT} lỗi (CONTENT): {e}")
        time.sleep(10)
        sys.exit(0)           

    while True:
        try:
            asyncio.run(action_pool(TOKENS, "", ID_CHANNEL, CONTENT, 1, N_DELAY))
        except (Exception, SystemError) as e:
            log_warning(" | Hệ thống gặp sự cố!")
            time.sleep(5)
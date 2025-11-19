from pystyle import Colors, Colorate
import os
import asyncio
import aiohttp
import sys
import threading
def get_keys_from_anotepad():
    try:
        url = 'dans link vao'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            note_content = soup.find('div', {'class': 'plaintext'})
            if note_content:
                keys = [line.strip() for line in note_content.get_text().strip().split('\n') if line.strip()]
                return keys
            else:
                print('Không tìm thấy nội dung ghi chú.')
                return []
        else:
            print(f'Yêu cầu thất bại với mã trạng thái: {response.status_code}')
            return []
    except Exception as e:
        print(f'Lỗi khi lấy key: {e}')
        return []

keys = get_keys_from_anotepad()
if not keys:
    print("Không thể lấy key bảo mật.")
    exit()

user_key = input("Nhập Key: ").strip()
if user_key not in keys:
    print("Key không đúng.")
    exit()

is_running = True

def log_info(msg): 
    print(Colorate.Horizontal(Colors.rainbow, f"[SYSTEM] {msg}"))

def log_success(msg): 
    print(Colorate.Horizontal(Colors.rainbow, f"[SYSTEM] {msg}"))

def log_warning(msg): 
    print(Colorate.Horizontal(Colors.rainbow, f"[SYSTEM] {msg}"))

def log_input(msg): 
    return input(Colorate.Horizontal(Colors.rainbow, f"[INPUT] {msg}"))

def input_listener():
    global is_running
    while True:
        try:
            cmd = input().strip().lower()
            if cmd == "n":
                is_running = False
                log_warning("Tạm dừng gửi tin nhắn!")
            elif cmd == "y":
                is_running = True
                log_success("Tiếp tục gửi tin nhắn!")
        except Exception:
            continue

async def get_channel_name(token, channel_id):
    url = f"https://discord.com/api/v10/channels/{channel_id}"
    headers = {"Authorization": token}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("name", "Unknown")
    except Exception:
        pass
    return "Unknown"

async def send_message(token, channel_id, message, typing=False):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
    send_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    async with aiohttp.ClientSession() as session:
        if typing:
            await session.post(typing_url, headers=headers)
            for char in message:
                sys.stdout.write(char)
                sys.stdout.flush()
                await asyncio.sleep(0.03)
            print()
        async with session.post(send_url, json={"content": message}, headers=headers) as resp:
            return resp.status in [200, 201]

async def main():
    global is_running
    banner = r"""

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
"""
    print(Colorate.Horizontal(Colors.rainbow, banner))
    log_info("Nhay Discord By Cnb")
    log_info("Chức năng:")
    log_info("1. Nhây")
    log_info("2. Nhây Fake Typing")
    log_info("3. Réo Tên")

    choice = log_input("Chọn 1 trong 3 : ").strip()
    if choice not in ("1", "2", "3"):
        log_warning("Chỉ hỗ trợ chức năng 1, 2, 3!")
        return

    mention_user = log_input("Có muốn tag người dùng không? (y/n): ").strip().lower() == 'y'

    user_ids = []
    names_to_call = []
    num_reo = 1
    if choice == "3":
        num_reo = int(log_input("Bạn muốn réo mấy người : ").strip())
        for i in range(num_reo):
            uid = log_input("ID người cần tag : ").strip()
            name_call = log_input("Tên cần réo : ").strip()
            user_ids.append(uid)
            names_to_call.append(name_call)
    else:
        user_ids_input = log_input("Nhập ID người cần tag : ").strip()
        if user_ids_input:
            user_ids = [uid.strip() for uid in user_ids_input.split(",") if uid.strip()]

    channel_ids = [cid.strip() for cid in log_input("Nhập ID Channel : ").split(",") if cid.strip()]

    token_file = log_input("Nhập file tokens.txt : ").strip()
    content_file = log_input("Nhập file chứa content.txt : ").strip()
    try:
        delay = float(log_input("Nhập delay : ").strip())
    except Exception:
        log_warning("Delay không hợp lệ!")
        return

    if not os.path.exists(token_file):
        log_warning(f"Không tìm thấy {token_file}")
        return
    with open(token_file, "r", encoding="utf-8") as f:
        tokens = [t.strip() for t in f if t.strip()]

    if not os.path.exists(content_file):
        log_warning(f"Không tìm thấy {content_file}")
        return
    with open(content_file, "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]
    if not messages:
        log_warning("File nội dung rỗng!")
        return

    log_info("Start")
    if choice == "2" or choice == "3":
        log_info("Đang giả soạn và chuẩn bị gửi!")
    else:
        log_info("Đang gửi!")

    threading.Thread(target=input_listener, daemon=True).start()
    semaphore = asyncio.Semaphore(20)

    if choice == "1":
        
        for channel_id in channel_ids:
            for token in tokens:
                msg_index = 0
                while True:
                    while not is_running:
                        await asyncio.sleep(0.5)
                    async with semaphore:
                        if mention_user and user_ids:
                            msg_to_send = " ".join([f"<@{uid}>" for uid in user_ids]) + " " + messages[msg_index % len(messages)]
                        else:
                            msg_to_send = messages[msg_index % len(messages)]
                        success = await send_message(token, channel_id, msg_to_send, typing=False)
                        channel_name = await get_channel_name(token, channel_id)
                        token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
                        if success:
                            log_success(f"| Token {token_preview} | Send successfully [ {channel_name} ] - [ {channel_id} ]")
                        else:
                            log_warning(f"| Token {token_preview} | Send FAILED [ {channel_name} ] - [ {channel_id} ]")
                        await asyncio.sleep(delay)
                        msg_index += 1

    elif choice == "2":
        
        for channel_id in channel_ids:
            for token in tokens:
                msg_index = 0
                while True:
                    while not is_running:
                        await asyncio.sleep(0.5)
                    async with semaphore:
                        if mention_user and user_ids:
                            msg_to_send = " ".join([f"<@{uid}>" for uid in user_ids]) + " " + messages[msg_index % len(messages)]
                        else:
                            msg_to_send = messages[msg_index % len(messages)]
                        success = await send_message(token, channel_id, msg_to_send, typing=True)
                        channel_name = await get_channel_name(token, channel_id)
                        token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
                        if success:
                            log_success(f"| Token {token_preview} | Send successfully [ {channel_name} ] - [ {channel_id} ]")
                        else:
                            log_warning(f"| Token {token_preview} | Send FAILED [ {channel_name} ] - [ {channel_id} ]")
                        await asyncio.sleep(delay)
                        msg_index += 1

    elif choice == "3":
        
        msg_index = 0
        while True:
            msg_raw = messages[msg_index % len(messages)]
            for idx in range(num_reo):
                uid = user_ids[idx]
                name_call = names_to_call[idx]
                for channel_id in channel_ids:
                    for token in tokens:
                        while not is_running:
                            await asyncio.sleep(0.5)
                        async with semaphore:
                            msg_to_send = f"<@{uid}> {msg_raw} {name_call}"
                            success = await send_message(token, channel_id, msg_to_send, typing=True)
                            channel_name = await get_channel_name(token, channel_id)
                            token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
                            if success:
                                log_success(f"| Token {token_preview} | Send successfully [ {channel_name} ] - [ {channel_id} ]")
                            else:
                                log_warning(f"| Token {token_preview} | Send FAILED [ {channel_name} ] - [ {channel_id} ]")
                            await asyncio.sleep(delay)
            msg_index += 1

if __name__ == "__main__":
    asyncio.run(main())
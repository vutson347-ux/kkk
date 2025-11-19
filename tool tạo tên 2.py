import os
import asyncio
import aiohttp

TOKENS_FILE = "tokens.txt"
DISCORD_API = "https://discord.com/api/v10"
TIMEOUT = aiohttp.Client

elif message.content.startswith("!anti"):
    if not os.path.exists(TOKENS_FILE):
        await message.channel.send("❌ Không tìm thấy file token. Dùng `!add` để thêm.")
        return

    with open(TOKENS_FILE, "r", encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]

    if not tokens:
        await message.channel.send("❌ File token rỗng.")
        return

    await message.channel.send(f"🔍 Đang quét và spam token sống...")

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        killed_tokens = []
        for idx, token in enumerate(tokens, 1):
            alive, reason = await check_token(session, token)
            if alive:
                # Spam token: gửi 5 request liên tiếp nhanh để gây stress
                success_count = 0
                for _ in range(5):
                    status = await api_get(session, f"{DISCORD_API}/users/@me", token)
                    if status == 200:
                        success_count += 1
                    await asyncio.sleep(0.1)
                if success_count < 5:
                    # Có thể token đã bị Discord khóa giữa chừng
                    killed_tokens.append(f"{idx}. {token[:8]}...{token[-4:]} ❌ Đã bị die sau spam")
                else:
                    killed_tokens.append(f"{idx}. {token[:8]}...{token[-4:]} ✅ Vẫn sống sau spam")
            else:
                killed_tokens.append(f"{idx}. {token[:8]}...{token[-4:]} ❌ Token chết từ đầu")

    # Gửi kết quả lại
    await message.channel.send("🔔 Kết quả quét và spam token:\n" + "\n".join(killed_tokens[:15]))

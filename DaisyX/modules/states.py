# Stats Module
import os
import time

import psutil
from pyrogram import filters
from wbb import bot_start_time
from wbb.core.decorators.errors import capture_err
from wbb.utils import formatter


async def bot_sys_stats():
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
{USERBOT_USERNAME}@William
------------------
UPTIME: {formatter.get_readable_time((bot_uptime))}
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
"""
    return stats


@app.on_message(filters.user(SUDOERS) & filters.command("stats"))
@capture_err
async def get_stats(_, message):
    stats = await bot_sys_stats()
    await message.reply_text(stats)

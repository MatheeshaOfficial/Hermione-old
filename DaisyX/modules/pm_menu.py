# Copyright (C) 2018 - 2020 MrYacha. All rights reserved. Source code available under the AGPL.
# Copyright (C) 2021 TeamDaisyX
# Copyright (C) 2020 Inuka Asith
#hermione
# This file is part of Daisy (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random
from contextlib import suppress

from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from DaisyX.decorator import register
from DaisyX.modules.utils.disable import disableable_dec

from . import MOD_HELP
from .language import select_lang_keyboard
from .utils.disable import disableable_dec
from .utils.language import get_strings_dec
from DaisyX.modules.states import bot_sys_stats

helpmenu_cb = CallbackData("helpmenu", "mod")


def help_markup(modules):
    markup = InlineKeyboardMarkup()
    for module in modules:
        markup.insert(
            InlineKeyboardButton(module, callback_data=helpmenu_cb.new(mod=module))
        )
    return markup


STICKERS = (
    "CAACAgUAAxkBAAIivWDr2T0buc1xq8Sschbe2OqgMiruAALQAwACZupgVztQDgABVViikx4E",
    "CAACAgUAAxkBAAIivmDr2U2tWmIwlN0FfBgsC5dpzP1tAALVAwACf8NgV9WDkUEV1bV7HgQ",
    "CAACAgUAAxkBAAIiv2Dr2VfYnGTRK1m7HrblirkAASWEkQACngMAAr2uYFdfOOy7PanETh4E",
    "CAACAgUAAxkBAAIiwGDr2W-R0BHMivAsBbsm4lTn77zmAAJJBAAClbxhV02b12_bQE8_HgQ",
    "CAACAgUAAxkBAAIiwWDr2XZE7HRx-CvtXf0tJK5-FbufAALjAgACEJRgVwlEAaqcX_qqHgQ",
    "CAACAgUAAxkBAAIiwmDr2X3tCHzCp53-5gbBQNbdYVPsAAIwBAACimZgV1j0HuTR_ej6HgQ",
    "CAACAgUAAxkBAAIiw2Dr2YVHF4gvDkn3SP9D9WdIKyawAALGAwACe6hhV84cO0her4U8HgQ",
    "CAACAgUAAxkBAAIixGDr2Yvpg91EAAFsh44spe2TlDXxlAACEgMAAnJuWFcK-J0yqY2qzh4E",
    "CAACAgUAAxkBAAIixmDr2ZrhwXjNKeaSj3Pcn-wj2D-xAALjAgACEJRgVwlEAaqcX_qqHgQ",
    "CAACAgUAAxkBAAIixWDr2ZFWitNjNGRFdQEKdANGkZcJAALaAgACUSJhV40-51_ZbzozHgQ",
)


@register(cmds="start", no_args=True, only_groups=True)
@disableable_dec("start")
@get_strings_dec("pm_menu")
async def start_group_cmd(message, strings):
    await message.reply(strings["start_hi_group"])


@register(cmds="start", no_args=True, only_pm=True)
async def start_cmd(message):
    await message.reply_sticker(random.choice(STICKERS))
    await get_start_func(message)


@get_strings_dec("pm_menu")
async def get_start_func(message, strings, edit=False):
    msg = message.message if hasattr(message, "message") else message

    task = msg.edit_text if edit else msg.reply
    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton(strings["btn_help"], callback_data="get_help"))
    buttons.add(
        InlineKeyboardButton(strings["btn_lang"], callback_data="lang_btn"),
        InlineKeyboardButton(
            strings["btn_source"],
            url="https://t.me/percy_jackson_4",
        ),
    )
    buttons.add(
        InlineKeyboardButton(
            strings["btn_channel"], url="https://t.me/HermioneUpdates"
        ),
        InlineKeyboardButton(
            strings["btn_group"], url="https://t.me/HermioneMusic_Help"
        ),
    )
    buttons.add(
        InlineKeyboardButton(
            text="System Stats 💻", callback_data="stats_callback"
        ),
    )
    buttons.add(
        InlineKeyboardButton(
            "😍Add Hermione to your group",
            url=f"https://telegram.me/miss_musicybot?startgroup=true",
        ),
    )

    # Handle error when user click the button 2 or more times simultaneously
    with suppress(MessageNotModified):
        await task(strings["start_hi"], reply_markup=buttons)


@register(regexp="get_help", f="cb")
@get_strings_dec("pm_menu")
async def help_cb(event, strings):
    button = help_markup(MOD_HELP)
    button.add(InlineKeyboardButton(strings["back"], callback_data="go_to_start"))
    with suppress(MessageNotModified):
        await event.message.edit_text(strings["help_header"], reply_markup=button)


@register(regexp="lang_btn", f="cb")
async def set_lang_cb(event):
    await select_lang_keyboard(event.message, edit=True)

@pbot.on_callback_query(filters.regex("stats_callback"))
async def stats_callback(_, CallbackQuery):
    text = await bot_sys_stats()
    await pbot.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@register(regexp="go_to_start", f="cb")
async def back_btn(event):
    await get_start_func(event, edit=True)


@register(cmds="help", only_pm=True)
@disableable_dec("help")
@get_strings_dec("pm_menu")
async def help_cmd(message, strings):
    button = help_markup(MOD_HELP)
    button.add(InlineKeyboardButton(strings["back"], callback_data="go_to_start"))
    await message.reply(strings["help_header"], reply_markup=button)


@register(cmds="help", only_groups=True)
@disableable_dec("help")
@get_strings_dec("pm_menu")
async def help_cmd_g(message, strings):
    text = strings["btn_group_help"]
    buttons = InlineKeyboardMarkup()
    buttons.add(
        InlineKeyboardButton(text=text, url="https://t.me/miss_musicybot?start")
    )
    buttons.add(
        InlineKeyboardButton(text="updates", url="https://t.me/HermioneUpdates")
    )
    await message.reply(strings["help_header"], reply_markup=buttons)


@register(helpmenu_cb.filter(), f="cb", allow_kwargs=True)
async def helpmenu_callback(query, callback_data=None, **kwargs):
    mod = callback_data["mod"]
    if not mod in MOD_HELP:
        await query.answer()
        return
    msg = f"Help for <b>{mod}</b> module:\n"
    msg += f"{MOD_HELP[mod]}"
    button = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="🏃‍♂️ Back", callback_data="get_help")
    )
    with suppress(MessageNotModified):
        await query.message.edit_text(
            msg, disable_web_page_preview=True, reply_markup=button
        )
        await query.answer("Help for " + mod)

"""
Ryhavean Userbot - Dil Əmri / Dil Komutu / Language command
.dildeyis az  → Azərbaycanca
.dildeyis tr  → Türkçe
.dildeyis en  → English

Seçim MongoDB-də saxlanılır, restartdan sonra da qüvvədə qalır.
"""

import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from tools import HARDCODED_PREFIXES, edit_or_reply
from languages import set_user_lang, get_text
import i18n

logger = logging.getLogger("userbot.language_cmd")

LANG_NAMES = {"az": "Azərbaycanca 🇦🇿", "tr": "Türkçe 🇹🇷", "en": "English 🇬🇧"}


@Client.on_message(
    filters.command(["dildeyis", "dildəyiş", "dil", "lang", "language"], prefixes=HARDCODED_PREFIXES)
    & filters.me
)
async def language_command(client: Client, message: Message):
    try:
        args = message.text.split()
        current = i18n.get_lang()

        if len(args) < 2:
            return await edit_or_reply(
                message,
                "🌐 <b>Dil Seçimi / Dil Seçimi / Language</b>\n"
                f"╰▸ Cari / Mevcut / Current: <i>{LANG_NAMES.get(current, current)}</i>\n\n"
                "• <code>.dildeyis az</code> — Azərbaycanca\n"
                "• <code>.dildeyis tr</code> — Türkçe\n"
                "• <code>.dildeyis en</code> — English",
            )

        code = args[1].lower().strip()
        if code not in i18n.SUPPORTED:
            return await edit_or_reply(
                message,
                "❌ <b>Xəta / Hata / Error</b>\n╰▸ <code>az</code>, <code>tr</code>, <code>en</code>",
            )

        user_id = message.from_user.id
        i18n.set_lang(code, user_id)
        await set_user_lang(user_id, code)

        text = get_text(code, "language", "lang_changed") or f"✅ {LANG_NAMES[code]}"
        await edit_or_reply(message, f"{text}\n╰▸ {LANG_NAMES[code]}")
        logger.info("Language switched to %s by %s", code, user_id)

    except Exception as e:
        logger.error("dildeyis error: %s", e)
        await edit_or_reply(message, f"❌ <b>Xəta / Hata / Error</b>\n╰▸ <code>{str(e)[:200]}</code>")

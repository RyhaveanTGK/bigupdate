"""
Ryhavean Userbot - Plugin Installer (MongoDB backed)
────────────────────────────────────────────────────
.pinstall    → .py fayla cavab verib plagini quraşdır  (reply to a .py file)
.unpinstall  → plagini sil (alias: .puninstall)
.plist       → quraşdırılmış plaginlərin siyahısı

Bütün plagin kodu MongoDB-də hər istifadəçi üçün AYRICA sənəddə saxlanılır
({"user_id": ..., "plugins": {"ad": "<kod>"}}), buna görə Render kimi
efemer disklərdə restart/deploy zamanı heç nə itmir — startda kod bazadan
diskə yenidən yazılır və yüklənir.
"""

import os
import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from tools import HARDCODED_PREFIXES, edit_or_reply
from config import user_sessions
from i18n import get_lang

logger = logging.getLogger("userbot.plugin_installer")

PLUGINS_DIR = os.getenv("USER_PLUGINS_DIR", "user_plugins")


# ─────────────────────────────────────────────────────────────────────────────
# Yardımçılar / helpers
# ─────────────────────────────────────────────────────────────────────────────
def user_dir(user_id: int) -> str:
    path = os.path.join(PLUGINS_DIR, str(user_id))
    os.makedirs(path, exist_ok=True)
    return path


def db_plugins(user_id: int) -> dict:
    """MongoDB-dən istifadəçinin plagin kodlarını gətir."""
    if user_sessions is None:
        return {}
    try:
        doc = user_sessions.find_one({"user_id": user_id}) or {}
        plugins = doc.get("plugins") or {}
        return plugins if isinstance(plugins, dict) else {}
    except Exception as e:
        logger.warning("Mongo plugin read failed: %s", e)
        return {}


def db_save_plugin(user_id: int, name: str, code: str) -> None:
    """Plagin kodunu MongoDB-də saxla (kalıcı)."""
    if user_sessions is None:
        return
    plugins = db_plugins(user_id)
    plugins[name] = code
    user_sessions.update_one(
        {"user_id": user_id},
        {"$set": {"plugins": plugins, "installed_plugins": sorted(plugins.keys())}},
        upsert=True,
    )


def db_remove_plugin(user_id: int, name: str) -> bool:
    if user_sessions is None:
        return False
    plugins = db_plugins(user_id)
    if name not in plugins:
        return False
    plugins.pop(name, None)
    user_sessions.update_one(
        {"user_id": user_id},
        {"$set": {"plugins": plugins, "installed_plugins": sorted(plugins.keys())}},
        upsert=True,
    )
    return True


def installed_names(user_id: int):
    """Bazadaki + diskdəki plaginlərin birləşmiş siyahısı."""
    names = set(db_plugins(user_id).keys())
    path = os.path.join(PLUGINS_DIR, str(user_id))
    if os.path.isdir(path):
        names.update(f[:-3] for f in os.listdir(path) if f.endswith(".py"))
    return sorted(names)


def restore_user_plugins(user_id: int):
    """Startda MongoDB-dəki plaginləri diskə yaz. main.py çağırır."""
    plugins = db_plugins(user_id)
    if not plugins:
        return []
    path = user_dir(user_id)
    restored = []
    for name, code in plugins.items():
        try:
            with open(os.path.join(path, f"{name}.py"), "w", encoding="utf-8") as fh:
                fh.write(code)
            restored.append(name)
        except Exception as e:
            logger.warning("Plugin restore failed (%s): %s", name, e)
    return restored


def _load_plugin_file(client: Client, path: str, name: str) -> str:
    """Plagini işləyən userbota canlı yüklə (restart tələb olunmur)."""
    try:
        from plugin_loader import load_plugin_file  # type: ignore
        load_plugin_file(client, path, name)
        return ""
    except Exception as e:
        return str(e)


def _msg(az: str, tr: str, en: str) -> str:
    lang = get_lang()
    return {"az": az, "tr": tr}.get(lang, en)


# ─────────────────────────────────────────────────────────────────────────────
# .pinstall
# ─────────────────────────────────────────────────────────────────────────────
@Client.on_message(filters.command("pinstall", prefixes=HARDCODED_PREFIXES) & filters.me)
async def install_plugin(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        replied = message.reply_to_message

        if not replied or not replied.document:
            return await edit_or_reply(
                message,
                _msg(
                    "❌ <b>Xəta</b>\n╰▸ Bir <code>.py</code> faylına cavab verin",
                    "❌ <b>Hata</b>\n╰▸ Bir <code>.py</code> dosyasına yanıt verin",
                    "❌ <b>Error</b>\n╰▸ Reply to a <code>.py</code> file",
                ),
            )

        file_name = replied.document.file_name or ""
        if not file_name.endswith(".py"):
            return await edit_or_reply(
                message,
                _msg(
                    "❌ <b>Xəta</b>\n╰▸ Yalnız <code>.py</code> faylları qəbul edilir",
                    "❌ <b>Hata</b>\n╰▸ Sadece <code>.py</code> dosyaları kabul edilir",
                    "❌ <b>Error</b>\n╰▸ Only <code>.py</code> files are accepted",
                ),
            )

        plugin_name = os.path.basename(file_name)[:-3]
        await edit_or_reply(
            message,
            _msg(
                f"⏳ <b>Quraşdırılır</b>\n╰▸ <code>{plugin_name}</code>",
                f"⏳ <b>Kuruluyor</b>\n╰▸ <code>{plugin_name}</code>",
                f"⏳ <b>Installing</b>\n╰▸ <code>{plugin_name}</code>",
            ),
        )

        path = os.path.join(user_dir(user_id), f"{plugin_name}.py")
        await client.download_media(replied.document, file_name=path)

        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            code = fh.read()

        # Sintaksis yoxlaması — pozuq plagin userbotu sındırmasın
        try:
            compile(code, path, "exec")
        except SyntaxError as e:
            os.remove(path)
            return await edit_or_reply(
                message,
                _msg(
                    f"❌ <b>Sintaksis xətası</b>\n╰▸ <code>{e}</code>",
                    f"❌ <b>Sözdizimi hatası</b>\n╰▸ <code>{e}</code>",
                    f"❌ <b>Syntax error</b>\n╰▸ <code>{e}</code>",
                ),
            )

        db_save_plugin(user_id, plugin_name, code)
        err = _load_plugin_file(client, path, plugin_name)

        total = len(installed_names(user_id))
        if err:
            return await edit_or_reply(
                message,
                _msg(
                    f"⚠️ <b>Plagin saxlanıldı, lakin yüklənmədi</b>\n╰▸ <code>{plugin_name}</code>\n╰▸ <code>{err[:200]}</code>\n╰▸ Restartdan sonra yenidən sınanacaq",
                    f"⚠️ <b>Eklenti kaydedildi ama yüklenemedi</b>\n╰▸ <code>{plugin_name}</code>\n╰▸ <code>{err[:200]}</code>\n╰▸ Yeniden başlatmada tekrar denenecek",
                    f"⚠️ <b>Plugin saved but not loaded</b>\n╰▸ <code>{plugin_name}</code>\n╰▸ <code>{err[:200]}</code>",
                ),
            )

        await edit_or_reply(
            message,
            _msg(
                f"✅ <b>Plagin quraşdırıldı</b>\n╰▸ <code>{plugin_name}</code>\n╰▸ MongoDB-də saxlanıldı (restartda itmir)\n╰▸ Cəmi: {total}",
                f"✅ <b>Eklenti kuruldu</b>\n╰▸ <code>{plugin_name}</code>\n╰▸ MongoDB'ye kaydedildi (yeniden başlatmada silinmez)\n╰▸ Toplam: {total}",
                f"✅ <b>Plugin installed</b>\n╰▸ <code>{plugin_name}</code>\n╰▸ Stored in MongoDB\n╰▸ Total: {total}",
            ),
        )
        logger.info("User %s installed plugin %s", user_id, plugin_name)

    except Exception as e:
        logger.error("pinstall error: %s", e)
        await edit_or_reply(message, f"❌ <b>Xəta / Hata / Error</b>\n╰▸ <code>{str(e)[:200]}</code>")


# ─────────────────────────────────────────────────────────────────────────────
# .unpinstall (alias: .puninstall)
# ─────────────────────────────────────────────────────────────────────────────
@Client.on_message(
    filters.command(["unpinstall", "puninstall"], prefixes=HARDCODED_PREFIXES) & filters.me
)
async def uninstall_plugin(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        args = message.text.split(maxsplit=1)
        plugins = installed_names(user_id)

        if len(args) < 2:
            if not plugins:
                return await edit_or_reply(
                    message,
                    _msg(
                        "❌ <b>Quraşdırılmış plagin yoxdur</b>",
                        "❌ <b>Kurulu eklenti yok</b>",
                        "❌ <b>No plugins installed</b>",
                    ),
                )
            listing = "\n".join(f"• <code>.unpinstall {p}</code>" for p in plugins)
            return await edit_or_reply(
                message,
                _msg(
                    f"📦 <b>Quraşdırılmış plaginlər</b>\n\n{listing}",
                    f"📦 <b>Kurulu eklentiler</b>\n\n{listing}",
                    f"📦 <b>Installed plugins</b>\n\n{listing}",
                ),
            )

        name = args[1].strip().removesuffix(".py")
        removed_db = db_remove_plugin(user_id, name)
        path = os.path.join(PLUGINS_DIR, str(user_id), f"{name}.py")
        removed_file = False
        if os.path.exists(path):
            os.remove(path)
            removed_file = True

        if not (removed_db or removed_file):
            return await edit_or_reply(
                message,
                _msg(
                    f"❌ <b>Tapılmadı</b>\n╰▸ <code>{name}</code>",
                    f"❌ <b>Bulunamadı</b>\n╰▸ <code>{name}</code>",
                    f"❌ <b>Not found</b>\n╰▸ <code>{name}</code>",
                ),
            )

        await edit_or_reply(
            message,
            _msg(
                f"✅ <b>Plagin silindi</b>\n╰▸ <code>{name}</code>\n╰▸ Tam təsir üçün <code>.restart</code> edin",
                f"✅ <b>Eklenti kaldırıldı</b>\n╰▸ <code>{name}</code>\n╰▸ Tam etki için <code>.restart</code> yapın",
                f"✅ <b>Plugin uninstalled</b>\n╰▸ <code>{name}</code>",
            ),
        )
        logger.info("User %s uninstalled plugin %s", user_id, name)

    except Exception as e:
        logger.error("unpinstall error: %s", e)
        await edit_or_reply(message, f"❌ <b>Xəta / Hata / Error</b>\n╰▸ <code>{str(e)[:200]}</code>")


# ─────────────────────────────────────────────────────────────────────────────
# .plist
# ─────────────────────────────────────────────────────────────────────────────
@Client.on_message(
    filters.command(["plist", "pluginlist"], prefixes=HARDCODED_PREFIXES) & filters.me
)
async def list_plugins(client: Client, message: Message):
    try:
        user_id = message.from_user.id
        plugins = installed_names(user_id)
        if not plugins:
            return await edit_or_reply(
                message,
                _msg(
                    "🔌 <b>Plaginlər</b>\n╰▸ Heç bir plagin quraşdırılmayıb\n╰▸ <code>.pinstall</code> ilə .py faylı quraşdırın",
                    "🔌 <b>Eklentiler</b>\n╰▸ Kurulu eklenti yok\n╰▸ <code>.pinstall</code> ile .py dosyası kurun",
                    "🔌 <b>Plugins</b>\n╰▸ No plugins installed",
                ),
            )
        body = "\n".join(f"  • <code>{p}</code>" for p in plugins)
        await edit_or_reply(
            message,
            _msg(
                f"🔌 <b>Quraşdırılmış plaginlər</b>\n╰▸ Cəmi: {len(plugins)}\n\n{body}",
                f"🔌 <b>Kurulu eklentiler</b>\n╰▸ Toplam: {len(plugins)}\n\n{body}",
                f"🔌 <b>Installed plugins</b>\n╰▸ Total: {len(plugins)}\n\n{body}",
            ),
        )
    except Exception as e:
        logger.error("plist error: %s", e)
        await edit_or_reply(message, f"❌ <b>Xəta / Hata / Error</b>\n╰▸ <code>{str(e)[:200]}</code>")

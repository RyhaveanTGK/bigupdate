"""
Ryhavean Userbot - Multi-Language Support Module
Dil dəstəyi: Azərbaycanca, Türkçe, English
Language Support: Azerbaijani, Turkish, English

Command: .dildeyis <az|tr|en>
"""

import os
import json
from typing import Dict, Optional

# Language dictionary structure
LANGUAGES = {
    "az": {  # Azərbaycanca
        "admin": {
            "admin_required": "👮 <b>Admin Hüququ Lazımdır</b>\n╰▸ Admin olmaq lazımdır",
            "ban_success": "✅ <b>Banlama Uğurlu</b>\n╰▸ {user} banlandi",
            "unban_success": "✅ <b>Banlama Ləğv Edildi</b>\n╰▸ {user} banlama ləğv edildi",
            "kick_success": "✅ <b>Qrupdan Çıxarıldı</b>\n╰▸ {user} qrupdan çıxarıldı",
            "mute_success": "✅ <b>Susturuldu</b>\n╰▸ {user} susturuldu",
            "unmute_success": "✅ <b>Susturma Ləğv Edildi</b>\n╰▸ {user} susturması ləğv edildi",
            "promote_success": "✅ <b>Yüksəldirildi</b>\n╰▸ {user} admin edildi",
            "demote_success": "✅ <b>Azaldıldı</b>\n╰▸ {user}-in admin hüququ azaldıldı",
        },
        "language": {
            "lang_changed": "✅ <b>Dil Dəyişdirildi</b>\n╰▸ Dil: Azərbaycanca ✓",
            "invalid_lang": "❌ <b>Xəta</b>\n╰▸ Dil: az (Azərbaycanca), tr (Türkçe) və en (English)",
        },
        "common": {
            "error": "❌ <b>Xəta</b>",
            "success": "✅ <b>Uğurlu</b>",
            "info": "ℹ️ <b>Məlumat</b>",
            "warning": "⚠️ <b>Xəbərdarlıq</b>",
            "loading": "⏳ <b>Yüklənir</b>...",
            "reply_needed": "❌ <b>Xəta</b>\n╰▸ Bir mesaja cavab verin",
            "invalid_args": "❌ <b>Xəta</b>\n╰▸ Yanlış arqumentlər",
        },
        "userbot": {
            "alive": "🤖 <b>Ryhavean Userbot</b> Aktiv!\n╰▸ Sistem işləyir ✓",
            "help": "📖 <b>Ryhavean Userbot Kömək</b>\n╰▸ Əmrləri görmək üçün .help-i istifadə edin",
            "plugins": "🔌 <b>Plaginlər</b>\n╰▸ {count} plağin yükləndi",
            "version": "📌 <b>Ryhavean Userbot</b> v1.0.0",
            "sudo_added": "✅ <b>Sudo İstifadəçisi Əlavə Edildi</b>",
            "sudo_removed": "✅ <b>Sudo İstifadəçisi Silindi</b>",
        },
        "plugins": {
            "install_success": "✅ <b>Plağin Quraşdırıldı</b>\n╰▸ {plugin} quraşdırıldı",
            "install_failed": "❌ <b>Quraşdırma Xətas</b>\n╰▸ {plugin} quraşdırılmadı",
            "uninstall_success": "✅ <b>Plağin Silindi</b>\n╰▸ {plugin} silindi",
            "uninstall_failed": "❌ <b>Silmə Xətas</b>\n╰▸ {plugin} silinmədi",
            "plugin_disabled": "⚠️ <b>Xəbərdarlıq</b>\n╰▸ Plağin deaktivdir",
        },
    },
    "tr": {  # Türkçe
        "admin": {
            "admin_required": "👮 <b>Yönetici Yetkileri Gerekli</b>\n╰▸ Yönetici olmalısınız",
            "ban_success": "✅ <b>Yasaklama Başarılı</b>\n╰▸ {user} yasaklandı",
            "unban_success": "✅ <b>Yasak Kaldırıldı</b>\n╰▸ {user} yasağı kaldırıldı",
            "kick_success": "✅ <b>Grubtan Çıkarıldı</b>\n╰▸ {user} gruptan çıkarıldı",
            "mute_success": "✅ <b>Susturuldu</b>\n╰▸ {user} susturuldu",
            "unmute_success": "✅ <b>Susturma Kaldırıldı</b>\n╰▸ {user} susturması kaldırıldı",
            "promote_success": "✅ <b>Yükseltildi</b>\n╰▸ {user} yönetici yapıldı",
            "demote_success": "✅ <b>İndirildi</b>\n╰▸ {user}-in yönetici yetkisi kaldırıldı",
        },
        "language": {
            "lang_changed": "✅ <b>Dil Değiştirildi</b>\n╰▸ Dil: Türkçe ✓",
            "invalid_lang": "❌ <b>Hata</b>\n╰▸ Dil: az (Azərbaycanca), tr (Türkçe) və en (English)",
        },
        "common": {
            "error": "❌ <b>Hata</b>",
            "success": "✅ <b>Başarılı</b>",
            "info": "ℹ️ <b>Bilgi</b>",
            "warning": "⚠️ <b>Uyarı</b>",
            "loading": "⏳ <b>Yükleniyor</b>...",
            "reply_needed": "❌ <b>Hata</b>\n╰▸ Bir mesaja cevap verin",
            "invalid_args": "❌ <b>Hata</b>\n╰▸ Geçersiz argümanlar",
        },
        "userbot": {
            "alive": "🤖 <b>Ryhavean Userbot</b> Aktif!\n╰▸ Sistem çalışıyor ✓",
            "help": "📖 <b>Ryhavean Userbot Yardım</b>\n╰▸ Komutları görmek için .help kullanın",
            "plugins": "🔌 <b>Eklentiler</b>\n╰▸ {count} eklenti yüklendi",
            "version": "📌 <b>Ryhavean Userbot</b> v1.0.0",
            "sudo_added": "✅ <b>Sudo Kullanıcı Eklendi</b>",
            "sudo_removed": "✅ <b>Sudo Kullanıcı Kaldırıldı</b>",
        },
        "plugins": {
            "install_success": "✅ <b>Eklenti Yüklendi</b>\n╰▸ {plugin} yüklendi",
            "install_failed": "❌ <b>Yükleme Hatası</b>\n╰▸ {plugin} yüklenemedi",
            "uninstall_success": "✅ <b>Eklenti Kaldırıldı</b>\n╰▸ {plugin} kaldırıldı",
            "uninstall_failed": "❌ <b>Kaldırma Hatası</b>\n╰▸ {plugin} kaldırılamadı",
            "plugin_disabled": "⚠️ <b>Uyarı</b>\n╰▸ Eklenti devre dışı",
        },
    },
    "en": {  # English
        "admin": {
            "admin_required": "👮 <b>Admin Privileges Required</b>\n╰▸ You must be admin",
            "ban_success": "✅ <b>Ban Successful</b>\n╰▸ {user} has been banned",
            "unban_success": "✅ <b>Unban Successful</b>\n╰▸ {user} has been unbanned",
            "kick_success": "✅ <b>Kicked From Group</b>\n╰▸ {user} has been kicked",
            "mute_success": "✅ <b>Muted</b>\n╰▸ {user} has been muted",
            "unmute_success": "✅ <b>Unmuted</b>\n╰▸ {user} has been unmuted",
            "promote_success": "✅ <b>Promoted</b>\n╰▸ {user} is now admin",
            "demote_success": "✅ <b>Demoted</b>\n╰▸ {user} is no longer admin",
        },
        "language": {
            "lang_changed": "✅ <b>Language Changed</b>\n╰▸ Language: English ✓",
            "invalid_lang": "❌ <b>Error</b>\n╰▸ Language: az (Azərbaycanca), tr (Türkçe) or en (English)",
        },
        "common": {
            "error": "❌ <b>Error</b>",
            "success": "✅ <b>Success</b>",
            "info": "ℹ️ <b>Info</b>",
            "warning": "⚠️ <b>Warning</b>",
            "loading": "⏳ <b>Loading</b>...",
            "reply_needed": "❌ <b>Error</b>\n╰▸ Reply to a message",
            "invalid_args": "❌ <b>Error</b>\n╰▸ Invalid arguments",
        },
        "userbot": {
            "alive": "🤖 <b>Ryhavean Userbot</b> is Alive!\n╰▸ System running ✓",
            "help": "📖 <b>Ryhavean Userbot Help</b>\n╰▸ Use .help to see commands",
            "plugins": "🔌 <b>Plugins</b>\n╰▸ {count} plugins loaded",
            "version": "📌 <b>Ryhavean Userbot</b> v1.0.0",
            "sudo_added": "✅ <b>Sudo User Added</b>",
            "sudo_removed": "✅ <b>Sudo User Removed</b>",
        },
        "plugins": {
            "install_success": "✅ <b>Plugin Installed</b>\n╰▸ {plugin} installed",
            "install_failed": "❌ <b>Installation Failed</b>\n╰▸ {plugin} could not be installed",
            "uninstall_success": "✅ <b>Plugin Uninstalled</b>\n╰▸ {plugin} uninstalled",
            "uninstall_failed": "❌ <b>Uninstall Failed</b>\n╰▸ {plugin} could not be uninstalled",
            "plugin_disabled": "⚠️ <b>Warning</b>\n╰▸ Plugin is disabled",
        },
    }
}


class LanguageManager:
    """Manage user language preferences with MongoDB storage"""
    
    def __init__(self, db_collection=None):
        self.db = db_collection
        self.default_lang = "en"
        self.supported_langs = list(LANGUAGES.keys())
    
    async def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language from database"""
        if not self.db:
            return self.default_lang
        
        try:
            user_data = self.db.find_one({"user_id": user_id})
            if user_data and "language" in user_data:
                lang = user_data["language"]
                return lang if lang in self.supported_langs else self.default_lang
            return self.default_lang
        except Exception:
            return self.default_lang
    
    async def set_user_language(self, user_id: int, lang_code: str) -> bool:
        """Set user's language preference in database"""
        if lang_code not in self.supported_langs:
            return False
        
        if not self.db:
            return False
        
        try:
            self.db.update_one(
                {"user_id": user_id},
                {"$set": {"language": lang_code}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error setting language: {e}")
            return False
    
    def get_text(self, lang_code: str, section: str, key: str, **kwargs) -> str:
        """Get translated text with variable substitution"""
        if lang_code not in LANGUAGES:
            lang_code = self.default_lang
        
        try:
            text = LANGUAGES[lang_code].get(section, {}).get(key, "")
            if kwargs:
                text = text.format(**kwargs)
            return text
        except (KeyError, KeyError):
            # Fallback to English
            return LANGUAGES[self.default_lang].get(section, {}).get(key, f"[{section}.{key}]")


# Global instance
_lang_manager = None


def init_language_manager(db_collection=None):
    """Initialize the global language manager"""
    global _lang_manager
    _lang_manager = LanguageManager(db_collection)
    return _lang_manager


def get_lang_manager() -> LanguageManager:
    """Get the global language manager"""
    global _lang_manager
    if _lang_manager is None:
        _lang_manager = LanguageManager()
    return _lang_manager


# Helper functions for easy access
async def get_user_lang(user_id: int) -> str:
    """Get user's language"""
    return await get_lang_manager().get_user_language(user_id)


async def set_user_lang(user_id: int, lang_code: str) -> bool:
    """Set user's language"""
    return await get_lang_manager().set_user_language(user_id, lang_code)


def get_text(user_lang: str, section: str, key: str, **kwargs) -> str:
    """Get translated text"""
    return get_lang_manager().get_text(user_lang, section, key, **kwargs)

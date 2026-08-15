"""
Ryhavean Userbot - Runtime i18n engine
──────────────────────────────────────
Bütün çıxış mesajlarını (userbot + köməkçi bot) aktiv dilə çevirir.
Translates every outgoing message (userbot + helper bot) into the active
language. Supported: az (Azərbaycanca), tr (Türkçe), en (English).

Aktiv dil MongoDB-də istifadəçi sənədində saxlanılır: {"user_id": ..., "language": "az"}
Restart zamanı heç nə itmir — dil bazadan yenidən yüklənir.

İstifadə / Usage:
    .dildeyis az | .dildeyis tr | .dildeyis en
"""

import os
import re
import logging

logger = logging.getLogger("i18n")

SUPPORTED = ("az", "tr", "en")
DEFAULT_LANG = (os.getenv("DEFAULT_LANG") or "az").lower()
if DEFAULT_LANG not in ("az", "tr", "en"):
    DEFAULT_LANG = "az"

# Aktiv dil (prosesə görə keş) — MongoDB-dən yüklənir.
_active_lang = DEFAULT_LANG
_owner_id = None
_collection = None


# ─────────────────────────────────────────────────────────────────────────────
# Söz / ifadə lüğəti.  Açar = İngiliscə orijinal mətn (kiçik-böyük fərqsiz).
# Dəyər = (az, tr)
# ─────────────────────────────────────────────────────────────────────────────
PHRASES = {
    # ── Statuslar / prefikslər ────────────────────────────────────────────
    "error": ("Xəta", "Hata"),
    "warning": ("Xəbərdarlıq", "Uyarı"),
    "success": ("Uğurlu", "Başarılı"),
    "info": ("Məlumat", "Bilgi"),
    "processing . . .": ("İşlənir . . .", "İşleniyor . . ."),
    "processing...": ("İşlənir...", "İşleniyor..."),
    "processing": ("İşlənir", "İşleniyor"),
    "loading": ("Yüklənir", "Yükleniyor"),
    "please wait": ("Zəhmət olmasa gözləyin", "Lütfen bekleyin"),
    "done": ("Tamamlandı", "Tamamlandı"),
    "cancelled": ("Ləğv edildi", "İptal edildi"),
    "pinging...": ("Ping atılır...", "Ping atılıyor..."),
    "deleting keys...": ("Açarlar silinir...", "Anahtarlar siliniyor..."),

    # ── Msg sabitləri (utils/message.py) ──────────────────────────────────
    "admin privileges required": ("Admin hüququ lazımdır", "Yönetici yetkisi gerekli"),
    "alive keys reset (emoji, text)": ("Alive açarları sıfırlandı (emoji, mətn)", "Alive anahtarları sıfırlandı (emoji, metin)"),
    "all message counts reset to 0": ("Bütün mesaj sayğacları 0-a sıfırlandı", "Tüm mesaj sayaçları 0'a sıfırlandı"),
    "all messages unpinned": ("Bütün mesajların sancağı götürüldü", "Tüm mesajların sabitlemesi kaldırıldı"),
    "all whitelisted users removed": ("Ağ siyahıdakı bütün istifadəçilər silindi", "Beyaz listedeki tüm kullanıcılar silindi"),
    "already a sudoer": ("Onsuz da sudo istifadəçisidir", "Zaten sudo kullanıcısı"),
    "already in whitelist": ("Onsuz da ağ siyahıdadır", "Zaten beyaz listede"),
    "approved & added to whitelist": ("Təsdiqləndi və ağ siyahıya əlavə edildi", "Onaylandı ve beyaz listeye eklendi"),
    "blacklist is empty": ("Qara siyahı boşdur", "Kara liste boş"),
    "bot is blocked. unblock @sangmata_beta_bot and try again.": ("Bot bloklanıb. @Sangmata_Beta_Bot blokunu açın və yenidən sınayın.", "Bot engellenmiş. @Sangmata_Beta_Bot engelini kaldırıp tekrar deneyin."),
    "cannot ban this admin": ("Bu admini banlamaq mümkün deyil", "Bu yönetici yasaklanamaz"),
    "cannot clone admin user": ("Admin istifadəçisini klonlamaq mümkün deyil", "Yönetici kullanıcı klonlanamaz"),
    "cannot dm spam the owner": ("Sahibə DM spam etmək mümkün deyil", "Sahibe DM spam yapılamaz"),
    "cannot fetch user from entity": ("İstifadəçi məlumatı alınmadı", "Kullanıcı bilgisi alınamadı"),
    "cannot kick this admin": ("Bu admini qrupdan çıxarmaq mümkün deyil", "Bu yönetici gruptan atılamaz"),
    "cannot mute this admin": ("Bu admini susdurmaq mümkün deyil", "Bu yönetici susturulamaz"),
    "cannot unmute this admin": ("Bu adminin susdurulması götürülə bilmir", "Bu yöneticinin susturması kaldırılamaz"),
    "cannot verify admin privileges": ("Admin hüquqları yoxlanıla bilmədi", "Yönetici yetkileri doğrulanamadı"),
    "command not found": ("Əmr tapılmadı", "Komut bulunamadı"),
    "count must be 1-100": ("Say 1-100 arasında olmalıdır", "Sayı 1-100 arasında olmalı"),
    "dm spam done": ("DM spam tamamlandı", "DM spam tamamlandı"),
    "document must be an image type": ("Sənəd şəkil tipində olmalıdır", "Belge resim türünde olmalı"),
    "failed after multiple retries": ("Bir neçə cəhddən sonra alınmadı", "Birkaç denemeden sonra başarısız"),
    "failed to generate quote": ("Sitat yaradıla bilmədi", "Alıntı oluşturulamadı"),
    "failed to get user info": ("İstifadəçi məlumatı alınmadı", "Kullanıcı bilgisi alınamadı"),
    "failed to start group call": ("Qrup zəngi başladıla bilmədi", "Grup araması başlatılamadı"),
    "failed. use @stickers bot to add sticker.": ("Alınmadı. Stiker əlavə etmək üçün @Stickers botundan istifadə edin.", "Başarısız. Çıkartma eklemek için @Stickers botunu kullanın."),
    "file exceeds 2gb limit": ("Fayl 2GB limitini aşır", "Dosya 2GB sınırını aşıyor"),
    "file exceeds 2gb limit. upgrade to telegram premium.": ("Fayl 2GB limitini aşır. Telegram Premium alın.", "Dosya 2GB sınırını aşıyor. Telegram Premium alın."),
    "group call ended": ("Qrup zəngi bitirildi", "Grup araması sonlandırıldı"),
    "group only": ("Yalnız qruplarda işləyir", "Sadece gruplarda çalışır"),
    "invalid channel or group": ("Yanlış kanal və ya qrup", "Geçersiz kanal veya grup"),
    "invalid chat id. provide a valid integer.": ("Yanlış chat ID. Düzgün rəqəm daxil edin.", "Geçersiz sohbet ID. Geçerli bir sayı girin."),
    "invalid command": ("Yanlış əmr", "Geçersiz komut"),
    "invalid count number": ("Yanlış say", "Geçersiz sayı"),
    "invalid count! use a number": ("Yanlış say! Rəqəm istifadə edin", "Geçersiz sayı! Bir rakam kullanın"),
    "invalid delay value": ("Yanlış gecikmə dəyəri", "Geçersiz gecikme değeri"),
    "invalid number": ("Yanlış rəqəm", "Geçersiz sayı"),
    "invalid time! use hh:mm:ss or hh:mm:ss:cc (24-hour)": ("Yanlış vaxt! HH:MM:SS və ya HH:MM:SS:CC (24 saat) istifadə edin", "Geçersiz saat! HH:MM:SS veya HH:MM:SS:CC (24 saat) kullanın"),
    "join requests processed": ("Qoşulma sorğuları icra edildi", "Katılma istekleri işlendi"),
    "join the group call before inviting users": ("İstifadəçiləri dəvət etməzdən əvvəl qrup zənginə qoşulun", "Kullanıcıları davet etmeden önce grup aramasına katılın"),
    "latest pin unpinned": ("Son sancaq götürüldü", "Son sabitleme kaldırıldı"),
    "mention dismissed": ("Etiketləmə dayandırıldı", "Etiketleme durduruldu"),
    "message count reset to 0": ("Mesaj sayğacı 0-a sıfırlandı", "Mesaj sayacı 0'a sıfırlandı"),
    "message pinned": ("Mesaj sancaqlandı", "Mesaj sabitlendi"),
    "message unpinned": ("Mesajın sancağı götürüldü", "Mesaj sabitlemesi kaldırıldı"),
    "need admin rights to pin": ("Sancaqlamaq üçün admin hüququ lazımdır", "Sabitlemek için yönetici yetkisi gerekli"),
    "need admin rights to unpin": ("Sancağı götürmək üçün admin hüququ lazımdır", "Sabitlemeyi kaldırmak için yönetici yetkisi gerekli"),
    "need manage users permission to unban": ("Ban ləğvi üçün istifadəçi idarə icazəsi lazımdır", "Yasak kaldırmak için kullanıcı yönetme izni gerekli"),
    "no active group call found": ("Aktiv qrup zəngi tapılmadı", "Aktif grup araması bulunamadı"),
    "no active tagall here": ("Burada aktiv tagall yoxdur", "Burada aktif tagall yok"),
    "no banned users found": ("Banlanmış istifadəçi tapılmadı", "Yasaklı kullanıcı bulunamadı"),
    "no blacklist found": ("Qara siyahı tapılmadı", "Kara liste bulunamadı"),
    "no clone data found": ("Klon məlumatı tapılmadı", "Klon verisi bulunamadı"),
    "no count found for this chat": ("Bu söhbət üçün sayğac tapılmadı", "Bu sohbet için sayaç bulunamadı"),
    "no data found": ("Məlumat tapılmadı", "Veri bulunamadı"),
    "no inline results found": ("Inline nəticə tapılmadı", "Inline sonuç bulunamadı"),
    "no pending join requests": ("Gözləyən qoşulma sorğusu yoxdur", "Bekleyen katılma isteği yok"),
    "no privileges to grant": ("Veriləcək hüquq yoxdur", "Verilecek yetki yok"),
    "no query provided": ("Sorğu daxil edilməyib", "Sorgu girilmedi"),
    "no results found": ("Nəticə tapılmadı", "Sonuç bulunamadı"),
    "no sudoers found": ("Sudo istifadəçisi tapılmadı", "Sudo kullanıcısı bulunamadı"),
    "no text found to quote": ("Sitat üçün mətn tapılmadı", "Alıntı için metin bulunamadı"),
    "no whitelisted users to remove": ("Silinəcək ağ siyahı istifadəçisi yoxdur", "Silinecek beyaz liste kullanıcısı yok"),
    "not a sudoer": ("Sudo istifadəçisi deyil", "Sudo kullanıcısı değil"),
    "not authorized": ("İcazə yoxdur", "Yetkiniz yok"),
    "not in whitelist": ("Ağ siyahıda deyil", "Beyaz listede değil"),
    "nothing given to gcast": ("Gcast üçün heç nə verilmədi", "Gcast için bir şey verilmedi"),
    "owner-only command": ("Yalnız sahib üçün əmr", "Sadece sahip komutu"),
    "private chat restricted": ("Şəxsi söhbət məhdudlaşdırılıb", "Özel sohbet kısıtlandı"),
    "profile reverted": ("Profil geri qaytarıldı", "Profil geri alındı"),
    "provide code to evaluate": ("İcra üçün kod daxil edin", "Çalıştırmak için kod girin"),
    "provide gcast flag": ("Gcast bayrağını daxil edin", "Gcast bayrağını girin"),
    "provide something to spam": ("Spam üçün nəsə daxil edin", "Spam için bir şey girin"),
    "quote generation failed": ("Sitat yaradılmadı", "Alıntı oluşturulamadı"),
    "reaction updated": ("Reaksiya yeniləndi", "Tepki güncellendi"),
    "reactions disabled": ("Reaksiyalar söndürüldü", "Tepkiler kapatıldı"),
    "reactions enabled": ("Reaksiyalar aktivləşdirildi", "Tepkiler açıldı"),
    "removed from whitelist & count reset": ("Ağ siyahıdan silindi və sayğac sıfırlandı", "Beyaz listeden silindi ve sayaç sıfırlandı"),
    "reply to a message to create a quote": ("Sitat yaratmaq üçün mesaja cavab verin", "Alıntı oluşturmak için mesaja yanıt verin"),
    "reply to a message to delete it": ("Silmək üçün mesaja cavab verin", "Silmek için mesaja yanıt verin"),
    "reply to a message to pin it": ("Sancaqlamaq üçün mesaja cavab verin", "Sabitlemek için mesaja yanıt verin"),
    "reply to a message to start purging": ("Təmizləməyə başlamaq üçün mesaja cavab verin", "Temizlemeye başlamak için mesaja yanıt verin"),
    "reply to a message": ("Bir mesaja cavab verin", "Bir mesaja yanıt verin"),
    "reply to a user": ("Bir istifadəçiyə cavab verin", "Bir kullanıcıya yanıt verin"),
    "reply to a user's message": ("İstifadəçinin mesajına cavab verin", "Kullanıcının mesajına yanıt verin"),
    "reply to a user's message to delete all their messages": ("Bütün mesajlarını silmək üçün istifadəçinin mesajına cavab verin", "Tüm mesajlarını silmek için kullanıcının mesajına yanıt verin"),
    "reply to an image/document": ("Şəkil/sənədə cavab verin", "Resim/belgeye yanıt verin"),
    "reply to any photo or sticker": ("İstənilən şəkil və ya stikerə cavab verin", "Herhangi bir resim veya çıkartmaya yanıt verin"),
    "reply to any sticker": ("İstənilən stikerə cavab verin", "Herhangi bir çıkartmaya yanıt verin"),
    "reply to photo/gif/sticker": ("Şəkil/GIF/Stikerə cavab verin", "Resim/GIF/Çıkartmaya yanıt verin"),
    "reply to user or provide user id": ("İstifadəçiyə cavab verin və ya ID daxil edin", "Kullanıcıya yanıt verin veya ID girin"),
    "reply to user or provide username/id": ("İstifadəçiyə cavab verin və ya istifadəçi adı/ID daxil edin", "Kullanıcıya yanıt verin veya kullanıcı adı/ID girin"),
    "restricted in dms": ("DM-lərdə məhdudlaşdırılıb", "DM'lerde kısıtlandı"),
    "session not found": ("Sessiya tapılmadı", "Oturum bulunamadı"),
    "settings saved": ("Ayarlar yadda saxlanıldı", "Ayarlar kaydedildi"),
    "specify a user to clone": ("Klonlanacaq istifadəçini göstərin", "Klonlanacak kullanıcıyı belirtin"),
    "sticker has no name": ("Stikerin adı yoxdur", "Çıkartmanın adı yok"),
    "sticker kanged": ("Stiker oğurlandı", "Çıkartma çalındı"),
    "sudo granted": ("Sudo hüququ verildi", "Sudo yetkisi verildi"),
    "sudo revoked": ("Sudo hüququ geri alındı", "Sudo yetkisi geri alındı"),
    "unable to retrieve history. user may have privacy enabled.": ("Tarixçə alınmadı. İstifadəçidə məxfilik aktiv ola bilər.", "Geçmiş alınamadı. Kullanıcıda gizlilik açık olabilir."),
    "unsupported file type": ("Dəstəklənməyən fayl tipi", "Desteklenmeyen dosya türü"),
    "unsupported file": ("Dəstəklənməyən fayl", "Desteklenmeyen dosya"),
    "unsupported media type": ("Dəstəklənməyən media tipi", "Desteklenmeyen medya türü"),
    "user already admin or cannot be promoted": ("İstifadəçi onsuz da admindir və ya yüksəldilə bilmir", "Kullanıcı zaten yönetici veya yükseltilemiyor"),
    "userbot rebooted": ("Userbot yenidən başladıldı", "Userbot yeniden başlatıldı"),
    "userbot stopped": ("Userbot dayandırıldı", "Userbot durduruldu"),
    "welcome reset": ("Qarşılama sıfırlandı", "Karşılama sıfırlandı"),
    "word list already empty": ("Söz siyahısı onsuz da boşdur", "Kelime listesi zaten boş"),

    # ── Modul mesajları ───────────────────────────────────────────────────
    "no data found for the bot user.": ("Bot istifadəçisi üçün məlumat tapılmadı.", "Bot kullanıcısı için veri bulunamadı."),
    "you have been approved and added to the whitelist.": ("Təsdiqləndiniz və ağ siyahıya əlavə edildiniz.", "Onaylandınız ve beyaz listeye eklendiniz."),
    "you have been removed from the whitelist and your message count has been reset.": ("Ağ siyahıdan çıxarıldınız və mesaj sayğacınız sıfırlandı.", "Beyaz listeden çıkarıldınız ve mesaj sayacınız sıfırlandı."),
    "you are not in the whitelist.": ("Ağ siyahıda deyilsiniz.", "Beyaz listede değilsiniz."),
    "you are already in the whitelist.": ("Onsuz da ağ siyahıdasınız.", "Zaten beyaz listedesiniz."),
    "there were no whitelisted users to remove.": ("Silinəcək ağ siyahı istifadəçisi yox idi.", "Silinecek beyaz liste kullanıcısı yoktu."),
    "no count found for your chat id.": ("Chat ID-niz üçün sayğac tapılmadı.", "Sohbet ID'niz için sayaç bulunamadı."),
    "no blacklist found for this bot.": ("Bu bot üçün qara siyahı tapılmadı.", "Bu bot için kara liste bulunamadı."),
    "invalid chat id. please provide a valid integer.": ("Yanlış chat ID. Düzgün rəqəm daxil edin.", "Geçersiz sohbet ID. Lütfen geçerli bir sayı girin."),
    "blacklist is empty.": ("Qara siyahı boşdur.", "Kara liste boş."),
    "all whitelisted users have been removed.": ("Ağ siyahıdakı bütün istifadəçilər silindi.", "Beyaz listedeki tüm kullanıcılar silindi."),
    "all users' message counts have been reset to 0.": ("Bütün istifadəçilərin mesaj sayğacı 0-a sıfırlandı.", "Tüm kullanıcıların mesaj sayaçları 0'a sıfırlandı."),
    "please provide code to evaluate.": ("İcra üçün kod daxil edin.", "Çalıştırmak için kod girin."),
    "you need to reply to a message or provide a user id.": ("Bir mesaja cavab verin və ya istifadəçi ID daxil edin.", "Bir mesaja yanıt verin veya kullanıcı ID girin."),
    "the replied message is not from a user.": ("Cavab verilən mesaj istifadəçidən deyil.", "Yanıtlanan mesaj bir kullanıcıya ait değil."),
    "please provide a valid user id.": ("Düzgün istifadəçi ID daxil edin.", "Lütfen geçerli bir kullanıcı ID girin."),
    "no sudoers list found.": ("Sudo siyahısı tapılmadı.", "Sudo listesi bulunamadı."),
    "no used words to reset.": ("Sıfırlanacaq işlənmiş söz yoxdur.", "Sıfırlanacak kullanılmış kelime yok."),
    "all used words have been reset.": ("Bütün işlənmiş sözlər sıfırlandı.", "Tüm kullanılmış kelimeler sıfırlandı."),
    "no active auto-game.": ("Aktiv avto-oyun yoxdur.", "Aktif otomatik oyun yok."),
    "welcome message too long. maximum 4096 characters allowed.": ("Qarşılama mesajı çox uzundur. Maksimum 4096 simvol.", "Karşılama mesajı çok uzun. En fazla 4096 karakter."),
    "welcome logo and message successfully reset": ("Qarşılama loqosu və mesajı sıfırlandı", "Karşılama logosu ve mesajı sıfırlandı"),
    "only photos, videos, gifs, and stickers are allowed.": ("Yalnız şəkil, video, GIF və stikerlərə icazə verilir.", "Sadece resim, video, GIF ve çıkartmalara izin verilir."),
    "nothing to update. message must contain text and/or media.": ("Yeniləmək üçün heç nə yoxdur. Mesajda mətn və/və ya media olmalıdır.", "Güncellenecek bir şey yok. Mesaj metin ve/veya medya içermeli."),
    "media size cannot exceed 5mb.": ("Media ölçüsü 5MB-ı keçə bilməz.", "Medya boyutu 5MB'ı geçemez."),
    "something went wrong ending the call.": ("Zəngi bitirərkən xəta baş verdi.", "Aramayı sonlandırırken hata oluştu."),
    "no active group call found.": ("Aktiv qrup zəngi tapılmadı.", "Aktif grup araması bulunamadı."),
    "failed to start group call": ("Qrup zəngi başladıla bilmədi", "Grup araması başlatılamadı"),
    "ended group call": ("Qrup zəngi bitirildi", "Grup araması sonlandırıldı"),
    "user promoted successfully.": ("İstifadəçi uğurla yüksəldildi.", "Kullanıcı başarıyla yükseltildi."),
    "user demoted successfully.": ("İstifadəçinin hüququ uğurla azaldıldı.", "Kullanıcının yetkisi başarıyla düşürüldü."),
    "starting to invite users to voice chat...": ("İstifadəçilər səs söhbətinə dəvət olunur...", "Kullanıcılar sesli sohbete davet ediliyor..."),
    "invalid command usage. please provide promotion type and title.": ("Yanlış istifadə. Yüksəltmə tipi və başlıq daxil edin.", "Geçersiz kullanım. Yükseltme türü ve başlık girin."),
    "leaving this chat...": ("Bu söhbətdən çıxılır...", "Bu sohbetten çıkılıyor..."),
    "nothing given to gcast.": ("Gcast üçün heç nə verilmədi.", "Gcast için bir şey verilmedi."),
    "gcasting message...": ("Mesaj yayımlanır...", "Mesaj yayınlanıyor..."),
    "downloading media/document......": ("Media/sənəd endirilir......", "Medya/belge indiriliyor......"),
    "can' operate on file more than 2gb": ("2GB-dan böyük faylla işləmək mümkün deyil", "2GB'den büyük dosyada işlem yapılamaz"),
    "give me a valid delay(int) to spam.": ("Spam üçün düzgün gecikmə (rəqəm) verin.", "Spam için geçerli bir gecikme (sayı) verin."),
    "give me a valid count number(float) to spam.": ("Spam üçün düzgün say verin.", "Spam için geçerli bir sayı verin."),
    "atleast give me something to spam.": ("Heç olmasa spam üçün nəsə verin.", "En azından spam için bir şey verin."),
    "looks like there is no tagall here.": ("Deyəsən burada tagall yoxdur.", "Görünüşe göre burada tagall yok."),
    "give a message or reply to a message!": ("Mesaj yazın və ya bir mesaja cavab verin!", "Bir mesaj yazın veya bir mesaja yanıt verin!"),
    "dismissing mention.": ("Etiketləmə dayandırılır.", "Etiketleme durduruluyor."),
    "please reply to any sticker!": ("Zəhmət olmasa bir stikerə cavab verin!", "Lütfen bir çıkartmaya yanıt verin!"),
    "please reply to photo/gif/sticker media!": ("Zəhmət olmasa şəkil/GIF/stikerə cavab verin!", "Lütfen resim/GIF/çıkartmaya yanıt verin!"),
    "reply to any photo or sticker!": ("İstənilən şəkil və ya stikerə cavab verin!", "Herhangi bir resim veya çıkartmaya yanıt verin!"),
    "sticker has no name!": ("Stikerin adı yoxdur!", "Çıkartmanın adı yok!"),
    "creating a new sticker pack": ("Yeni stiker paketi yaradılır", "Yeni çıkartma paketi oluşturuluyor"),
    "successfully deleted alive keys (emoji, text)": ("Alive açarları uğurla silindi (emoji, mətn)", "Alive anahtarları başarıyla silindi (emoji, metin)"),
    "please provide some text or reply to a text": ("Mətn yazın və ya bir mətnə cavab verin", "Bir metin yazın veya bir metne yanıt verin"),
    "please provide an emoji": ("Bir emoji daxil edin", "Bir emoji girin"),
    "reply to an image/document": ("Şəkil/sənədə cavab verin", "Resim/belgeye yanıt verin"),
    "document must be an image type": ("Sənəd şəkil tipində olmalıdır", "Belge resim türünde olmalı"),
    "companion bot is not configured/started. cannot run inline command.": ("Köməkçi bot qurulmayıb/başladılmayıb. Inline əmr işə düşmür.", "Yardımcı bot yapılandırılmamış/başlatılmamış. Inline komut çalıştırılamıyor."),
    "already up to date.": ("Onsuz da ən son versiyadır.", "Zaten güncel."),
    "update applied. restarting...": ("Yeniləmə tətbiq edildi. Yenidən başladılır...", "Güncelleme uygulandı. Yeniden başlatılıyor..."),
    "dependencies changed — reinstalling...": ("Asılılıqlar dəyişdi — yenidən quraşdırılır...", "Bağımlılıklar değişti — yeniden kuruluyor..."),
    "you weren't afk": ("Siz AFK deyildiniz", "AFK değildiniz"),
    "collecting stats...": ("Statistika toplanır...", "İstatistikler toplanıyor..."),
    "no active group call": ("Aktiv qrup zəngi yoxdur", "Aktif grup araması yok"),
    "is up and running.": ("aktivdir və işləyir.", "aktif ve çalışıyor."),

    # ── Ümumi başlıq sözləri ──────────────────────────────────────────────
    "userbot settings": ("Userbot Ayarları", "Userbot Ayarları"),
    "features": ("Xüsusiyyətlər", "Özellikler"),
    "getting started": ("Başlanğıc", "Başlangıç"),
    "community": ("İcma", "Topluluk"),
    "updates": ("Yeniliklər", "Güncellemeler"),
    "commands": ("Əmrlər", "Komutlar"),
    "settings": ("Ayarlar", "Ayarlar"),
    "status": ("Vəziyyət", "Durum"),
    "help": ("Kömək", "Yardım"),
    "uptime": ("İşləmə müddəti", "Çalışma süresi"),
    "owner": ("Sahib", "Sahip"),
    "user": ("İstifadəçi", "Kullanıcı"),
    "group": ("Qrup", "Grup"),
    "channel": ("Kanal", "Kanal"),
    "usage": ("İstifadə", "Kullanım"),
    "total": ("Cəmi", "Toplam"),
    "plugins": ("Plaginlər", "Eklentiler"),
    "installed": ("Quraşdırıldı", "Kuruldu"),
    "uninstalled": ("Silindi", "Kaldırıldı"),
}

# Tam cümlələr — söz-söz tərcümədən əvvəl tətbiq olunur (uzunluğa görə sıralanır),
# beləliklə qarışıq dil (yarı ingilis / yarı türk) mətnlər yaranmır.
SENTENCES = {
    "Please choose a category to see its commands:": (
        "Əmrləri görmək üçün kateqoriya seçin:",
        "Komutları görmek için bir kategori seçin:",
    ),
    "No categories available.": ("Kateqoriya yoxdur.", "Kategori bulunamadı."),
    "This command is restricted to the userbot owner.": (
        "Bu əmr yalnız userbot sahibi üçündür.",
        "Bu komut sadece userbot sahibine özeldir.",
    ),
    "Userbot is already stopped.": (
        "Userbot artıq dayandırılıb.",
        "Userbot zaten durdurulmuş.",
    ),
    "Use /restart to bring it back online.": (
        "Yenidən işə salmaq üçün /restart yazın.",
        "Yeniden başlatmak için /restart yazın.",
    ),
    "Stopping userbot...": ("Userbot dayandırılır...", "Userbot durduruluyor..."),
    "The process will relaunch in a moment.": (
        "Proses bir anda yenidən başlayacaq.",
        "İşlem birazdan yeniden başlayacak.",
    ),
    "is Up and Running.": ("işləyir və aktivdir.", "çalışıyor ve aktif."),
    "Plugin installed successfully": (
        "Plagin uğurla quraşdırıldı",
        "Eklenti başarıyla kuruldu",
    ),
    "Plugin uninstalled successfully": (
        "Plagin uğurla silindi",
        "Eklenti başarıyla kaldırıldı",
    ),
    "No plugins installed": (
        "Quraşdırılmış plagin yoxdur",
        "Kurulu eklenti yok",
    ),
    "Reply to a .py file": (
        ".py faylına cavab verin",
        ".py dosyasına yanıt verin",
    ),
    "Only .py files are accepted": (
        "Yalnız .py faylları qəbul edilir",
        "Sadece .py dosyaları kabul edilir",
    ),
    "Something went wrong": ("Nəsə səhv getdi", "Bir şeyler ters gitti"),
    "Please try again": ("Yenidən yoxlayın", "Tekrar deneyin"),
    "Owner only": ("Yalnız sahib", "Sadece sahip"),
    "Not found": ("Tapılmadı", "Bulunamadı"),
    "Access denied": ("Giriş qadağandır", "Erişim reddedildi"),
    "Permission denied": ("İcazə yoxdur", "İzin yok"),
    "Invalid usage": ("Yanlış istifadə", "Hatalı kullanım"),
    "Successfully completed": ("Uğurla tamamlandı", "Başarıyla tamamlandı"),
    "Downloading...": ("Endirilir...", "İndiriliyor..."),
    "Uploading...": ("Yüklənir...", "Yükleniyor..."),
    "Processing...": ("Emal olunur...", "İşleniyor..."),
    "Restarting...": ("Yenidən başlayır...", "Yeniden başlatılıyor..."),
    "Success Rate": ("Uğur nisbəti", "Başarı oranı"),
    "Language changed": ("Dil dəyişdirildi", "Dil değiştirildi"),
}

PHRASES.update(SENTENCES)

# Smallcaps etiketlər (utils/message.py font.smallcaps ilə yaradılır)
_SMALLCAPS_LABELS = {
    "ᴇʀʀᴏʀ": ("Xəta", "Hata"),
    "ᴡᴀʀɴɪɴɢ": ("Xəbərdarlıq", "Uyarı"),
    "sᴜᴄᴄᴇss": ("Uğurlu", "Başarılı"),
    "ɪɴꜰᴏ": ("Məlumat", "Bilgi"),
}

_LANG_INDEX = {"az": 0, "tr": 1}

# Uzun ifadələr əvvəl əvəzlənsin
_SORTED_KEYS = sorted(PHRASES.keys(), key=len, reverse=True)

# Kod blokları, URL-lər, mention, əmrlər (.help) və HTML teqləri toxunulmaz qalır
_PROTECTED = re.compile(
    r"(<[^>\n]{1,80}>|```.*?```|`[^`\n]*`|https?://\S+|tg://\S+|@[A-Za-z0-9_]{3,}"
    r"|[./!?^_][A-Za-z][A-Za-z0-9_]{1,24}|&[a-z]+;)",
    re.DOTALL,
)


def _keep_case(original: str, replacement: str) -> str:
    """Orijinal mətnin böyük/kiçik hərf formasını qoru."""
    if original.isupper() and len(original) > 3:
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def _replace_segment(segment: str, idx: int) -> str:
    out = segment
    for key in _SORTED_KEYS:
        value = PHRASES[key][idx]
        if re.fullmatch(r"[A-Za-z]+", key):
            pattern = re.compile(r"\b" + re.escape(key) + r"\b", re.IGNORECASE)
        else:
            pattern = re.compile(re.escape(key), re.IGNORECASE)
        if pattern.search(out):
            out = pattern.sub(lambda m: _keep_case(m.group(0), value), out)
    for key, value in _SMALLCAPS_LABELS.items():
        if key in out:
            out = out.replace(key, value[idx])
    return out


def translate(text, lang=None):
    """Mətni aktiv dilə çevir. Kod blokları/linklər dəyişmir."""
    if not text or not isinstance(text, str):
        return text
    lang = lang or get_lang()
    idx = _LANG_INDEX.get(lang)
    if idx is None:  # en → orijinal mətn
        return text
    try:
        parts = _PROTECTED.split(text)
        for i in range(0, len(parts), 2):  # yalnız qorunmayan hissələr
            parts[i] = _replace_segment(parts[i], idx)
        return "".join(parts)
    except Exception as e:  # heç vaxt mesajı sındırma
        logger.debug("translate failed: %s", e)
        return text


# ─────────────────────────────────────────────────────────────────────────────
# Aktiv dil idarəsi (MongoDB-də saxlanılır — hər istifadəçi üçün ayrıca sənəd)
# ─────────────────────────────────────────────────────────────────────────────
def bind_storage(collection, owner_id=None):
    """MongoDB kolleksiyasını və sahibin ID-sini bağla."""
    global _collection, _owner_id
    _collection = collection
    if owner_id:
        _owner_id = owner_id


def load_lang_from_db(user_id):
    """Restartdan sonra dili bazadan yüklə."""
    global _active_lang, _owner_id
    _owner_id = user_id
    if _collection is None:
        return _active_lang
    try:
        doc = _collection.find_one({"user_id": user_id}) or {}
        lang = doc.get("language")
        if lang in SUPPORTED:
            _active_lang = lang
    except Exception as e:
        logger.warning("Dil bazadan yüklənmədi / language load failed: %s", e)
    return _active_lang


def set_lang(lang, user_id=None):
    """Dili dəyiş və MongoDB-yə yaz (kalıcı)."""
    global _active_lang
    if lang not in SUPPORTED:
        return False
    _active_lang = lang
    uid = user_id or _owner_id
    if _collection is not None and uid:
        try:
            _collection.update_one(
                {"user_id": uid}, {"$set": {"language": lang}}, upsert=True
            )
        except Exception as e:
            logger.warning("Dil yadda saxlanmadı / language save failed: %s", e)
    return True


def get_lang():
    return _active_lang


# ─────────────────────────────────────────────────────────────────────────────
# Pyrogram hook: bütün çıxan mətnlər avtomatik tərcümə olunur
# ─────────────────────────────────────────────────────────────────────────────
_installed = False


def install_hook():
    """Monkeypatch Pyrogram so every outgoing text is translated."""
    global _installed
    if _installed:
        return
    try:
        from pyrogram.client import Client as _Client
        from pyrogram.types import Message as _Message
    except Exception as e:
        logger.warning("i18n hook yüklənmədi: %s", e)
        return

    def _wrap(owner, name, arg_index):
        original = getattr(owner, name, None)
        if original is None or getattr(original, "_i18n", False):
            return

        async def wrapper(self, *args, **kwargs):
            try:
                if "text" in kwargs:
                    kwargs["text"] = translate(kwargs["text"])
                elif "caption" in kwargs and name.endswith("media") is False and args:
                    pass
                if len(args) > arg_index and isinstance(args[arg_index], str):
                    args = list(args)
                    args[arg_index] = translate(args[arg_index])
                    args = tuple(args)
                if "caption" in kwargs and isinstance(kwargs["caption"], str):
                    kwargs["caption"] = translate(kwargs["caption"])
            except Exception:
                pass
            return await original(self, *args, **kwargs)

        wrapper._i18n = True
        wrapper.__name__ = name
        setattr(owner, name, wrapper)

    # Client metodları
    _wrap(_Client, "send_message", 1)
    _wrap(_Client, "edit_message_text", 2)
    # Message metodları
    for meth in ("edit_text", "edit", "reply_text", "reply"):
        _wrap(_Message, meth, 0)

    _installed = True
    logger.info("i18n hook aktivdir / active (lang=%s)", _active_lang)

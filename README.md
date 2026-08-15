# 🤖 Ryhavean Userbot

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Updates-blue?logo=telegram)](https://t.me/ryhaveanupdates)

**Ryhavean Userbot** - Telegram-da çox güclü və funksiyaca zəngin bir istifadəçi botu. Pyrogram ilə quruluşdur.

> 📢 **Rəsmi Kanallar**
> - 📰 [Updates Channel](https://t.me/ryhaveanupdates)
> - 👥 [Team Group](https://t.me/RyhaveanTeam)

---

## ✨ Əsas Xüsusiyyətlər

### 🎵 Musiqi & Əyləncə
- **Ses Söhbətində Musiqi**: Telegram ses söhbətlərində musiqi çal
- **YouTube Axtarışı**: YouTubedan musiqi tap və çal
- **Sıra İdarəsi**: Musiqi sırasını idarə et
- **Media Dəstəyi**: Müxtəlif formatları dəstəkləyir

### 📁 Faylları İdarə Etmə
- **Avtomatik Yüklənə**: Kanallardan medianı avtomatik saxla
- **Faylları İdarə Et**: Faylları yüklə, endir və sax
- **Media Emalı**: Şəkil və video emal et

### 🛠️ Faydalı Alətkisən
- **Statistika**: Söhbət və istifadəçi fəaliyyətini izlə
- **Sessiya İdarəsi**: Telegram sessialarını bax
- **Ping/Uptime**: Sistemin işləyən vəziyyətini yoxla
- **Məlumat Komandaları**: İstifadəçi və söhbət haqqında məlumat

### 🎨 Şəxsiləşdirmə
- **Yazı Tərzi**: Müxtəlif yazı stilləri tətbiq et
- **Çıxarmazlar**: Custom çıxarmazları idarə et
- **Profil Rəngləməsi**: Profili klon et

### 🔧 Admin Alətkələri
- **İstifadəçi İdarəsi**: İstifadəçiləri idarə et
- **Spam Mübarizəsi**: Spam aşkarla və qarşısını al
- **Mesaj İdarəsi**: Mesajları sil, təmizlə

### 🤖 AI Integrasyonu
- **AI Agent**: `.ask` ilə AI modeli sor
- **Ağıllı Cavablar**: AI-powered məsələ həlli

### 📱 Ünsiyyət
- **Avtomatik Cavab**: Şəxsi söhbətlərdə avtomatik cavab
- **AFK Sistemi**: Uzaqda olduğunu göstər
- **Yayımlama**: Bir çox söhbətə mesaj göndər

### 🎮 Oyunlar & Əyləncə
- **Word Games**: Sözləri tapan oyun
- **Automatic Solvers**: Oyun həlləricisi
- **Custom Responses**: Şəxsi cavablar

---

## 🚀 Sürətli Başlanğıc

### Tələblər
- Python 3.11+
- MongoDB (Pulsuz: [Atlas](https://mongodb.com/cloud/atlas))
- Telegram API Keys (my.telegram.org)

### Quraşdırma

```bash
# Repo klon et
git clone https://github.com/yourusername/ryhavean-userbot.git
cd ryhavean-userbot

# Paketləri quraşdır
pip install -r requirements.txt

# .env faylı yarad
cp .env.example .env

# Dəyişənləri redaktə et
nano .env
```

### .env Dəyişənləri

```env
# Telegram (my.telegram.org-dan)
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH

# Session String (pyrogram ilə əldə et)
SESSION_STR=YOUR_SESSION_STRING

# Bot Token (@BotFather-dan)
BOT_TOKEN=YOUR_BOT_TOKEN

# MongoDB
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ryhavean_userbot

# Ryhavean Channels
GROUP=RyhaveanTeam
CHANNEL=ryhaveanupdates
```

### Botun Başladılması

```bash
# Lokal çalıştır
python main.py

# Render-ə deploy et
# RENDER_DEPLOYMENT.md bax
```

---

## 📋 Komandalar

### Ümumi Komandalar
- `.alive` - Botun işləyib-işləməməsini yoxla
- `.help` - Kömək mesajını gör
- `.ping` - Gecikməni ölç (ms)

### Dil Komandaları
- `.dildeyis az` - Azərbaycancaya dəyiş
- `.dildeyis tr` - Türkçəyə dəyiş
- `.dildeyis en` - Ingilizcəyə dəyiş

### Plağin Komandaları
- `.pinstall` - .py faylına cavab vərərək quraşdır
- `.puninstall <adı>` - Plağini sil
- `.plist` - Quraşdırılmış plağinləri gör

### Admin Komandaları
- `.ban` - İstifadəçini ban et
- `.unban` - Ban ləğv et
- `.kick` - Qrupdan çıxar
- `.mute` - Sustur
- `.promote` - Admin et

### Musiqi Komandaları
- `.play <musiqi>` - Musiqi çal
- `.stop` - Musiqini dayandır
- `.skip` - Sonrakısına keç
- `.queue` - Sıraları gör

---

## 🌐 Render-ə Deploy (24/7)

Render free tier-də pulsuz 24/7 hoisting:

```bash
# RENDER_DEPLOYMENT.md faylını oxu
cat RENDER_DEPLOYMENT.md
```

**Məsələn üçün:**
1. GitHub-a push et
2. Render.com-a daxil ol
3. Repo-nu seç və deploy et
4. .env dəyişənlərini əlavə et
5. Uptime Robot konfigur et

---

## 📦 Verilənlər Saxlama

Ryhavean Userbot **MongoDB** ilə verilənləri saxlayır:

- **Hər istifadəçi ayrıca data**: Müstəqil verilənlər
- **Persistent Storage**: Restart olunsa da data qalmaz
- **Pulsuz**: MongoDB Atlas pulsuz

```env
# Pulsuz MongoDB istifadə et
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

---

## 🔐 Təhlükəsizlik

⚠️ **ÖNEMLİ**: 

- SESSION_STR-i asla şəhər edin
- BOT_TOKEN-i asla paylaşmayın
- `.env` faylını `.gitignore`-a əlavə et
- Source code-u öz əminliyiniz üçün saxlayın

```bash
# .gitignore-da var mı?
grep SESSION_STR .gitignore
grep BOT_TOKEN .gitignore
```

---

## 🛠️ Çox Vaxt Soruşulan Suallar

**S: Render-də uyqu problemi var?**
C: Uptime Robot istifadə et, 5 dəqiqə hər 5 dəqiqə ping göndir

**S: Database bağlantısı xətası?**
C: MONGO_URI düzəldildiyinə əmin ol, IP whitelist aç

**S: Komandalar işləmirlər?**
C: `.alive` yaz əvvəlcə, sonra digər komandalı yaz

**S: Başqa plağin əlavə etmək?**
C: `.pinstall` - .py faylına cavab vər

---

## 📚 Əlavə Qaynaqlar

- 📖 [Pyrogram Docs](https://docs.pyrogram.org)
- 🗄️ [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- 🚀 [Render Docs](https://render.com/docs)
- 📞 [Telegram API](https://core.telegram.org)

---

## 👥 Dəstək

Problemlər olsa əlaqə saxla:

- 📢 **Updates Channel**: [@ryhaveanupdates](https://t.me/ryhaveanupdates)
- 👥 **Team Group**: [@RyhaveanTeam](https://t.me/RyhaveanTeam)

---

## 📄 Lisenziya

MIT License - Dəfət mit istifadə et, dəyiş, paylış

[LICENSE](LICENSE) faylına bax ətraflı məlumat üçün

---

## 🙏 Təşəkkürü

Bu bot aşağıdakı layihələrə əsasən hazırlanıb:
- **Pyrogram** - Telegram API Python kitabxanası
- **Heroku/Render** - Cloud hosting

---

**Ryhavean Userbot v1.0.0**

🤖 Powered by Pyrogram | 📢 [@ryhaveanupdates](https://t.me/ryhaveanupdates)

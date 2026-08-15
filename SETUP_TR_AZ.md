# 🤖 Ryhavean Userbot - Quraşdırma Kılavuzu
# 🤖 Ryhavean Userbot - Kurulum Rehberi

## 📋 Azərbaycanca / Türkçe

---

# AZƏRBAYCANCA BÖLÜM

## 1️⃣ Tələblər (Sistem Məsələri)

```
✓ Python 3.11 və ya daha yükşəgi
✓ MongoDB (Pulsuz: atlas.mongodb.com)
✓ Telegram Hesabı (kişi hesabı)
✓ Git (Render-ə deploy etmək üçün)
```

## 2️⃣ API Keys-lərin Əldə Edilməsi

### Telegram API Keys (my.telegram.org)

1. https://my.telegram.org qeydiyyatdan keçin
2. "API Development Tools" seçin
3. "Create new application" düyməsinə basın
4. Məlumatları doldurun:
   - **App title**: Ryhavean Userbot
   - **Short name**: ryhavean-userbot
5. **api_id** və **api_hash**-ı kopyalayın

### Bot Token (@BotFather-dan)

1. Telegram-da [@BotFather](https://t.me/BotFather) yazın
2. `/newbot` komandası yazın
3. Bot adını yazın: `Ryhavean Bot`
4. Bot username-i yazın: `ryhavean_xxxbot`
5. Token-i kopyalayın

### MongoDB URI (Free Cluster)

1. https://mongodb.com/cloud/atlas qeydiyyatdan keçin
2. Pulsuz cluster yaradın
3. Username və password seçin
4. "Allow Access from Anywhere" (`0.0.0.0/0`) seçin
5. Connection string kopyalayın:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

## 3️⃣ Pyrogram Session String-i Əldə Etmə

Session string olmadan userbot işləməz. Əldə etmə:

```bash
# Python yüklü olmalıdır
pip install pyrogram tgcrypto

# Python interaksiyası aç
python

# Aşağıdakı kodu yapışdır:
from pyrogram import Client

async def get_session():
    async with Client("my_session", api_id=YOUR_API_ID, api_hash="YOUR_API_HASH") as app:
        print(app.export_session_string())

import asyncio
asyncio.run(get_session())
```

**İşlem:**
1. API_ID-ni dəyiş
2. API_HASH-ı dəyiş
3. Təlimləri izlə
4. Telefon nömrənizi daxil edin
5. OTP (SMS) kodu daxil edin
6. Session string-i kopyalayın

## 4️⃣ .env Faylı Yaradın

Layihə qovluğunda `.env` faylı yaradın:

```env
# ════════════════════════════════════
# TELEGRAM API (Tələb Edilir)
# ════════════════════════════════════
API_ID=123456789
API_HASH=abcdefghijklmnopqrstuvwxyz0
SESSION_STR=BQA_xxxxxxxxxxxxxxxxxxxxxxxxxxx
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWxyz

# ════════════════════════════════════
# MONGODB (Pulsuz: Atlas)
# ════════════════════════════════════
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ryhavean_userbot

# ════════════════════════════════════
# RYHAVEAN CHANNELS
# ════════════════════════════════════
GROUP=RyhaveanTeam
CHANNEL=ryhaveanupdates
TEAM_CHANNEL=RyhaveanTeam
UPDATE_CHANNEL=ryhaveanupdates

# ════════════════════════════════════
# DEPLOYMENT (Render üçün)
# ════════════════════════════════════
DEPLOYMENT_PLATFORM=render
```

## 5️⃣ Lokal Çalıştırma

```bash
# Qovluğa daxil ol
cd ryhavean-userbot

# Paketləri yükləyin
pip install -r requirements.txt

# Botun başladın
python main.py

# Səbətə mesaj gönder
# .alive yazarsa javab verəcəkdir
```

## 6️⃣ Render-ə Deploy (24/7)

### GitHub-a Push Et

```bash
git add .
git commit -m "Initial Ryhavean Userbot setup"
git push origin main
```

### Render-ə Deploy Et

1. https://render.com qeydiyyatdan keçin
2. Dashboard-a daxil olun
3. "New +" → "Web Service" seçin
4. GitHub repo-nuz seçin
5. Quraşdırma:
   ```
   Name: ryhavean-userbot
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   Instance: Free
   ```
6. "Advanced" → "Add Environment Variable"
7. .env dəyişənlərini əlavə edin
8. "Deploy" düyməsinə basın

### Uptime Robot (Opsiyonal ama Tövsiyə Edilir)

Render free-də botun uyqu problemi yaşanırsa:

1. https://uptimerobot.com qeydiyyatdan keçin
2. "New Monitor" seçin
3. URL: `https://your-app.onrender.com/status`
4. Interval: 5 dəqiqə
5. Tamam

## 7️⃣ Komanda Testi

Bot quraşdırıldıqdan sonra tət edin:

```
.alive          → Bot vəziyyətini yoxla
.dildeyis az    → Dili Azərbaycancaya dəyiş
.dildeyis tr    → Dili Türkçəyə dəyiş
.help           → Komandaları gör
.pinstall       → Plağin quraşdır (faylına cavab vər)
.plist          → Plağinləri sırala
```

---

# TÜRKÇE BÖLÜM

## 1️⃣ Gereksinimler (Sistem Gereksinimleri)

```
✓ Python 3.11 ve üzeri
✓ MongoDB (Ücretsiz: atlas.mongodb.com)
✓ Telegram Hesabı (kişi hesabı)
✓ Git (Render'a dağıtım için)
```

## 2️⃣ API Anahtarlarının Alınması

### Telegram API Anahtarları (my.telegram.org)

1. https://my.telegram.org'a kaydolun
2. "API Development Tools" öğesini seçin
3. "Create new application" düğmesine tıklayın
4. Bilgileri doldurun:
   - **App title**: Ryhavean Userbot
   - **Short name**: ryhavean-userbot
5. **api_id** ve **api_hash**'ı kopyalayın

### Bot Tokeni (@BotFather'dan)

1. Telegram'da [@BotFather](https://t.me/BotFather) yazın
2. `/newbot` komutunu yazın
3. Bot adını yazın: `Ryhavean Bot`
4. Bot kullanıcı adını yazın: `ryhavean_xxxbot`
5. Token'i kopyalayın

### MongoDB URI (Ücretsiz Cluster)

1. https://mongodb.com/cloud/atlas'a kaydolun
2. Ücretsiz bir cluster oluşturun
3. Kullanıcı adı ve şifreyi seçin
4. "Allow Access from Anywhere" (`0.0.0.0/0`) seçeneğini işaretleyin
5. Bağlantı dizesini kopyalayın:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

## 3️⃣ Pyrogram Oturum Dizesini Alın

Oturum dizesi olmadan userbot çalışmaz. Almak için:

```bash
# Python yüklü olmalıdır
pip install pyrogram tgcrypto

# Python etkileşimini aç
python

# Aşağıdaki kodu yapıştır:
from pyrogram import Client

async def get_session():
    async with Client("my_session", api_id=YOUR_API_ID, api_hash="YOUR_API_HASH") as app:
        print(app.export_session_string())

import asyncio
asyncio.run(get_session())
```

**Adımlar:**
1. API_ID'yi değiştir
2. API_HASH'ı değiştir
3. Talimatları izle
4. Telefon numaranızı girin
5. OTP (SMS) kodunu girin
6. Oturum dizesini kopyalayın

## 4️⃣ .env Dosyasını Oluşturun

Proje klasöründe `.env` dosyası oluşturun:

```env
# ════════════════════════════════════
# TELEGRAM API (Gerekli)
# ════════════════════════════════════
API_ID=123456789
API_HASH=abcdefghijklmnopqrstuvwxyz0
SESSION_STR=BQA_xxxxxxxxxxxxxxxxxxxxxxxxxxx
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWxyz

# ════════════════════════════════════
# MONGODB (Ücretsiz: Atlas)
# ════════════════════════════════════
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ryhavean_userbot

# ════════════════════════════════════
# RYHAVEAN CHANNELS
# ════════════════════════════════════
GROUP=RyhaveanTeam
CHANNEL=ryhaveanupdates
TEAM_CHANNEL=RyhaveanTeam
UPDATE_CHANNEL=ryhaveanupdates

# ════════════════════════════════════
# DEPLOYMENT (Render için)
# ════════════════════════════════════
DEPLOYMENT_PLATFORM=render
```

## 5️⃣ Yerel Çalıştırma

```bash
# Klasöre girin
cd ryhavean-userbot

# Paketleri yükleyin
pip install -r requirements.txt

# Bot'u başlatın
python main.py

# Hesabınıza mesaj gönderin
# .alive yazarsanız yanıt verecektir
```

## 6️⃣ Render'a Dağıt (24/7)

### GitHub'a Push Et

```bash
git add .
git commit -m "Initial Ryhavean Userbot setup"
git push origin main
```

### Render'a Dağıt

1. https://render.com'a kaydolun
2. Dashboard'a giriş yapın
3. "New +" → "Web Service" öğesini seçin
4. GitHub depo'nuzı seçin
5. Yapılandırma:
   ```
   Name: ryhavean-userbot
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   Instance: Free
   ```
6. "Advanced" → "Add Environment Variable"
7. .env değişkenlerini ekleyin
8. "Deploy" düğmesine tıklayın

### Uptime Robot (İsteğe Bağlı ama Önerilir)

Render free'de bot uyku sorunu yaşarsa:

1. https://uptimerobot.com'a kaydolun
2. "New Monitor" öğesini seçin
3. URL: `https://your-app.onrender.com/status`
4. Interval: 5 dakika
5. Kaydet

## 7️⃣ Komut Testi

Bot kurulduktan sonra test edin:

```
.alive          → Bot durumunu kontrol et
.dildeyis az    → Dili Azerbaycanca'ya değiştir
.dildeyis tr    → Dili Türkçe'ye değiştir
.help           → Komutları gör
.pinstall       → Eklentiyi kur (dosyaya cevap ver)
.plist          → Eklentileri listele
```

---

## 🔒 Güvenlik (Azərbaycanca / Türkçe)

### ⚠️ ÖNEMLİ / VACIB:

```
✗ SESSION_STR-i kimseyle PAYLAŞMA / PAYLAŞ
✗ BOT_TOKEN-i kimseyle PAYLAŞMA / PAYLAŞ  
✗ API_ID/HASH-ı kimseyle PAYLAŞMA / PAYLAŞ
✗ MONGO_URI-ni kimseyle PAYLAŞMA / PAYLAŞ
```

### Dosyaları Koru

```bash
# .gitignore kontrol et
cat .gitignore

# .env dosyasının içinde olması gerekir
echo ".env" >> .gitignore
```

---

## 🆘 Sıkça Sorulan Sorular / Tez-tez Soruşulan Suallar

### Q: "Bot başlamıyor" / "Bot başlamır"
**A**: 
- SESSION_STR kontrol et
- API_ID/HASH kontrol et
- MongoDB bağlantısını kontrol et

### Q: "Komutlar çalışmıyor" / "Komandalar işləmirlər"
**A**:
- `.alive` yazarak kontrol et
- Prefix doğru mu? (`.`, `!`, `?` vb.)

### Q: "Render'da bot uyuyor" / "Render'da bot yuxu gedir"
**A**:
- Uptime Robot konfigürasyonunu kontrol et
- 5 dakika interval ayarla

### Q: "Database bağlantı hatası" / "Veritabanı bağlantı xətası"
**A**:
- MONGO_URI kontrol et
- IP whitelist'i aç (`0.0.0.0/0`)

---

## 📞 Destek / Dəstək

Sorunlar olursa:
- 📢 Updates: [@ryhaveanupdates](https://t.me/ryhaveanupdates)
- 👥 Team: [@RyhaveanTeam](https://t.me/RyhaveanTeam)

---

**Ryhavean Userbot v1.0.0** | 🤖 Pyrogram Powered

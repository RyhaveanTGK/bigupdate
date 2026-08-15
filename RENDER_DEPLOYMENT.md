# 🚀 Ryhavean Userbot - Render Deployment Guide

Bu qılavuz Ryhavean Userbot-u Render free tier üzərində 24/7 işləməsi üçün necə yerləşdiriləcəyini göstərir.

## Render nədir?

Render, Heroku kimi bir cloud platform olmasına rəğmən, **daha yaxşı free tier** təqdim edir:
- **24/7 uptime** (uyqu yoxdur)
- **1GB RAM**
- **0.5 CPU**
- **Pulsuz MongoDB database**

---

## 📋 Tələblər

1. **Ryhavean Userbot** - Bu repo
2. **Render Account** - [render.com](https://render.com) adresində qeydiyyat
3. **Telegram Account** - Userbot üçün
4. **MongoDB Atlas** - Pulsuz cluster (Render-də də avtomatik əldə edilə bilər)
5. **Uptime Robot** - Opsiyonal (24/7 tutmaq üçün, [uptimerobot.com](https://uptimerobot.com))

---

## 🔧 Adım 1: MongoDB Bazasını Quraşdırın

### Seçenek A: Render-də MongoDB (Tövsiyə Edilir)

1. Render Dashboard-a daxil olun
2. "New +" → "PostgreSQL" seçin (MongoDB dəstəyi gəlir)
3. Veya **MongoDB Atlas**-ı istifadə edin (aşağıda)

### Seçenek B: MongoDB Atlas (Pulsuz)

1. [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) qeydiyyatdan keçin
2. Pulsuz cluster yaradın
3. Username və password seçin
4. IP whitelist-ə `0.0.0.0/0` əlavə edin (Render üçün)
5. Connection string kopyalayın:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

---

## 📝 Adım 2: .env Faylını Hazırlayın

Aşağıdakı tələb olunan dəyişənlərə sahib `.env` faylı yaradın:

```env
# Telegram API Credentials (my.telegram.org-dan)
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH

# Session String (pyrogram strings.session ilə əldə edin)
SESSION_STR=YOUR_SESSION_STRING

# Bot Token (@BotFather-dan)
BOT_TOKEN=YOUR_BOT_TOKEN

# MongoDB (Render istifadə edirsə)
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=ryhavean_userbot

# Ryhavean Channels
GROUP=RyhaveanTeam
CHANNEL=ryhaveanupdates
TEAM_CHANNEL=RyhaveanTeam
UPDATE_CHANNEL=ryhaveanupdates

# Render Deployment
DEPLOYMENT_PLATFORM=render
```

---

## 🚀 Adım 3: Render-ə Deploy Edin

### GitHub vasitəsilə Deploy (Tövsiyə Edilir)

1. Bu repo-yu GitHub-a push edin (ya da fork edin)
2. [Render.com](https://render.com) qeydiyyatdan keçin
3. Dashboard-da "New +" → "Web Service" seçin
4. GitHub repo-nuz seçin
5. Quraşdırma:
   - **Name**: `ryhavean-userbot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: `Free`

6. **Environment Variables** seçin və `.env` dəyişənlərini əlavə edin

### Manuel Deploy (CLI vasitəsilə)

```bash
# Render CLI yükləyin
npm install -g @render-oss/cli

# Qeydiyyatdan keçin
render login

# Deploy edin
render deploy --repo https://github.com/YOUR_USERNAME/ryhavean-userbot
```

---

## 🤖 Adım 4: Uptime Robot Quraşdırması (24/7 Tutmaq üçün)

Render free tier-də, xidmətlər 15+ dəqiqə inactivity sonra uyqu vəziyyətinə gedir. Bundan çəkinmək üçün:

### Uptime Robot Xidməti:

1. [Uptime Robot](https://uptimerobot.com) qeydiyyatdan keçin (Pulsuz)
2. "New Monitor" seçin
3. Quraşdırma:
   - **Type**: `HTTP(s)`
   - **URL**: `https://your-render-app.onrender.com/status`
   - **Monitoring Interval**: `5 minutes`
   - **Alert Contacts**: Email və ya Telegram

4. Render-in status endpoint-i əlavə ediləcəkdir:
   ```
   GET /health → JSON response
   GET /ping   → pong
   GET /status → HTML status page
   ```

---

## ✅ Kontrol Nöqtələri

Deployment uğurlu oldu mu?

```bash
# 1. Status endpoint test edin
curl https://your-render-app.onrender.com/status

# 2. Telegram bot-u sınayın
# Botunuza .alive yazın - cavab verməlidir

# 3. Logs-u görün
# Render Dashboard → Logs
```

---

## 📊 Sistem Dəyişənləri

Render deployment-ə əlavə edilən dəyişənlər:

| Dəyişən | Dəyər | Məqsəd |
|---------|-------|--------|
| `DEPLOYMENT_PLATFORM` | `render` | Render-də olunduğu tanıtmaq |
| `RENDER` | `true` | Render tərəfindən avtomatik təyin olunur |
| `PORT` | `8000` | Uptime Robot üçün HTTP port |

---

## 🛠 Faydalı Komandalar

```bash
# Logs-u real-time görmək
render logs --tail -f

# Service restart
render deploy --id your-service-id

# Enviroment dəyişkənləri dəyişmək
render env update
```

---

## 🚨 Ümumi Problemlər

### Problem: "Bot uyanmır"
**Həll**: Uptime Robot konfigurə edin və 5 dəqiqəlik interval təyin edin

### Problem: "Database bağlantı xətas"
**Həll**: MONGO_URI düzəldildiyinə əmin olun və IP whitelist açıq olsun

### Problem: "SESSION_STR xətası"
**Həll**: `.env` faylındakı SESSION_STR-in doğru olduğundan əmin olun

### Problem: "Module not found"
**Həll**: 
```bash
render deploy --build-command "pip install --no-cache-dir -r requirements.txt"
```

---

## 📞 Dəstək

Problemlər olsa:
- 📢 Kanal: [@ryhaveanupdates](https://t.me/ryhaveanupdates)
- 👥 Qrup: [@RyhaveanTeam](https://t.me/RyhaveanTeam)

---

## 💰 Xərc Cədvəli (Aylıq)

| Xidmət | Qiymət |
|--------|--------|
| Render Web Service (Free) | $0 |
| MongoDB Atlas (Free) | $0 |
| Uptime Robot (Free) | $0 |
| **CƏMİ** | **$0** |

---

## 📚 Əlavə Qaynaqlar

- [Render Docs](https://render.com/docs)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Pyrogram Docs](https://docs.pyrogram.org)
- [Uptime Robot Help](https://uptimerobot.com/help/)

---

**Ryhavean Userbot v1.0.0** | 🤖 Powered by Pyrogram

---

# ✅ Yekun Yoxlama Cədvəli / Son Kontrol Listesi (v1.0 — Ryhavean)

## 1. Render-də servis yaratmaq

1. GitHub-a bu repo-nu push edin.
2. [render.com](https://render.com) → **New +** → **Blueprint** (repo-dakı `render.yaml` avtomatik oxunur).
   - Blueprint istəməsəniz: **New +** → **Web Service** → repo seçin →
     Build: `pip install -r requirements.txt` → Start: `python main.py` → Plan: **Free**.
3. **Health Check Path** = `/health`
4. **Environment** bölməsindən aşağıdaki dəyişənləri əlavə edin.

## 2. ENV — tam siyahı

### Məcburi / Zorunlu

| Key | Dəyər / Nə üçün |
|---|---|
| `API_ID` | my.telegram.org → API ID |
| `API_HASH` | my.telegram.org → API HASH |
| `SESSION_STR` | Pyrogram/Kurigram session string (userbot hesabı) |
| `BOT_TOKEN` | @BotFather-dan alınan bot tokeni |
| `MONGO_URI` | `mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority` |

### Tövsiyə edilən / Önerilen

| Key | Standart | İzah |
|---|---|---|
| `DB_NAME` | `ryhavean_userbot` | MongoDB baza adı |
| `STORAGE_BACKEND` | `mongo` | `mongo` / `sqlite` / `memory` |
| `DEFAULT_LANG` | `az` | Başlanğıc dil: `az`, `tr`, `en` |
| `DEPLOYMENT_PLATFORM` | `render` | Render rejimi (health server açılır) |
| `PORT` | `8000` | Render özü verir, əl ilə lazım deyil |
| `USER_PLUGINS_DIR` | `user_plugins` | `.pinstall` plaginlərinin qovluğu |
| `EXTRA_PLUGINS_DIR` | `plugins` | Repo daxilindəki əlavə plaginlər |
| `GROUP` / `TEAM_CHANNEL` | `RyhaveanTeam` | https://t.me/RyhaveanTeam |
| `CHANNEL` / `UPDATE_CHANNEL` | `ryhaveanupdates` | https://t.me/ryhaveanupdates |

### Opsional (AI və YouTube)

| Key | İzah |
|---|---|
| `AI_API_KEY`, `AI_BASE_URL` | `.ask` AI əmri üçün (ikisi birlikdə) |
| `AGENT_MODEL`, `AGENT_VISION_MODEL` | Model adları |
| `AGENT_ALLOW_SHELL`, `AGENT_ALLOW_MODERATION`, `AGENT_ALLOW_TELEGRAM_API` | Default `false` — təhlükəsizlik üçün belə qalsın |
| `YT_DLP_API_KEY`, `YT_DLP_BASE_URL` | YouTube endirmə API-si (öz serveriniz) |
| `SQLITE_PATH` | Yalnız `STORAGE_BACKEND=sqlite` olarsa |

## 3. Uptime Robot ilə 7/24

1. [uptimerobot.com](https://uptimerobot.com) → **Add New Monitor**
2. Monitor Type: **HTTP(s)**
3. URL: `https://<render-servis-adınız>.onrender.com/health`
4. Monitoring Interval: **5 minutes**
5. Save. Render free tier 15 dəqiqə hərəkətsizlikdə yatdığı üçün bu ping xidməti ayıq saxlayır.

Mövcud endpointlər: `/health` (JSON), `/ping` (`pong`), `/status` (HTML panel), `/` .

## 4. MongoDB kalıcılığı

- Hər istifadəçi üçün `user_sessions` kolleksiyasında **ayrıca sənəd** (`user_id` açarı ilə) saxlanılır:
  dil seçimi, ayarlar, sudo istifadəçilər, `.pinstall` ilə quraşdırılmış plaginlərin **tam kodu**.
- Render diski efemerdir: hər deploy/restartda disk sıfırlanır, lakin start zamanı
  `restore_user_plugins()` bütün plaginləri MongoDB-dən diskə geri yazır və canlı yükləyir.
  Nəticə: **restart, deploy və ya crash zamanı heç nə silinmir.**

## 5. Plagin əmrləri

| Əmr | İş |
|---|---|
| `.pinstall` | `.py` faylına **reply** edin → plagin quraşdırılır, MongoDB-yə yazılır, dərhal aktiv olur |
| `.unpinstall <ad>` | Plagini silir (bazadan və diskdən). Arqumentsiz yazsanız siyahı gəlir |
| `.plist` | Quraşdırılmış plaginlərin siyahısı |

## 6. Dil əmri

| Əmr | Nəticə |
|---|---|
| `.dildeyis az` | Bütün userbot çıxışı **Azərbaycanca** |
| `.dildeyis tr` | Bütün userbot çıxışı **Türkçe** |
| `.dildeyis en` | English |

Seçim MongoDB-də saxlanılır — restartdan sonra da qüvvədədir.

## 7. Təhlükəsizlik

- Botun `/commands`, `/settings`, `/status`, `/ping`, `/stop`, `/restart` əmrləri **yalnız sahibə** açıqdır.
- Bot içindən **heç kim** öz hesabına userbot/avto-bot qura bilməz; kənar istifadəçi yalnız
  tanıtım mətnini və kanal linklərini görür.

# ✅ Deployment Checklist - SQLite Edition

## 🎯 Hızlı Kurulum (Adım Adım)

### 📋 Ön Hazırlık

- [ ] Node.js kurulu (v16+)
- [ ] n8n kurulu ve çalışıyor
- [ ] Telegram bot token'ınız hazır
- [ ] Workspace dosyaları indirildi

---

## 🔧 Kurulum Adımları

### 1️⃣ Paket Kurulumu (2 dakika)

```bash
cd /workspace
npm install
```

**Beklenen çıktı:**
```
✓ sqlite3@5.1.7
✓ Installed 15 packages
```

- [ ] ✅ Paketler kuruldu

---

### 2️⃣ Database Oluşturma (1 dakika)

```bash
npm run init
```

**Beklenen çıktı:**
```
🚀 Starting database initialization...
✅ Connected to SQLite database
✅ [45/45] statements executed
📚 Vocabulary entries: 30
🎉 Setup complete!
```

**Kontrol:**
```bash
ls -lh turkish_learning_bot.db
# Dosya boyutu ~20KB olmalı
```

- [ ] ✅ Database oluşturuldu
- [ ] ✅ `turkish_learning_bot.db` dosyası var
- [ ] ✅ 30 kelime yüklendi

---

### 3️⃣ n8n Credentials (3 dakika)

#### A. SQLite Credential Oluştur

```
1. n8n'de sol menüden "Settings" → "Credentials"
2. Sağ üstten "Add Credential" tıkla
3. "SQLite" ara ve seç
4. İsimlendirme: "Turkish Bot SQLite"
5. Database Path: /workspace/turkish_learning_bot.db
   (veya tam path: /home/user/workspace/turkish_learning_bot.db)
6. "Save" tıkla
```

**Test:**
```sql
SELECT COUNT(*) FROM vocabulary;
-- Sonuç: 30 olmalı
```

- [ ] ✅ SQLite credential oluşturuldu
- [ ] ✅ Test sorgusu çalıştı

#### B. Telegram Credential Oluştur

```
1. "Add Credential" → "Telegram"
2. İsimlendirme: "Turkish Bot Telegram"
3. Access Token: YOUR_BOT_TOKEN
4. "Save" tıkla
```

- [ ] ✅ Telegram credential oluşturuldu

---

### 4️⃣ Workflow Import (2 dakika)

```
1. n8n → "Workflows" tab
2. Sağ üstten "Import from File"
3. "turkish_learning_bot_sqlite.json" seçin
4. Import başarılı!
```

- [ ] ✅ Workflow import edildi
- [ ] ✅ Workflow adı: "Turkish Learning Bot - SQLite Edition"

---

### 5️⃣ Node Konfigürasyonu (5 dakika)

**Yapılandırılması gereken node'lar:**

#### SQLite Node'ları (6 adet):

1. **Get Vocabulary (Prioritized)**
   - [ ] Credential: "Turkish Bot SQLite" seçildi
   - [ ] Query kontrol edildi
   
2. **Save Current Question**
   - [ ] Credential: "Turkish Bot SQLite" seçildi
   
3. **Get Current Question**
   - [ ] Credential: "Turkish Bot SQLite" seçildi
   
4. **Update Word History**
   - [ ] Credential: "Turkish Bot SQLite" seçildi
   
5. **Update User Progress**
   - [ ] Credential: "Turkish Bot SQLite" seçildi
   
6. **Get Stats**
   - [ ] Credential: "Turkish Bot SQLite" seçildi

#### Telegram Node'ları (5 adet):

1. **Telegram Trigger**
   - [ ] Credential: "Turkish Bot Telegram" seçildi
   
2. **Send Welcome**
   - [ ] Credential: "Turkish Bot Telegram" seçildi
   
3. **Send Question**
   - [ ] Credential: "Turkish Bot Telegram" seçildi
   
4. **Send Feedback**
   - [ ] Credential: "Turkish Bot Telegram" seçildi
   
5. **Send Statistics**
   - [ ] Credential: "Turkish Bot Telegram" seçildi
   
6. **Send Help**
   - [ ] Credential: "Turkish Bot Telegram" seçildi

**Tüm node'ları kontrol:**
- [ ] ✅ Hiçbir node'da kırmızı uyarı yok
- [ ] ✅ Tüm credentials atandı

---

### 6️⃣ Workflow Aktivasyonu (30 saniye)

```
1. Workflow'u aç
2. Sağ üstten "Active" toggle'ı aç
3. Yeşil "Active" yazısını gör
```

- [ ] ✅ Workflow aktif

---

### 7️⃣ Test (2 dakika)

#### Test 1: Welcome Message
```
Telegram'da botunuza: /start
```

**Beklenen çıktı:**
```
🎓 Welcome [İsminiz]!

I'm your Turkish language tutor! 🇹🇷

📚 Commands:
/quiz - Start quiz
/stats - View progress
/help - Show help

✨ Powered by SQLite - No limits!

Type /quiz to start! 🚀
```

- [ ] ✅ Welcome mesajı geldi

#### Test 2: Quiz
```
/quiz
```

**Beklenen çıktı:**
```
What is the correct Turkish translation for "Car"?

A) depo
B) araba
C) çiçek
D) elma

📝 Reply with A, B, C, or D
```

- [ ] ✅ Soru geldi
- [ ] ✅ 4 şık var
- [ ] ✅ 2 saniyeden kısa sürdü

#### Test 3: Answer
```
B
```

**Beklenen çıktı:**
```
Excellent! 🎉

✅ araba = Car

🎯 Type /quiz for next question!
```

- [ ] ✅ Feedback geldi
- [ ] ✅ Doğru/yanlış kontrolü çalışıyor

#### Test 4: Stats
```
/stats
```

**Beklenen çıktı:**
```
📊 Your Statistics
━━━━━━━━━━━━━━━━━━━

📈 Performance
  • Total: 1
  • Correct: ✅ 1
  • Wrong: ❌ 0
  • Accuracy: 100.0%

🔥 Streak
  • Current: 1
  • Best: 1
```

- [ ] ✅ İstatistikler geldi
- [ ] ✅ Sayılar doğru

#### Test 5: Multiple Questions
```
/quiz → Cevapla → /quiz → Cevapla (5 kez tekrar)
```

- [ ] ✅ 5 soru sorunsuz geldi
- [ ] ✅ "Quota exceeded" hatası YOK
- [ ] ✅ Yanıt hızlı (<1 saniye)

---

## 🎉 Kurulum Tamamlandı!

### ✅ Başarı Kriterleri

- [x] Database oluştu (30 kelime)
- [x] n8n credentials ayarlandı
- [x] Workflow import edildi
- [x] Tüm node'lar yapılandırıldı
- [x] Workflow aktif
- [x] /start çalışıyor
- [x] /quiz soru veriyor
- [x] Cevap kontrolü çalışıyor
- [x] /stats gösteriyor
- [x] 5+ soru sorunsuz

---

## 📊 Performans Kontrolü

### Benchmark Test

```bash
# Terminal'de n8n loglarını izleyin:
tail -f ~/.n8n/logs/n8n.log
```

**Telegram'da:**
```
/quiz → [Not Execution Time] → Cevap → [Not Time] (10 kez tekrar)
```

**Hedef:**
- Quiz response time: < 500ms
- Answer validation: < 200ms
- Stats response: < 200ms

- [ ] ✅ Performans hedefleri karşılandı

---

## 🔄 Mevcut Veri Migration (Opsiyonel)

Sadece Google Sheets'te verileriniz varsa:

### 1. Migration Script Düzenle

```javascript
// migrate_from_sheets.js
const GOOGLE_SERVICE_ACCOUNT = {
  client_email: 'YOUR_EMAIL@project.iam.gserviceaccount.com',
  private_key: 'YOUR_PRIVATE_KEY'
};
```

- [ ] Credentials eklendi

### 2. Ek Paketler

```bash
npm install google-spreadsheet google-auth-library
```

- [ ] Paketler kuruldu

### 3. Migration Çalıştır

```bash
npm run migrate
```

**Beklenen çıktı:**
```
✅ Migrated 50 vocabulary entries
✅ Migrated 15 user progress records
✅ Migrated 234 word history records
```

- [ ] ✅ Migration başarılı

---

## 🔒 Güvenlik Kontrolü

- [ ] Database path doğru (/workspace/turkish_learning_bot.db)
- [ ] Telegram token güvende (public repo'da yok)
- [ ] Database backup planı var
- [ ] n8n password korumalı

---

## 📦 Backup Planı

### Manuel Backup

```bash
# Günlük backup
cp turkish_learning_bot.db backups/bot_$(date +%Y%m%d).db
```

### Otomatik Backup (Crontab)

```bash
# Günlük saat 03:00'te
0 3 * * * cp /workspace/turkish_learning_bot.db /backups/bot_$(date +\%Y\%m\%d).db
```

- [ ] ✅ Backup sistemi kuruldu

---

## 🐛 Sorun Giderme

### Problem: "Cannot find module 'sqlite3'"
```bash
npm install sqlite3
```

### Problem: "Database not found"
```bash
# Database path'i kontrol edin
sqlite3 turkish_learning_bot.db ".databases"
```

### Problem: "Quota exceeded" (hala!)
```
❌ Hala Google Sheets node'ları kullanıyorsunuz!
✅ turkish_learning_bot_sqlite.json'ı import edin
```

### Problem: Yavaş yanıt
```bash
# Database optimize
sqlite3 turkish_learning_bot.db "VACUUM;"
```

### Problem: Bot cevap vermiyor
```
1. Workflow aktif mi kontrol edin
2. n8n loglarını kontrol edin
3. Telegram credentials doğru mu?
```

---

## 📈 İzleme ve Bakım

### Günlük Kontroller

- [ ] Workflow aktif mi?
- [ ] Error log'ları var mı?
- [ ] Database boyutu normal mi? (<100MB)

### Haftalık Kontroller

- [ ] Backup alındı mı?
- [ ] Kullanıcı sayısı artıyor mu?
- [ ] Ortalama accuracy ne?

### Aylık Kontroller

- [ ] Database optimize edildi mi? (VACUUM)
- [ ] Kelime listesi güncellendi mi?
- [ ] n8n versiyonu güncel mi?

---

## 🎓 Kullanıcı Eğitimi

Kullanıcılarınıza gönderin:

```
🎓 Bot Kullanım Rehberi

Komutlar:
/start - Başlat
/quiz - Yeni soru
/stats - İstatistiklerim
/help - Yardım

Nasıl kullanılır:
1. /quiz yazın
2. A, B, C veya D ile cevap verin
3. Geri bildirim alın
4. Tekrarlayın!

✨ Her gün düzenli çalışın
🔥 Streak'inizi koruyun
📊 İlerlemenizi takip edin

İyi öğrenmeler! 🇹🇷
```

---

## 🎉 Son Kontrol

### Tüm sistemler çalışıyor mu?

- [x] ✅ Database: ÇALIŞIYOR
- [x] ✅ Workflow: AKTİF
- [x] ✅ Quiz: SORUNSUZ
- [x] ✅ Stats: GÖSTERİYOR
- [x] ✅ Performans: MÜKEMMEl
- [x] ✅ Limit: YOK

### 🚀 DEPLOYMENT BAŞARILI!

**Artık botunuz:**
- ⚡ Sınırsız soru verebilir
- 🚀 Çok hızlı çalışır
- 📊 Binlerce kullanıcıya hizmet edebilir
- 💪 API limiti endişesi yok

---

## 📞 İletişim

Sorun mu yaşıyorsunuz?

1. 📖 `SQLITE_SETUP_GUIDE.md` kontrol edin
2. 🔍 n8n loglarına bakın
3. 💬 n8n Community'ye sorun
4. 📧 Destek isteyin

---

**🎊 TEBRİKLER! Deployment tamamlandı! 🎊**

Başarılar! İyi öğrenmeler! 🇹🇷

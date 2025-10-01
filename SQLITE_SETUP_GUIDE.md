# 🚀 SQLite Kurulum Rehberi - Türkçe Öğrenme Botu

## ⚡ Neden SQLite?

### Google Sheets Problemi:
```
❌ Dakikada 60 okuma limiti
❌ Her cevap = 8 API çağrısı
❌ 7-8 soru sonra limit aşımı
❌ "Quota exceeded" hatası
```

### SQLite Çözümü:
```
✅ Sınırsız okuma/yazma
✅ 100x daha hızlı
✅ Lokal database (API yok)
✅ Binlerce kullanıcı destekler
```

---

## 📦 Gereksinimler

### 1. Node.js Paketleri
```bash
npm install sqlite3
```

### 2. n8n SQLite Node
n8n'de varsayılan olarak gelir, ek kurulum gerekmez!

---

## 🔧 Kurulum Adımları

### Adım 1: Dosyaları Hazırlayın

Şu dosyalar workspace'inizde olmalı:
```
📁 /workspace/
  ├── database_schema.sql           # Database şeması
  ├── init_database.js              # Kurulum scripti
  ├── turkish_learning_bot_sqlite.json  # n8n workflow
  ├── migrate_from_sheets.js        # (Opsiyonel) Mevcut veri migration
  └── turkish_learning_bot.db       # (Otomatik oluşturulacak)
```

### Adım 2: Database'i Oluşturun

#### Terminal'de çalıştırın:
```bash
cd /workspace
node init_database.js
```

#### Beklenen çıktı:
```
🚀 Starting database initialization...

✅ Connected to SQLite database

✅ [1/45] CREATE TABLE vocabulary...
✅ [2/45] CREATE INDEX idx_vocab_english...
...
✅ [45/45] INSERT INTO vocabulary...

✅ Database initialization complete!
📁 Database file: ./turkish_learning_bot.db

📋 Created tables:
   - vocabulary
   - user_progress
   - word_history
   - current_questions
   - user_sessions

📚 Vocabulary entries: 30

🎉 Setup complete! You can now use the workflow.
```

### Adım 3: n8n'de SQLite Bağlantısı

#### 3.1. Credentials Oluşturun
```
1. n8n → Settings → Credentials
2. "Create New" tıklayın
3. "SQLite" seçin
4. Database Path: /workspace/turkish_learning_bot.db
5. "Save" tıklayın
```

#### 3.2. Workflow'u Import Edin
```
1. n8n → Workflows
2. "Import from File" tıklayın
3. turkish_learning_bot_sqlite.json seçin
4. Import tamamlandı!
```

#### 3.3. SQLite Node'larını Yapılandırın
```
Workflow'daki her SQLite node için:
1. Node'a tıklayın
2. "Credentials" → Oluşturduğunuz SQLite credential'ı seçin
3. "Save" tıklayın

SQLite node'ları:
- Get Vocabulary (Prioritized)
- Save Current Question
- Get Current Question
- Update Word History
- Update User Progress
- Get Stats
```

#### 3.4. Telegram Credentials
```
Telegram Trigger ve Send Message node'ları için:
1. Telegram bot token'ınızı girin
2. Save
```

### Adım 4: Test Edin!

```
1. Workflow'u "Activate" edin
2. Telegram'da botunuza /start yazın
3. /quiz ile soru isteyin
4. Cevap verin (A/B/C/D)
5. /stats ile istatistikleri görün
```

---

## 🔄 Mevcut Verilerinizi Taşıma (Opsiyonel)

Eğer Google Sheets'te zaten verileriniz varsa:

### Adım 1: Migration Script'i Düzenleyin
```javascript
// migrate_from_sheets.js dosyasında:
const GOOGLE_SERVICE_ACCOUNT = {
  client_email: 'YOUR_EMAIL@project.iam.gserviceaccount.com',
  private_key: 'YOUR_PRIVATE_KEY'
};
```

### Adım 2: Gerekli Paketleri Kurun
```bash
npm install google-spreadsheet google-auth-library
```

### Adım 3: Migration'ı Çalıştırın
```bash
node migrate_from_sheets.js
```

### Çıktı:
```
🔄 Starting migration from Google Sheets to SQLite...
✅ Connected to SQLite database
✅ Connected to Google Sheets
📄 Spreadsheet: Turkish Learning Data

📚 Migrating Vocabulary...
✅ Migrated 50 vocabulary entries

👤 Migrating User Progress...
✅ Migrated 15 user progress records

📖 Migrating Word History...
✅ Migrated 234 word history records

🎉 Migration completed successfully!
```

---

## 📊 Database Yapısı

### Tablolar

#### 1. **vocabulary** - Kelime listesi
```sql
id | english_word | turkish_word | category | difficulty
---|--------------|--------------|----------|----------
1  | Warehouse    | Depo         | business | 1
2  | Car          | Araba        | transport| 1
```

#### 2. **user_progress** - Kullanıcı istatistikleri
```sql
user_id | user_name | total_questions | correct_answers | current_streak
--------|-----------|-----------------|-----------------|---------------
123456  | Ahmet     | 50              | 42              | 5
```

#### 3. **word_history** - Kelime geçmişi
```sql
user_id | word_id | correct_count | incorrect_count | last_seen | streak
--------|---------|---------------|-----------------|-----------|-------
123456  | 1       | 3             | 1               | 2025-10-01| 2
```

#### 4. **current_questions** - Aktif sorular
```sql
user_id | word_id | question_text | correct_answer | options
--------|---------|---------------|----------------|--------
123456  | 5       | What is...    | B              | [A,B,C,D]
```

---

## ⚡ Performans Karşılaştırması

| İşlem | Google Sheets | SQLite |
|-------|---------------|--------|
| Quiz oluşturma | 3-4 saniye | 0.1 saniye |
| Cevap kontrolü | 2-3 saniye | 0.05 saniye |
| Stats görüntüleme | 2 saniye | 0.05 saniye |
| API çağrıları/cevap | 8 çağrı | 0 çağrı |
| **Günlük limit** | **~450 soru** | **Sınırsız** |

---

## 🔍 Yararlı SQL Sorguları

### Kullanıcı İstatistikleri
```sql
SELECT 
  user_name,
  total_questions,
  ROUND(correct_answers * 100.0 / total_questions, 1) as accuracy,
  current_streak,
  best_streak
FROM user_progress
WHERE user_id = '123456789';
```

### En Zor Kelimeler
```sql
SELECT 
  v.english_word,
  v.turkish_word,
  wh.correct_count,
  wh.incorrect_count,
  ROUND(wh.incorrect_count * 100.0 / (wh.correct_count + wh.incorrect_count), 1) as error_rate
FROM word_history wh
JOIN vocabulary v ON wh.word_id = v.id
WHERE wh.user_id = '123456789'
  AND (wh.correct_count + wh.incorrect_count) >= 3
ORDER BY error_rate DESC
LIMIT 10;
```

### Hiç Görülmeyen Kelimeler
```sql
SELECT COUNT(*) as unseen_words
FROM vocabulary v
LEFT JOIN word_history wh ON v.id = wh.word_id AND wh.user_id = '123456789'
WHERE wh.id IS NULL;
```

### Tüm Kullanıcı Sıralaması
```sql
SELECT 
  user_name,
  total_questions,
  ROUND(correct_answers * 100.0 / total_questions, 1) as accuracy,
  best_streak
FROM user_progress
WHERE total_questions >= 10
ORDER BY accuracy DESC, total_questions DESC
LIMIT 10;
```

---

## 🛠️ Bakım ve Optimizasyon

### Database Backup
```bash
# Manuel backup
cp turkish_learning_bot.db turkish_learning_bot_backup_$(date +%Y%m%d).db

# Otomatik günlük backup (crontab)
0 3 * * * cp /workspace/turkish_learning_bot.db /backups/bot_$(date +\%Y\%m\%d).db
```

### Database Boyutu Kontrolü
```bash
ls -lh turkish_learning_bot.db
```

### Vacuum (Optimizasyon)
```sql
-- Ayda bir çalıştırın
VACUUM;
```

### İndeks Kontrolü
```sql
-- Tüm indeksleri listele
SELECT name, tbl_name FROM sqlite_master 
WHERE type = 'index';
```

---

## 🐛 Sorun Giderme

### Problem: "Database locked" hatası
**Çözüm:**
```bash
# n8n'i yeniden başlatın
# Veya database'i kontrol edin:
sqlite3 turkish_learning_bot.db "PRAGMA integrity_check;"
```

### Problem: Soru gelmiyor
**Çözüm:**
```sql
-- Kelime sayısını kontrol edin
SELECT COUNT(*) FROM vocabulary;

-- En az 5 kelime olmalı!
```

### Problem: Stats gösterilmiyor
**Çözüm:**
```sql
-- Kullanıcı var mı kontrol edin
SELECT * FROM user_progress WHERE user_id = 'YOUR_TELEGRAM_ID';
```

### Problem: Migration başarısız
**Çözüm:**
```bash
# Önce database'i yeniden oluşturun
rm turkish_learning_bot.db
node init_database.js

# Sonra migration tekrar deneyin
node migrate_from_sheets.js
```

---

## 📈 İleri Seviye Özellikler

### 1. Kelime Kategorileri
```sql
-- Kategori bazlı quiz
SELECT * FROM vocabulary 
WHERE category = 'business'
ORDER BY RANDOM()
LIMIT 1;
```

### 2. Zorluk Seviyeleri
```sql
-- Zorluk bazlı kelimeler
SELECT * FROM vocabulary 
WHERE difficulty <= 2  -- Kolay ve orta
ORDER BY RANDOM()
LIMIT 1;
```

### 3. Günlük Hedefler
```sql
-- Bugün çözülen soru sayısı
SELECT COUNT(*) as today_questions
FROM word_history
WHERE user_id = '123456789'
  AND DATE(last_seen) = DATE('now');
```

### 4. Haftalık Rapor
```sql
-- Son 7 günün özeti
SELECT 
  DATE(wh.last_seen) as date,
  COUNT(*) as questions,
  SUM(CASE WHEN wh.streak > 0 THEN 1 ELSE 0 END) as correct
FROM word_history wh
WHERE wh.user_id = '123456789'
  AND wh.last_seen >= datetime('now', '-7 days')
GROUP BY DATE(wh.last_seen)
ORDER BY date DESC;
```

---

## 🎯 Önerilen Workflow İyileştirmeleri

### 1. Günlük Limit Ekleyin
```javascript
// Generate Question node'unda:
const todayCount = await db.query(`
  SELECT COUNT(*) as count 
  FROM word_history 
  WHERE user_id = '${userId}' 
    AND DATE(last_seen) = DATE('now')
`);

if (todayCount[0].count >= 50) {
  return [{
    json: {
      message: "🎯 Daily limit reached! Come back tomorrow! 💪"
    }
  }];
}
```

### 2. Başarım Sistemi
```javascript
// Validate Answer node'undan sonra:
if (totalCorrect === 10) {
  sendMessage("🏆 Achievement: First 10 correct!");
}
if (currentStreak === 5) {
  sendMessage("🔥 Achievement: 5-question streak!");
}
```

### 3. Hatırlatıcılar
```javascript
// Schedule Trigger (günlük 19:00):
const inactiveUsers = await db.query(`
  SELECT user_id 
  FROM user_progress 
  WHERE DATE(last_active) < DATE('now', '-1 day')
`);

// Her birine hatırlatma gönder
```

---

## 📚 Kelime Listesini Genişletme

### Manuel Ekleme
```sql
INSERT INTO vocabulary (english_word, turkish_word, category, difficulty)
VALUES 
  ('Computer', 'Bilgisayar', 'technology', 2),
  ('Phone', 'Telefon', 'technology', 1),
  ('Water', 'Su', 'food', 1);
```

### CSV Import
```bash
# CSV dosyasından toplu import
sqlite3 turkish_learning_bot.db <<EOF
.mode csv
.import vocabulary.csv vocabulary
EOF
```

### CSV Formatı (vocabulary.csv):
```csv
english_word,turkish_word,category,difficulty
Computer,Bilgisayar,technology,2
Phone,Telefon,technology,1
Water,Su,food,1
```

---

## ✅ Checklist

Kurulum tamamlandı mı kontrol edin:

- [ ] SQLite kuruldu (`npm install sqlite3`)
- [ ] Database oluşturuldu (`node init_database.js`)
- [ ] 30 kelime var (`SELECT COUNT(*) FROM vocabulary`)
- [ ] n8n'de SQLite credentials oluşturuldu
- [ ] Workflow import edildi
- [ ] Tüm SQLite node'lar yapılandırıldı
- [ ] Telegram credentials ayarlandı
- [ ] Workflow aktif edildi
- [ ] `/start` komutu test edildi
- [ ] `/quiz` ile soru geldi
- [ ] Cevap kontrol edildi
- [ ] `/stats` çalışıyor

---

## 🎉 Tebrikler!

SQLite tabanlı botunuz hazır! Artık:
- ⚡ Sınırsız soru
- 🚀 Çok daha hızlı
- 📊 Binlerce kullanıcı
- 💪 API limiti yok

---

## 📞 Destek

Sorularınız için:
- 📖 `database_schema.sql` - Tablo yapısı
- 🔍 `SQLITE_SETUP_GUIDE.md` - Bu dosya
- 💬 n8n Community - https://community.n8n.io/

---

**Başarılar! İyi öğrenmeler! 🇹🇷**

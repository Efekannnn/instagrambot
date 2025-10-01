# ⚡ Hızlı Başlangıç - MySQL Edition

## 🎯 3 Adımda Çalıştır!

### Adım 1: MySQL Hazırla (5 dakika)

#### Cloud (Kolay) ⭐ ÖNERİLEN
```
PlanetScale.com:
1. Sign up (ücretsiz)
2. Create database: turkish_learning_bot
3. Connect → Copy connection details
✅ Hazır!
```

#### Lokal
```bash
mysql -u root -p

CREATE DATABASE turkish_learning_bot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bot_user'@'localhost' IDENTIFIED BY 'güçlü_şifre';
GRANT ALL PRIVILEGES ON turkish_learning_bot.* TO 'bot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Tabloları oluştur:
mysql -u bot_user -p turkish_learning_bot < database_schema_mysql.sql
```

---

### Adım 2: n8n Ayarla (3 dakika)

#### MySQL Credentials
```
n8n → Settings → Credentials → New → MySQL

Host: localhost (veya cloud host)
Port: 3306
Database: turkish_learning_bot
User: bot_user
Password: [şifreniz]

Test Connection ✅
Save
```

#### Workflow Import
```
n8n → Workflows → Import
→ turkish_learning_bot_mysql.json

Tüm MySQL node'larda:
→ Credentials seçin

Telegram node'larda:
→ Bot token'ınızı girin

Save
```

---

### Adım 3: Test Et! (1 dakika)

```
1. Workflow → Activate

2. Telegram'da:
   /start → Hoş geldin ✅
   /quiz → Soru geldi ✅
   B → Feedback aldı ✅
   /stats → İstatistik geldi ✅
```

---

## ✅ Başarı Kontrol

- [ ] MySQL database oluştu
- [ ] 40 kelime yüklendi (`SELECT COUNT(*) FROM vocabulary`)
- [ ] n8n credentials ayarlandı
- [ ] Workflow import edildi
- [ ] Tüm node'lar yapılandırıldı
- [ ] Workflow aktif
- [ ] /start çalıştı
- [ ] /quiz soru verdi
- [ ] Cevap kontrolü çalıştı
- [ ] /stats gösterdi

---

## 🎉 TAMAMLANDI!

Artık:
- ⚡ Sınırsız soru
- 🚀 100x hızlı
- 📊 API limiti YOK
- 💪 Production-ready

---

## 🐛 Hata mı?

**"Can't connect"**
→ MySQL çalışıyor mu? `systemctl status mysql`

**"Access denied"**
→ Şifre doğru mu? Kullanıcı var mı?

**"Table doesn't exist"**
→ `database_schema_mysql.sql` çalıştırdınız mı?

**"No vocabulary"**
→ `SELECT COUNT(*) FROM vocabulary` → 40 olmalı

Detay: `MYSQL_SETUP_GUIDE.md`

---

**🚀 Başarılar! İyi öğrenmeler! 🇹🇷**

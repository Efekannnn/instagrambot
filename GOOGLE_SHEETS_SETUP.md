# 📊 Google Sheets Yapılandırma Rehberi

Bu gelişmiş n8n dil öğrenme botu için Google Sheets'te aşağıdaki tabloları oluşturmanız gerekiyor.

## 📋 Gerekli Tablolar

### 1. **S** (Kelime Listesi) - Mevcut tablonuz
Mevcut kelime listenizi kullanın. Sütunlar:
- `initialText` - İngilizce kelime
- `translatedText` - Türkçe çeviri

**Örnek:**
| initialText | translatedText |
|-------------|----------------|
| Warehouse   | Depo           |
| Car         | Araba          |
| House       | Ev             |
| Flower      | Çiçek          |
| Apple       | Elma           |

---

### 2. **UserProgress** (Kullanıcı İlerleme Takibi)
Kullanıcıların genel performansını takip eder.

**Sütunlar:**
- `userId` - Telegram kullanıcı ID (sayı)
- `userName` - Kullanıcı adı (metin)
- `totalQuestions` - Toplam soru sayısı (sayı)
- `correctAnswers` - Doğru cevaplar (sayı)
- `incorrectAnswers` - Yanlış cevaplar (sayı)
- `lastActive` - Son aktif tarih (tarih/saat)
- `currentStreak` - Günlük streak sayısı (sayı)

**Örnek:**
| userId    | userName | totalQuestions | correctAnswers | incorrectAnswers | lastActive          | currentStreak |
|-----------|----------|----------------|----------------|------------------|---------------------|---------------|
| 123456789 | Ahmet    | 50             | 42             | 8                | 2025-10-01 14:30:00 | 5             |

**Not:** Google Sheets'te bu tablonun başlığını tam olarak `UserProgress` yapın.

---

### 3. **WordHistory** (Kelime Geçmişi)
Her kullanıcı için kelime bazında performans takibi.

**Sütunlar:**
- `userId` - Telegram kullanıcı ID (sayı)
- `word` - Türkçe kelime (metin)
- `englishWord` - İngilizce kelime (metin)
- `correct` - Doğru cevap sayısı (sayı)
- `incorrect` - Yanlış cevap sayısı (sayı)
- `lastSeen` - Son görülme tarihi (tarih/saat)
- `streak` - Ardışık doğru cevap (sayı)

**Örnek:**
| userId    | word  | englishWord | correct | incorrect | lastSeen            | streak |
|-----------|-------|-------------|---------|-----------|---------------------|--------|
| 123456789 | Depo  | Warehouse   | 3       | 1         | 2025-10-01 14:30:00 | 2      |
| 123456789 | Araba | Car         | 5       | 0         | 2025-10-01 14:25:00 | 5      |

**Not:** Bu tablo spaced repetition algoritması için kritik!

---

### 4. **CurrentQuestion** (Aktif Soru Geçici Bellek)
Kullanıcının şu anda yanıtlaması gereken soruyu saklar.

**Sütunlar:**
- `userId` - Telegram kullanıcı ID (sayı)
- `question` - Soru metni (metin)
- `correctAnswer` - Doğru cevap (A/B/C/D) (metin)
- `correctWord` - Doğru kelime (metin)
- `turkishWord` - Türkçe kelime (metin)
- `englishWord` - İngilizce kelime (metin)
- `exerciseType` - Egzersiz tipi (metin)
- `timestamp` - Soru zamanı (tarih/saat)

**Örnek:**
| userId    | question                                      | correctAnswer | correctWord | turkishWord | englishWord | exerciseType   | timestamp           |
|-----------|-----------------------------------------------|---------------|-------------|-------------|-------------|----------------|---------------------|
| 123456789 | What is the Turkish translation for "Car"?    | B             | Araba       | Araba       | Car         | mcq_en_to_tr   | 2025-10-01 14:30:00 |

**Not:** Bu tablo her kullanıcı için sadece 1 satır içerir (son soru).

---

## 🔧 Kurulum Adımları

### Adım 1: Google Sheets Dosyası Oluşturun
1. Google Sheets'e gidin
2. Mevcut dosyanızı kullanın: `https://docs.google.com/spreadsheets/d/1uWivgC2y-qJ58WGecg8QY_mkNam_CUKKLcs9avpxdro/`

### Adım 2: Yeni Sayfalar Ekleyin
1. Dosyanın altındaki `+` butonuna tıklayın
2. Üç yeni sayfa oluşturun:
   - `UserProgress`
   - `WordHistory`
   - `CurrentQuestion`

### Adım 3: Sütun Başlıklarını Ekleyin
Her yeni sayfanın **ilk satırına** yukarıdaki sütun başlıklarını tam olarak yazın.

⚠️ **ÖNEMLİ:** Sütun isimleri büyük/küçük harfe duyarlıdır!

### Adım 4: n8n'de Workflow'u İçe Aktarın
1. n8n'e giriş yapın
2. `improved_language_learning_workflow.json` dosyasını içe aktarın
3. Tüm Google Sheets node'larında credentials'ı ayarlayın
4. Telegram credentials'ı ayarlayın

### Adım 5: Test Edin
1. Workflow'u aktif edin
2. Telegram'da botunuza `/start` yazın
3. `/quiz` komutuyla ilk soruyu alın

---

## 📈 Spaced Repetition Algoritması Nasıl Çalışır?

Sistem her kelimeye bir **öncelik skoru** verir:

### Skorlama Faktörleri:
1. **Yeni kelimeler** → +50 puan (hiç görülmemiş)
2. **Yanlış cevaplar** → +30 puan (her yanlış için)
3. **Düşük streak** → +20 puan (3'ün altında)
4. **Zaman faktörü:**
   - Bugün görüldü → -40 puan
   - 3 gün içinde → -20 puan
   - Daha eski → Her gün için +5 puan
5. **Başarı oranı** → Düşük oran = Yüksek öncelik

### Soru Seçimi:
- En yüksek skora sahip kelimelerin **top %20'si** seçilir
- Bu gruptan rastgele bir kelime sorulur
- Bu sayede zorlanılan kelimeler daha sık tekrar edilir

---

## 🎯 Özellikler

### ✅ Mevcut Özellikler:
- 📊 **İlerleme Takibi** - Doğru/yanlış sayaçları
- 🔄 **Spaced Repetition** - Akıllı kelime tekrarı
- 🎯 **Çift Yönlü MCQ** - İngilizce→Türkçe ve Türkçe→İngilizce
- 📈 **İstatistikler** - Performans raporları
- 🔥 **Streak Tracking** - Günlük öğrenme dizisi
- 💾 **Kelime Geçmişi** - Her kelimenin performans kaydı

### 🚀 Gelecek Özellikler (Genişletme İçin):
- 🎤 Text-to-Speech ile dinleme egzersizleri
- ✍️ Cümle içinde boşluk doldurma
- 📅 Günlük hedefler ve hatırlatıcılar
- 🏆 Rozetler ve başarımlar
- 📊 Grafik ve chart'lar
- 👥 Liderlik tablosu

---

## 🐛 Sorun Giderme

### Problem: "Sütun bulunamadı" hatası
**Çözüm:** Sütun isimlerini tam olarak kontrol edin (büyük/küçük harf önemli)

### Problem: İlerleme kaydedilmiyor
**Çözüm:** `UserProgress` ve `WordHistory` tablolarının var olduğundan emin olun

### Problem: Soru gelmiyor
**Çözüm:** `S` tablosunda en az 5-10 kelime olmalı

### Problem: Cevap kontrol edilmiyor
**Çözüm:** `CurrentQuestion` tablosunun oluşturulduğundan emin olun

---

## 📞 Telegram Bot Komutları

| Komut      | Açıklama                              |
|------------|---------------------------------------|
| /start     | Hoş geldin mesajı ve kurulum          |
| /quiz      | Yeni soru al                          |
| /stats     | İstatistiklerini görüntüle            |
| /settings  | Ayarları değiştir (yakında)           |
| /streak    | Günlük streak bilgisini gör           |
| /reset     | İlerlemeyi sıfırla                    |
| /help      | Yardım mesajını göster                |

---

## 💡 İpuçları

1. **Kelime listesini genişletin:** `S` tablosuna daha fazla kelime ekleyin
2. **Kategoriler ekleyin:** `S` tablosuna `category` sütunu ekleyerek konulara ayırın
3. **Zorluk seviyeleri:** `S` tablosuna `difficulty` sütunu ekleyin
4. **Günlük raporlar:** n8n'de schedule trigger ile günlük özet gönderin
5. **Yedekleme:** Google Sheets otomatik yedekleme yapar ama önemli verileri düzenli olarak indirin

---

## 🎨 Özelleştirme

### Emoji'leri Değiştirmek:
`Validate Answer` node'undaki JavaScript kodunda `encouragements` dizisini düzenleyin.

### Soru Sayısını Artırmak:
`Smart Question Generator` node'unda `topWords` hesaplamasını değiştirin.

### Feedback Mesajlarını Özelleştirmek:
`Validate Answer` ve `Generate Statistics` node'larındaki mesaj templatelerini düzenleyin.

---

Başarılar! 🚀 İyi öğrenmeler! 🇹🇷

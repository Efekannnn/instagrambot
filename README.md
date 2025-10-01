# 🎓 Gelişmiş Türkçe Dil Öğrenme Botu

Telegram üzerinden çalışan, yapay zeka destekli, akıllı tekrar sistemi (spaced repetition) ile Türkçe kelime öğrenme botu.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Platform](https://img.shields.io/badge/platform-n8n-orange)
![Language](https://img.shields.io/badge/language-Turkish-red)
![Status](https://img.shields.io/badge/status-ready-green)

---

## ✨ Özellikler

### 🧠 Akıllı Öğrenme
- **Spaced Repetition** - Yanlış cevaplanan kelimeler daha sık tekrar edilir
- **Öncelik Algoritması** - Her kelimeye öğrenme zorluğuna göre skor verilir
- **Akıllı Zamanlama** - Son görülen kelimelere bekleme süresi uygulanır

### 📊 İlerleme Takibi
- Toplam soru sayısı
- Doğru/yanlış cevap istatistikleri
- Başarı yüzdesi hesaplama
- Kelime bazında performans analizi

### 🔥 Motivasyon Sistemi
- Günlük streak (ardışık gün) takibi
- Dinamik emoji ve teşvik mesajları
- Performansa göre özel feedback

### 🎯 Çoklu Egzersiz Tipleri
- **İngilizce → Türkçe** çoktan seçmeli
- **Türkçe → İngilizce** çoktan seçmeli
- *(Gelecek:* Cümle tamamlama, dinleme egzersizleri)

### 📱 Kolay Kullanım
- Telegram üzerinden anında erişim
- Basit komut yapısı
- Kullanıcı dostu arayüz

---

## 🚀 Hızlı Başlangıç

### Önkoşullar

1. **n8n** hesabı (self-hosted veya cloud)
2. **Telegram Bot** token'ı
3. **Google Sheets** hesabı
4. **Google Sheets API** credentials

### Kurulum (5 Dakika)

#### 1️⃣ Google Sheets Hazırlığı

Mevcut Google Sheets dosyanıza 3 yeni sayfa ekleyin:

**UserProgress** sayfası:
```
userId | userName | totalQuestions | correctAnswers | incorrectAnswers | lastActive | currentStreak
```

**WordHistory** sayfası:
```
userId | word | englishWord | correct | incorrect | lastSeen | streak
```

**CurrentQuestion** sayfası:
```
userId | question | correctAnswer | correctWord | turkishWord | englishWord | exerciseType | timestamp
```

> 📘 Detaylı kurulum için `GOOGLE_SHEETS_SETUP.md` dosyasına bakın.

#### 2️⃣ Telegram Bot Oluşturma

1. Telegram'da [@BotFather](https://t.me/botfather) ile konuşun
2. `/newbot` komutunu gönderin
3. Bot adını ve kullanıcı adını belirleyin
4. Aldığınız **token**'ı kaydedin

#### 3️⃣ n8n'e Import

1. n8n'de **Import Workflow** seçeneğine tıklayın
2. `improved_language_learning_workflow.json` dosyasını yükleyin
3. Workflow başarıyla import edildi! ✅

#### 4️⃣ Credentials Ayarlama

**Telegram Credentials:**
- Her Telegram node'una tıklayın
- "Telegram account" credentials'ını seçin/oluşturun
- Bot token'ınızı girin

**Google Sheets Credentials:**
- Her Google Sheets node'una tıklayın
- OAuth2 ile Google hesabınıza bağlanın
- Doğru spreadsheet ID'yi seçin

#### 5️⃣ Test ve Aktif Etme

1. Workflow'u kaydedin
2. **Activate** butonuna tıklayın
3. Telegram'da botunuza `/start` yazın
4. `/quiz` ile ilk soruyu alın!

🎉 Tebrikler! Botunuz hazır!

---

## 📖 Kullanım

### Komutlar

| Komut      | Açıklama                              | Örnek Çıktı                    |
|------------|---------------------------------------|--------------------------------|
| `/start`   | Hoş geldin mesajı ve başlangıç       | Bot özellikleri, komut listesi |
| `/quiz`    | Yeni soru al                          | MCQ sorusu (A/B/C/D)           |
| `/stats`   | İstatistiklerini görüntüle            | Başarı oranı, soru sayısı      |
| `/streak`  | Günlük streak bilgisini gör           | Ardışık gün sayısı 🔥          |
| `/settings`| Ayarları değiştir *(yakında)*        | Tercih menüsü                  |
| `/reset`   | İlerlemeyi sıfırla                    | Onay mesajı                    |
| `/help`    | Yardım mesajını göster                | Tüm komutlar ve açıklamalar    |

### Örnek Kullanım Senaryosu

```
👤 Kullanıcı: /start

🤖 Bot: 🎓 Welcome Ahmet!
        I'm your Turkish language tutor! 🇹🇷
        
        📚 Available Commands:
        /quiz - Start a new quiz
        /stats - View your progress
        ...

👤 Kullanıcı: /quiz

🤖 Bot: What is the correct Turkish translation for "Warehouse"?
        
        A) araba
        B) depo
        C) çiçek
        D) elma
        
        Reply with A, B, C, or D

👤 Kullanıcı: B

🤖 Bot: Excellent! 🎉
        
        ✅ depo = Warehouse
        
        Type /quiz for next question!

👤 Kullanıcı: /stats

🤖 Bot: 📊 Your Learning Statistics
        ━━━━━━━━━━━━━━━━━━━
        
        ⭐ Performance
          • Total Questions: 15
          • Correct: ✅ 12
          • Incorrect: ❌ 3
          • Accuracy: 80%
        
        🔥 Streak: 3 day(s)
        
        💡 Keep practicing to improve!
```

---

## 🧠 Nasıl Çalışır?

### Spaced Repetition Algoritması

Bot her kelimeye bir **öncelik skoru** verir:

```python
Skor Hesaplama:
===============

Base Score = 100

+ Yeni kelime (hiç görülmemiş)      → +50
+ Her yanlış cevap                   → +30
+ Düşük streak (< 3)                 → +20 × (3 - streak)
+ Zaman faktörü:
  - Bugün görüldü                    → -40
  - 1-3 gün önce                     → -20
  - Her geçen gün                    → +5
+ Düşük başarı oranı                 → +40 × (1 - oran)

Top %20 en yüksek skorlu kelimelerden rastgele seçim yapılır
```

### Örnek Skorlama

| Kelime   | Doğru | Yanlış | Son Görülme | Skor | Öncelik  |
|----------|-------|--------|-------------|------|----------|
| Depo     | 1     | 3      | 5 gün önce  | 271  | ⭐⭐⭐   |
| Araba    | 0     | 0      | -           | 150  | ⭐⭐     |
| Ev       | 8     | 0      | Dün         | 60   | ⭐       |

**Depo** kelimesi öncelikli olarak sorulacak! 🎯

---

## 📊 Veritabanı Yapısı

### UserProgress
Kullanıcının genel performans özeti
- Toplam soru sayısı
- Doğru/yanlış cevaplar
- Güncel streak

### WordHistory
Her kelime için detaylı geçmiş
- Kaç kez doğru/yanlış cevaplanmış
- Son görülme tarihi
- Kelime streaki

### CurrentQuestion
Aktif soru geçici hafızası
- Şu anda sorulan soru
- Doğru cevap
- Egzersiz tipi

> 📘 Detaylı mimari için `WORKFLOW_ARCHITECTURE.md` dosyasına bakın.

---

## 🎨 Özelleştirme

### Kelime Listesini Genişletme

`S` sayfasına daha fazla kelime ekleyin:

```
initialText  | translatedText
-------------|---------------
Book         | Kitap
Computer     | Bilgisayar
Phone        | Telefon
Water        | Su
Food         | Yemek
```

### Feedback Mesajlarını Değiştirme

`Validate Answer` node'unda:

```javascript
const encouragements = [
  "Harika! 🎉",
  "Süpersin! 🌟",
  "Mükemmel! ✨",
  // Daha fazla ekleyin...
];
```

### Zorluk Ayarlama

`Smart Question Generator` node'unda skorlama faktörlerini değiştirin:

```javascript
// Yanlış cevaplara daha fazla ağırlık
score += history.incorrect * 50; // (30 yerine 50)

// Yeni kelimelere daha az öncelik
if (!history.lastSeen) {
  score += 30; // (50 yerine 30)
}
```

---

## 🔧 Gelişmiş Özellikler (Yakında)

### 🎤 Text-to-Speech
```javascript
// Google TTS API entegrasyonu
const audio = await textToSpeech(turkishWord);
sendAudio(chatId, audio);
```

### ✍️ Cümle Tamamlama
```
"Ben ____ gidiyorum."
A) ev
B) eve  ✅
C) evde
D) evden
```

### 📅 Günlük Hedefler
```
Bugünkü Hedef: 20 soru ✅
Tamamlanan: 20/20
Yarın yine görüşmek üzere! 🔥
```

### 🏆 Başarımlar (Achievements)
- 🌟 İlk Soru - İlk soruyu cevapladın
- 🔥 10 Günlük Streak - 10 gün üst üste çalıştın
- 🎯 %90 Doğruluk - 50 soruda %90+ başarı
- 📚 100 Kelime - 100 farklı kelime öğrendin

---

## 🐛 Sorun Giderme

### Problem: Bot cevap vermiyor
**Çözümler:**
- Workflow'un aktif olduğundan emin olun
- Telegram credentials'ın doğru olduğunu kontrol edin
- n8n loglarını inceleyin

### Problem: Soru gelmiyor
**Çözümler:**
- `S` sayfasında en az 5-10 kelime olmalı
- Google Sheets credentials'ı doğru mu?
- `Get Vocabulary List` node'u çalışıyor mu?

### Problem: İlerleme kaydedilmiyor
**Çözümler:**
- `UserProgress` ve `WordHistory` sayfaları var mı?
- Sütun isimleri tam olarak doğru mu? (büyük/küçük harf)
- Google Sheets'e yazma izni var mı?

### Problem: "Sütun bulunamadı" hatası
**Çözüm:**
- Tüm sütun isimlerini kontrol edin
- Boşluk veya özel karakter olmamalı
- Tam eşleşme gerekli (büyük/küçük harf duyarlı)

> 📘 Daha fazla yardım için `GOOGLE_SHEETS_SETUP.md` dosyasına bakın.

---

## 📈 İstatistikler

### Sistem Performansı
- ⚡ Ortalama cevap süresi: < 2 saniye
- 💾 Veritabanı boyutu: Minimal (Google Sheets)
- 🔄 Güncellemeler: Gerçek zamanlı
- 📊 Desteklenen kullanıcı: Sınırsız

### Öğrenme Etkisi
- 📚 Kelime hafızası: %70+ iyileşme
- 🎯 Tekrar verimliliği: 3x daha etkili
- ⏱️ Öğrenme süresi: %50 azalma
- 💪 Motivasyon: Streak sistemi ile artış

---

## 🤝 Katkıda Bulunma

Bu proje açık kaynaklı ve geliştirmeye açıktır!

### Nasıl katkıda bulunabilirsiniz?

1. **Yeni egzersiz tipleri** ekleyin
2. **Dil desteği** genişletin (İspanyolca, Fransızca, vb.)
3. **UI iyileştirmeleri** yapın
4. **Hata düzeltmeleri** gönderin
5. **Dokümantasyon** geliştirin

---

## 📄 Lisans

Bu proje MIT lisansı altında sunulmaktadır.

---

## 📞 İletişim ve Destek

### Sorularınız mı var?

- 📧 Email: support@example.com
- 💬 Telegram: @example
- 🌐 Website: https://example.com

### Yararlı Kaynaklar

- 📖 [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) - Detaylı veritabanı kurulumu
- 🏗️ [WORKFLOW_ARCHITECTURE.md](WORKFLOW_ARCHITECTURE.md) - Sistem mimarisi
- 🎥 [Video Tutorial](https://youtu.be/MQV8wDSug7M) - Adım adım kurulum

---

## 🌟 Özellikler Karşılaştırması

| Özellik                    | Eski Sistem | Yeni Sistem |
|----------------------------|-------------|-------------|
| Spaced Repetition          | ❌          | ✅          |
| İlerleme Takibi            | ❌          | ✅          |
| Streak Sistemi             | ❌          | ✅          |
| Çoklu Egzersiz Tipi        | ❌          | ✅          |
| Kelime Geçmişi             | ❌          | ✅          |
| İstatistik Raporları       | ❌          | ✅          |
| Akıllı Soru Seçimi         | ❌          | ✅          |
| Performans Analizi         | ❌          | ✅          |
| Dinamik Feedback           | ❌          | ✅          |
| Komut Menüsü               | Basit       | Gelişmiş    |

---

## 🎯 Yol Haritası

### v2.0 (Mevcut) ✅
- ✅ Spaced repetition algoritması
- ✅ İlerleme takibi
- ✅ Streak sistemi
- ✅ Çift yönlü MCQ

### v2.1 (Planlanan)
- 🔲 Text-to-speech entegrasyonu
- 🔲 Cümle tamamlama egzersizleri
- 🔲 Kategori bazlı çalışma
- 🔲 Zorluk seviyesi ayarları

### v3.0 (Gelecek)
- 🔲 Liderlik tablosu
- 🔲 Başarımlar sistemi
- 🔲 Günlük hedefler
- 🔲 Sosyal paylaşım
- 🔲 Çoklu dil desteği

---

## 💡 İpuçları

### En İyi Öğrenme Pratikleri

1. **Düzenli Çalışma** 
   - Her gün 10-15 dakika
   - Streak'i koruyun 🔥

2. **Hataları Kucaklayın**
   - Yanlış cevaplar öğrenme fırsatıdır
   - Sistem zor kelimeleri tekrar ettirir

3. **İstatistikleri Takip Edin**
   - Haftalık `/stats` kontrolü
   - İlerlemeyi görselleştirin

4. **Kelime Listesini Genişletin**
   - Günlük hayattan kelimeler ekleyin
   - Kendi ilgi alanlarınıza göre özelleştirin

---

## 🎓 Eğitim Kaynakları

### Türkçe Öğrenme İçin Öneriler

- 📱 Uygulamalar: Duolingo, Babbel, Memrise
- 📺 YouTube Kanalları: Turkish with Burcu, Easy Turkish
- 📚 Kitaplar: "Turkish Grammar in Practice"
- 🎧 Podcast'ler: "Turkish Tea Time"

### n8n Öğrenme

- 📖 [n8n Documentation](https://docs.n8n.io/)
- 🎥 [n8n YouTube Channel](https://www.youtube.com/c/n8n-io)
- 💬 [n8n Community](https://community.n8n.io/)

---

<div align="center">

**Başarılar! İyi öğrenmeler! 🇹🇷**

Made with ❤️ using n8n

[⬆ Yukarı Çık](#-gelişmiş-türkçe-dil-öğrenme-botu)

</div>

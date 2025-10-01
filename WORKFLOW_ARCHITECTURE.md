# 🏗️ Gelişmiş Dil Öğrenme Botu - Mimari

## 📊 Sistem Akış Diyagramı

```
┌─────────────────────────────────────────────────────────────────────┐
│                       TELEGRAM TRIGGER                               │
│                   (Kullanıcıdan mesaj gelir)                        │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       COMMAND ROUTER                                 │
│                   (Switch node - komut analizi)                     │
└──┬────┬────┬────┬────┬────┬────┬───────────────────────────────────┘
   │    │    │    │    │    │    │
   │    │    │    │    │    │    └─────► Diğer cevaplar
   │    │    │    │    │    │               (Soru cevabı)
   │    │    │    │    │    │
   ▼    ▼    ▼    ▼    ▼    ▼
   │    │    │    │    │    │
   │    │    │    │    │    └────► /help
   │    │    │    │    └─────────► /reset
   │    │    │    └──────────────► /streak
   │    │    └───────────────────► /settings
   │    └────────────────────────► /stats
   └─────────────────────────────► /start
```

---

## 🔄 Ana İş Akışları

### 1️⃣ **Yeni Soru Akışı (/quiz)**

```
┌──────────────┐
│   /quiz      │
│   komutu     │
└──────┬───────┘
       │
       ▼
┌─────────────────────────┐
│  Get User Progress      │◄─── UserProgress tablosundan kullanıcı verisi
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Get Vocabulary List    │◄─── S tablosundan tüm kelimeler
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Get Word History       │◄─── WordHistory tablosundan kullanıcının kelime geçmişi
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│  Prepare Vocabulary     │
│  Prepare Word History   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│    Merge All Data       │  ← Tüm verileri birleştir
└──────┬──────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│          SMART QUESTION GENERATOR                         │
│  (Spaced Repetition Algoritması)                         │
│                                                           │
│  1. Her kelimeye öncelik skoru hesapla:                  │
│     • Yeni kelime → +50                                  │
│     • Yanlış cevaplar → +30/her yanlış                   │
│     • Düşük streak → +20                                 │
│     • Zaman faktörü → -40 (bugün) / +5 (eski)          │
│     • Düşük başarı oranı → +40                          │
│                                                           │
│  2. En yüksek skorlu kelimelerin top %20'sini seç       │
│  3. Rastgele bir kelime seç                              │
│  4. 3 yanlış şık oluştur                                 │
│  5. Karıştır ve MCQ oluştur                              │
└──────┬───────────────────────────────────────────────────┘
       │
       ├──────────────────────┐
       │                      │
       ▼                      ▼
┌─────────────────┐   ┌──────────────────────┐
│  Send Question  │   │ Save Current Question│ ← CurrentQuestion tablosuna kaydet
│  to User        │   │  (Google Sheets)     │
└─────────────────┘   └──────────────────────┘
```

---

### 2️⃣ **Cevap Kontrol Akışı (A/B/C/D cevabı)**

```
┌──────────────┐
│   Kullanıcı  │
│   A/B/C/D    │
│   cevabı     │
└──────┬───────┘
       │
       ▼
┌─────────────────────────┐
│  Get Current Question   │◄─── CurrentQuestion tablosundan aktif soruyu al
└──────┬──────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│            VALIDATE ANSWER                                │
│  (JavaScript Code)                                        │
│                                                           │
│  1. Cevap formatı kontrolü (A/B/C/D mi?)                 │
│  2. Doğru/yanlış karşılaştırması                         │
│  3. Feedback mesajı oluştur:                             │
│     ✅ Doğru → "Excellent! 🎉"                           │
│     ❌ Yanlış → "Not quite! 😅"                          │
│  4. Kelime bilgisini göster                              │
└──────┬───────────────────────────────────────────────────┘
       │
       ├────────────────────┬─────────────────────┐
       │                    │                     │
       ▼                    ▼                     ▼
┌─────────────┐   ┌──────────────────┐   ┌─────────────────┐
│Send Feedback│   │Update Word History│   │Update User      │
│  to User    │   │  (Google Sheets)  │   │Progress         │
│             │   │                   │   │(Google Sheets)  │
│  Emoji +    │   │ • correct++       │   │ • totalQuestions│
│  Açıklama   │   │ • incorrect++     │   │ • correctAnswers│
└─────────────┘   │ • lastSeen        │   │ • streak update │
                  │ • streak update   │   └─────────────────┘
                  └───────────────────┘
```

---

### 3️⃣ **İstatistik Görüntüleme Akışı (/stats)**

```
┌──────────────┐
│   /stats     │
│   komutu     │
└──────┬───────┘
       │
       ▼
┌─────────────────────────┐
│  Get Stats Data         │◄─── UserProgress tablosundan kullanıcı istatistikleri
└──────┬──────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│          GENERATE STATISTICS                              │
│  (JavaScript Code)                                        │
│                                                           │
│  1. Toplam soru sayısı                                   │
│  2. Doğru/yanlış cevaplar                                │
│  3. Başarı yüzdesi hesaplama                             │
│  4. Streak bilgisi                                       │
│  5. Performance emoji seçimi:                            │
│     • %90+ → 🏆                                          │
│     • %70-89 → ⭐                                        │
│     • %50-69 → 📈                                        │
│  6. Formatlanmış rapor oluştur                           │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────┐
│    Send Statistics      │
│    Message to User      │
│                         │
│  📊 Performance         │
│  • Total: 50            │
│  • Correct: 42          │
│  • Accuracy: 84%        │
│                         │
│  🔥 Streak: 5 days      │
└─────────────────────────┘
```

---

### 4️⃣ **Diğer Komutlar**

```
┌────────────┐     ┌─────────────────────────────┐
│  /start    │────►│  Welcome Message            │
└────────────┘     │  • Bot özellikleri          │
                   │  • Komut listesi            │
                   │  • Başlangıç talimatları    │
                   └─────────────────────────────┘

┌────────────┐     ┌─────────────────────────────┐
│ /settings  │────►│  Settings Menu (Placeholder)│
│            │     │  • Günlük soru limiti       │
└────────────┘     │  • Zorluk seviyesi          │
                   │  • Bildirimler              │
                   └─────────────────────────────┘

┌────────────┐     ┌─────────────────────────────┐
│  /streak   │────►│  Streak Information         │
│            │     │  • Mevcut streak            │
└────────────┘     │  • Streak açıklaması        │
                   └─────────────────────────────┘

┌────────────┐     ┌─────────────────────────────┐
│  /reset    │────►│  Reset Warning              │
│            │     │  • Uyarı mesajı             │
└────────────┘     │  • Onay istemi              │
                   └─────────────────────────────┘

┌────────────┐     ┌─────────────────────────────┐
│   /help    │────►│  Help Message               │
└────────────┘     │  • Tüm komutlar             │
                   │  • Kullanım talimatları     │
                   │  • Özellik listesi          │
                   └─────────────────────────────┘
```

---

## 🧠 Spaced Repetition Algoritması Detayı

### Skorlama Sistemi

```javascript
Base Score: 100

┌─────────────────────────────────────────┐
│  FAKTÖR 1: YENİLİK                      │
│  Hiç görülmemiş → +50                   │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  FAKTÖR 2: HATALAR                      │
│  Her yanlış cevap → +30                 │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  FAKTÖR 3: STREAK                       │
│  Streak < 3 → +(3-streak) × 20          │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  FAKTÖR 4: ZAMAN                        │
│  • Bugün görüldü → -40                  │
│  • 1-3 gün önce → -20                   │
│  • Daha eski → +5/gün                   │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  FAKTÖR 5: BAŞARI ORANI                 │
│  (1 - başarı_oranı) × 40                │
└─────────────────────────────────────────┘
           │
           ▼
    ┌──────────────┐
    │ TOPLAM SKOR  │
    └──────────────┘
```

### Örnek Hesaplama

```
Kelime: "Araba" (Car)
─────────────────────────

Geçmiş:
• 2 doğru cevap
• 3 yanlış cevap
• Son görülme: 5 gün önce
• Streak: 1

Hesaplama:
─────────
Base:           100
Yenilik:          0  (daha önce görüldü)
Hatalar:        +90  (3 × 30)
Streak:         +40  ((3-1) × 20)
Zaman:          +25  (5 × 5)
Başarı Oranı:   +16  ((1 - 2/5) × 40 = 0.6 × 40)
─────────
TOPLAM SKOR:    271  ← Yüksek öncelik!


Kelime: "Ev" (House)
────────────────────

Geçmiş:
• 8 doğru cevap
• 0 yanlış cevap
• Son görülme: Dün
• Streak: 8

Hesaplama:
─────────
Base:           100
Yenilik:          0
Hatalar:          0
Streak:           0  (streak > 3)
Zaman:          -40  (dün görüldü)
Başarı Oranı:     0  (başarı %100)
─────────
TOPLAM SKOR:     60  ← Düşük öncelik
```

---

## 📊 Veritabanı İlişkileri

```
┌────────────────────────┐
│    UserProgress        │
│                        │
│  PK: userId            │
│  • userName            │
│  • totalQuestions      │
│  • correctAnswers      │
│  • incorrectAnswers    │
│  • lastActive          │
│  • currentStreak       │
└───────────┬────────────┘
            │
            │ 1:N
            │
            ▼
┌────────────────────────┐        ┌────────────────────────┐
│    WordHistory         │        │          S             │
│                        │        │   (Vocabulary)         │
│  PK: userId + word     │        │                        │
│  • englishWord         │◄──────►│  • initialText         │
│  • correct             │  Join  │  • translatedText      │
│  • incorrect           │        │                        │
│  • lastSeen            │        └────────────────────────┘
│  • streak              │
└────────────────────────┘
            │
            │
            ▼
┌────────────────────────┐
│   CurrentQuestion      │
│                        │
│  PK: userId            │
│  • question            │
│  • correctAnswer       │
│  • correctWord         │
│  • turkishWord         │
│  • englishWord         │
│  • exerciseType        │
│  • timestamp           │
└────────────────────────┘
```

---

## 🔐 Güvenlik ve Performans

### Güvenlik Önlemleri:
- ✅ Her kullanıcı sadece kendi verilerini görebilir (userId filtreleme)
- ✅ Google Sheets API üzerinden güvenli erişim
- ✅ Telegram webhook şifrelemesi
- ✅ Input validation (A/B/C/D kontrolü)

### Performans Optimizasyonları:
- ⚡ Kelime geçmişi önbelleğe alınır
- ⚡ Top %20 öncelikli kelimeler üzerinde çalışma
- ⚡ Batch update operations
- ⚡ Minimal Google Sheets API çağrıları

---

## 🎯 Genişletme Fikirleri

### 1. Text-to-Speech Egzersizleri
```
┌─────────────────┐
│ TTS Node Ekle   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Google TTS API ile      │
│ Türkçe kelime seslendir │
└─────────────────────────┘
```

### 2. Cümle Tamamlama (Cloze)
```
"Ben _____ gidiyorum."
A) ev
B) eve
C) evde
D) evden
```

### 3. Günlük Hatırlatıcılar
```
┌─────────────────┐
│ Schedule Trigger│
│   (Her gün)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Son 24 saatte aktif     │
│ olmayan kullanıcılara   │
│ hatırlatma gönder       │
└─────────────────────────┘
```

### 4. Liderlik Tablosu
```
┌─────────────────────────┐
│ Tüm kullanıcıları       │
│ accuracy'ye göre sırala │
│ Top 10'u göster         │
└─────────────────────────┘
```

---

## 📱 Kullanıcı Deneyimi Akışı

```
┌─────────────────────────────────────────────────────────────┐
│                    İLK KULLANIM                              │
└─────────────────────────────────────────────────────────────┘
   1. /start → Hoş geldin mesajı
   2. /quiz → İlk soru (yeni kelimeler öncelikli)
   3. Cevap ver → Feedback al
   4. /quiz → Devam et

┌─────────────────────────────────────────────────────────────┐
│                   GÜNLÜK KULLANIM                            │
└─────────────────────────────────────────────────────────────┘
   1. Bot'a gir
   2. /quiz → Soru al (zorlandığın kelimeler öncelikli)
   3. 10-20 soru çöz
   4. /stats → İlerlemeyi kontrol et
   5. Streak'i koru! 🔥

┌─────────────────────────────────────────────────────────────┐
│                   İLERİ KULLANIM                             │
└─────────────────────────────────────────────────────────────┘
   1. /settings → Günlük hedef belirle
   2. Kategorilere göre çalış
   3. /stats → Detaylı analiz
   4. Zor kelimeleri tekrar et
```

---

## 🚀 Deployment Checklist

- [ ] Google Sheets tabloları oluşturuldu
- [ ] Telegram bot token alındı
- [ ] Google Sheets API credentials ayarlandı
- [ ] n8n workflow import edildi
- [ ] Tüm node'lar yapılandırıldı
- [ ] Test kullanıcısı ile denendi
- [ ] /start komutu çalışıyor
- [ ] /quiz soru veriyor
- [ ] Cevap kontrolü çalışıyor
- [ ] İstatistikler gösteriliyor
- [ ] Workflow aktif edildi

---

Başarılar! 🎓🇹🇷

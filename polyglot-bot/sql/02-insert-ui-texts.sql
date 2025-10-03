USE polyglot_bot;

-- UI Metinleri
INSERT INTO ui_texts (text_key, language_code, text_value) VALUES
-- Hoş geldin mesajları
('welcome_message', 'tr', '🎉 Hoş geldin {name}!\n\nİngilizce öğrenme botuna hoş geldin!\n\nKullanabileceğin komutlar:\n/learn - Yeni kelime öğren\n/quiz - Quiz yap\n/stats - İstatistiklerini gör\n/language - Dil değiştir\n/help - Yardım\n\nHadi başlayalım! 🚀'),
('welcome_message', 'uk', '🎉 Вітаємо {name}!\n\nЛаскаво просимо до бота для вивчення англійської!\n\nДоступні команди:\n/learn - Вивчити нове слово\n/quiz - Пройти тест\n/stats - Переглянути статистику\n/language - Змінити мову\n/help - Допомога\n\nПочнімо! 🚀'),

-- Dil seçimi
('choose_language', 'tr', 'Lütfen ana dilinizi seçin:'),
('choose_language', 'uk', 'Будь ласка, оберіть вашу рідну мову:'),

-- Kelime öğrenme
('new_word', 'tr', '📚 Yeni Kelime:'),
('new_word', 'uk', '📚 Нове слово:'),
('translation', 'tr', 'Çeviri'),
('translation', 'uk', 'Переклад'),
('example', 'tr', '📝 Örnek:'),
('example', 'uk', '📝 Приклад:'),
('mark_learned', 'tr', 'Öğrendin mi? ✅'),
('mark_learned', 'uk', 'Вивчили? ✅'),

-- Quiz
('quiz_start', 'tr', '🎯 Quiz başlıyor! {count} soru gelecek.'),
('quiz_start', 'uk', '🎯 Тест починається! Буде {count} питань.'),

-- İstatistikler
('stats_title', 'tr', '📊 İstatistikleriniz:'),
('stats_title', 'uk', '📊 Ваша статистика:'),
('stats_learned', 'tr', '✅ Öğrenilen Kelimeler:'),
('stats_learned', 'uk', '✅ Вивчені слова:'),
('stats_total', 'tr', '👀 Görülen Kelimeler:'),
('stats_total', 'uk', '👀 Переглянуті слова:'),
('stats_score', 'tr', '🏆 Toplam Puan:'),
('stats_score', 'uk', '🏆 Загальний рахунок:'),
('stats_level', 'tr', '📈 Seviye:'),
('stats_level', 'uk', '📈 Рівень:'),
('stats_streak', 'tr', '🔥 Streak:'),
('stats_streak', 'uk', '🔥 Серія:'),
('stats_days', 'tr', 'gün'),
('stats_days', 'uk', 'днів'),
('stats_congrats', 'tr', 'Harika gidiyorsun! 💪'),
('stats_congrats', 'uk', 'Чудова робота! 💪'),

-- Seviyeler
('level_beginner', 'tr', 'Başlangıç'),
('level_beginner', 'uk', 'Початковий'),
('level_intermediate', 'tr', 'Orta'),
('level_intermediate', 'uk', 'Середній'),
('level_advanced', 'tr', 'İleri'),
('level_advanced', 'uk', 'Просунутий'),

-- Hatalar
('no_words_left', 'tr', 'Seviyene uygun yeni kelime kalmadı! 🎉'),
('no_words_left', 'uk', 'Немає нових слів для вашого рівня! 🎉'),
('no_words_for_quiz', 'tr', 'Quiz için yeterli kelime yok. Önce kelime öğrenmelisin!'),
('no_words_for_quiz', 'uk', 'Недостатньо слів для тесту. Спочатку вивчіть більше слів!')
ON DUPLICATE KEY UPDATE text_value=VALUES(text_value);

USE polyglot_bot;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- UI Metinleri
INSERT INTO ui_texts (text_key, language_code, text_value) VALUES
-- Hosgeldin mesajlari
('welcome_message', 'tr', 'Hos geldin {name}!\n\nIngilizce ogrenme botuna hos geldin!\n\nKomutlar:\n/learn - Yeni kelime ogren\n/quiz - Quiz yap\n/stats - Istatistikler\n/language - Dil degistir\n/help - Yardim\n\nHadi baslayalim!'),
('welcome_message', 'uk', 'Vitayemo {name}!\n\nLaskavo prosymo!\n\nKomandy:\n/learn - Vyvchyty slovo\n/quiz - Proyty test\n/stats - Statystyka\n/language - Zminyty movu\n/help - Dopomoha\n\nPochnimo!'),

-- Dil secimi
('choose_language', 'tr', 'Lutfen ana dilinizi secin:'),
('choose_language', 'uk', 'Bud laska oberit vashu movu:'),

-- Kelime ogrenme
('new_word', 'tr', 'Yeni Kelime:'),
('new_word', 'uk', 'Nove slovo:'),
('translation', 'tr', 'Ceviri'),
('translation', 'uk', 'Pereklad'),
('example', 'tr', 'Ornek:'),
('example', 'uk', 'Pryklad:'),
('mark_learned', 'tr', 'Ogrendin mi?'),
('mark_learned', 'uk', 'Vyvchyly?'),

-- Quiz
('quiz_start', 'tr', 'Quiz basliyor! {count} soru gelecek.'),
('quiz_start', 'uk', 'Test pochynaetsya! Bude {count} pytan.'),

-- Istatistikler
('stats_title', 'tr', 'Istatistikleriniz:'),
('stats_title', 'uk', 'Vasha statystyka:'),
('stats_learned', 'tr', 'Ogrenilen Kelimeler:'),
('stats_learned', 'uk', 'Vyvcheni slova:'),
('stats_total', 'tr', 'Gorulen Kelimeler:'),
('stats_total', 'uk', 'Perehlyanuti slova:'),
('stats_score', 'tr', 'Toplam Puan:'),
('stats_score', 'uk', 'Zahalnyi rakhunok:'),
('stats_level', 'tr', 'Seviye:'),
('stats_level', 'uk', 'Riven:'),
('stats_streak', 'tr', 'Seri:'),
('stats_streak', 'uk', 'Seriya:'),
('stats_days', 'tr', 'gun'),
('stats_days', 'uk', 'dniv'),
('stats_congrats', 'tr', 'Harika gidiyorsun!'),
('stats_congrats', 'uk', 'Chudova robota!'),

-- Seviyeler
('level_beginner', 'tr', 'Baslangic'),
('level_beginner', 'uk', 'Pochatkovyi'),
('level_intermediate', 'tr', 'Orta'),
('level_intermediate', 'uk', 'Serednii'),
('level_advanced', 'tr', 'Ileri'),
('level_advanced', 'uk', 'Prosunutyi'),

-- Hatalar
('no_words_left', 'tr', 'Yeni kelime kalmadi!'),
('no_words_left', 'uk', 'Nemaye novykh sliv!'),
('no_words_for_quiz', 'tr', 'Quiz icin yeterli kelime yok. Once kelime ogrenmelisin!'),
('no_words_for_quiz', 'uk', 'Nedostatno sliv dlya testu!')
ON DUPLICATE KEY UPDATE text_value=VALUES(text_value);

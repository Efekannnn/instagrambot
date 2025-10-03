USE polyglot_bot;

-- UI texts
INSERT INTO ui_texts (text_key, language_code, text_value) VALUES
-- Welcome messages
('welcome_message', 'tr', 'Hos geldin {name}! Ingilizce ogrenme botuna hos geldin! /learn - Yeni kelime ogren /quiz - Quiz yap /stats - Istatistiklerini gor /language - Dil degistir /help - Yardim'),
('welcome_message', 'uk', 'Vitaemo {name}! Laskavo prosymo do bota! /learn - Vyvchyty nove slovo /quiz - Proyty test /stats - Pereglyanuti statystyku'),

-- Language selection
('choose_language', 'tr', 'Lutfen ana dilinizi secin:'),
('choose_language', 'uk', 'Bud laska oberit vashu ridnu movu:'),

-- Word learning
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

-- Statistics
('stats_title', 'tr', 'Istatistikleriniz:'),
('stats_title', 'uk', 'Vasha statystyka:'),
('stats_learned', 'tr', 'Ogrenilen Kelimeler:'),
('stats_learned', 'uk', 'Vyvcheni slova:'),
('stats_total', 'tr', 'Gorulen Kelimeler:'),
('stats_total', 'uk', 'Pereglyanuti slova:'),
('stats_score', 'tr', 'Toplam Puan:'),
('stats_score', 'uk', 'Zagalnyy rakhunok:'),
('stats_level', 'tr', 'Seviye:'),
('stats_level', 'uk', 'Riven:'),
('stats_streak', 'tr', 'Streak:'),
('stats_streak', 'uk', 'Seriya:'),
('stats_days', 'tr', 'gun'),
('stats_days', 'uk', 'dniv'),
('stats_congrats', 'tr', 'Harika gidiyorsun!'),
('stats_congrats', 'uk', 'Chudova robota!'),

-- Levels
('level_beginner', 'tr', 'Baslangic'),
('level_beginner', 'uk', 'Pochatkovyy'),
('level_intermediate', 'tr', 'Orta'),
('level_intermediate', 'uk', 'Seredniy'),
('level_advanced', 'tr', 'Ileri'),
('level_advanced', 'uk', 'Prosunutyy'),

-- Errors
('no_words_left', 'tr', 'Seviyene uygun yeni kelime kalmadi!'),
('no_words_left', 'uk', 'Nemaye novykh sliv dlya vashoho rivnya!'),
('no_words_for_quiz', 'tr', 'Quiz icin yeterli kelime yok. Once kelime ogrenmelisin!'),
('no_words_for_quiz', 'uk', 'Nedostatno sliv dlya testu. Spochatku vivchit bilshe sliv!')
ON DUPLICATE KEY UPDATE text_value=VALUES(text_value);

USE polyglot_bot;

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- English UI texts
INSERT INTO ui_texts (text_key, language_code, text_value) VALUES
('welcome_message', 'en', '🎉 Welcome {name}!\n\nWelcome to the language learning bot!\n\n📚 Commands:\n/learn - Learn new word\n/quiz - Take a quiz\n/stats - View statistics\n/language - Change settings\n/help - Get help\n\n🚀 Let''s start!'),
('choose_learning', 'en', '🌍 What do you want to learn?'),
('choose_learning', 'uk', '🌍 Що ви хочете вивчити?'),
('new_word', 'en', '📚 New Word:'),
('translation', 'en', 'Meaning'),
('example', 'en', '📝 Example:'),
('mark_learned', 'en', 'Got it! ✅'),
('quiz_start', 'en', '🎯 Quiz starting! {count} questions coming.'),
('stats_title', 'en', '📊 Your Statistics:'),
('stats_learned', 'en', '✅ Words Learned:'),
('stats_total', 'en', '👀 Words Seen:'),
('stats_score', 'en', '🏆 Total Score:'),
('stats_level', 'en', '📈 Level:'),
('stats_streak', 'en', '🔥 Streak:'),
('stats_days', 'en', 'days'),
('stats_congrats', 'en', 'Great job! 💪'),
('level_beginner', 'en', 'Beginner'),
('level_intermediate', 'en', 'Intermediate'),
('level_advanced', 'en', 'Advanced'),
('no_words_left', 'en', 'No new words for your level! 🎉'),
('no_words_for_quiz', 'en', 'Not enough words for quiz. Learn some words first!')
ON DUPLICATE KEY UPDATE text_value=VALUES(text_value);

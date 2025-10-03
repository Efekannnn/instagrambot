USE polyglot_bot;

-- Languages tablosu
CREATE TABLE IF NOT EXISTS languages (
    language_id INT AUTO_INCREMENT PRIMARY KEY,
    language_code VARCHAR(5) UNIQUE NOT NULL,
    language_name VARCHAR(50) NOT NULL,
    flag_emoji VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Dilleri ekle
INSERT INTO languages (language_code, language_name, flag_emoji) VALUES
('tr', 'Türkçe', '🇹🇷'),
('uk', 'Українська', '🇺🇦'),
('en', 'English', '🇬🇧')
ON DUPLICATE KEY UPDATE language_name=language_name;

-- Users tablosu
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    native_language VARCHAR(5) DEFAULT 'tr',
    learning_language VARCHAR(5) DEFAULT 'en',
    level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    total_score INT DEFAULT 0,
    daily_goal INT DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_telegram_id (telegram_id),
    INDEX idx_native_lang (native_language),
    FOREIGN KEY (native_language) REFERENCES languages(language_code),
    FOREIGN KEY (learning_language) REFERENCES languages(language_code)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Vocabulary tablosu
CREATE TABLE IF NOT EXISTS vocabulary (
    word_id INT AUTO_INCREMENT PRIMARY KEY,
    english_word VARCHAR(255) NOT NULL,
    word_type ENUM('noun', 'verb', 'adjective', 'adverb', 'phrase', 'other') DEFAULT 'other',
    difficulty_level ENUM('beginner', 'intermediate', 'advanced') NOT NULL,
    pronunciation VARCHAR(255),
    image_url VARCHAR(500),
    audio_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_difficulty (difficulty_level),
    INDEX idx_word_type (word_type),
    INDEX idx_english (english_word)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Vocabulary translations tablosu
CREATE TABLE IF NOT EXISTS vocabulary_translations (
    translation_id INT AUTO_INCREMENT PRIMARY KEY,
    word_id INT NOT NULL,
    language_code VARCHAR(5) NOT NULL,
    translation VARCHAR(255) NOT NULL,
    example_sentence_en TEXT,
    example_sentence_translated TEXT,
    FOREIGN KEY (word_id) REFERENCES vocabulary(word_id) ON DELETE CASCADE,
    FOREIGN KEY (language_code) REFERENCES languages(language_code),
    UNIQUE KEY unique_word_lang (word_id, language_code),
    INDEX idx_word_lang (word_id, language_code)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- User progress tablosu
CREATE TABLE IF NOT EXISTS user_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    word_id INT NOT NULL,
    learned BOOLEAN DEFAULT FALSE,
    review_count INT DEFAULT 0,
    correct_count INT DEFAULT 0,
    wrong_count INT DEFAULT 0,
    last_reviewed TIMESTAMP NULL,
    next_review TIMESTAMP NULL,
    confidence_level INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (word_id) REFERENCES vocabulary(word_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_word (user_id, word_id),
    INDEX idx_next_review (next_review),
    INDEX idx_user_learned (user_id, learned)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Quiz history tablosu
CREATE TABLE IF NOT EXISTS quiz_history (
    quiz_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    quiz_type ENUM('multiple_choice', 'translation_en_native', 'translation_native_en') NOT NULL,
    score INT NOT NULL,
    total_questions INT NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, completed_at)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Daily challenges tablosu
CREATE TABLE IF NOT EXISTS daily_challenges (
    challenge_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    challenge_date DATE NOT NULL,
    words_learned_today INT DEFAULT 0,
    words_reviewed_today INT DEFAULT 0,
    streak_count INT DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, challenge_date),
    INDEX idx_date (challenge_date)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- UI texts tablosu
CREATE TABLE IF NOT EXISTS ui_texts (
    text_id INT AUTO_INCREMENT PRIMARY KEY,
    text_key VARCHAR(100) NOT NULL,
    language_code VARCHAR(5) NOT NULL,
    text_value TEXT NOT NULL,
    FOREIGN KEY (language_code) REFERENCES languages(language_code),
    UNIQUE KEY unique_key_lang (text_key, language_code),
    INDEX idx_key (text_key)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

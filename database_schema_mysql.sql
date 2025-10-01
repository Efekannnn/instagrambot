-- ============================================
-- Turkish Language Learning Bot - MySQL Schema
-- MySQL/MariaDB Database Structure
-- ============================================

-- Drop tables if exist (for fresh install)
DROP TABLE IF EXISTS current_questions;
DROP TABLE IF EXISTS word_history;
DROP TABLE IF EXISTS user_progress;
DROP TABLE IF EXISTS vocabulary;
DROP TABLE IF EXISTS user_sessions;

-- ============================================
-- 1. VOCABULARY TABLE
-- ============================================
CREATE TABLE vocabulary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    english_word VARCHAR(100) NOT NULL UNIQUE,
    turkish_word VARCHAR(100) NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    difficulty INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_vocab_english (english_word),
    INDEX idx_vocab_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 2. USER PROGRESS TABLE
-- ============================================
CREATE TABLE user_progress (
    user_id VARCHAR(50) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    total_questions INT DEFAULT 0,
    correct_answers INT DEFAULT 0,
    incorrect_answers INT DEFAULT 0,
    current_streak INT DEFAULT 0,
    best_streak INT DEFAULT 0,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_last_active (last_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 3. WORD HISTORY TABLE
-- ============================================
CREATE TABLE word_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    word_id INT NOT NULL,
    english_word VARCHAR(100) NOT NULL,
    turkish_word VARCHAR(100) NOT NULL,
    correct_count INT DEFAULT 0,
    incorrect_count INT DEFAULT 0,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    streak INT DEFAULT 0,
    priority_score DECIMAL(10,2) DEFAULT 100.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES vocabulary(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_word (user_id, word_id),
    INDEX idx_word_history_user (user_id),
    INDEX idx_word_history_score (user_id, priority_score DESC),
    INDEX idx_word_history_last_seen (last_seen)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 4. CURRENT QUESTIONS TABLE
-- ============================================
CREATE TABLE current_questions (
    user_id VARCHAR(50) PRIMARY KEY,
    word_id INT NOT NULL,
    question_text TEXT NOT NULL,
    correct_answer VARCHAR(1) NOT NULL,
    correct_word VARCHAR(100) NOT NULL,
    turkish_word VARCHAR(100) NOT NULL,
    english_word VARCHAR(100) NOT NULL,
    exercise_type VARCHAR(50) NOT NULL,
    options JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES vocabulary(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- 5. USER SESSIONS TABLE (for caching)
-- ============================================
CREATE TABLE user_sessions (
    user_id VARCHAR(50) PRIMARY KEY,
    vocabulary_cache JSON,
    last_cache_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    session_data JSON
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- SAMPLE DATA INSERT
-- ============================================
INSERT INTO vocabulary (english_word, turkish_word, category, difficulty) VALUES
    ('Warehouse', 'Depo', 'business', 1),
    ('Car', 'Araba', 'transportation', 1),
    ('House', 'Ev', 'housing', 1),
    ('Flower', 'Çiçek', 'nature', 1),
    ('Apple', 'Elma', 'food', 1),
    ('Book', 'Kitap', 'education', 1),
    ('Computer', 'Bilgisayar', 'technology', 2),
    ('Phone', 'Telefon', 'technology', 1),
    ('Water', 'Su', 'food', 1),
    ('Food', 'Yemek', 'food', 1),
    ('School', 'Okul', 'education', 1),
    ('Teacher', 'Öğretmen', 'education', 2),
    ('Student', 'Öğrenci', 'education', 2),
    ('Friend', 'Arkadaş', 'social', 1),
    ('Family', 'Aile', 'social', 1),
    ('Mother', 'Anne', 'family', 1),
    ('Father', 'Baba', 'family', 1),
    ('Brother', 'Kardeş', 'family', 1),
    ('Sister', 'Kız Kardeş', 'family', 2),
    ('Dog', 'Köpek', 'animals', 1),
    ('Cat', 'Kedi', 'animals', 1),
    ('Bird', 'Kuş', 'animals', 1),
    ('Fish', 'Balık', 'animals', 1),
    ('Sun', 'Güneş', 'nature', 1),
    ('Moon', 'Ay', 'nature', 1),
    ('Star', 'Yıldız', 'nature', 1),
    ('Tree', 'Ağaç', 'nature', 1),
    ('Mountain', 'Dağ', 'nature', 1),
    ('Sea', 'Deniz', 'nature', 1),
    ('River', 'Nehir', 'nature', 2),
    ('Coffee', 'Kahve', 'food', 1),
    ('Tea', 'Çay', 'food', 1),
    ('Bread', 'Ekmek', 'food', 1),
    ('Milk', 'Süt', 'food', 1),
    ('Cheese', 'Peynir', 'food', 1),
    ('Door', 'Kapı', 'housing', 1),
    ('Window', 'Pencere', 'housing', 1),
    ('Table', 'Masa', 'housing', 1),
    ('Chair', 'Sandalye', 'housing', 1),
    ('Bed', 'Yatak', 'housing', 1);

-- ============================================
-- USEFUL QUERIES
-- ============================================

-- Get user statistics
-- SELECT 
--     user_name,
--     total_questions,
--     correct_answers,
--     ROUND(correct_answers * 100.0 / total_questions, 2) as accuracy,
--     current_streak
-- FROM user_progress
-- WHERE user_id = '123456789';

-- Get words that need practice (high priority)
-- SELECT 
--     w.english_word,
--     w.turkish_word,
--     wh.correct_count,
--     wh.incorrect_count,
--     wh.priority_score,
--     wh.last_seen
-- FROM word_history wh
-- JOIN vocabulary w ON wh.word_id = w.id
-- WHERE wh.user_id = '123456789'
-- ORDER BY wh.priority_score DESC
-- LIMIT 10;

-- Get never-seen words for a user
-- SELECT v.id, v.english_word, v.turkish_word
-- FROM vocabulary v
-- LEFT JOIN word_history wh ON v.id = wh.word_id AND wh.user_id = '123456789'
-- WHERE wh.id IS NULL;

-- Update priority score (run periodically)
-- UPDATE word_history
-- SET priority_score = 
--     100 + 
--     (incorrect_count * 30) +
--     (CASE WHEN streak < 3 THEN (3 - streak) * 20 ELSE 0 END) +
--     (CASE 
--         WHEN TIMESTAMPDIFF(DAY, last_seen, NOW()) < 1 THEN -40
--         WHEN TIMESTAMPDIFF(DAY, last_seen, NOW()) < 3 THEN -20
--         ELSE TIMESTAMPDIFF(DAY, last_seen, NOW()) * 5
--     END) +
--     (CASE 
--         WHEN (correct_count + incorrect_count) > 0 
--         THEN (1 - (correct_count * 1.0 / (correct_count + incorrect_count))) * 40
--         ELSE 50
--     END)
-- WHERE user_id = '123456789';

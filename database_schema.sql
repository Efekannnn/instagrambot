-- ============================================
-- Turkish Language Learning Bot - Database Schema
-- SQLite Database Structure
-- ============================================

-- Drop tables if exist (for fresh install)
DROP TABLE IF EXISTS user_progress;
DROP TABLE IF EXISTS word_history;
DROP TABLE IF EXISTS current_questions;
DROP TABLE IF EXISTS vocabulary;
DROP TABLE IF EXISTS user_sessions;

-- ============================================
-- 1. VOCABULARY TABLE
-- ============================================
CREATE TABLE vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    english_word TEXT NOT NULL UNIQUE,
    turkish_word TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    difficulty INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast lookups
CREATE INDEX idx_vocab_english ON vocabulary(english_word);
CREATE INDEX idx_vocab_category ON vocabulary(category);

-- ============================================
-- 2. USER PROGRESS TABLE
-- ============================================
CREATE TABLE user_progress (
    user_id TEXT PRIMARY KEY,
    user_name TEXT NOT NULL,
    total_questions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    incorrect_answers INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for active users
CREATE INDEX idx_user_last_active ON user_progress(last_active);

-- ============================================
-- 3. WORD HISTORY TABLE
-- ============================================
CREATE TABLE word_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    word_id INTEGER NOT NULL,
    english_word TEXT NOT NULL,
    turkish_word TEXT NOT NULL,
    correct_count INTEGER DEFAULT 0,
    incorrect_count INTEGER DEFAULT 0,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    streak INTEGER DEFAULT 0,
    priority_score REAL DEFAULT 100.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES vocabulary(id),
    UNIQUE(user_id, word_id)
);

-- Indexes for performance
CREATE INDEX idx_word_history_user ON word_history(user_id);
CREATE INDEX idx_word_history_score ON word_history(user_id, priority_score DESC);
CREATE INDEX idx_word_history_last_seen ON word_history(last_seen);

-- ============================================
-- 4. CURRENT QUESTIONS TABLE
-- ============================================
CREATE TABLE current_questions (
    user_id TEXT PRIMARY KEY,
    word_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    correct_word TEXT NOT NULL,
    turkish_word TEXT NOT NULL,
    english_word TEXT NOT NULL,
    exercise_type TEXT NOT NULL,
    options TEXT NOT NULL, -- JSON array of options
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES vocabulary(id)
);

-- ============================================
-- 5. USER SESSIONS TABLE (for caching)
-- ============================================
CREATE TABLE user_sessions (
    user_id TEXT PRIMARY KEY,
    vocabulary_cache TEXT, -- JSON cache of vocabulary
    last_cache_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_data TEXT -- JSON for any extra session data
);

-- ============================================
-- SAMPLE DATA INSERT
-- ============================================
-- Insert sample vocabulary (you can add more)
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
    ('River', 'Nehir', 'nature', 2);

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
--         WHEN julianday('now') - julianday(last_seen) < 1 THEN -40
--         WHEN julianday('now') - julianday(last_seen) < 3 THEN -20
--         ELSE (julianday('now') - julianday(last_seen)) * 5
--     END) +
--     (CASE 
--         WHEN (correct_count + incorrect_count) > 0 
--         THEN (1 - (correct_count * 1.0 / (correct_count + incorrect_count))) * 40
--         ELSE 50
--     END)
-- WHERE user_id = '123456789';

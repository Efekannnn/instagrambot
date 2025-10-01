// ============================================
// Migration Script: Google Sheets → SQLite
// Run this to transfer existing data
// ============================================

const sqlite3 = require('sqlite3').verbose();
const { GoogleSpreadsheet } = require('google-spreadsheet');
const { JWT } = require('google-auth-library');

// ============================================
// CONFIGURATION
// ============================================
const DB_PATH = './turkish_learning_bot.db';
const SPREADSHEET_ID = '1uWivgC2y-qJ58WGecg8QY_mkNam_CUKKLcs9avpxdro';

// Google Sheets credentials (from n8n)
const GOOGLE_SERVICE_ACCOUNT = {
  // Add your Google Service Account credentials here
  // You can get this from n8n's Google Sheets credentials
  client_email: 'YOUR_CLIENT_EMAIL@project.iam.gserviceaccount.com',
  private_key: 'YOUR_PRIVATE_KEY'
};

console.log('🔄 Starting migration from Google Sheets to SQLite...\n');

// ============================================
// CONNECT TO DATABASE
// ============================================
const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) {
    console.error('❌ Error opening database:', err.message);
    process.exit(1);
  }
  console.log('✅ Connected to SQLite database\n');
});

// ============================================
// CONNECT TO GOOGLE SHEETS
// ============================================
async function migrateData() {
  try {
    const serviceAccountAuth = new JWT({
      email: GOOGLE_SERVICE_ACCOUNT.client_email,
      key: GOOGLE_SERVICE_ACCOUNT.private_key,
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });

    const doc = new GoogleSpreadsheet(SPREADSHEET_ID, serviceAccountAuth);
    await doc.loadInfo();
    console.log('✅ Connected to Google Sheets\n');
    console.log(`📄 Spreadsheet: ${doc.title}\n`);

    // ============================================
    // 1. MIGRATE VOCABULARY
    // ============================================
    console.log('📚 Migrating Vocabulary...');
    const vocabSheet = doc.sheetsByTitle['S'];
    if (vocabSheet) {
      const vocabRows = await vocabSheet.getRows();
      let vocabCount = 0;

      for (const row of vocabRows) {
        const englishWord = row.get('initialText');
        const turkishWord = row.get('translatedText');

        if (englishWord && turkishWord) {
          await new Promise((resolve, reject) => {
            db.run(
              `INSERT OR IGNORE INTO vocabulary (english_word, turkish_word, category, difficulty) 
               VALUES (?, ?, 'general', 1)`,
              [englishWord, turkishWord],
              (err) => {
                if (err) reject(err);
                else {
                  vocabCount++;
                  resolve();
                }
              }
            );
          });
        }
      }
      console.log(`✅ Migrated ${vocabCount} vocabulary entries\n`);
    } else {
      console.log('⚠️ Vocabulary sheet "S" not found\n');
    }

    // ============================================
    // 2. MIGRATE USER PROGRESS
    // ============================================
    console.log('👤 Migrating User Progress...');
    const progressSheet = doc.sheetsByTitle['UserProgress'];
    if (progressSheet) {
      const progressRows = await progressSheet.getRows();
      let progressCount = 0;

      for (const row of progressRows) {
        const userId = row.get('userId');
        const userName = row.get('userName');
        const totalQuestions = parseInt(row.get('totalQuestions')) || 0;
        const correctAnswers = parseInt(row.get('correctAnswers')) || 0;
        const incorrectAnswers = parseInt(row.get('incorrectAnswers')) || 0;
        const currentStreak = parseInt(row.get('currentStreak')) || 0;
        const lastActive = row.get('lastActive') || new Date().toISOString();

        if (userId) {
          await new Promise((resolve, reject) => {
            db.run(
              `INSERT OR REPLACE INTO user_progress 
               (user_id, user_name, total_questions, correct_answers, incorrect_answers, 
                current_streak, best_streak, last_active, created_at, updated_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))`,
              [userId, userName, totalQuestions, correctAnswers, incorrectAnswers, 
               currentStreak, currentStreak, lastActive],
              (err) => {
                if (err) reject(err);
                else {
                  progressCount++;
                  resolve();
                }
              }
            );
          });
        }
      }
      console.log(`✅ Migrated ${progressCount} user progress records\n`);
    } else {
      console.log('⚠️ UserProgress sheet not found\n');
    }

    // ============================================
    // 3. MIGRATE WORD HISTORY
    // ============================================
    console.log('📖 Migrating Word History...');
    const historySheet = doc.sheetsByTitle['WordHistory'];
    if (historySheet) {
      const historyRows = await historySheet.getRows();
      let historyCount = 0;

      for (const row of historyRows) {
        const userId = row.get('userId');
        const englishWord = row.get('englishWord');
        const turkishWord = row.get('turkishWord');
        const correct = parseInt(row.get('correct')) || 0;
        const incorrect = parseInt(row.get('incorrect')) || 0;
        const lastSeen = row.get('lastSeen') || new Date().toISOString();
        const streak = parseInt(row.get('streak')) || 0;

        if (userId && englishWord) {
          // Get word_id from vocabulary table
          await new Promise((resolve, reject) => {
            db.get(
              `SELECT id FROM vocabulary WHERE english_word = ?`,
              [englishWord],
              (err, vocabRow) => {
                if (err) {
                  reject(err);
                } else if (vocabRow) {
                  db.run(
                    `INSERT OR REPLACE INTO word_history 
                     (user_id, word_id, english_word, turkish_word, correct_count, 
                      incorrect_count, last_seen, streak, created_at, updated_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))`,
                    [userId, vocabRow.id, englishWord, turkishWord, correct, 
                     incorrect, lastSeen, streak],
                    (err) => {
                      if (err) reject(err);
                      else {
                        historyCount++;
                        resolve();
                      }
                    }
                  );
                } else {
                  // Word not in vocabulary, skip
                  resolve();
                }
              }
            );
          });
        }
      }
      console.log(`✅ Migrated ${historyCount} word history records\n`);
    } else {
      console.log('⚠️ WordHistory sheet not found\n');
    }

    console.log('🎉 Migration completed successfully!\n');
    
    // Print summary
    db.get('SELECT COUNT(*) as count FROM vocabulary', (err, row) => {
      if (!err) console.log(`📚 Total vocabulary: ${row.count}`);
    });
    
    db.get('SELECT COUNT(*) as count FROM user_progress', (err, row) => {
      if (!err) console.log(`👤 Total users: ${row.count}`);
    });
    
    db.get('SELECT COUNT(*) as count FROM word_history', (err, row) => {
      if (!err) console.log(`📖 Total word records: ${row.count}`);
      db.close();
      console.log('\n✅ Database closed. Migration complete!');
    });

  } catch (error) {
    console.error('❌ Migration error:', error.message);
    db.close();
    process.exit(1);
  }
}

// ============================================
// RUN MIGRATION
// ============================================
migrateData();

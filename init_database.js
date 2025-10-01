// ============================================
// Database Initialization Script
// Run this ONCE to setup your SQLite database
// ============================================

const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');

// Database file path
const DB_PATH = './turkish_learning_bot.db';

console.log('🚀 Starting database initialization...\n');

// Create/Open database
const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) {
    console.error('❌ Error opening database:', err.message);
    process.exit(1);
  }
  console.log('✅ Connected to SQLite database\n');
});

// Read SQL schema file
const schema = fs.readFileSync('./database_schema.sql', 'utf8');

// Split by semicolon and execute each statement
const statements = schema.split(';').filter(s => s.trim().length > 0);

let completed = 0;
let total = statements.length;

db.serialize(() => {
  statements.forEach((statement, index) => {
    db.run(statement + ';', (err) => {
      completed++;
      
      if (err) {
        // Ignore "table already exists" errors
        if (!err.message.includes('already exists')) {
          console.error(`❌ Error in statement ${index + 1}:`, err.message);
        }
      } else {
        // Show progress
        const statementPreview = statement.trim().substring(0, 50);
        console.log(`✅ [${completed}/${total}] ${statementPreview}...`);
      }
      
      // Close database when all done
      if (completed === total) {
        console.log('\n✅ Database initialization complete!');
        console.log(`📁 Database file: ${DB_PATH}\n`);
        
        // Verify tables were created
        db.all("SELECT name FROM sqlite_master WHERE type='table'", (err, tables) => {
          if (err) {
            console.error('❌ Error verifying tables:', err.message);
          } else {
            console.log('📋 Created tables:');
            tables.forEach(table => {
              console.log(`   - ${table.name}`);
            });
          }
          
          // Count vocabulary entries
          db.get("SELECT COUNT(*) as count FROM vocabulary", (err, row) => {
            if (!err && row) {
              console.log(`\n📚 Vocabulary entries: ${row.count}`);
            }
            
            console.log('\n🎉 Setup complete! You can now use the workflow.\n');
            db.close();
          });
        });
      }
    });
  });
});

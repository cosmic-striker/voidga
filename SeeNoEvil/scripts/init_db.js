const sqlite3 = require("sqlite3").verbose();
const fs = require("fs");

const dbFile = "../db/database.sqlite3";
const flag = fs.readFileSync("../enc.txt", "utf-8").trim();

// Remove DB if exists
if (fs.existsSync(dbFile)) {
  fs.unlinkSync(dbFile);
}

const db = new sqlite3.Database(dbFile);

db.serialize(() => {
  db.run(`CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )`);

  db.run(`CREATE TABLE flags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flag TEXT NOT NULL
    )`);

  db.run(`INSERT INTO users (username, password) VALUES (?, ?)`, [
    "admin",
    "#h3y_i_@m_7he_b055!!",
  ]);
  db.run(`INSERT INTO flags (flag) VALUES (?)`, [flag]);
});

db.close(() => {
  console.log("✅ Database initialized and seeded.");
});

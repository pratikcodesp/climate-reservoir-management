const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { Pool } = require('pg');

const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// ✅ PostgreSQL connection config - UPDATE WITH YOUR CREDENTIALS
const pool = new Pool({
  user: 'postgres',         // ✅ Your actual PostgreSQL user
  host: 'localhost',
  database: 'onevote_db',   // ✅ Your actual database name
  password: 'postgres',     // ✅ Your actual password
  port: 5432,
});

// Test database connection on startup
pool.connect()
  .then(client => {
    console.log("✅ Connected to PostgreSQL database");
    client.release();
  })
  .catch(err => {
    console.error("❌ Failed to connect to PostgreSQL:", err);
    process.exit(1); // Exit the app if DB fails
  });

// ➕ Submit a vote
app.post('/vote', async (req, res) => {
  console.log("📥 Incoming vote request:", req.body);

  const { candidate } = req.body;

  if (!candidate) {
    return res.status(400).json({ error: "Candidate is required" });
  }

  try {
    await pool.query('INSERT INTO votes (candidate) VALUES ($1)', [candidate]);
    res.json({ message: "✅ Vote recorded successfully" });
  } catch (err) {
    console.error('❌ Error saving vote:', err);
    res.status(500).json({ error: "Failed to save vote" });
  }
});

// 📊 Get vote counts
app.get('/vote-counts', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT candidate, COUNT(*) AS votes 
      FROM votes 
      GROUP BY candidate
    `);

    const voteCounts = {};
    result.rows.forEach(row => {
      voteCounts[row.candidate] = parseInt(row.votes);
    });

    res.json(voteCounts);
  } catch (err) {
    console.error('❌ Error fetching vote counts:', err);
    res.status(500).json({ error: "Failed to fetch vote counts" });
  }
});

// 🧪 Health check
app.get('/', (req, res) => {
  res.send("✅ One Vote backend is running");
});

// Start server
app.listen(port, () => {
  console.log(`🚀 Server is live at: http://localhost:${port}`);
});

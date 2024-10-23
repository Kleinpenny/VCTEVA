const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();
const port = 3307;
app.use(cors());

// 创建 MySQL 连接
const db = mysql.createConnection({
    host: 'localhost', // MySQL 服务器地址
    user: 'root', // MySQL 用户名
    password: 'vcteva_2024', // MySQL 密码
    database: 'VCTEVA' // 数据库名称
});

// 连接到数据库
db.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err.message);
        return;
    }
    console.log('Connected to MySQL database');
});

app.get('/players', (req, res) => {
    const query = 'SELECT * FROM PlayerAverageStats'; // 替换为你的查询
    db.query(query, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});
app.get('/average', (req, res) => {
    const query = `SELECT
                       AVG(average_combat_score) AS avg_combat_score,
                       AVG(average_kills) AS avg_kills,
                       AVG(average_deaths) AS avg_deaths,
                       AVG(average_assists) AS avg_assists,
                       AVG(average_kpr) AS avg_kpr,
                       AVG(average_dpr) AS avg_dpr,
                       AVG(average_total_damage_taken) AS avg_total_damage_taken,
                       AVG(average_total_damage_caused) AS avg_total_damage_caused,
                       AVG(average_damage_per_round) AS average_damage_per_round,
                       AVG(average_damage_taken_per_round) AS average_damage_taken_per_round,
                       AVG(average_dddelta) AS avg_dddelta,
                       AVG(average_headshot_hit_rate) AS average_headshot_hit_rate FROM PlayerAverageStats`; // 替换为你的查询
    db.query(query, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(results);
    });
});
app.get('/regions', (req, res) => {
    const query = `
        SELECT DISTINCT region
        FROM players
        WHERE region IS NOT NULL AND region NOT IN ('nan', '');
    `;

    db.query(query, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }

        // 将结果转换为一个纯粹的数组列表
        const regions = results.map(row => row.region);
        res.json(regions);
    });
});


// 启动服务器
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

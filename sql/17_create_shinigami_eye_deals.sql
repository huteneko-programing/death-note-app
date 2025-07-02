-- 死神の目の取引記録
CREATE TABLE shinigami_eye_deals (
    deal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    acquired_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    original_lifespan INTEGER,
    halved_lifespan INTEGER,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ミサが死神の目を取得
INSERT INTO shinigami_eye_deals (user_id, original_lifespan, halved_lifespan)
SELECT user_id, 50, 25 FROM users WHERE user_name = 'ミサ';
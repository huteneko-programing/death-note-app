-- 人物マスタテーブル
CREATE TABLE people (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    real_name TEXT NOT NULL UNIQUE,
    birth_date DATE,
    death_date DATE,
    is_alive BOOLEAN DEFAULT 1,
    failed_attempts INTEGER DEFAULT 0
);

-- テスト用の人物データ
INSERT INTO people (real_name, birth_date) VALUES
('竜崎', '1979-10-31'),
('模木完造', '1973-09-13'),
('夜神総一郎', '1955-07-12');

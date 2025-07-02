-- 死神テーブル
CREATE TABLE shinigami (
    shinigami_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shinigami_name TEXT NOT NULL UNIQUE
);

-- 死神を登録
INSERT INTO shinigami (shinigami_name) VALUES
('リューク'),
('レム');

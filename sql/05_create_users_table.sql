-- ユーザー（使用者）テーブル
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE
);

-- ユーザーを登録
INSERT INTO users (user_name) VALUES
('夜神月'),
('ミサ');

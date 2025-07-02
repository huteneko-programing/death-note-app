-- 所有履歴テーブル
CREATE TABLE ownership_history (
    ownership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    owned_from DATETIME DEFAULT CURRENT_TIMESTAMP,
    owned_until DATETIME,

    FOREIGN KEY (note_id) REFERENCES death_notes(note_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 所有権を設定
INSERT INTO ownership_history (note_id, user_id)
SELECT 1, user_id FROM users WHERE user_name = '夜神月';

INSERT INTO ownership_history (note_id, user_id)
SELECT 2, user_id FROM users WHERE user_name = 'ミサ';

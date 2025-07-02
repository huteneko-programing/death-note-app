-- バックアップ
ALTER TABLE death_note_v1 RENAME TO death_note_backup;

-- 新しい死亡記録テーブル
CREATE TABLE death_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    victim_name TEXT NOT NULL,
    cause_of_death TEXT DEFAULT '心臓麻痺',
    death_details TEXT,
    written_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    death_at DATETIME,
    writer_id INTEGER NOT NULL,
    face_remembered BOOLEAN DEFAULT 0,
    shinigami_id INTEGER,

    -- 外部キー（他のテーブルとの関係）
    FOREIGN KEY (writer_id) REFERENCES users(user_id),
    FOREIGN KEY (shinigami_id) REFERENCES shinigami(shinigami_id)
);

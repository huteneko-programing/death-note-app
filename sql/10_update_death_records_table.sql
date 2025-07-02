-- 既存のdeath_recordsを退避
CREATE TABLE death_records_old AS SELECT * FROM death_records;
DROP TABLE death_records;

-- note_id列を追加した新しいテーブル
CREATE TABLE death_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    victim_name TEXT NOT NULL,
    cause_of_death TEXT DEFAULT '心臓麻痺',
    death_details TEXT,
    written_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    death_at DATETIME,
    note_id INTEGER NOT NULL,
    writer_id INTEGER NOT NULL,
    face_remembered BOOLEAN NOT NULL DEFAULT 1,

    FOREIGN KEY (note_id) REFERENCES death_notes(note_id),
    FOREIGN KEY (writer_id) REFERENCES users(user_id)
);
-- 既存のテーブルを退避
CREATE TABLE death_records_backup2 AS SELECT * FROM death_records;
DROP TABLE death_records;

-- person_idを使う新しいテーブル
CREATE TABLE death_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    cause_of_death TEXT DEFAULT '心臓麻痺',
    death_details TEXT,
    written_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    death_at DATETIME,
    note_id INTEGER NOT NULL,
    writer_id INTEGER NOT NULL,

    FOREIGN KEY (person_id) REFERENCES people(person_id),
    FOREIGN KEY (note_id) REFERENCES death_notes(note_id),
    FOREIGN KEY (writer_id) REFERENCES users(user_id)
);
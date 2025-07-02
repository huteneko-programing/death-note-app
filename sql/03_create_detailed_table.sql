-- 前のテーブルを削除
DROP TABLE IF EXISTS death_note_records;

-- デスノートの詳細版テーブル
CREATE TABLE death_note_v1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 犠牲者情報
    victim_name TEXT NOT NULL,

    -- 死因（デフォルトは心臓麻痺）
    cause_of_death TEXT DEFAULT '心臓麻痺',

    -- 詳細な状況
    death_details TEXT,

    -- 時間関係
    written_at TEXT NOT NULL,
    death_at TEXT,

    -- 書いた人
    writer_name TEXT NOT NULL,

    -- 顔を思い浮かべたか
    face_remembered TEXT CHECK(face_remembered IN ('yes', 'no')),

    -- デスノート情報
    note_owner TEXT,
    shinigami_name TEXT
);

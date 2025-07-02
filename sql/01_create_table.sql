-- デスノートの最初のテーブルを作成
-- CREATE TABLE = 「表を作る」命令です

CREATE TABLE death_note_records (
    -- id = 通し番号（自動で増える）
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 犠牲者の名前
    victim_name TEXT NOT NULL,

    -- いつ書いたか
    written_date TEXT,

    -- 誰が書いたか
    writer_name TEXT
);
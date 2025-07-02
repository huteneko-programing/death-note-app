-- デスノート自体を管理
CREATE TABLE death_notes (
    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shinigami_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (shinigami_id) REFERENCES shinigami(shinigami_id)
);

-- デスノートを作成
INSERT INTO death_notes (shinigami_id)
SELECT shinigami_id FROM shinigami WHERE shinigami_name = 'リューク';

INSERT INTO death_notes (shinigami_id)
SELECT shinigami_id FROM shinigami WHERE shinigami_name = 'レム';

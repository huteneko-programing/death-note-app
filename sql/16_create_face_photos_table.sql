-- 顔写真テーブル
CREATE TABLE face_photos (
    photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL UNIQUE,
    photo_path TEXT NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (person_id) REFERENCES people(person_id)
);

-- テスト用の顔写真
INSERT INTO face_photos (person_id, photo_path)
SELECT person_id, 'photos/' || real_name || '.jpg'
FROM people
WHERE real_name IN ('竜崎', '模木完造');

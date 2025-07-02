-- デスノートの実際の犠牲者データ

-- 1人目：音原田九郎（渋井丸拓男）
INSERT INTO death_note_v1
(victim_name, written_at, writer_name, face_remembered, note_owner, shinigami_name)
VALUES
('音原田九郎', '2003-11-28 18:00:00', '夜神月', 'yes', '夜神月', 'リューク');

-- 2人目：渋井丸拓男
INSERT INTO death_note_v1
(victim_name, written_at, writer_name, face_remembered, note_owner, shinigami_name)
VALUES
('渋井丸拓男', '2003-11-28 18:05:00', '夜神月', 'yes', '夜神月', 'リューク');

-- 3人目：恐田奇一郎（交通事故を指定）
INSERT INTO death_note_v1
(victim_name, cause_of_death, written_at, writer_name, face_remembered, note_owner, shinigami_name)
VALUES
('恐田奇一郎', '交通事故', '2003-11-29 19:00:00', '夜神月', 'yes', '夜神月', 'リューク');

-- 月による殺害
INSERT INTO death_records (person_id, writer_id, note_id, cause_of_death)
SELECT p.person_id, 1, 1, '心臓麻痺'
FROM people p
WHERE p.real_name IN (
    '渋井丸拓男', '音原田九郎', '恐田奇一郎', '空条新一'
);

-- FBI捜査官の殺害
INSERT INTO death_records (person_id, writer_id, note_id, cause_of_death, death_details)
SELECT
    p.person_id,
    1,
    1,
    '心臓麻痺',
    '山手線の車内で苦しみながら死亡'
FROM people p
WHERE p.real_name = 'レイ・ペンバー';

-- ナオミ・ミソラの悲劇
INSERT INTO death_records (person_id, writer_id, note_id, cause_of_death, death_details)
SELECT
    p.person_id,
    1,
    1,
    '自殺',
    '遺書を残さず、自分の痕跡を全て消してから死亡'
FROM people p
WHERE p.real_name = 'ナオミ・ミソラ';
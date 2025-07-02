-- 死神の目を持つユーザーのビュー
CREATE VIEW users_with_shinigami_eyes AS
SELECT
    u.user_id,
    u.user_name,
    sed.acquired_at,
    sed.halved_lifespan as remaining_years
FROM users u
JOIN shinigami_eye_deals sed ON u.user_id = sed.user_id
WHERE sed.is_active = 1;

-- 顔認識ビュー
CREATE VIEW face_recognition AS
SELECT
    fp.photo_path,
    p.person_id,
    p.real_name,
    CASE
        WHEN p.is_alive = 0 THEN 0
        ELSE CAST((julianday(date('now', '+80 years')) - julianday('now')) / 365.25 AS INTEGER)
    END as remaining_lifespan_years
FROM face_photos fp
JOIN people p ON fp.person_id = p.person_id;

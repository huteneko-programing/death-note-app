-- 現在の所有者一覧
CREATE VIEW current_owners AS
SELECT
    dn.note_id,
    u.user_name as owner,
    s.shinigami_name as shinigami
FROM death_notes dn
JOIN ownership_history oh ON dn.note_id = oh.note_id
JOIN users u ON oh.user_id = u.user_id
JOIN shinigami s ON dn.shinigami_id = s.shinigami_id
WHERE oh.owned_until IS NULL;

-- キラの活動統計
CREATE VIEW kira_statistics AS
SELECT
    u.user_name,
    COUNT(dr.record_id) as total_kills,
    MIN(dr.written_at) as first_kill,
    MAX(dr.written_at) as last_kill
FROM users u
LEFT JOIN death_records dr ON u.user_id = dr.writer_id
GROUP BY u.user_id, u.user_name;
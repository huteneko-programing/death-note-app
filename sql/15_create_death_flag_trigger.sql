-- 死亡時にis_aliveを更新
CREATE TRIGGER mark_person_as_dead
AFTER INSERT ON death_records
FOR EACH ROW
BEGIN
    UPDATE people
    SET is_alive = 0,
        death_date = NEW.death_at
    WHERE person_id = NEW.person_id;
END;

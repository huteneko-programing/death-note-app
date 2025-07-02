-- 40秒ルールの自動化
CREATE TRIGGER auto_death_time
AFTER INSERT ON death_records
FOR EACH ROW
WHEN NEW.death_at IS NULL
BEGIN
    UPDATE death_records
    SET death_at = datetime(NEW.written_at, '+40 seconds')
    WHERE record_id = NEW.record_id;
END;
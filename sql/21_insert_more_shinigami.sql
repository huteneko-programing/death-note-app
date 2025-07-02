-- 追加の死神
INSERT INTO shinigami (shinigami_name) VALUES
('ジェラス'),
('シドウ'),
('ミードラ'),
('グック');

-- 追加のデスノート
INSERT INTO death_notes (shinigami_id) VALUES
((SELECT shinigami_id FROM shinigami WHERE shinigami_name = 'シドウ')),
((SELECT shinigami_id FROM shinigami WHERE shinigami_name = 'ジェラス'));

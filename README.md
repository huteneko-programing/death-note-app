# デスノートDXで学ぶSQL入門

## 🎯 プロジェクト概要

人気アニメ「デスノート」を題材に、SQLとデータベースの基礎を楽しく学ぶプロジェクトです。

**学習内容**：

- SQLの基本操作（CREATE, INSERT, SELECT, UPDATE, DELETE）
- データベース設計と正規化
- リレーションとJOIN
- トリガーとビュー
- PythonでのWebアプリ開発

**想定時間**：2-3時間

**対象**：プログラミング・データベース完全初心者

## 🛠 環境構築

### 必要なツール

1. **SQLite** - 軽量なデータベース
2. **VSCode** - コードエディタ
3. **Python 3.8+** - アプリ開発用（Phase 8以降）

### インストール手順

### Mac

```bash
# Homebrewのインストール（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# SQLiteのインストール
brew install sqlite3

# Pythonのインストール
brew install python3

```

### Windows

1. [SQLite公式サイト](https://www.sqlite.org/download.html)からダウンロード
2. [VSCode公式サイト](https://code.visualstudio.com/)からダウンロード
3. [Python公式サイト](https://www.python.org/downloads/)からダウンロード

### VSCode拡張機能

VSCodeを開いて、以下の拡張機能をインストール：

1. 左サイドバーの拡張機能アイコンをクリック
2. 「SQLite」で検索（作者：alexcvzz）
3. インストールボタンをクリック

### プロジェクトセットアップ

```bash
# プロジェクトフォルダを作成
mkdir death-note-dx
cd death-note-dx

# SQLファイル用フォルダを作成
mkdir sql

```

## Phase 1: はじめてのデータベース

### 1-1. データベースとは何か？

データベースは「表（テーブル）」でデータを管理します。
Excelの表のようなものです！

| 名前 | 学年 | クラス |
| --- | --- | --- |
| 田中太郎 | 1 | A |
| 佐藤花子 | 2 | B |

### 1-2. 最初のテーブルを作ろう

**ファイル作成：`sql/01_create_table.sql`**

```sql
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

```

**実行方法：**

```bash
# データベースを作成してテーブルを作る
sqlite3 death_note.db < sql/01_create_table.sql

# 確認
sqlite3 death_note.db
.tables  # テーブル一覧を表示
.exit    # 終了

```

### 1-3. データを入れてみよう

**ファイル作成：`sql/02_insert_first_data.sql`**

```sql
-- 最初の犠牲者を入れる
INSERT INTO death_note_records (victim_name, written_date, writer_name)
VALUES ('音原田九郎', '2003-11-28 18:00:00', '夜神月');

```

**実行と確認：**

```bash
# データを入れる
sqlite3 death_note.db < sql/02_insert_first_data.sql

# 確認する
sqlite3 death_note.db
SELECT * FROM death_note_records;
.exit

```

### 1-4. VSCodeで見てみよう

1. VSCodeでプロジェクトフォルダを開く
2. 左サイドバーで`death_note.db`を右クリック
3. 「Open Database」を選択
4. 下部のSQLITE EXPLORERでテーブルを確認

## Phase 2: デスノートらしくする

### 2-1. デスノートのルールを思い出そう

- 40秒以内に死因を書かないと心臓麻痺
- 6分40秒以内なら詳細を書ける
- 顔を思い浮かべる必要がある

### 2-2. 詳細なテーブル設計

**ファイル作成：`sql/03_create_detailed_table.sql`**

```sql
-- 前のテーブルを削除
DROP TABLE IF EXISTS death_note_records;

-- デスノートの詳細版テーブル
CREATE TABLE death_note_v1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 犠牲者情報
    victim_name TEXT NOT NULL,

    -- 死因（デフォルトは心臓麻痺）
    cause_of_death TEXT DEFAULT '心臓麻痺',

    -- 詳細な状況
    death_details TEXT,

    -- 時間関係
    written_at TEXT NOT NULL,
    death_at TEXT,

    -- 書いた人
    writer_name TEXT NOT NULL,

    -- 顔を思い浮かべたか
    face_remembered TEXT CHECK(face_remembered IN ('yes', 'no')),

    -- デスノート情報
    note_owner TEXT,
    shinigami_name TEXT
);

```

**実行：**

```bash
sqlite3 death_note.db < sql/03_create_detailed_table.sql

```

### 2-3. テストデータを入れる

**ファイル作成：`sql/04_insert_test_data.sql`**

```sql
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

```

**実行と確認：**

```bash
sqlite3 death_note.db < sql/04_insert_test_data.sql

# VSCodeで確認するか、以下のコマンドで確認
sqlite3 death_note.db
SELECT victim_name, cause_of_death FROM death_note_v1;
.exit

```

### 2-4. 問題点を発見

同じ名前（夜神月、リューク）を何度も書いている...これは無駄！

## Phase 3: データの正規化

### 3-1. 正規化とは？

同じデータを何度も書かないように、データを整理することです。

### 3-2. ユーザーテーブルを作る

**ファイル作成：`sql/05_create_users_table.sql`**

```sql
-- ユーザー（使用者）テーブル
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE
);

-- ユーザーを登録
INSERT INTO users (user_name) VALUES
('夜神月'),
('ミサ');

```

**実行：**

```bash
sqlite3 death_note.db < sql/05_create_users_table.sql

```

### 3-3. 死神テーブルを作る

**ファイル作成：`sql/06_create_shinigami_table.sql`**

```sql
-- 死神テーブル
CREATE TABLE shinigami (
    shinigami_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shinigami_name TEXT NOT NULL UNIQUE
);

-- 死神を登録
INSERT INTO shinigami (shinigami_name) VALUES
('リューク'),
('レム');

```

**実行：**

```bash
sqlite3 death_note.db < sql/06_create_shinigami_table.sql

```

### 3-4. 正規化した死亡記録テーブル

**ファイル作成：`sql/07_create_normalized_death_records.sql`**

```sql
-- バックアップ
ALTER TABLE death_note_v1 RENAME TO death_note_backup;

-- 新しい死亡記録テーブル
CREATE TABLE death_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    victim_name TEXT NOT NULL,
    cause_of_death TEXT DEFAULT '心臓麻痺',
    death_details TEXT,
    written_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    death_at DATETIME,
    writer_id INTEGER NOT NULL,
    face_remembered BOOLEAN DEFAULT 0,
    shinigami_id INTEGER,

    -- 外部キー（他のテーブルとの関係）
    FOREIGN KEY (writer_id) REFERENCES users(user_id),
    FOREIGN KEY (shinigami_id) REFERENCES shinigami(shinigami_id)
);

```

**実行：**

```bash
sqlite3 death_note.db < sql/07_create_normalized_death_records.sql

```

### 3-5. リレーションを使ったデータ確認

```bash
sqlite3 death_note.db

# まずIDを確認
SELECT * FROM users;
SELECT * FROM shinigami;

# IDを使ってデータを入れる
INSERT INTO death_records (victim_name, writer_id, face_remembered, shinigami_id)
VALUES ('火口卿介', 1, 1, 1);

# JOINを使って名前で表示
SELECT
    dr.victim_name,
    u.user_name as writer,
    s.shinigami_name as shinigami
FROM death_records dr
JOIN users u ON dr.writer_id = u.user_id
LEFT JOIN shinigami s ON dr.shinigami_id = s.shinigami_id;

.exit

```

## Phase 4: デスノート管理

### 4-1. デスノートテーブル

**ファイル作成：`sql/08_create_death_notes_table.sql`**

```sql
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

```

**実行：**

```bash
sqlite3 death_note.db < sql/08_create_death_notes_table.sql

```

### 4-2. 所有履歴テーブル

**ファイル作成：`sql/09_create_ownership_history.sql`**

```sql
-- 所有履歴テーブル
CREATE TABLE ownership_history (
    ownership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    owned_from DATETIME DEFAULT CURRENT_TIMESTAMP,
    owned_until DATETIME,

    FOREIGN KEY (note_id) REFERENCES death_notes(note_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 所有権を設定
INSERT INTO ownership_history (note_id, user_id)
SELECT 1, user_id FROM users WHERE user_name = '夜神月';

INSERT INTO ownership_history (note_id, user_id)
SELECT 2, user_id FROM users WHERE user_name = 'ミサ';

```

**実行：**

```bash
sqlite3 death_note.db < sql/09_create_ownership_history.sql

```

### 4-3. death_recordsテーブルの更新

**ファイル作成：`sql/10_update_death_records_table.sql`**

```sql
-- 既存のdeath_recordsを退避
CREATE TABLE death_records_old AS SELECT * FROM death_records;
DROP TABLE death_records;

-- note_id列を追加した新しいテーブル
CREATE TABLE death_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    victim_name TEXT NOT NULL,
    cause_of_death TEXT DEFAULT '心臓麻痺',
    death_details TEXT,
    written_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    death_at DATETIME,
    note_id INTEGER NOT NULL,
    writer_id INTEGER NOT NULL,
    face_remembered BOOLEAN NOT NULL DEFAULT 1,

    FOREIGN KEY (note_id) REFERENCES death_notes(note_id),
    FOREIGN KEY (writer_id) REFERENCES users(user_id)
);

```

**実行：**

```bash
sqlite3 death_note.db < sql/10_update_death_records_table.sql

```

### 4-4. 便利なビューを作る

**ファイル作成：`sql/11_create_views.sql`**

```sql
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

```

**実行と確認：**

```bash
sqlite3 death_note.db < sql/11_create_views.sql

# ビューを使ってみる
sqlite3 death_note.db
SELECT * FROM current_owners;
SELECT * FROM kira_statistics;
.exit

```

## Phase 5: ルール実装

### 5-1. 人物マスタテーブル

**ファイル作成：`sql/12_create_people_table.sql`**

```sql
-- 人物マスタテーブル
CREATE TABLE people (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    real_name TEXT NOT NULL UNIQUE,
    birth_date DATE,
    death_date DATE,
    is_alive BOOLEAN DEFAULT 1,
    failed_attempts INTEGER DEFAULT 0
);

-- テスト用の人物データ
INSERT INTO people (real_name, birth_date) VALUES
('竜崎', '1979-10-31'),
('模木完造', '1973-09-13'),
('夜神総一郎', '1955-07-12');

```

**実行：**

```bash
sqlite3 death_note.db < sql/12_create_people_table.sql

```

### 5-2. death_recordsを人物IDに対応

**ファイル作成：`sql/13_update_death_records_with_person.sql`**

```sql
-- 既存のテーブルを退避
CREATE TABLE death_records_backup2 AS SELECT * FROM death_records;
DROP TABLE death_records;

-- person_idを使う新しいテーブル
CREATE TABLE death_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    cause_of_death TEXT DEFAULT '心臓麻痺',
    death_details TEXT,
    written_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    death_at DATETIME,
    note_id INTEGER NOT NULL,
    writer_id INTEGER NOT NULL,

    FOREIGN KEY (person_id) REFERENCES people(person_id),
    FOREIGN KEY (note_id) REFERENCES death_notes(note_id),
    FOREIGN KEY (writer_id) REFERENCES users(user_id)
);

```

**実行：**

```bash
sqlite3 death_note.db < sql/13_update_death_records_with_person.sql

```

### 5-3. 40秒ルールのトリガー

**ファイル作成：`sql/14_create_40_seconds_trigger.sql`**

```sql
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

```

**実行：**

```bash
sqlite3 death_note.db < sql/14_create_40_seconds_trigger.sql

```

### 5-4. 重複防止トリガー

**ファイル作成：`sql/15_create_duplicate_prevention_trigger.sql`**

```sql
-- 同じ人を2回殺せない
CREATE TRIGGER prevent_duplicate_death
BEFORE INSERT ON death_records
FOR EACH ROW
WHEN EXISTS (
    SELECT 1 FROM death_records
    WHERE person_id = NEW.person_id
)
BEGIN
    SELECT RAISE(ABORT, 'この人物は既にデスノートに記載済みです');
END;

```

**実行：**

```bash
sqlite3 death_note.db < sql/15_create_duplicate_prevention_trigger.sql

```

### 5-5. 死亡フラグ更新トリガー

**ファイル作成：`sql/16_create_death_flag_trigger.sql`**

```sql
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

```

**実行：**

```bash
sqlite3 death_note.db < sql/16_create_death_flag_trigger.sql

```

### 5-6. トリガーのテスト

```bash
sqlite3 death_note.db

# テスト用の人物を追加
INSERT INTO people (real_name, birth_date)
VALUES ('松田桃太', '1978-12-14');

# デスノートに記入
INSERT INTO death_records (person_id, writer_id, note_id)
SELECT person_id, 1, 1 FROM people WHERE real_name = '松田桃太';

# 結果確認（40秒後の死亡時刻とis_alive=0）
SELECT p.real_name, p.is_alive, dr.death_at
FROM people p
JOIN death_records dr ON p.person_id = dr.person_id
WHERE p.real_name = '松田桃太';

# 重複テスト（エラーになるはず）
INSERT INTO death_records (person_id, writer_id, note_id)
SELECT person_id, 1, 1 FROM people WHERE real_name = '松田桃太';

.exit

```

## Phase 6: 死神の目

### 6-1. 顔写真テーブル

**ファイル作成：`sql/17_create_face_photos_table.sql`**

```sql
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

```

**実行：**

```bash
sqlite3 death_note.db < sql/17_create_face_photos_table.sql

```

### 6-2. 死神の目の取引

**ファイル作成：`sql/18_create_shinigami_eye_deals.sql`**

```sql
-- 死神の目の取引記録
CREATE TABLE shinigami_eye_deals (
    deal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    acquired_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    original_lifespan INTEGER,
    halved_lifespan INTEGER,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ミサが死神の目を取得
INSERT INTO shinigami_eye_deals (user_id, original_lifespan, halved_lifespan)
SELECT user_id, 50, 25 FROM users WHERE user_name = 'ミサ';

```

**実行：**

```bash
sqlite3 death_note.db < sql/18_create_shinigami_eye_deals.sql

```

### 6-3. 顔認識ビュー

**ファイル作成：`sql/19_create_face_recognition_view.sql`**

```sql
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

```

**実行と確認：**

```bash
sqlite3 death_note.db < sql/19_create_face_recognition_view.sql

# 確認
sqlite3 death_note.db
SELECT * FROM users_with_shinigami_eyes;
SELECT * FROM face_recognition;
.exit

```

## Phase 7: サンプルデータ投入

### 7-1. 大量の人物データ

**ファイル作成：`sql/20_insert_many_people.sql`**

```sql
-- デスノートに登場する主要人物を追加
INSERT INTO people (real_name, birth_date) VALUES
-- キラ事件関係者
('夜神粧裕', '1989-02-18'),
('高田清美', '1985-02-14'),
('魅上照', '1982-11-07'),
('出目川仁', '1972-08-13'),

-- FBI捜査官
('レイ・ペンバー', '1975-12-31'),
('ナオミ・ミソラ', '1976-02-11'),
('フレデリック・ガンター', '1974-03-15'),
('アレックス・ドワイト', '1973-07-22'),

-- ヨツバグループ
('火口卿介', '1955-04-22'),
('樹多正彦', '1958-08-15'),
('奈南川零司', '1960-11-03'),
('三堂芯吾', '1962-03-27'),

-- 犯罪者たち
('渋井丸拓男', '1970-06-15'),
('音原田九郎', '1968-11-28'),
('恐田奇一郎', '1965-03-22'),
('空条新一', '1972-09-10'),

-- ワイミーズハウス関係者
('ニア', '1991-08-24'),
('メロ', '1989-12-13'),
('マット', '1990-02-01');

```

**実行：**

```bash
sqlite3 death_note.db < sql/20_insert_many_people.sql

```

### 7-2. キラの大量殺人データ

**ファイル作成：`sql/21_insert_death_records.sql`**

```sql
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

```

**実行：**

```bash
sqlite3 death_note.db < sql/21_insert_death_records.sql

```

### 7-3. 追加の死神とノート

**ファイル作成：`sql/22_insert_more_shinigami.sql`**

```sql
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

```

**実行：**

```bash
sqlite3 death_note.db < sql/22_insert_more_shinigami.sql

```

### 7-4. 統計を見てみよう

```bash
sqlite3 death_note.db

# 基本統計
SELECT COUNT(*) as 総死亡者数 FROM death_records;

# キラ別の殺害数
SELECT
    u.user_name as キラ,
    COUNT(*) as 殺害数
FROM death_records dr
JOIN users u ON dr.writer_id = u.user_id
GROUP BY u.user_name
ORDER BY 殺害数 DESC;

# 死因の統計
SELECT
    cause_of_death as 死因,
    COUNT(*) as 人数,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM death_records), 1) as 割合
FROM death_records
GROUP BY cause_of_death;

.exit

```

## Phase 8: Webアプリ作成

### 8-1. Python環境のセットアップ

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 必要なパッケージをインストール
pip install streamlit pandas plotly

```

### 8-2. フォルダ構造の準備

```bash
# pagesフォルダを作成（マルチページ用）
mkdir pages

# photosフォルダを作成（顔写真用）
mkdir photos

```

### 8-3. メインページ（app.py）

**ファイル作成：`app.py`**

```python
import streamlit as st
import sqlite3
import pandas as pd

# ページ設定
st.set_page_config(
    page_title="DEATH NOTE DX",
    page_icon="📔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# データベース接続関数
@st.cache_resource
def get_connection():
    return sqlite3.connect('death_note.db', check_same_thread=False)

# データベース操作関数
def check_person_exists(conn, name):
    """人物が既に登録されているか確認"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT person_id FROM people WHERE real_name = ?",
        (name,)
    )
    result = cursor.fetchone()
    return result[0] if result else None

def register_person(conn, name):
    """新しい人物を登録"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO people (real_name) VALUES (?)",
        (name,)
    )
    conn.commit()
    return cursor.lastrowid

def write_death_note(conn, person_id, user_id, note_id, cause=None):
    """デスノートに記入"""
    cursor = conn.cursor()
    
    try:
        if cause:
            cursor.execute("""
                INSERT INTO death_records 
                (person_id, writer_id, note_id, cause_of_death)
                VALUES (?, ?, ?, ?)
            """, (person_id, user_id, note_id, cause))
        else:
            cursor.execute("""
                INSERT INTO death_records 
                (person_id, writer_id, note_id)
                VALUES (?, ?, ?)
            """, (person_id, user_id, note_id))
        
        conn.commit()
        return True, "記入成功"
    except Exception as e:
        if "この人物は既にデスノートに記載済みです" in str(e):
            return False, "この人物は既にデスノートに記載済みです"
        return False, str(e)

# タイトル
st.title("📔 DEATH NOTE DX")

# データベース接続
conn = get_connection()

# サイドバー：ユーザー選択
with st.sidebar:
    st.header("📝 使用者情報")
    
    # ユーザー一覧を取得
    users_df = pd.read_sql_query(
        "SELECT user_id, user_name FROM users", 
        conn
    )
    
    if len(users_df) > 0:
        selected_user = st.selectbox(
            "使用者を選択",
            users_df['user_name'].tolist()
        )
        
        # 選択されたユーザーのIDを取得
        selected_user_id = users_df[
            users_df['user_name'] == selected_user
        ]['user_id'].iloc[0]
        
        # セッション状態に保存（他のページでも使える）
        st.session_state['selected_user'] = selected_user
        st.session_state['selected_user_id'] = selected_user_id
        
        st.info(f"現在の使用者: {selected_user}")
        
        # 所有しているノートを表示
        notes_df = pd.read_sql_query("""
            SELECT 
                dn.note_id,
                s.shinigami_name
            FROM death_notes dn
            JOIN ownership_history oh ON dn.note_id = oh.note_id
            JOIN shinigami s ON dn.shinigami_id = s.shinigami_id
            WHERE oh.user_id = ? AND oh.owned_until IS NULL
        """, conn, params=[selected_user_id])
        
        if len(notes_df) > 0:
            st.success(f"所有ノート: {len(notes_df)}冊")
            for _, note in notes_df.iterrows():
                st.write(f"- ノート{note['note_id']} (死神: {note['shinigami_name']})")
    else:
        st.error("ユーザーが登録されていません")
        selected_user_id = None
    
    # ページ説明
    st.markdown("---")
    st.markdown("""
    ### 📖 ページ一覧
    - **ホーム**: デスノート記入
    - **統計**: 死亡記録の分析
    - **死神の目**: 特殊機能
    - **SQL学習**: 練習問題
    """)

# メインエリア
st.header("🖊️ デスノートに記入")

if selected_user_id:
    # 使用可能なノートを取得
    available_notes = pd.read_sql_query("""
        SELECT note_id FROM ownership_history 
        WHERE user_id = ? AND owned_until IS NULL
    """, conn, params=[selected_user_id])
    
    # ノートが見つからない場合は最初のノートを使用
    if len(available_notes) == 0:
        available_notes = pd.read_sql_query("SELECT note_id FROM death_notes LIMIT 1", conn)
    
    # 最近の記録を表示
    st.subheader("📜 最近の記録")
    recent_records = pd.read_sql_query("""
        SELECT 
            p.real_name as '犠牲者',
            dr.cause_of_death as '死因',
            dr.written_at as '記入時刻',
            dr.death_at as '死亡予定時刻'
        FROM death_records dr
        JOIN people p ON dr.person_id = p.person_id
        WHERE dr.writer_id = ?
        ORDER BY dr.written_at DESC
        LIMIT 5
    """, conn, params=[selected_user_id])
    
    if len(recent_records) > 0:
        st.dataframe(recent_records, use_container_width=True)
    else:
        st.info("まだ記録がありません")
    
    st.markdown("---")
    
    # 入力フォーム
    with st.form("death_note_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            victim_name = st.text_input("犠牲者の名前", placeholder="例: 田中太郎")
            
            # 顔を思い浮かべたかのチェック
            face_remembered = st.checkbox(
                "対象の顔を思い浮かべた",
                value=False,
                help="顔を思い浮かべないと効果がありません"
            )
        
        with col2:
            # 死因（オプション）
            cause_of_death = st.text_input(
                "死因（40秒以内・空欄なら心臓麻痺）",
                placeholder="心臓麻痺"
            )
            
            # 詳細（オプション）
            death_details = st.text_area(
                "詳細（6分40秒以内）",
                placeholder="任意",
                height=68
            )
        
        # 送信ボタン
        submitted = st.form_submit_button("デスノートに記入", type="primary", use_container_width=True)
        
        if submitted:
            if not victim_name:
                st.error("❌ 名前を入力してください")
            elif not face_remembered:
                st.error("❌ 顔を思い浮かべる必要があります")
            else:
                # 人物の確認/登録
                person_id = check_person_exists(conn, victim_name)
                if not person_id:
                    person_id = register_person(conn, victim_name)
                
                # ノートIDを取得（最初のノート）
                note_id = available_notes.iloc[0]['note_id']
                
                # デスノートに記入
                success, message = write_death_note(
                    conn, 
                    person_id, 
                    selected_user_id,
                    note_id,
                    cause_of_death if cause_of_death else None
                )
                
                if success:
                    st.success(f"✅ {victim_name}をデスノートに記入しました")
                    st.info("40秒後に効果が現れます...")
                    st.balloons()
                else:
                    st.error(f"❌ エラー: {message}")
else:
    st.info("👈 サイドバーからユーザーを選択してください")

# デスノートのルール表示
with st.expander("📖 デスノートのルール"):
    st.markdown("""
    **基本ルール:**
    - このノートに名前を書かれた人間は死ぬ
    - 書く人物の顔が頭に入っていないと効果はない
    - 名前の後に40秒以内に死因を書くと、その通りになる
    - 死因を書かなければ心臓麻痺となる
    - 死因を書いた後、6分40秒以内に詳細を記載する事で、詳しい死の状況を記せる
    
    **このアプリでの制限:**
    - 同じ人物を2回殺すことはできない
    - 780日未満の人間には効果がない
    - 124歳を超える人間には効果がない
    """)
```

### 8-4. 死神の目ページ

**ファイル作成：`shinigami_eyes.py`**

```jsx

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="死神の目 - DEATH NOTE DX", page_icon="👁️")

st.title("👁️ 死神の目")
st.markdown("**「寿命の半分と引き換えに、人間の名前と寿命が見える眼」**")

# データベース接続
@st.cache_resource
def get_connection():
    return sqlite3.connect('death_note.db', check_same_thread=False)

conn = get_connection()

# 現在のユーザーを取得（セッション状態から）
if 'selected_user' in st.session_state:
    current_user = st.session_state.selected_user
    current_user_id = st.session_state.selected_user_id
    
    # 死神の目を持っているか確認
    has_eyes = pd.read_sql_query("""
        SELECT COUNT(*) as count
        FROM shinigami_eye_deals sed
        JOIN users u ON sed.user_id = u.user_id
        WHERE u.user_name = ? AND sed.is_active = 1
    """, conn, params=[current_user]).iloc[0, 0] > 0
    
    if has_eyes:
        st.success(f"✅ {current_user}は死神の目を所有しています")
        
        # 取引情報を表示
        deal_info = pd.read_sql_query("""
            SELECT 
                acquired_at,
                original_lifespan,
                halved_lifespan
            FROM shinigami_eye_deals
            WHERE user_id = ? AND is_active = 1
        """, conn, params=[current_user_id])
        
        if len(deal_info) > 0:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("取得日", deal_info.iloc[0]['acquired_at'].split()[0])
            with col2:
                st.metric("元の寿命", f"{deal_info.iloc[0]['original_lifespan']}年")
            with col3:
                st.metric("残り寿命", f"{deal_info.iloc[0]['halved_lifespan']}年")
        
        st.markdown("---")
        
        # タブで機能を分割
        tab1, tab2, tab3 = st.tabs(["👤 人物識別", "📊 寿命統計", "🔍 顔写真検索"])
        
        with tab1:
            st.header("👤 登録済み人物の識別")
            
            # 登録済みの顔写真一覧
            faces = pd.read_sql_query("""
                SELECT 
                    fp.photo_path,
                    p.person_id,
                    p.real_name,
                    p.is_alive,
                    p.birth_date,
                    CASE 
                        WHEN p.is_alive = 0 THEN '死亡'
                        ELSE CAST(80 - (julianday('now') - julianday(p.birth_date)) / 365.25 AS INTEGER) || '年'
                    END as remaining_lifespan
                FROM face_photos fp
                JOIN people p ON fp.person_id = p.person_id
                ORDER BY p.real_name
            """, conn)
            
            if len(faces) > 0:
                # 検索フィルター
                search_term = st.text_input("🔍 名前で検索", placeholder="例: 竜崎")
                
                if search_term:
                    faces = faces[faces['real_name'].str.contains(search_term, case=False, na=False)]
                
                # グリッド表示
                cols = st.columns(3)
                for idx, face in faces.iterrows():
                    with cols[idx % 3]:
                        # カード風の表示
                        with st.container():
                            st.write("---")
                            st.write(f"📷 **{face['photo_path'].split('/')[-1]}**")
                            
                            if face['is_alive'] == 0:
                                st.error(f"💀 **{face['real_name']}** (死亡)")
                            else:
                                st.success(f"✅ **{face['real_name']}**")
                                st.write(f"⏰ 残り寿命: **{face['remaining_lifespan']}**")
                            
                            # 生年月日を表示
                            if face['birth_date']:
                                age = int((datetime.now() - datetime.strptime(face['birth_date'], '%Y-%m-%d')).days / 365.25)
                                st.caption(f"年齢: {age}歳")
            else:
                st.info("📷 顔写真が登録されていません")
        
        with tab2:
            st.header("📊 寿命統計")
            
            # 生存者の寿命統計
            lifespan_stats = pd.read_sql_query("""
                SELECT 
                    COUNT(*) as total_people,
                    AVG(80 - (julianday('now') - julianday(birth_date)) / 365.25) as avg_remaining,
                    MIN(80 - (julianday('now') - julianday(birth_date)) / 365.25) as min_remaining,
                    MAX(80 - (julianday('now') - julianday(birth_date)) / 365.25) as max_remaining
                FROM people
                WHERE is_alive = 1 AND birth_date IS NOT NULL
            """, conn)
            
            if len(lifespan_stats) > 0 and lifespan_stats.iloc[0]['total_people'] > 0:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("生存者数", f"{int(lifespan_stats.iloc[0]['total_people'])}人")
                with col2:
                    st.metric("平均残り寿命", f"{int(lifespan_stats.iloc[0]['avg_remaining'])}年")
                with col3:
                    st.metric("最短寿命", f"{int(lifespan_stats.iloc[0]['min_remaining'])}年")
                with col4:
                    st.metric("最長寿命", f"{int(lifespan_stats.iloc[0]['max_remaining'])}年")
                
                # 年齢層別分布
                st.subheader("年齢層別分布")
                age_distribution = pd.read_sql_query("""
                    SELECT 
                        CASE 
                            WHEN (julianday('now') - julianday(birth_date)) / 365.25 < 20 THEN '0-19歳'
                            WHEN (julianday('now') - julianday(birth_date)) / 365.25 < 40 THEN '20-39歳'
                            WHEN (julianday('now') - julianday(birth_date)) / 365.25 < 60 THEN '40-59歳'
                            ELSE '60歳以上'
                        END as age_group,
                        COUNT(*) as count
                    FROM people
                    WHERE is_alive = 1 AND birth_date IS NOT NULL
                    GROUP BY age_group
                """, conn)
                
                if len(age_distribution) > 0:
                    st.bar_chart(age_distribution.set_index('age_group'))
        
        with tab3:
            st.header("🔍 顔写真アップロード")
            st.info("新しい人物の顔写真を登録できます（デモ版では実際の画像アップロードは非対応）")
            
            # 顔写真がない人物のリスト
            no_photo_people = pd.read_sql_query("""
                SELECT p.person_id, p.real_name
                FROM people p
                LEFT JOIN face_photos fp ON p.person_id = fp.person_id
                WHERE fp.photo_id IS NULL AND p.is_alive = 1
                ORDER BY p.real_name
            """, conn)
            
            if len(no_photo_people) > 0:
                st.subheader("📸 顔写真未登録の人物")
                
                selected_person = st.selectbox(
                    "人物を選択",
                    no_photo_people['real_name'].tolist()
                )
                
                if st.button("顔写真を登録（デモ）", type="primary"):
                    # デモなので実際には登録しない
                    st.success(f"✅ {selected_person}の顔写真を登録しました（デモ）")
                    st.balloons()
                
                # 未登録者リスト
                with st.expander("未登録者一覧"):
                    st.dataframe(no_photo_people['real_name'], use_container_width=True)
            
    else:
        st.warning(f"⚠️ {current_user}は死神の目を持っていません")
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("💀 死神の目の取引")
            st.markdown("""
            **取引条件：**
            - 現在の寿命の半分と引き換え
            - 人の顔を見るだけで名前がわかる
            - 残りの寿命も見える
            - 一度取引すると取り消せない
            
            **メリット：**
            - 顔写真から即座に本名を特定
            - デスノートの効果を確実に発動
            - 相手の残り寿命を把握
            
            **デメリット：**
            - 寿命が半分になる
            - 取り消し不可
            """)
        
        with col2:
            st.image("https://via.placeholder.com/300x400/000000/FF0000?text=死神の目", caption="死神の目のイメージ")
        
        st.markdown("---")
        
        # 取引ボタン
        st.subheader("⚡ 取引を実行")
        
        # 確認用チェックボックス
        confirm1 = st.checkbox("寿命が半分になることを理解しました")
        confirm2 = st.checkbox("取引は取り消せないことを理解しました")
        
        if confirm1 and confirm2:
            if st.button("死神の目の取引を実行する", type="primary", use_container_width=True):
                # 取引処理
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO shinigami_eye_deals 
                    (user_id, original_lifespan, halved_lifespan)
                    VALUES (?, 80, 40)
                """, (current_user_id,))
                conn.commit()
                
                st.success("✅ 死神の目の取引が完了しました")
                st.info("寿命の半分と引き換えに、死神の目を手に入れました")
                st.balloons()
                
                # ページをリロード
                st.experimental_rerun()
        else:
            st.info("👆 両方のチェックボックスにチェックを入れると取引ボタンが有効になります")
else:
    st.error("❌ ユーザーが選択されていません")
    st.info("👈 ホームページでユーザーを選択してください")

# 死神の目の説明
with st.expander("📚 死神の目について詳しく"):
    st.markdown("""
    **死神の目とは：**
    
    死神の目は、デスノートの世界における特殊能力です。
    
    **原作での設定：**
    - 死神は元々この能力を持っている
    - 人間は寿命の半分と引き換えに取得可能
    - ミサやメロが取引を行った
    
    **能力の詳細：**
    1. **名前の視認**: 顔を見るだけで本名がわかる
    2. **寿命の視認**: その人の残り寿命が数字で見える
    3. **写真でも有効**: 顔写真からでも情報を読み取れる
    
    **制限事項：**
    - デスノート所有者同士では寿命が見えない
    - 自分の寿命は見えない
    - 取引は一度きりで取り消し不可
    """)

```

### 8-5. SQL学習用ページ

**ファイル作成：`sql_learning.py`**

```jsx
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="SQL学習 - DEATH NOTE DX", page_icon="🎓")

st.title("🎓 SQL学習モード")
st.markdown("**「知識こそが最強の武器」- L**")

# データベース接続
@st.cache_resource
def get_connection():
    return sqlite3.connect('death_note.db', check_same_thread=False)

conn = get_connection()

# 学習進捗を管理（セッション状態）
if 'completed_problems' not in st.session_state:
    st.session_state.completed_problems = set()

# サイドバーに進捗を表示
with st.sidebar:
    st.header("📊 学習進捗")
    total_problems = 15
    completed = len(st.session_state.completed_problems)
    progress = completed / total_problems
    
    st.progress(progress)
    st.metric("完了した問題", f"{completed}/{total_problems}")
    
    if completed == total_problems:
        st.success("🎉 全問題クリア！")
        st.balloons()
    
    if st.button("進捗をリセット"):
        st.session_state.completed_problems = set()
        st.experimental_rerun()

# タブで難易度を分類
tab1, tab2, tab3, tab4 = st.tabs(["🔰 基礎編", "🎯 中級編", "🏆 上級編", "🧪 実験室"])

# 問題表示関数
def show_problem(problem_id, title, description, hint, answer, difficulty="基礎"):
    """問題を表示する共通関数"""
    # 問題タイトル
    if problem_id in st.session_state.completed_problems:
        st.success(f"✅ {title}")
    else:
        st.subheader(title)
    
    # 問題説明
    st.write(description)
    
    # SQLエディタ
    user_query = st.text_area(
        "SQLを入力してください",
        height=150,
        placeholder="SELECT ...",
        key=f"query_{problem_id}"
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("実行", key=f"run_{problem_id}"):
            if user_query.strip():
                try:
                    # SELECTクエリのみ許可
                    if not user_query.strip().upper().startswith('SELECT'):
                        st.error("❌ SELECTクエリのみ実行可能です")
                    else:
                        result = pd.read_sql_query(user_query, conn)
                        st.success("✅ 実行成功！")
                        
                        # 結果を表示
                        with st.expander("実行結果", expanded=True):
                            st.dataframe(result, use_container_width=True)
                            st.caption(f"結果: {len(result)}行")
                        
                        # 正解判定（簡易版）
                        try:
                            expected = pd.read_sql_query(answer, conn)
                            if result.equals(expected):
                                st.balloons()
                                st.success("🎉 正解です！素晴らしい！")
                                st.session_state.completed_problems.add(problem_id)
                            else:
                                st.info("実行はできましたが、期待する結果と異なるようです")
                        except:
                            pass
                            
                except Exception as e:
                    st.error(f"❌ エラー: {e}")
            else:
                st.warning("SQLを入力してください")
    
    with col2:
        if st.button("ヒント", key=f"hint_{problem_id}"):
            st.info(f"💡 ヒント: {hint}")
    
    with col3:
        if st.button("解答", key=f"answer_{problem_id}"):
            st.code(answer, language='sql')
    
    with col4:
        if st.button("リセット", key=f"reset_{problem_id}"):
            st.experimental_rerun()
    
    st.markdown("---")

# 基礎編
with tab1:
    st.header("🔰 基礎編 - SQLの基本を学ぼう")
    st.info("まずは基本的なSELECT文から始めましょう！")
    
    show_problem(
        "basic_1",
        "問題1: 全ての死亡記録を5件だけ表示",
        "death_recordsテーブルから最初の5件のデータを取得してください。",
        "SELECT * FROM ... LIMIT ...",
        "SELECT * FROM death_records LIMIT 5;"
    )
    
    show_problem(
        "basic_2",
        "問題2: 生きている人の名前一覧",
        "peopleテーブルから生きている人（is_alive = 1）の名前を取得してください。",
        "WHERE句を使って条件を指定します",
        "SELECT real_name FROM people WHERE is_alive = 1;"
    )
    
    show_problem(
        "basic_3",
        "問題3: 心臓麻痺で死んだ人の数をカウント",
        "death_recordsテーブルから死因が'心臓麻痺'の件数を数えてください。",
        "COUNT(*)とWHERE句を組み合わせます",
        "SELECT COUNT(*) FROM death_records WHERE cause_of_death = '心臓麻痺';"
    )
    
    show_problem(
        "basic_4",
        "問題4: ユーザー名の一覧（アルファベット順）",
        "usersテーブルから全てのユーザー名をアルファベット順で取得してください。",
        "ORDER BY句を使います",
        "SELECT user_name FROM users ORDER BY user_name;"
    )
    
    show_problem(
        "basic_5",
        "問題5: 死神の数を数える",
        "shinigamiテーブルに登録されている死神の総数を取得してください。",
        "COUNT(*)を使います",
        "SELECT COUNT(*) as shinigami_count FROM shinigami;"
    )

# 中級編
with tab2:
    st.header("🎯 中級編 - JOINとGROUP BYをマスター")
    st.info("複数のテーブルを結合して、より複雑な分析をしてみましょう！")
    
    show_problem(
        "intermediate_1",
        "問題6: 各使用者の殺害数",
        "各ユーザーが何人殺害したかを集計してください。ユーザー名と殺害数を表示します。",
        "JOINとGROUP BYを使います",
        """
        SELECT 
            u.user_name,
            COUNT(dr.record_id) as kill_count
        FROM users u
        LEFT JOIN death_records dr ON u.user_id = dr.writer_id
        GROUP BY u.user_id, u.user_name
        ORDER BY kill_count DESC;
        """
    )
    
    show_problem(
        "intermediate_2",
        "問題7: 死因別の統計（パーセント付き）",
        "死因ごとの件数と全体に対する割合を計算してください。",
        "サブクエリまたはウィンドウ関数を使います",
        """
        SELECT 
            cause_of_death,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM death_records), 1) as percentage
        FROM death_records
        GROUP BY cause_of_death
        ORDER BY count DESC;
        """
    )
    
    show_problem(
        "intermediate_3",
        "問題8: 現在のデスノート所有者",
        "現在デスノートを所有しているユーザーと、そのノートに憑いている死神を表示してください。",
        "複数のJOINを使います",
        """
        SELECT 
            u.user_name as owner,
            s.shinigami_name as shinigami
        FROM death_notes dn
        JOIN ownership_history oh ON dn.note_id = oh.note_id
        JOIN users u ON oh.user_id = u.user_id
        JOIN shinigami s ON dn.shinigami_id = s.shinigami_id
        WHERE oh.owned_until IS NULL;
        """
    )
    
    show_problem(
        "intermediate_4",
        "問題9: 死神の目を持つユーザー",
        "死神の目の取引をしたユーザーとその残り寿命を表示してください。",
        "JOINとWHERE句を組み合わせます",
        """
        SELECT 
            u.user_name,
            sed.halved_lifespan as remaining_years,
            sed.acquired_at
        FROM users u
        JOIN shinigami_eye_deals sed ON u.user_id = sed.user_id
        WHERE sed.is_active = 1;
        """
    )
    
    show_problem(
        "intermediate_5",
        "問題10: 月別の殺害数",
        "月ごとの殺害数を集計してください（データがある月のみ）。",
        "日付関数とGROUP BYを使います",
        """
        SELECT 
            strftime('%Y-%m', written_at) as month,
            COUNT(*) as kills
        FROM death_records
        GROUP BY month
        ORDER BY month;
        """
    )

# 上級編
with tab3:
    st.header("🏆 上級編 - 複雑なクエリに挑戦")
    st.info("実践的な分析クエリを書いてみましょう！")
    
    show_problem(
        "advanced_1",
        "問題11: 死神別の殺害効率",
        "各死神のノートで何人が殺害されたか、何人のユーザーが使用したかを集計してください。",
        "複数のJOINとGROUP BYを使います",
        """
        SELECT 
            s.shinigami_name,
            COUNT(DISTINCT dr.writer_id) as unique_users,
            COUNT(dr.record_id) as total_kills
        FROM shinigami s
        JOIN death_notes dn ON s.shinigami_id = dn.shinigami_id
        LEFT JOIN death_records dr ON dn.note_id = dr.note_id
        GROUP BY s.shinigami_id, s.shinigami_name;
        """
    )
    
    show_problem(
        "advanced_2",
        "問題12: 最も危険な時間帯",
        "何時台に最も多くの殺害が行われたかを分析してください。",
        "時間の抽出とGROUP BYを使います",
        """
        SELECT 
            strftime('%H', written_at) as hour,
            COUNT(*) as kills
        FROM death_records
        GROUP BY hour
        ORDER BY kills DESC
        LIMIT 5;
        """
    )
    
    show_problem(
        "advanced_3",
        "問題13: 生存率の分析",
        "全人物に対する生存者と死亡者の割合を計算してください。",
        "CASE文とCOUNTを組み合わせます",
        """
        SELECT 
            COUNT(CASE WHEN is_alive = 1 THEN 1 END) as alive_count,
            COUNT(CASE WHEN is_alive = 0 THEN 1 END) as dead_count,
            ROUND(COUNT(CASE WHEN is_alive = 1 THEN 1 END) * 100.0 / COUNT(*), 1) as survival_rate
        FROM people;
        """
    )
    
    show_problem(
        "advanced_4",
        "問題14: 顔写真登録率",
        "生きている人のうち、顔写真が登録されている人の割合を計算してください。",
        "LEFT JOINとCOUNTを使います",
        """
        SELECT 
            COUNT(DISTINCT p.person_id) as total_alive,
            COUNT(DISTINCT fp.person_id) as with_photo,
            ROUND(COUNT(DISTINCT fp.person_id) * 100.0 / COUNT(DISTINCT p.person_id), 1) as photo_rate
        FROM people p
        LEFT JOIN face_photos fp ON p.person_id = fp.person_id
        WHERE p.is_alive = 1;
        """
    )
    
    show_problem(
        "advanced_5",
        "問題15: キラの活動パターン分析",
        "各ユーザーの初回殺害日、最終殺害日、活動期間（日数）を計算してください。",
        "日付関数と集計関数を組み合わせます",
        """
        SELECT 
            u.user_name,
            MIN(dr.written_at) as first_kill,
            MAX(dr.written_at) as last_kill,
            julianday(MAX(dr.written_at)) - julianday(MIN(dr.written_at)) as active_days,
            COUNT(dr.record_id) as total_kills
        FROM users u
        JOIN death_records dr ON u.user_id = dr.writer_id
        GROUP BY u.user_id, u.user_name
        HAVING COUNT(dr.record_id) > 0;
        """
    )

# 実験室
with tab4:
    st.header("🧪 SQL実験室 - 自由にクエリを試そう")
    st.info("ここでは自由にSQLクエリを実行できます。データベースの構造を探索してみましょう！")
    
    # テーブル一覧を表示
    with st.expander("📊 データベース構造"):
        tables = pd.read_sql_query("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name;
        """, conn)
        
        st.write("**テーブル一覧:**")
        for table in tables['name']:
            st.write(f"- {table}")
            
            # 各テーブルの構造を表示
            if st.checkbox(f"{table}の構造を見る", key=f"schema_{table}"):
                schema = pd.read_sql_query(f"PRAGMA table_info({table})", conn)
                st.dataframe(schema[['name', 'type', 'notnull', 'pk']], use_container_width=True)
    
    st.subheader("🔬 自由記述SQL")
    
    free_query = st.text_area(
        "SQLクエリを入力（SELECTのみ）",
        height=200,
        placeholder="""例：
-- デスノートの統計情報を取得
SELECT 
    COUNT(DISTINCT writer_id) as total_kiras,
    COUNT(*) as total_deaths,
    COUNT(DISTINCT person_id) as unique_victims
FROM death_records;
"""
    )
    
    if st.button("実行", type="primary", use_container_width=True):
        if free_query.strip():
            if not free_query.strip().upper().startswith('SELECT'):
                st.error("❌ SELECTクエリのみ実行可能です")
            else:
                try:
                    result = pd.read_sql_query(free_query, conn)
                    st.success(f"✅ 実行成功！（{len(result)}行）")
                    st.dataframe(result, use_container_width=True)
                    
                    # CSV形式でダウンロード可能に
                    csv = result.to_csv(index=False)
                    st.download_button(
                        label="📥 CSVでダウンロード",
                        data=csv,
                        file_name="query_result.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"❌ エラー: {e}")
        else:
            st.warning("SQLクエリを入力してください")
    
    # サンプルクエリ集
    st.subheader("📝 サンプルクエリ集")
    
    sample_queries = {
        "複雑な統計": """
-- 死神、使用者、殺害数の関係を分析
SELECT 
    s.shinigami_name,
    u.user_name as current_owner,
    COUNT(dr.record_id) as kills,
    dn.note_id
FROM shinigami s
JOIN death_notes dn ON s.shinigami_id = dn.shinigami_id
LEFT JOIN ownership_history oh ON dn.note_id = oh.note_id AND oh.owned_until IS NULL
LEFT JOIN users u ON oh.user_id = u.user_id
LEFT JOIN death_records dr ON dn.note_id = dr.note_id
GROUP BY s.shinigami_name, u.user_name, dn.note_id;
        """,
        "時系列分析": """
-- 日別の殺害数推移
SELECT 
    DATE(written_at) as date,
    COUNT(*) as daily_kills,
    GROUP_CONCAT(DISTINCT writer_id) as active_kiras
FROM death_records
GROUP BY DATE(written_at)
ORDER BY date;
        """,
        "ビューの活用": """
-- 登録済みビューを使った分析
SELECT * FROM kira_statistics;
        """
    }
    
    selected_sample = st.selectbox("サンプルを選択", list(sample_queries.keys()))
    
    if st.button("サンプルをコピー"):
        st.code(sample_queries[selected_sample], language='sql')
        st.info("👆 このクエリをコピーして上の実験室で実行してみてください")

# フッター
st.markdown("---")
st.markdown("""
### 📚 SQL学習のヒント

1. **基本から始める**: SELECT, WHERE, ORDER BYから始めましょう
2. **段階的に学ぶ**: JOIN → GROUP BY → サブクエリの順で学習
3. **実データで練習**: このデスノートデータベースで実践的に学べます
4. **エラーを恐れない**: エラーメッセージから学ぶことも多いです

頑張ってSQLマスターを目指しましょう！🚀
""")
```

### 8-6. アプリの実行

```bash
# Streamlitアプリを起動
streamlit run app.py

# ブラウザが自動で開きます
# 開かない場合は http://localhost:8501 にアクセス

```

### 8-6. 各ページの説明

**1. ホーム（app.py）**

- デスノートに名前を記入する機能
- 現在の使用者情報の表示
- 最近の記録の確認
- デスノートのルール説明

**2. 死神の目ページ（shinigami_eyes.py）**

- 死神の目の取引機能
- 顔写真から人物を識別
- 寿命の統計表示
- 年齢層別分布グラフ

**4. SQL学習ページ（sql_learning.py）**

- 基礎編：SELECT、WHERE、ORDER BYの練習
- 中級編：JOIN、GROUP BYの練習
- 上級編：複雑なクエリの練習
- 実験室：自由にSQLを実行
- 学習進捗の管理

## 🎯 学習のポイント

### SQL基礎

- **CREATE TABLE**: テーブルを作る
- **INSERT**: データを入れる
- **SELECT**: データを見る
- **UPDATE**: データを変更する
- **DELETE**: データを削除する

### SQL中級

- **JOIN**: 複数のテーブルを結合
- **GROUP BY**: グループ化して集計
- **WHERE**: 条件を指定
- **ORDER BY**: 並び替え

### データベース設計

- **正規化**: データの重複を排除
- **主キー**: レコードを一意に識別
- **外部キー**: テーブル間の関係

### 高度な機能

- **VIEW**: よく使うSELECTに名前をつける
- **TRIGGER**: イベント時に自動実行
- **DEFAULT**: デフォルト値
- **CHECK**: データの検証

## 🔧 トラブルシューティング

### よくあるエラー

**1. "no such table" エラー**

```bash
# テーブルが存在しない場合
sqlite3 death_note.db
.tables  # テーブル一覧を確認

```

**2. "FOREIGN KEY constraint failed" エラー**

```bash
# 外部キー制約違反（存在しないIDを参照）
# 正しいIDを確認してから再実行

```

**3. Streamlitが起動しない**

```bash
# 仮想環境が有効か確認
which python  # venv内のpythonが表示されるべき

# パッケージを再インストール
pip install --upgrade streamlit

```

### データベースのリセット

何か問題が発生したら、最初からやり直すことができます：

```bash
# データベースを削除
rm death_note.db

# 最初から実行
sqlite3 death_note.db < sql/01_create_table.sql
# ... 順番に実行

```

## 📚 さらに学習したい方へ

### 発展課題

1. **インデックス**: 検索を高速化
2. **トランザクション**: 複数の処理をまとめる
3. **バックアップ**: データの保護
4. **API化**: REST APIでアクセス

### 追加機能のアイデア

- 死神ランキング
- 死亡予定カレンダー
- キラ捜査本部モード
- 6分40秒ルールの実装

## 🎉 まとめ

デスノートを題材に、以下を学びました：

- SQLの基本操作
- データベース設計の重要性
- 正規化の概念
- トリガーやビューの活用
- Webアプリとの連携

これらの技術は実際の開発でも使える本物のスキルです！

---

**作成者**: ふてぶてしい猫
**ライセンス**: MIT
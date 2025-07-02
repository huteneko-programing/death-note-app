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
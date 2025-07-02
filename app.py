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
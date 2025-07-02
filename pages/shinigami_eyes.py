
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

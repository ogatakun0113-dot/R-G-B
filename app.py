import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="カラー抵抗計算アシスト", layout="centered")

# --- 見た目の設定（CSS） ---
st.markdown("""
    <style>
    .credit { text-align: right; font-size: 14px; color: #666; margin-bottom: -20px; }
    .resistor-body {
        background-color: #f2ce8e; /* 抵抗器の地色 */
        height: 60px;
        width: 100%;
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: space-around;
        padding: 0 40px;
        border: 2px solid #d4a75a;
        margin: 20px 0;
    }
    .band { height: 100%; width: 15px; }
    .result-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4169E1;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)
st.title('🎨 カラー抵抗計算アシスト')

# --- カラーデータ定義 ---
colors = {
    "黒": {"val": 0, "mul": 1, "hex": "#000000", "tol": None},
    "茶": {"val": 1, "mul": 10, "hex": "#8B4513", "tol": 1},
    "赤": {"val": 2, "mul": 100, "hex": "#FF0000", "tol": 2},
    "橙": {"val": 3, "mul": 1000, "hex": "#FFA500", "tol": None},
    "黄": {"val": 4, "mul": 10000, "hex": "#FFFF00", "tol": None},
    "緑": {"val": 5, "mul": 100000, "hex": "#008000", "tol": 0.5},
    "青": {"val": 6, "mul": 1000000, "hex": "#0000FF", "tol": 0.25},
    "紫": {"val": 7, "mul": 10000000, "hex": "#800080", "tol": 0.1},
    "灰": {"val": 8, "mul": 100000000, "hex": "#808080", "tol": 0.05},
    "白": {"val": 9, "mul": 1000000000, "hex": "#FFFFFF", "tol": None},
    "金": {"val": None, "mul": 0.1, "hex": "#D4AF37", "tol": 5},
    "銀": {"val": None, "mul": 0.01, "hex": "#C0C0C0", "tol": 10},
}

# --- モード選択 ---
mode = st.radio("帯の数を選択", ["4本帯", "5本帯"], horizontal=True)

st.subheader("カラーを選択")
cols = st.columns(5 if mode == "5本帯" else 4)

# 選択肢の生成
val_list = [k for k, v in colors.items() if v["val"] is not None]
mul_list = list(colors.keys())
tol_list = [k for k, v in colors.items() if v["tol"] is not None]

# --- ユーザー入力 ---
with cols[0]:
    b1 = st.selectbox("第1帯", val_list, index=1) # 茶
with cols[1]:
    b2 = st.selectbox("第2帯", val_list, index=0) # 黒
if mode == "5本帯":
    with cols[2]:
        b3 = st.selectbox("第3帯", val_list, index=0)
    with cols[3]:
        bm = st.selectbox("倍数", mul_list, index=2) # 赤
    with cols[4]:
        bt = st.selectbox("許容差", tol_list, index=4) # 金
else:
    b3 = None
    with cols[2]:
        bm = st.selectbox("倍数", mul_list, index=2) # 赤
    with cols[3]:
        bt = st.selectbox("許容差", tol_list, index=4) # 金

# --- カラー表示用HTML ---
def get_band_html(color_name):
    return f'<div class="band" style="background-color: {colors[color_name]["hex"]};"></div>'

resistor_html = f'<div class="resistor-body">'
resistor_html += get_band_html(b1) + get_band_html(b2)
if b3: resistor_html += get_band_html(b3)
resistor_html += get_band_html(bm)
resistor_html += '<div style="width: 20px;"></div>' # 許容差の前の隙間
resistor_html += get_band_html(bt)
resistor_html += '</div>'

st.markdown(resistor_html, unsafe_allow_html=True)

# --- 計算ロジック ---
if mode == "4本帯":
    base_val = colors[b1]["val"] * 10 + colors[b2]["val"]
else:
    base_val = colors[b1]["val"] * 100 + colors[b2]["val"] * 10 + colors[b3]["val"]

ohm_val = base_val * colors[bm]["mul"]
tolerance = colors[bt]["tol"]

# 単位変換
if ohm_val >= 1000000:
    display_val = f"{ohm_val / 1000000:,.2f} MΩ"
elif ohm_val >= 1000:
    display_val = f"{ohm_val / 1000:,.2f} kΩ"
else:
    display_val = f"{ohm_val:,.1f} Ω"

# --- 結果表示 ---
st.markdown('<div class="result-box">', unsafe_allow_html=True)
st.subheader("📊 抵抗値")
st.metric("計算結果", display_val, f"許容差: ±{tolerance}%")
st.markdown('</div>', unsafe_allow_html=True)



# --- 画面下部中央に「戻る」ボタンを配置 ---
st.markdown("---")  # 区切り線
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # 中央の列を使用
    # 水色のアイコン（🏠）と「戻る」を表示するボタン
    if st.link_button("🏠\n\n戻る", "https://7fjndw39dicdzckugyepb2.streamlit.app/", use_container_width=True):
        pass

# ボタンの色（水色）を調整するカスタム設定
st.markdown("""
    <style>
    div.stLinkButton > a {
        background-color: #00BFFF !important; /* 水色（DeepSkyBlue） */
        color: white !important;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)


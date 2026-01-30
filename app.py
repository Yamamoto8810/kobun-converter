import html
import streamlit as st
from translator import translate, translate_reverse

# ================================
# ページ設定
# ================================
st.set_page_config(
    page_title="古文・現代文 翻訳AIアプリ",
    page_icon="📜",
    layout="centered"
)

# ================================
# UI スタイル
# ================================
st.markdown(
    """
    <style>
    .stApp { background-color: #f3f4f6; color: #111827; }
    .titlebar {
        font-size: 28px;
        font-weight: 700;
        margin: 4px 0 8px 0;
        color: #111827;
        text-align: center;
        padding: 10px 12px;
        border-radius: 12px;
        background: #f9fafb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    /* タブを2分割で入力欄と同じ幅に */
    div[data-testid="stTabs"] {
        width: 100%;
        background: #f9fafb;
        border-radius: 12px;
        padding: 6px 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 8px;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        width: 50%;
    }
    /* タブとタブパネルの文字色を黒へ */
    div[data-testid="stTabs"] button[role="tab"],
    div[data-testid="stTabs"] button[role="tab"] p,
    div[data-testid="stTabs"] div[role="tabpanel"],
    div[data-testid="stTabs"] div[role="tabpanel"] * {
        color: #111827 !important;
    }
    /* タブの中身を白いボックスとして伸縮させる */
    div[data-testid="stTabs"] div[role="tabpanel"] {
        background: #ffffff;
        border-radius: 12px;
        padding: 12px 12px 28px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        box-sizing: border-box;
    }
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-weight: 600;
    }
    div.stButton > button * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div.stButton > button span,
    div.stButton > button p,
    div.stButton > button div {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div.stButton {
        margin-top: 6px;
        margin-bottom: 6px;
    }
    div[data-testid="stTextArea"] {
        margin-bottom: 12px;
    }
    div[data-testid="stTextArea"] > div {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    textarea {
        background-color: #e5e7eb !important;
        color: #111827 !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    textarea::placeholder {
        color: #6b7280 !important;
        opacity: 1;
    }
    .result-box {
        background: #e8f5d6;
        border-radius: 10px;
        padding: 20px 18px;
        margin-top: 12px;
        width: 100%;
        box-sizing: border-box;
    }
    .result-box--error {
        background: #ffe4e6;
    }
    .result-box--warn {
        background: #fef3c7;
    }
    .result-box--info {
        background: #dbeafe;
    }
    .result-title {
        font-weight: 700;
        margin-bottom: 6px;
        color: #14532d;
    }
    .result-text {
        color: #111827;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }
    /* Expanderの黒化対策 */
    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] summary {
        background: #ffffff !important;
        color: #111827 !important;
        border-radius: 10px;
    }
    div[data-testid="stExpander"] summary:hover,
    div[data-testid="stExpander"] summary:focus,
    div[data-testid="stExpander"] summary:active {
        background: #ffffff !important;
        color: #111827 !important;
    }
    div[data-testid="stExpander"] div,
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] span {
        color: #111827 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================================
# タイトルバー
# ================================
st.markdown('<div class="titlebar">古文・現代文 翻訳AIアプリ</div>', unsafe_allow_html=True)

# ================================
# タブバー
# ================================
tab1, tab2 = st.tabs(["古文 → 現代文", "現代文 → 古文"])

with tab1:
    st.write("古文を入力すると、意味の近い現代文に変換します。")

    # 入力欄
    text = st.text_area(
        "古文を入力してください",
        placeholder="例：春はあけぼの",
        height=120
    )

    # 翻訳ボタン
    if st.button("翻訳する", use_container_width=True):
        if text.strip() == "":
            st.markdown(
                """
                <div class="result-box result-box--warn">
                    <div class="result-title">翻訳結果</div>
                    <div class="result-text">古文を入力してください。</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            try:
                result = translate(text)
                safe_result = html.escape(result)
                is_error_result = result.strip() == "翻訳できませんでした"
                box_class = "result-box result-box--error" if is_error_result else "result-box"
                st.markdown(
                    f"""
                    <div class=\"{box_class}\">
                        <div class=\"result-title\">翻訳結果</div>
                        <div class=\"result-text\">{safe_result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            except Exception as e:
                safe_error = html.escape("翻訳中にエラーが発生しました。")
                safe_detail = html.escape(str(e))
                st.markdown(
                    f"""
                    <div class=\"result-box result-box--error\">
                        <div class=\"result-title\">翻訳結果</div>
                        <div class=\"result-text\">{safe_error}\n{safe_detail}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

with tab2:
    st.write("現代文を入力すると、意味の近い古文に変換します。")

    modern_text = st.text_area(
        "現代文を入力してください",
        placeholder="例：春の明け方はとても美しい",
        height=120
    )

    if st.button("翻訳する", use_container_width=True, key="modern_to_kobun"):
        if modern_text.strip() == "":
            st.markdown(
                """
                <div class="result-box result-box--warn">
                    <div class="result-title">翻訳結果</div>
                    <div class="result-text">現代文を入力してください。</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            try:
                result = translate_reverse(modern_text)
                safe_result = html.escape(result)
                is_error_result = result.strip() == "翻訳できませんでした"
                box_class = "result-box result-box--error" if is_error_result else "result-box"
                st.markdown(
                    f"""
                    <div class=\"{box_class}\">
                        <div class=\"result-title\">翻訳結果</div>
                        <div class=\"result-text\">{safe_result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            except Exception as e:
                safe_error = html.escape("翻訳中にエラーが発生しました。")
                safe_detail = html.escape(str(e))
                st.markdown(
                    f"""
                    <div class=\"result-box result-box--error\">
                        <div class=\"result-title\">翻訳結果</div>
                        <div class=\"result-text\">{safe_error}\n{safe_detail}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ================================
# 補足説明
# ================================
with st.expander("このAIについて"):
    st.write("""
    - 古文と現代文の対応データをもとに学習しています  
    - 文章を文字単位の n-gram に分解し、TF-IDFで数値化しています  
    - 入力文と最も意味が近い文章を探して翻訳しています  
    """)
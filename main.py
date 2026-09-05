import pathlib
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LexiAid",
    page_icon="🦉",
    layout="wide",
)

# Streamlit-тің әдепкі padding/margin-ін алып тастап, HTML-ды толық еніне жаю
st.markdown(
    """
    <style>
        .block-container {padding: 0 !important; max-width: 100% !important;}
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

html_path = pathlib.Path(__file__).parent / "lexiaid.html"
html_content = html_path.read_text(encoding="utf-8")

components.html(html_content, height=1400, scrolling=True)

import i18n
import streamlit as st
from typing import List
from create_order_module import create_order_section
from edit_order_module import edit_order_section
from convert_sequence_module import convert_sequence_section

st.set_page_config(page_title="Factory Order ERP", layout="wide")

# simulate database
if 'orders' not in st.session_state:
    st.session_state.orders = {}
if 'lang' not in st.session_state:
    st.session_state.lang = "en"

# language options
lang_display = st.sidebar.selectbox("Language (語言)", list(i18n.LANGUAGES))
if lang_display:
    st.session_state.lang = i18n.LANGUAGES[lang_display]

st.session_state.order_classes = i18n.ORDER_CLASSES[st.session_state.lang]
st.session_state.methods = i18n.MANUFACTURE_METHODS[st.session_state.lang]

def t(key):
    return i18n.mapped(key, st.session_state.lang)

# side bar menu
menu = st.sidebar.radio("Menu", [t("menu_create"), t("menu_edit"), t("menu_convert")])

# create factory order
if menu == t("menu_create"):
    st.session_state = create_order_section(t, st.session_state)

# edit order
elif menu == t("menu_edit"):
    st.session_state = edit_order_section(t, st.session_state)

# convert to sequence
elif menu == t("menu_convert"):
    st.session_state = convert_sequence_section(t, st.session_state)

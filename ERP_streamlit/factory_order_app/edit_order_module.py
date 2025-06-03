import streamlit as st

def edit_order_section(t, session) -> dict:
    st.title(t("title_edit"))
    order_ids = list(session.orders.keys())
    if not order_ids:
        st.info(t("no_orders"))
        return session
    
    selected_order_id = st.selectbox(t("select_order"), order_ids)
    order = session.orders[selected_order_id]

    st.write(f"**{t('order_status')}**: {order['status']}")
    for i, item in enumerate(order["items"]):
        with st.expander(f"Item {i + 1} - {item['drawing_no']}"):
            engraved_text: str = f"Engraving Text [{item['id'][:4]}...]"
            item["engraving"] = st.text_input(engraved_text, item["engraving"], key=item["id"])
    
    return session

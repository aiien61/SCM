import streamlit as st

def convert_sequence_section(t, session) -> dict:
    st.title(t("title_convert"))
    order_ids = list(session.orders.keys())
    if not order_ids:
        st.info(t("no_orders"))
        return session
    
    selected_order_id = st.selectbox(t("select_order"), order_ids)
    order = session.orders[selected_order_id]

    st.write(f"**{t('order_status')}**: {order['status']}")
    for i, item in enumerate(order["items"]):
        with st.expander(f"Item {i + 1} - {item['drawing_no']}"):
            if st.button(t("convert_button"), key="convert_" + item["id"]):
                item["status"] = "Pending Sequence"
                st.success(t("success_converted"))

    if all(i["status"] == "Pending Sequence" for i in order["items"]):
        order["status"] = "Pending Sequence"

    return session

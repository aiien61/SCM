import streamlit as st
import uuid
from utils import generate_order_number

def create_order_section(t, session) -> dict:
    st.title(t("title_create"))

    with st.form("order_form"):
        st.subheader(t("basic_info"))
        order_class = st.selectbox(t("order_class"), session.order_classes)
        material_type = st.selectbox(t("material_type"), ["A", "B", "C"])
        customer_no = st.text_input(t("customer_no"))
        sales_order_no = st.text_input(t("sales_order_no"))
        customer_order_no = st.text_input(t("customer_order_no"), placeholder="")

        st.subheader(t("item_info"))
        drawing_no = st.text_input(t("drawing_no"))
        revision = st.text_input(t("revision"))
        due_date = st.date_input(t("due_date"))
        quantity = st.number_input(t("quantity"), min_value=1)
        unit = st.selectbox(t("unit"), ["pcs", "Set"])
        quantity_per_set = st.number_input(t("qty_per_set"), min_value=1) if unit == "Set" else None
        method = st.selectbox(t("method"), session.methods)

        submitted = st.form_submit_button(t("save_btn"))

        if submitted:
            order_class_index: int = session.order_classes.index(order_class)
            order_id: str = generate_order_number(order_class_index, material_type)
            session.orders[order_id] = {
                "order_id": order_id,
                "order_class": order_class,
                "material_type": material_type,
                "customer_no": customer_no,
                "sales_order_no": sales_order_no,
                "customer_order_no": customer_order_no,
                "status": "Created",
                "items": [{
                    "id": str(uuid.uuid4()),
                    "drawing_no": drawing_no,
                    "due_date": str(due_date),
                    "quantity": quantity,
                    "unit": unit,
                    "quantity_per_set": quantity_per_set,
                    "method": method,
                    "engraving": "",
                    "status": "Unconverted"
                }]
            }

            st.success(t("success_created") + order_id)
    
    return session

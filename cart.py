import streamlit as st


def init_cart():
    if "cart" not in st.session_state:
        st.session_state.cart = {}


def add_to_cart(product):
    init_cart()
    pid = str(product["id"])
    if pid in st.session_state.cart:
        st.session_state.cart[pid]["quantity"] += 1
    else:
        st.session_state.cart[pid] = {"product": product, "quantity": 1}


def remove_from_cart(product_id):
    init_cart()
    pid = str(product_id)
    if pid in st.session_state.cart:
        del st.session_state.cart[pid]


def update_quantity(product_id, quantity):
    init_cart()
    pid = str(product_id)
    if pid in st.session_state.cart:
        if quantity <= 0:
            remove_from_cart(product_id)
        else:
            st.session_state.cart[pid]["quantity"] = quantity


def get_cart_items():
    init_cart()
    return [
        {
            "product": item["product"],
            "quantity": item["quantity"],
            "subtotal": item["product"]["price"] * item["quantity"],
        }
        for item in st.session_state.cart.values()
    ]


def get_cart_count():
    init_cart()
    return sum(i["quantity"] for i in st.session_state.cart.values())


def get_cart_total():
    init_cart()
    return sum(
        i["product"]["price"] * i["quantity"]
        for i in st.session_state.cart.values()
    )


def clear_cart():
    st.session_state.cart = {}

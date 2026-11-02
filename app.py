import streamlit as st
from recommender import load_products, get_categories, filter_products
from cart import (init_cart, add_to_cart, remove_from_cart,
                  update_quantity, get_cart_items, get_cart_count,
                  get_cart_total, clear_cart)
from review_summarizer import analyze_reviews
from chatbot import ProfessionalChatbot

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CartScout",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ──────────────────────────────────────────────────────────────
init_cart()
if "page" not in st.session_state:
    st.session_state.page = "home"
if "cart_open" not in st.session_state:
    st.session_state.cart_open = False
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --crimson:       #8B0000;
    --crimson-light: #A50000;
    --crimson-deep:  #5C0000;
    --crimson-glow:  #C0392B;
    --bg-dark:       #0F0808;
    --bg-card:       #1A0A0A;
    --bg-card2:      #220D0D;
    --white:         #FAF5F5;
    --white-dim:     #D4C8C8;
    --gold:          #D4AF37;
    --green:         #2ECC71;
    --text-muted:    #9E7B7B;
    --border:        rgba(139,0,0,0.35);
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--white); }

.stApp {
    background: var(--bg-dark);
    background-image:
        radial-gradient(ellipse at 10% 0%, rgba(139,0,0,0.18) 0%, transparent 60%),
        radial-gradient(ellipse at 90% 100%, rgba(92,0,0,0.12) 0%, transparent 60%);
    background-attachment: fixed;
}

/* Hide ALL streamlit chrome */
#MainMenu, footer, header,
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stDecoration"],
[data-testid="stHeader"],
.stDeployButton { display: none !important; }

.block-container { padding: 0 2rem 3rem 2rem !important; max-width: 100% !important; }

/* ── TOP NAVBAR ── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 0 0.9rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
    gap: 1rem;
}
.navbar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 900;
    color: var(--white);
    white-space: nowrap;
    letter-spacing: 0.02em;
    flex-shrink: 0;
}
.navbar-logo span { color: var(--crimson-glow); }

/* ── CONTROL BAR ── */
.control-bar {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-bottom: 1.4rem;
    padding: 1rem 1.2rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
}

/* Search & filter inputs */
[data-testid="stTextInput"] input {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 0.8rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--crimson-glow) !important;
    box-shadow: 0 0 0 2px rgba(192,57,43,0.2) !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--text-muted) !important; }
[data-testid="stTextInput"] label { color: var(--white-dim) !important; font-size: 0.75rem !important; margin-bottom: 0.25rem !important; }

[data-testid="stSelectbox"] label { color: var(--white-dim) !important; font-size: 0.75rem !important; margin-bottom: 0.25rem !important; }
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
    font-size: 0.85rem !important;
}
[data-testid="stSelectbox"] svg { fill: var(--text-muted) !important; }

[data-testid="stSlider"] label { color: var(--white-dim) !important; font-size: 0.75rem !important; }
[data-testid="stSlider"] [data-testid="stTickBar"] { display: none; }
.stSlider > div > div > div > div { background: var(--crimson) !important; }

/* ── ALL BUTTONS ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--crimson) 0%, var(--crimson-deep) 100%) !important;
    color: var(--white) !important;
    border: 1px solid rgba(139,0,0,0.6) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--crimson-glow) 0%, var(--crimson) 100%) !important;
    border-color: var(--crimson-glow) !important;
    box-shadow: 0 4px 15px rgba(139,0,0,0.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:disabled {
    opacity: 0.45 !important;
    cursor: not-allowed !important;
    transform: none !important;
}

/* Nav buttons - make them look different */
.nav-btn .stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 0.9rem !important;
}
.nav-btn .stButton > button:hover {
    background: rgba(139,0,0,0.2) !important;
    border-color: var(--crimson-glow) !important;
    box-shadow: none !important;
}

/* ── CART PILL (top right) ── */
.cart-pill {
    background: linear-gradient(135deg, var(--crimson), var(--crimson-deep));
    border: 1px solid var(--crimson-glow);
    border-radius: 24px;
    padding: 0.45rem 1rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    white-space: nowrap;
    cursor: pointer;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--white);
    box-shadow: 0 2px 10px rgba(139,0,0,0.35);
}
.cart-pill-total { color: var(--gold); font-size: 0.82rem; }

/* ── PRODUCT CARD ── */
.product-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    transition: all 0.25s ease;
    margin-bottom: 0.5rem;
}
.product-card:hover {
    border-color: var(--crimson-glow);
    box-shadow: 0 8px 30px rgba(139,0,0,0.25);
    transform: translateY(-3px);
}
.product-img-wrapper {
    width: 100%;
    height: 185px;
    overflow: hidden;
    background: var(--bg-card2);
}
.product-img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
    display: block;
}
.product-card:hover .product-img-wrapper img { transform: scale(1.04); }
.product-body { padding: 0.9rem; }
.product-name { font-size: 0.88rem; font-weight: 600; color: var(--white); line-height: 1.35; margin-bottom: 0.3rem; }
.product-brand { font-size: 0.7rem; color: var(--crimson-glow); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.4rem; }
.badge-row { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-bottom: 0.45rem; }
.badge { font-size: 0.62rem; padding: 0.14rem 0.5rem; border-radius: 20px; font-weight: 500; }
.badge-category { background: rgba(139,0,0,0.25); border: 1px solid rgba(139,0,0,0.4); color: #FF8F8F; }
.badge-rating   { background: rgba(212,175,55,0.18); border: 1px solid rgba(212,175,55,0.4); color: var(--gold); }
.badge-stock-y  { background: rgba(46,204,113,0.15); border: 1px solid rgba(46,204,113,0.35); color: #7DCEA0; }
.badge-stock-n  { background: rgba(231,76,60,0.15);  border: 1px solid rgba(231,76,60,0.35);  color: #F1948A; }
.tag-chip { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: var(--white-dim); font-size: 0.6rem; padding: 0.1rem 0.4rem; border-radius: 20px; }
.price-row { display: flex; align-items: center; justify-content: space-between; margin: 0.5rem 0 0.6rem 0; }
.product-price { font-family: 'Playfair Display', serif; font-size: 1.25rem; font-weight: 700; color: var(--white); }
.review-count  { font-size: 0.68rem; color: var(--text-muted); }

/* ── RESULTS BAR ── */
.results-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}
.results-title { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 900; color: var(--white); }
.results-count {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.25rem 0.85rem;
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* ── REVIEW ── */
.review-summary {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.85rem;
}
.verdict-label { font-size: 0.82rem; font-weight: 600; margin-bottom: 0.5rem; }
.pros-cons-title { font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem; }
.pro-item { font-size: 0.76rem; color: #7DCEA0; padding: 0.1rem 0; }
.con-item { font-size: 0.76rem; color: #F1948A; padding: 0.1rem 0; }

/* ── CART PAGE ── */
.cart-header { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 900; color: var(--white); margin-bottom: 1.2rem; padding-bottom: 0.8rem; border-bottom: 1px solid var(--border); }
.cart-total-box {
    background: linear-gradient(135deg, var(--crimson-deep) 0%, #0F0404 100%);
    border: 1px solid var(--crimson);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1.2rem;
}
.cart-total-label { font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); }
.cart-total-amount { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: var(--gold); }

/* ── ABOUT ── */
.about-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 2rem; max-width: 700px; margin: 0 auto; }
.about-title { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 900; color: var(--white); margin-bottom: 0.4rem; }
.about-tagline { font-size: 1rem; color: var(--crimson-glow); margin-bottom: 1.4rem; }
.about-body { font-size: 0.88rem; color: var(--white-dim); line-height: 1.75; }
.feature-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; margin-top: 1.2rem; }
.feature-item { background: var(--bg-card2); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1rem; font-size: 0.82rem; color: var(--white-dim); }

/* ── EXPANDER ── */
[data-testid="stExpander"] { background: transparent !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
[data-testid="stExpander"] summary { color: var(--white-dim) !important; font-size: 0.78rem !important; }
[data-testid="stExpander"] > div > div { background: var(--bg-card2) !important; }

/* ── NUMBER INPUT ── */
[data-testid="stNumberInput"] input { background: var(--bg-card2) !important; border: 1px solid var(--border) !important; color: var(--white) !important; border-radius: 6px !important; }
[data-testid="stNumberInput"] label { color: var(--white-dim) !important; font-size: 0.75rem !important; }

hr { border-color: var(--border) !important; }

.empty-state { text-align: center; padding: 4rem 2rem; color: var(--text-muted); }
.empty-state-icon { font-size: 3.5rem; margin-bottom: 1rem; }
.empty-state-title { font-family: 'Playfair Display', serif; font-size: 1.5rem; color: var(--white-dim); }
.empty-state-sub { font-size: 0.85rem; margin-top: 0.4rem; }

/* success toast */
.stSuccess { background: rgba(46,204,113,0.1) !important; border: 1px solid rgba(46,204,113,0.3) !important; color: #7DCEA0 !important; border-radius: 8px !important; }

/* ── CART DROPDOWN PANEL ── */
.cart-dropdown {
    background: #1A0A0A;
    border: 1px solid rgba(139,0,0,0.55);
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 16px 48px rgba(0,0,0,0.6), 0 0 0 1px rgba(139,0,0,0.2);
    margin-top: 0.3rem;
}
.cd-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #FAF5F5;
    margin-bottom: 0.85rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(139,0,0,0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.cd-header-total { font-size: 0.9rem; color: #D4AF37; font-family: 'DM Sans', sans-serif; font-weight: 600; }
.cd-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(139,0,0,0.15);
    gap: 0.5rem;
}
.cd-item-info { flex: 1; min-width: 0; }
.cd-item-name { font-size: 0.82rem; font-weight: 600; color: #FAF5F5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cd-item-brand { font-size: 0.67rem; color: #C0392B; text-transform: uppercase; letter-spacing: 0.08em; }
.cd-item-qty { font-size: 0.72rem; color: #9E7B7B; margin-top: 0.1rem; }
.cd-item-price { font-size: 0.88rem; font-weight: 600; color: #D4AF37; white-space: nowrap; flex-shrink: 0; }
.cd-empty { text-align: center; padding: 1.5rem 0; color: #9E7B7B; font-size: 0.85rem; }
.cd-footer { margin-top: 0.85rem; padding-top: 0.75rem; border-top: 1px solid rgba(139,0,0,0.25); display: flex; justify-content: space-between; align-items: center; }
.cd-footer-total-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.12em; color: #9E7B7B; }
.cd-footer-total-amt { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 700; color: #D4AF37; }
</style>
""", unsafe_allow_html=True)

# # ── Load data ──────────────────────────────────────────────────────────────────
# @st.cache_data
# def get_products():
#     return load_products()

# products   = get_products()
# categories = ["All"] + get_categories(products)

# ============================================================================
# LOAD DATA & CHATBOT
# ============================================================================

# 1. Products Load karne ka function (Optimized)
@st.cache_data
def get_products():
    # load_products() wahi function hai jo aapka json read karta hai
    return load_products()

# 2. Chatbot Initialize karne ka function (Resource optimized)
@st.cache_resource
def get_chatbot_instance():
    # Hum get_products() ka result pass kar rahay hain
    return ProfessionalChatbot(get_products())

# 3. Categories nikalne ka function
@st.cache_data
def get_all_categories():
    data = get_products()
    # Unique categories nikal kar sort karna
    cats = sorted(list(set([p['category'] for p in data])))
    return ["All"] + cats

# --- Implementation ---

# Inko functions ke bahar variable mein store karein
products = get_products()
chatbot = get_chatbot_instance()
categories = get_all_categories()


# ── Image maps ─────────────────────────────────────────────────────────────────
IMAGES = {
    1:  "https://images.unsplash.com/photo-1606741965326-cb990ae01bb2?w=400&h=260&fit=crop",
    2:  "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=260&fit=crop",
    3:  "https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?w=400&h=260&fit=crop",
    4:  "https://images.unsplash.com/photo-1551816230-ef5deaed4a26?w=400&h=260&fit=crop",
    5:  "https://images.unsplash.com/photo-1544244015-0df4cec9d125?w=400&h=260&fit=crop",
    6:  "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=260&fit=crop",
    7:  "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=260&fit=crop",
    8:  "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=260&fit=crop",
    9:  "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=400&h=260&fit=crop",
    10: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=260&fit=crop",
    11: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=260&fit=crop",
    12: "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400&h=260&fit=crop",
    13: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=260&fit=crop",
    14: "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=260&fit=crop",
    15: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=260&fit=crop",
    16: "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&h=260&fit=crop",
}
BRAND_IMAGES = {
    "Apple":   "https://images.unsplash.com/photo-1491933382434-500287f9b54b?w=400&h=260&fit=crop",
    "Samsung": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=260&fit=crop",
    "Sony":    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=260&fit=crop",
    "Xiaomi":  "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=260&fit=crop",
    "Nike":    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=260&fit=crop",
    "Adidas":  "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&h=260&fit=crop",
    "Zara":    "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=260&fit=crop",
    "Philips": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400&h=260&fit=crop",
    "IKEA":    "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=260&fit=crop",
    "Generic": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=260&fit=crop",
}
CAT_IMAGES = {
    "Electronics":   "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=260&fit=crop",
    "Fashion":       "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=400&h=260&fit=crop",
    "Fitness":       "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=260&fit=crop",
    "Home":          "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=260&fit=crop",
    "Personal Care": "https://images.unsplash.com/photo-1526045612212-70caf35c14df?w=400&h=260&fit=crop",
}
CAT_EMOJI = {"Electronics":"📱","Fashion":"👗","Fitness":"🏋️","Home":"🏠","Personal Care":"🧴"}

def get_image(p):
    return IMAGES.get(p["id"]) or BRAND_IMAGES.get(p.get("brand","")) or CAT_IMAGES.get(p.get("category",""),"")

# ── TOP NAVBAR ─────────────────────────────────────────────────────────────────
cnt   = get_cart_count()
total = get_cart_total()

nav_l, nav_logo, nav_r = st.columns([1, 3, 2])
with nav_logo:
    st.markdown('<div class="navbar-logo">Cart<span>Scout</span> <span style="font-size:0.95rem;color:var(--text-muted);font-family:\'DM Sans\',sans-serif;font-weight:300">— AI Shopping</span></div>', unsafe_allow_html=True)
with nav_r:
    # 1. Yahan 4 ki jagah 5 values dein (e.g., [1, 1, 1, 2, 3])
    ncols = st.columns([1.2, 1.2, 1.2, 1.8, 3.0])
    
    with ncols[0]:
        if st.button("🏠 Home", key="nav_home"):
            st.session_state.page = "home"; st.rerun()
            
    with ncols[1]:
        if st.button("ℹ️ About", key="nav_about"):
            st.session_state.page = "about"; st.rerun()
            
    with ncols[2]:
        if st.button("🤖 Chat", key="nav_chat"):
            st.session_state.show_chat = not st.session_state.show_chat
            st.rerun()
            
    with ncols[3]:
        # View Cart button
        if st.button("🛒 View Cart", key="nav_cart_page"):
            st.session_state.page = "cart"; st.rerun()
            
    with ncols[4]: # AB YEH ERROR NAHI DEGA
        pill_label = f"🛒  {cnt} item{'s' if cnt!=1 else ''}  ·  ${total:,.2f}"
        if st.button(pill_label, key="cart_pill_btn"):
            st.session_state.cart_open = not st.session_state.cart_open
            st.rerun()

st.markdown("<hr style='margin:0 0 1.2rem 0;border-color:rgba(139,0,0,0.3)'>", unsafe_allow_html=True)
# ============================================================================
# CHAT PANEL

# ============================================================================

if st.session_state.show_chat:
    st.markdown("### 💬 AI Chat")
    
    for msg in chatbot.conversation:
        if msg["role"] == "user":
            st.markdown(f"*👤 You:* {msg['content']}")
        else:
            st.markdown(f"*🤖 Bot:*\n{msg['content']}")
    
    user_input = st.text_input("Ask...", placeholder="e.g., iPhone 15 Pro", key="chat_input")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("Send", use_container_width=True):
            if user_input:
                with st.spinner("🤖..."):
                    response = chatbot.chat(user_input)
                st.rerun()
    with col3:
        if st.button("Close", use_container_width=True):
            st.session_state.show_chat = False
            st.rerun()
    
    if st.button("Clear", use_container_width=True):
        chatbot.reset()
        st.rerun()
    
    st.markdown("---")
# ============================================================================


# ── INLINE CART DROPDOWN ──────────────────────────────────────────────────────
if st.session_state.cart_open:
    cart_items = get_cart_items()
    grand      = get_cart_total()

    with st.container():
        # Build items HTML
        if not cart_items:
            items_html = '<div class="cd-empty">🛒 Your cart is empty</div>'
        else:
            rows = ""
            for item in cart_items:
                p = item["product"]
                rows += f"""
                <div class="cd-item">
                    <div class="cd-item-info">
                        <div class="cd-item-name">{p['name']}</div>
                        <div class="cd-item-brand">{p['brand']}</div>
                        <div class="cd-item-qty">Qty: {item['quantity']}</div>
                    </div>
                    <div class="cd-item-price">${item['subtotal']:,.2f}</div>
                </div>"""
            items_html = rows

        footer_html = "" if not cart_items else f"""
            <div class="cd-footer">
                <div>
                    <div class="cd-footer-total-label">Order Total</div>
                    <div class="cd-footer-total-amt">${grand:,.2f}</div>
                </div>
            </div>"""

        st.markdown(f"""
            <div class="cart-dropdown">
                <div class="cd-header">
                    <span>Your Cart</span>
                    <span class="cd-header-total">{cnt} item{'s' if cnt!=1 else ''}</span>
                </div>
                {items_html}
                {footer_html}
            </div>
        """, unsafe_allow_html=True)

        # Remove buttons for each item + action row
        if cart_items:
            st.markdown("<div style='margin-top:0.6rem'></div>", unsafe_allow_html=True)
            for item in cart_items:
                p   = item["product"]
                pid = p["id"]
                rc1, rc2, rc3 = st.columns([4, 1, 1])
                with rc1:
                    st.markdown(
                        f"<div style='font-size:0.8rem;color:#D4C8C8;padding:0.35rem 0'>"
                        f"{p['name']} <span style='color:#9E7B7B'>×{item['quantity']}</span></div>",
                        unsafe_allow_html=True)
                with rc2:
                    # quantity nudge
                    if st.button("＋", key=f"cd_plus_{pid}"):
                        update_quantity(pid, item["quantity"] + 1); st.rerun()
                with rc3:
                    if st.button("✕", key=f"cd_rm_{pid}"):
                        remove_from_cart(pid); st.rerun()

            st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
            btn_c1, btn_c2, btn_c3 = st.columns([2, 2, 1])
            with btn_c1:
                if st.button("✅ Checkout", key="cd_checkout"):
                    clear_cart()
                    st.session_state.cart_open = False
                    st.success("🎉 Order placed! Thank you for shopping with CartScout.")
                    st.balloons()
                    st.rerun()
            with btn_c2:
                if st.button("📄 Full Cart View", key="cd_fullcart"):
                    st.session_state.cart_open = False
                    st.session_state.page = "cart"
                    st.rerun()
            with btn_c3:
                if st.button("✖ Close", key="cd_close"):
                    st.session_state.cart_open = False; st.rerun()
        else:
            if st.button("✖ Close", key="cd_close_empty"):
                st.session_state.cart_open = False; st.rerun()

    st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

# ── HOME ───────────────────────────────────────────────────────────────────────
if st.session_state.page == "home":

    # ── CONTROL BAR ──
    with st.container():
        c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
        with c1:
            search_query = st.text_input("🔍 Search Products",
                placeholder="Search by name, brand, tag…", key="search_input")
        with c2:
            selected_category = st.selectbox("📂 Category", categories, key="cat_filter")
        with c3:
            price_max = st.selectbox("💰 Max Price",
                ["Any", "$50", "$100", "$250", "$500", "$1000", "$2000", "$5000"],
                key="price_filter")
        with c4:
            min_rating = st.selectbox("⭐ Min Rating",
                ["Any", "3.0+", "3.5+", "4.0+", "4.5+"],
                key="rating_filter")

    # Parse filters
    pmax = {"Any":5000,"$50":50,"$100":100,"$250":250,
            "$500":500,"$1000":1000,"$2000":2000,"$5000":5000}.get(price_max, 5000)
    rmin = {"Any":0.0,"3.0+":3.0,"3.5+":3.5,"4.0+":4.0,"4.5+":4.5}.get(min_rating, 0.0)

    filtered = filter_products(
        products,
        search_query=search_query,
        category=selected_category,
        min_price=0,
        max_price=pmax,
        min_rating=rmin,
    )

    st.markdown(f"""
        <div class="results-bar">
            <div class="results-title">Discover Products</div>
            <div class="results-count">{len(filtered)} result{"s" if len(filtered)!=1 else ""}</div>
        </div>
    """, unsafe_allow_html=True)

    if not filtered:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-title">No products found</div>
                <div class="empty-state-sub">Try a different search or adjust filters</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        COLS = 3
        for row_start in range(0, len(filtered), COLS):
            row  = filtered[row_start:row_start + COLS]
            cols = st.columns(COLS)
            for ci, product in enumerate(row):
                with cols[ci]:
                    pid       = product["id"]
                    img_url   = get_image(product)
                    emoji     = CAT_EMOJI.get(product["category"], "🛍️")
                    in_stock  = product.get("in_stock", True)
                    rev_count = product.get("review_count", 0)
                    tags_html = "".join(f'<span class="tag-chip">{t}</span>'
                                        for t in product.get("tags",[])[:3])
                    stock_cls = "badge-stock-y" if in_stock else "badge-stock-n"
                    stock_txt = "✓ In Stock"   if in_stock else "✗ Out of Stock"

                    st.markdown(f"""
                        <div class="product-card">
                            <div class="product-img-wrapper">
                                <img src="{img_url}" alt="{product['name']}" loading="lazy">
                            </div>
                            <div class="product-body">
                                <div class="product-brand">{product['brand']}</div>
                                <div class="product-name">{product['name']}</div>
                                <div class="badge-row">
                                    <span class="badge badge-category">{emoji} {product['category']}</span>
                                    <span class="badge badge-rating">★ {product['rating']}</span>
                                    <span class="badge {stock_cls}">{stock_txt}</span>
                                </div>
                                <div class="badge-row">{tags_html}</div>
                                <div class="price-row">
                                    <div class="product-price">${product['price']:,.2f}</div>
                                    <div class="review-count">({rev_count:,} reviews)</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # ── ADD TO CART BUTTON ──
                    if in_stock:
                        if st.button("🛒 Add to Cart", key=f"add_{pid}"):
                            add_to_cart(product)
                            st.toast(f"✅ {product['name']} added to cart!", icon="🛒")
                            st.rerun()
                    else:
                        st.button("⛔ Out of Stock", key=f"oos_{pid}", disabled=True)

                    # Review expander
                    with st.expander("📋 Review Summary"):
                        summary   = analyze_reviews(product.get("reviews", []))
                        pros_html = "".join(f'<div class="pro-item">+ {p}</div>'
                                            for p in summary["pros"]) \
                                    or '<div style="color:var(--text-muted);font-size:0.76rem">—</div>'
                        cons_html = "".join(f'<div class="con-item">− {c}</div>'
                                            for c in summary["cons"]) \
                                    or '<div style="color:var(--text-muted);font-size:0.76rem">—</div>'
                        st.markdown(f"""
                            <div class="review-summary">
                                <div class="verdict-label">{summary['verdict']}</div>
                                <div class="pros-cons-title">✅ Pros</div>
                                {pros_html}
                                <div class="pros-cons-title" style="margin-top:0.5rem">❌ Cons</div>
                                {cons_html}
                                <div style="font-size:0.67rem;color:var(--text-muted);margin-top:0.45rem">
                                    Based on {summary['total']} reviews
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

# ── CART ───────────────────────────────────────────────────────────────────────
elif st.session_state.page == "cart":
    st.markdown('<div class="cart-header">🛒 Your Cart</div>', unsafe_allow_html=True)
    items = get_cart_items()

    if not items:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🛒</div>
                <div class="empty-state-title">Your cart is empty</div>
                <div class="empty-state-sub">Head back and find something you love</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🏠 Continue Shopping"):
            st.session_state.page = "home"; st.rerun()
    else:
        hcols = st.columns([4, 2, 2, 2, 1])
        for col, txt in zip(hcols, ["Product", "Unit Price", "Qty", "Subtotal", ""]):
            with col:
                st.markdown(f"<div style='font-size:0.67rem;letter-spacing:0.12em;text-transform:uppercase;"
                            f"color:var(--text-muted);padding:0.3rem 0;"
                            f"border-bottom:1px solid rgba(139,0,0,0.3)'>{txt}</div>",
                            unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:0.3rem'></div>", unsafe_allow_html=True)

        for item in items:
            p   = item["product"]
            pid = p["id"]
            c1, c2, c3, c4, c5 = st.columns([4, 2, 2, 2, 1])
            with c1:
                st.markdown(f"""
                    <div style="padding:0.45rem 0">
                        <div style="font-weight:600;font-size:0.88rem;color:#FAF5F5">{p['name']}</div>
                        <div style="font-size:0.7rem;color:#C0392B;text-transform:uppercase;letter-spacing:0.08em">{p['brand']}</div>
                        <div style="font-size:0.68rem;color:#9E7B7B;margin-top:0.15rem">
                            {CAT_EMOJI.get(p['category'],'🛍️')} {p['category']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='padding:0.7rem 0;font-size:0.88rem;color:#D4C8C8'>${p['price']:,.2f}</div>",
                            unsafe_allow_html=True)
            with c3:
                new_qty = st.number_input("qty", min_value=1, max_value=99,
                                          value=item["quantity"], key=f"qty_{pid}",
                                          label_visibility="collapsed")
                if new_qty != item["quantity"]:
                    update_quantity(pid, new_qty); st.rerun()
            with c4:
                st.markdown(f"<div style='padding:0.7rem 0;font-size:0.9rem;font-weight:600;color:#D4AF37'>${item['subtotal']:,.2f}</div>",
                            unsafe_allow_html=True)
            with c5:
                if st.button("✕", key=f"rm_{pid}"):
                    remove_from_cart(pid); st.rerun()

            st.markdown("<hr style='margin:0.2rem 0;border-color:rgba(139,0,0,0.15)'>",
                        unsafe_allow_html=True)

        grand = get_cart_total()
        st.markdown(f"""
            <div class="cart-total-box">
                <div class="cart-total-label">Order Total</div>
                <div class="cart-total-amount">${grand:,.2f}</div>
                <div style="font-size:0.72rem;color:#9E7B7B;margin-top:0.3rem">
                    {get_cart_count()} item(s) · Free shipping on orders over $50
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
        ca, cb, cc = st.columns([2, 2, 1])
        with ca:
            if st.button("✅ Proceed to Checkout", key="checkout"):
                st.success("🎉 Order placed! Thank you for shopping with CartScout.")
                clear_cart()
                st.balloons()
                st.rerun()
        with cb:
            if st.button("🏠 Continue Shopping", key="cont"):
                st.session_state.page = "home"; st.rerun()
        with cc:
            if st.button("🗑 Clear Cart", key="clr"):
                clear_cart(); st.rerun()

# ── ABOUT ──────────────────────────────────────────────────────────────────────
elif st.session_state.page == "about":
    st.markdown("""
        <div style="padding:1rem 0 2rem 0">
            <div class="about-card">
                <div class="about-title">Cart<span style="color:#C0392B">Scout</span></div>
                <div class="about-tagline">Your AI-Powered Shopping Companion</div>
                <div class="about-body">
                    CartScout helps you discover, compare, and buy from a curated catalog
                    of 100 products across Electronics, Fashion, Fitness, Home, and
                    Personal Care — with AI-summarized reviews showing real pros & cons.
                </div>
                <div class="feature-grid">
                    <div class="feature-item">🔍 Smart Search & Filters</div>
                    <div class="feature-item">🤖 AI Review Summaries</div>
                    <div class="feature-item">🛒 Easy Cart Management</div>
                    <div class="feature-item">⭐ Rating-Based Discovery</div>
                    <div class="feature-item">💰 Price Range Filtering</div>
                    <div class="feature-item">📦 100 Curated Products</div>
                </div>
                <div style="margin-top:1.4rem;font-size:0.72rem;color:#9E7B7B;text-align:center;letter-spacing:0.05em">
                    Built with Streamlit · Python · Dark Crimson Edition
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🏠 Back to Store"):
        st.session_state.page = "home"; st.rerun()

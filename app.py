import streamlit as st
import time
from persia_gram import create_persian_caption, analyze_page_stats

# --- PAGE CONFIG ---
st.set_page_config(page_title="فالو | دستیار هوشمند", page_icon="🦅", layout="wide")

# --- 1. FONT LOADING ---
st.markdown("""
    <link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.0.3/misc/Farsi-Digits/font-face.css" rel="stylesheet" type="text/css" />
""", unsafe_allow_html=True)

# --- 2. CUSTOM CSS (FINAL UI + HIDE INSTRUCTIONS) ---
st.markdown("""
    <style>
        /* 1. GLOBAL FONT & DIRECTION */
        html, body, [class*="css"], div, input, select, textarea, button, label, p, h1, h2, h3, h4, h5, h6, li {
            font-family: 'Vazirmatn', sans-serif !important;
            font-weight: 700 !important;
            direction: rtl;
        }

        /* 2. HIDE "PRESS ENTER TO APPLY" */
        div[data-testid="InputInstructions"] {
            display: none !important;
        }

        /* 3. INPUT BOX STYLING */
        div[data-baseweb="input"], 
        div[data-baseweb="base-input"], 
        div[data-baseweb="select"] > div {
            background-color: #1E1E2F !important;
            border: 2px solid #2B2D42 !important; 
            border-radius: 20px !important;
            color: white !important;
            padding: 0px !important;
            box-shadow: none !important;
            min-height: 55px !important;
            display: flex !important;
            align-items: center !important;
        }
        
        /* Dropdown specific */
        div[data-baseweb="select"] > div {
            padding-right: 10px !important;
        }

        /* Inner Transparency */
        div[data-baseweb="base-input"] {
            background-color: transparent !important;
            border: none !important;
        }

        /* Text Fix */
        input[type="text"], textarea {
            background-color: transparent !important;
            border: none !important;
            color: white !important;
            outline: none !important;
            text-align: center !important;
            font-size: 16px !important;
            line-height: normal !important;
            height: 100% !important;
        }

        /* Hide Steppers */
        [data-testid="stNumberInput"] button {
            display: none !important;
        }

        /* Focus Glow */
        div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
            border-color: #7B61FF !important;
            box-shadow: 0 0 15px rgba(123, 97, 255, 0.5) !important;
        }

        /* 4. BUTTONS & LAYOUT */
        h1, h2, h3, p, label {
            text-align: center !important;
        }

        div.stButton {
            width: 100% !important;
            display: flex;
            justify-content: center;
        }
        div.stButton > button {
            background: linear-gradient(90deg, #7B61FF 0%, #AA00FF 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 22px 0px !important;
            font-size: 24px !important;
            font-weight: 900 !important;
            width: 100% !important;
            margin-top: 25px !important;
            box-shadow: 0 10px 30px rgba(123, 97, 255, 0.3) !important;
        }
        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 15px 40px rgba(123, 97, 255, 0.5) !important;
        }

        /* 5. THE RESULT CARD FIX (Purple Info Box) */
        div[data-baseweb="notification"] {
            background-color: #1E1E2F !important;
            border: 2px solid #2B2D42 !important;
            border-right: 8px solid #7B61FF !important;
            border-radius: 25px !important;
            padding: 25px !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4) !important;
        }
        
        div[data-baseweb="notification"] * {
            color: white !important;
            text-align: right !important;
            direction: rtl !important;
        }
        
        div[data-baseweb="notification"] h1, 
        div[data-baseweb="notification"] h2, 
        div[data-baseweb="notification"] h3 {
            color: #7B61FF !important;
            margin-bottom: 10px !important;
            text-align: right !important;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: #161725 !important;
            border-left: 2px solid #2B2D42;
        }
        #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- HELPER: NUMBER CLEANER ---
def clean_number(value):
    if not value: return 0
    persian_nums = {'۰':'0', '۱':'1', '۲':'2', '۳':'3', '۴':'4', '۵':'5', '۶':'6', '۷':'7', '۸':'8', '۹':'9'}
    for p, e in persian_nums.items():
        value = value.replace(p, e)
    value = value.replace(",", "").replace(" ", "")
    try:
        return int(value)
    except:
        return 0

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🦅 هوش مصنوعی فالو")
    st.caption("نسخه: ۲.۵ (لایت)")
    st.divider()
    page = st.radio("منو:", ["دکتر پیج (آنالیز)", "کپشن‌نویس", "تنظیمات"])
    st.divider()
    st.info("💡 نکته: آمار را دقیق وارد کنید")

# --- PAGE 1: DOCTOR ---
if page == "دکتر پیج (آنالیز)":
    st.title("🏥 کلینیک تخصصی اینستاگرام")
    st.markdown("آمار پیج را وارد کنید تا **نسخه درمانی** دریافت کنید")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col2:
            niche = st.text_input("موضوع پیج:", placeholder="مثلا: فروشگاه لباس...")
            followers_str = st.text_input("تعداد فالوور:", value="1000")
        
        with col1:
            likes_str = st.text_input("میانگین لایک:", value="100")
            stories_str = st.text_input("ویو استوری:", value="300")
        
        complaint = st.text_input("مشکل اصلی شما چیست؟", placeholder="مثلا: فالوور میاد ولی خرید نمیکنه...")
        
        if st.button("شروع آنالیز و دریافت نسخه", type="primary", use_container_width=True):
            followers = clean_number(followers_str)
            likes = clean_number(likes_str)
            stories = clean_number(stories_str)

            if followers > 0:
                with st.spinner("دکتر فالو در حال بررسی..."):
                    diagnosis = analyze_page_stats(niche, followers, likes, stories, complaint)
                    time.sleep(1)
                
                # Using st.info for automatic formatting + Custom CSS for style
                st.info(diagnosis, icon="🩺")
                
            else:
                st.error("تعداد فالوور نمیتواند صفر باشد")

# --- PAGE 2: CAPTION ---
elif page == "کپشن‌نویس":
    st.title("✍️ تولید محتوای ویرال")
    
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        with col2:
            topic = st.text_input("موضوع پست:", placeholder="مثلا: تخفیف یلدا")
        with col1:
            details = st.text_area("جزئیات:", placeholder="قیمت، جنس، آدرس...")
            
        if st.button("نوشتن کپشن هوشمند", type="primary", use_container_width=True):
            with st.spinner("در حال نوشتن..."):
                caption = create_persian_caption(topic, details)
            
            st.subheader("👇 کپشن پیشنهادی شما:")
            st.code(caption, language=None)

# --- PAGE 3: SETTINGS ---
elif page == "تنظیمات":
    st.title("⚙️ وضعیت سیستم")
    st.info("✅ سرور متصل است (Gemini 2.5)")
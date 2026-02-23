import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة وإخفاء عناصر Streamlit و GitHub تماماً
st.set_page_config(page_title="نتائج جامعة ابن سينا", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .main { text-align: right; direction: rtl; font-family: 'Arial'; }
    
    .university-header {
        text-align: center;
        padding: 30px;
        border-bottom: 4px double #1e3c72;
        margin-bottom: 40px;
    }
    .university-name { color: #1e3c72; font-size: 36px; font-weight: bold; margin: 0; }
    .college-name { color: #2a5298; font-size: 30px; font-weight: bold; margin-top: 10px; }
    
    .system-title {
        text-align: center; 
        font-size: 26px; 
        color: #444; 
        font-weight: bold; 
        margin-top: 15px;
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 8px;
    }

    .stSelectbox label, .stTextInput label { font-size: 22px !important; font-weight: bold !important; }
    .stButton>button { font-size: 24px !important; height: 3em; font-weight: bold; width: 100%; }

    .student-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        padding: 35px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }
    .student-name-text { font-size: 38px !important; font-weight: bold; margin: 0; }
    .student-id-text { font-size: 24px !important; opacity: 0.9; margin-top: 10px; }
    
    .grade-box {
        background-color: #ffffff;
        border: 2px solid #dee2e6;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    .subject-name { color: #555; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
    .subject-grade { color: #1e3c72; font-size: 32px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if not os.path.exists("data"): 
    os.makedirs("data")

# --- بوابة الإدارة ---
with st.sidebar:
    st.markdown("### 🔐 الإدارة")
    admin_pass = st.text_input("كلمة مرور الإدارة:", type="password")
    
    if admin_pass == "secure_admin_2024": 
        st.success("تم تسجيل الدخول")
        stage = st.selectbox("تحديث نتائج:", ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
        up_file = st.file_uploader(f"ارفع ملف Excel لـ {stage}:", type=["xlsx"])
        
        if up_file:
            file_path = os.path.join("data", f"{stage}.xlsx")
            with open(file_path, "wb") as f:
                f.write(up_file.getbuffer())
            st.sidebar.success(f"تم تحديث بيانات {stage}")

# --- الواجهة الرئيسية ---
st.markdown("""
    <div class="university-header">
        <h1 class="university-name">جامعة ابن سينا للعلوم الطبية والصيدلانية</h1>
        <h2 class="college-name">كلية طب الاسنان</h2>
        <div class="system-title">نظام الاستعلام عن النتائج النهائية</div>
    </div>
""", unsafe_allow_html=True)

st.write("---")

col1, col2 = st.columns(2)
with col1:
    st_stage = st.selectbox("اختر المرحلة الدراسية:", ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
with col2:
    st_id = st.text_input("أدخل الرقم الأكاديمي:", placeholder="اكتب رقمك هنا")

if st.button("🔍 عـرض النتيجة الآن"):
    if not st_id:
        st.warning("⚠️ يرجى إدخال الرقم الأكاديمي أولاً")
    else:
        file_path = os.path.join("data", f"{st_stage}.xlsx")
        
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
                df['الرقم الأكاديمي'] = df['الرقم الأكاديمي'].astype(str).str.strip()
                result = df[df['الرقم الأكاديمي'] == st_id.strip()]

                if not result.empty:
                    student = result.iloc[0]
                    
                    st.markdown(f"""
                        <div class='student-header'>
                            <p class='student-name-text'>{student['اسم الطالب']}</p>
                            <p class='student-id-text'>الرقم الأكاديمي: {student['الرقم الأكاديمي']} | {st_stage}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<h2 style='text-align: right; color: #1e3c72;'>📋 تفاصيل الدرجات:</h2>", unsafe_allow_html=True)
                    
                    cols_to_drop = [c for c in ['الرقم الأكاديمي', 'اسم الطالب'] if c in df.columns]
                    grades = student.drop(labels=cols_to_drop)

                    cols = st.columns(3)
                    for idx, (subject, grade) in enumerate(grades.items()):
                        with cols[idx % 3]:
                            st.markdown(f"""
                                <div class="grade-box">
                                    <div class="subject-name">{subject}</div>
                                    <div class="subject-grade">{grade}</div>
                                </div>
                                <br>
                            """, unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.error("❌ الرقم الأكاديمي غير موجود.")
            except Exception as e:
                st.error("⚠️ خطأ في قراءة ملف الإكسل.")
        else:
            st.info(f"ℹ️ لم يتم رفع نتائج {st_stage} بعد.")

st.markdown("<br><br><hr><p style='text-align: center; font-size: 16px; color: #777; font-weight: bold;'>قسم تكنولوجيا المعلومات - جامعة ابن سينا</p>", unsafe_allow_html=True)

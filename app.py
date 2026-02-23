import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة وإخفاء عناصر Streamlit و GitHub تماماً
st.set_page_config(page_title="نتائج جامعة ابن سينا", layout="centered")

st.markdown("""
    <style>
    /* إخفاء القائمة العلوية وأيقونة GitHub وعناصر Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* تنسيق الواجهة العامة */
    .main { text-align: right; direction: rtl; font-family: 'Arial'; }
    
    /* تصميم رأس الصفحة (اسم الجامعة) */
    .university-header {
        text-align: center;
        padding: 20px;
        border-bottom: 3px double #1e3c72;
        margin-bottom: 30px;
    }
    .university-name { color: #1e3c72; font-size: 26px; font-weight: bold; margin: 0; }
    .college-name { color: #2a5298; font-size: 22px; font-weight: normal; margin-top: 5px; }
    
    /* تصميم بطاقة معلومات الطالب */
    .student-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* تصميم مربعات الدرجات */
    .grade-box {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .subject-name { color: #555; font-size: 13px; font-weight: bold; margin-bottom: 5px; }
    .subject-grade { color: #1e3c72; font-size: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# التأكد من وجود مجلد البيانات
if not os.path.exists("data"): 
    os.makedirs("data")

# --- بوابة الإدارة (Sidebar) ---
with st.sidebar:
    st.markdown("### 🔐 الإدارة")
    admin_pass = st.text_input("كلمة مرور الإدارة:", type="password")
    
    if admin_pass == "secure_admin_2024": 
        st.success("تم تسجيل الدخول")
        stage = st.selectbox("المرحلة:", ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
        up_file = st.file_uploader("رفع ملف Excel:", type=["xlsx"])
        
        if up_file:
            file_path = os.path.join("data", f"{stage}.xlsx")
            with open(file_path, "wb") as f:
                f.write(up_file.getbuffer())
            st.sidebar.success(f"تم تحديث بيانات {stage}")

# --- الواجهة الرئيسية (اسم الجامعة والكلية) ---
st.markdown("""
    <div class="university-header">
        <h1 class="university-name">جامعة ابن سينا للعلوم الطبية والصيدلانية</h1>
        <h2 class="college-name">كلية طب الاسنان</h2>
    </div>
    <p style='text-align: center; font-size: 18px; color: #444; font-weight: bold; margin-top: 10px;'>نظام الاستعلام عن النتائج النهائية</p>
""", unsafe_allow_html=True)

st.write("---")

col1, col2 = st.columns(2)
with col1:
    st_stage = st.selectbox("المرحلة الدراسية:", ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
with col2:
    st_id = st.text_input("الرقم الأكاديمي:", placeholder="أدخل رقمك هنا")

if st.button("🔍 عرض النتيجة"):
    if not st_id:
        st.warning("يرجى إدخال الرقم الأكاديمي")
    else:
        file_path = os.path.join("data", f"{st_stage}.xlsx")
        
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
                df['الرقم الأكاديمي'] = df['الرقم الأكاديمي'].astype(str).str.strip()
                result = df[df['الرقم الأكاديمي'] == st_id.strip()]

                if not result.empty:
                    student = result.iloc[0]
                    
                    # عرض معلومات الطالب
                    st.markdown(f"""
                        <div class='student-header'>
                            <h2 style='margin:0;'>{student['اسم الطالب']}</h2>
                            <p style='margin:5px 0 0 0;'>الرقم الأكاديمي: {student['الرقم الأكاديمي']} | {st_stage}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("### 📋 تفاصيل المواد والدرجات:")
                    
                    # استخراج المواد
                    cols_to_drop = [c for c in ['الرقم الأكاديمي', 'اسم الطالب'] if c in df.columns]
                    grades = student.drop(labels=cols_to_drop)

                    # عرض الدرجات في شبكة منظمة
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
                    st.error("❌ الرقم الأكاديمي غير صحيح أو غير متوفر حالياً.")
            except Exception as e:
                st.error("⚠️ حدث خطأ في معالجة البيانات، يرجى مراجعة الإدارة.")
        else:
            st.info(f"ℹ️ لم يتم رفع نتائج {st_stage} بعد.")

st.markdown("<br><hr><p style='text-align: center; font-size: 13px; color: #777;'>قسم تكنولوجيا المعلومات - جامعة ابن سينا</p>", unsafe_allow_html=True)

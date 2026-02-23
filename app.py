import streamlit as st
import pandas as pd
import os

# 1. إعدادات الصفحة وإخفاء عناصر Streamlit و GitHub
st.set_page_config(page_title="جامعة ابن سينا للعلوم الطبية والصيدلانية/ كلية طب الاسنان/البوابة الرسمية للنتائج", layout="centered")

st.markdown("""
    <style>
    /* إخفاء القائمة العلوية وأيقونة GitHub */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* تنسيق الواجهة */
    .main { text-align: right; direction: rtl; font-family: 'Arial'; }
    .student-header {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .grade-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .subject-name { color: #444; font-size: 14px; font-weight: bold; margin-bottom: 8px; }
    .subject-grade { color: #1a5f7a; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# التأكد من وجود مجلد البيانات
if not os.path.exists("data"): 
    os.makedirs("data")

# --- بوابة الإدارة (محمية ومخفية في القائمة الجانبية) ---
with st.sidebar:
    st.markdown("### 🔐 منطقة المسؤولين")
    admin_pass = st.text_input("كلمة مرور الإدارة:", type="password")
    
    # تغيير كلمة المرور هنا لزيادة الأمان
    if admin_pass == "secure_admin_2024": 
        st.success("صلاحية الوصول مفعّلة")
        stage = st.selectbox("تحديث نتائج:", ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
        up_file = st.file_uploader("رفع ملف النتائج الجديد:", type=["xlsx"])
        
        if up_file:
            file_path = os.path.join("data", f"{stage}.xlsx")
            with open(file_path, "wb") as f:
                f.write(up_file.getbuffer())
            st.sidebar.success(f"تم تحديث بيانات {stage} بأمان")
    elif admin_pass != "":
        st.error("كلمة المرور غير صحيحة")

# --- الواجهة الرئيسية للطالب ---
st.markdown("<h1 style='text-align: center; color: #1e3c72;'>🎓 بوابة استعلام النتائج الرسمية</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #666;'>نظام آمن لاستخراج الدرجات الأكاديمية</p>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)
with col1:
    st_stage = st.selectbox("المرحلة الدراسية:", ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
with col2:
    st_id = st.text_input("أدخل الرقم الأكاديمي:", placeholder="مثال: 2024100")

if st.button("🔍 عرض النتيجة الآمن"):
    if not st_id:
        st.warning("يرجى إدخال الرقم الأكاديمي")
    else:
        file_path = os.path.join("data", f"{st_stage}.xlsx")
        
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path, engine='openpyxl')
                # تنظيف البيانات لضمان دقة البحث
                df['الرقم الأكاديمي'] = df['الرقم الأكاديمي'].astype(str).str.strip()
                result = df[df['الرقم الأكاديمي'] == st_id.strip()]

                if not result.empty:
                    student = result.iloc[0]
                    
                    # عرض الهوية الأكاديمية
                    st.markdown(f"""
                        <div class='student-header'>
                            <h2 style='margin:0;'>{student['اسم الطالب']}</h2>
                            <p style='margin:10px 0 0 0;'>الرقم الأكاديمي: {student['الرقم الأكاديمي']} | {st_stage}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("### 📋 كشف الدرجات:")
                    
                    # استخراج المواد الدراسية فقط
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
                    st.error("❌ الرقم الأكاديمي غير موجود في سجلات هذه المرحلة.")
            except Exception as e:
                st.error("⚠️ خطأ تقني في معالجة الملف. يرجى التواصل مع الدعم الفني.")
        else:
            st.info("ℹ️ لم يتم رفع نتائج هذه المرحلة في النظام بعد.")

st.markdown("<br><hr><p style='text-align: center; font-size: 12px; color: #999;'>نظام مشفر ومحمي - كافة الحقوق محفوظة © 2024</p>", unsafe_allow_html=True)


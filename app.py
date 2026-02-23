import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="نظام النتائج الأكاديمي", layout="centered")

# تنسيق الواجهة (CSS) لدعم اللغة العربية وتحسين المظهر
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div[data-baseweb="select"] { direction: rtl; }
    .stTextInput > div > div > input { text-align: center; font-size: 18px; direction: rtl; }
    .result-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        border-right: 8px solid #28a745;
        margin-top: 20px;
        text-align: right;
    }
    th { background-color: #f8f9fa !important; text-align: right !important; font-weight: bold; }
    td { text-align: right !important; }
    .stTable { direction: rtl !important; }
    </style>
    """, unsafe_allow_html=True)

# إنشاء مجلد تخزين الملفات إذا لم يكن موجوداً
if not os.path.exists("data"):
    os.makedirs("data")

# --- بوابة الموظفين (Sidebar) ---
st.sidebar.title("🔐 إدارة النتائج")
admin_pass = st.sidebar.text_input("كلمة مرور المسؤول:", type="password")

if admin_pass == "admin123":
    st.sidebar.success("تم تسجيل الدخول")
    target_stage = st.sidebar.selectbox("تحديث نتائج:", 
                                        ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
    
    uploaded_file = st.sidebar.file_uploader(f"ارفع ملف Excel لـ {target_stage}", type=["xlsx"])
    
    if uploaded_file:
        file_path = os.path.join("data", f"{target_stage}.xlsx")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"تم رفع ملف {target_stage} بنجاح!")

# --- واجهة الطالب (الرئيسية) ---
st.title("🎓 بوابة نتائج الطلاب")
st.write("اختر المرحلة الدراسية وادخل رقمك الأكاديمي للاستعلام عن النتيجة.")

col1, col2 = st.columns(2)
with col1:
    student_stage = st.selectbox("المرحلة الدراسية:", 
                                 ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
with col2:
    student_id = st.text_input("الرقم الأكاديمي:", placeholder="مثال: 202401")

if st.button("بحث عن النتيجة"):
    if not student_id:
        st.warning("الرجاء إدخال الرقم الأكاديمي أولاً.")
    else:
        file_path = os.path.join("data", f"{student_stage}.xlsx")
        
        if os.path.exists(file_path):
            try:
                # قراءة ملف الإكسل
                df = pd.read_excel(file_path, engine='openpyxl')
                
                # توحيد نوع البيانات في عمود الرقم الأكاديمي للبحث بدقة
                df['الرقم الأكاديمي'] = df['الرقم الأكاديمي'].astype(str).str.strip()
                
                # البحث عن الطالب بناءً على الرقم المدخل
                result = df[df['الرقم الأكاديمي'] == student_id.strip()]

                if not result.empty:
                    student_data = result.iloc[0]
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.subheader(f"👤 الاسم: {student_data['اسم الطالب']}")
                    st.write(f"🆔 الرقم الأكاديمي: {student_data['الرقم الأكاديمي']}")
                    st.divider()
                    
                    st.markdown("### 📋 تفاصيل الدرجات:")
                    
                    # استخراج الدرجات فقط وتنسيقها في جدول جديد ليظهر اسم المادة بوضوح
                    cols_to_drop = [c for c in ['الرقم الأكاديمي', 'اسم الطالب'] if c in df.columns]
                    grades_series = student_data.drop(labels=cols_to_drop)
                    
                    grades_df = pd.DataFrame({
                        'المادة الدراسية': grades_series.index,
                        'الدرجة': grades_series.values
                    })
                    
                    # عرض الجدول النهائي
                    st.table(grades_df)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("الرقم الأكاديمي غير موجود. تأكد من الرقم أو المرحلة المختارة.")
            except Exception as e:
                st.error(f"حدث خطأ في قراءة البيانات. تأكد أن الملف يحتوي على الأعمدة المطلوبة.")
        else:
            st.info(f"نعتذر، نتائج {student_stage} لم ترفع بعد في النظام.")

st.markdown("---")
st.caption("نظام عرض النتائج الأكاديمي | تم التحديث لعام 2024")

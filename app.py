import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="بوابة النتائج الرسمية", layout="centered")

# تنسيق CSS احترافي
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; font-family: 'Arial'; }
    .stTextInput > div > div > input { text-align: center; font-size: 20px; border-radius: 10px; }
    .student-header {
        background: linear-gradient(90deg, #2c3e50, #4ca1af);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    }
    .grade-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .grade-box:hover { transform: translateY(-5px); }
    .subject-name { color: #555; font-size: 14px; font-weight: bold; margin-bottom: 10px; }
    .subject-grade { color: #2e7d32; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if not os.path.exists("data"): os.makedirs("data")

# --- بوابة الإدارة (Sidebar) ---
with st.sidebar:
    st.title("⚙️ لوحة التحكم")
    admin_pass = st.text_input("كلمة مرور المسؤول:", type="password")
    if admin_pass == "admin123":
        st.success("تم تسجيل الدخول")
        stage = st.selectbox("المرحلة الدراسية:", ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
        up_file = st.file_uploader("رفع ملف النتائج (Excel):", type=["xlsx"])
        if up_file:
            with open(os.path.join("data", f"{stage}.xlsx"), "wb") as f:
                f.write(up_file.getbuffer())
            st.success(f"تم تحديث {stage}")

# --- واجهة الطالب (Main) ---
st.markdown("<h1 style='text-align: center;'>🎓 نظام استعلام النتائج</h1>", unsafe_allow_html=True)
st.write("---")

c1, c2 = st.columns(2)
with c1: 
    st_stage = st.selectbox("اختر المرحلة:", ["المرحلة الأولى", "المرحلة الثانية", "المرحلة الثالثة", "المرحلة الرابعة", "المرحلة الخامسة"])
with c2: 
    st_id = st.text_input("أدخل الرقم الأكاديمي:", placeholder="مثال: 1001")

if st.button("🔍 عرض النتيجة الآن"):
    file_path = os.path.join("data", f"{st_stage}.xlsx")
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
            df['الرقم الأكاديمي'] = df['الرقم الأكاديمي'].astype(str).str.strip()
            result = df[df['الرقم الأكاديمي'] == st_id.strip()]

            if not result.empty:
                student = result.iloc[0]
                
                # رأس النتيجة (معلومات الطالب)
                st.markdown(f"""
                    <div class='student-header'>
                        <h2>{student['اسم الطالب']}</h2>
                        <p>الرقم الأكاديمي: {student['الرقم الأكاديمي']} | {st_stage}</p>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("### 📊 تفاصيل الدرجات الدراسية:")
                
                # استخراج المواد فقط
                cols_to_drop = [c for c in ['الرقم الأكاديمي', 'اسم الطالب'] if c in df.columns]
                grades = student.drop(labels=cols_to_drop)

                # عرض الدرجات في شبكة (Grid) من 3 أعمدة
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
                
                st.balloons() # احتفال بسيط عند ظهور النتيجة
            else:
                st.error("❌ عذراً، لم يتم العثور على هذا الرقم الأكاديمي.")
        except Exception as e:
            st.error("⚠️ خطأ في قراءة ملف البيانات. تأكد من مطابقة أسماء الأعمدة.")
    else:
        st.info("ℹ️ لم يتم رفع نتائج هذه المرحلة بعد.")

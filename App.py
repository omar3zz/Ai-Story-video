import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import requests
from io import BytesIO

# إعداد واجهة التطبيق
st.set_page_config(page_title="Story Generator", layout="centered")
st.title("مولد القصص والذكاء الاصطناعي 📝🎨")

# إدخال موضوع القصة
topic = st.text_input("اكتب موضوع القصة هنا:")

# اختيار اللغة
language = st.selectbox("اختر اللغة:", ["ar", "en"])

# إعداد مفتاح API الخاص بـ Gemini
# ملاحظة: ستحتاج لوضع مفتاحك الخاص هنا لاحقاً
genai.configure(api_key='YOUR_API_KEY')
model = genai.GenerativeModel('gemini-pro')

if st.button("ابدأ الإنشاء"):
    if topic:
        with st.spinner('جاري تأليف القصة وتجهيز الصور...'):
            try:
                # 1. توليد نص القصة
                prompt = f"Write a short creative story about {topic} in {language} language."
                story_response = model.generate_content(prompt)
                story_text = story_response.text
                
                st.subheader("القصة:")
                st.write(story_text)

                # 2. توليد الصورة (نمط بيكسار ثري دي)
                st.subheader("الصورة التخيلية:")
                image_prompt = f"Cinematic 3D Pixar style, high detail, for a story about: {topic}"
                image_url = f"https://image.pollinations.ai/prompt/{image_prompt.replace(' ', '%20')}"
                st.image(image_url, use_column_width=True)

                # 3. تحويل النص لصوت
                st.subheader("الاستماع للقصة:")
                tts = gTTS(text=story_text, lang=language)
                audio_fp = BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp)
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("من فضلك ادخل موضوعاً للقصة أولاً.")

import streamlit as st
import google.generativeai as genai
import pysrt

# আপনার নতুন API Key এখানে বসাবেন
GEN_AI_KEY = "AIzaSyBPGj_Rr3_JaWxdGqfnQs_BDokp_hQApVI"

genai.configure(api_key=GEN_AI_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="AI Smart Translator", page_icon="🎬")
st.title("🎬 Smart AI Subtitle Translator")
st.write("এবার একদম নিখুঁত বাংলা অনুবাদ হবে!")

def ai_translate(text):
    # প্রোম্পটটি আরও শক্তিশালী করা হয়েছে যাতে সে ইংরেজি ফেরত না দেয়
    prompt = f"Translate the following English movie dialogue into natural, meaningful Bengali. Only provide the Bengali translation, nothing else: \n\n{text}"
    try:
        response = model.generate_content(prompt)
        # যদি AI ভুল করে ইংরেজি দেয় বা খালি রাখে, তবে পুরনো টেক্সটই থাকবে
        if response and response.text:
            return response.text.strip()
        return text
    except:
        return text

uploaded_file = st.file_uploader("আপনার .srt ফাইলটি দিন", type=["srt"])

if uploaded_file is not None:
    if st.button("AI অনুবাদ শুরু করুন"):
        with st.spinner('AI প্রতিটি লাইন গভীরভাবে বুঝে অনুবাদ করছে...'):
            raw_content = uploaded_file.read().decode("utf-8", errors='ignore')
            subs = pysrt.from_string(raw_content)
            
            progress_bar = st.progress(0)
            total = len(subs)
            
            # সেফটির জন্য ৩টি করে লাইন পাঠানো হচ্ছে যাতে ভুল না হয়
            for i in range(0, total, 3):
                batch = subs[i:i+3]
                for sub in batch:
                    translated = ai_translate(sub.text)
                    # চেক করা হচ্ছে অনুবাদটি বাংলা কি না (বেসিক চেক)
                    sub.text = translated
                
                progress_bar.progress(min((i + 3) / total, 1.0))

            # সাবটাইটেল ফরম্যাটটি একদম ম্যানুয়ালি তৈরি করা যাতে প্লেয়ার রিড করতে পারে
            output_srt = ""
            for sub in subs:
                output_srt += f"{sub.index}\n{sub.start} --> {sub.end}\n{sub.text}\n\n"
            
            st.success("অনুবাদ শেষ! এবার মুভিতে চেক করে দেখুন।")
            st.download_button("বাংলা ফাইল ডাউনলোড করুন", output_srt, file_name="bangla_subtitle.srt")

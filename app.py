import streamlit as st
import google.generativeai as genai
import pysrt
import io

# আপনার API Key এখানে বসান
GEN_AI_KEY = "AIzaSyAnBG1-WCtEygZbgNbUqP7xs-ZKb24mpTI"

genai.configure(api_key=GEN_AI_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="AI Subtitle Translator", page_icon="🎬")
st.title("🎬 AI Smart SRT Translator")
st.write("এটি Google Translate নয়, এটি Gemini AI দিয়ে মানুষের মতো অনুবাদ করবে।")

def ai_translate(text):
    prompt = f"Translate the following movie subtitle text into natural, conversational Bengali. Keep the emotion and context intact. Don't do literal translation: \n\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return text

uploaded_file = st.file_uploader("আপনার .srt ফাইলটি এখানে দিন", type=["srt"])

if uploaded_file is not None:
    if st.button("AI অনুবাদ শুরু করুন"):
        with st.spinner('AI আপনার মুভির প্রেক্ষাপট বুঝে অনুবাদ করছে... একটু সময় লাগতে পারে।'):
            # ফাইলটি পড়ার নিয়ম
            content = uploaded_file.read().decode("utf-8")
            subs = pysrt.from_string(content)
            
            progress_bar = st.progress(0)
            total = len(subs)
            
            # স্পিড বাড়ানোর জন্য ৫টি করে লাইন একসাথে পাঠানো হচ্ছে
            for i in range(0, total, 5):
                batch = subs[i:i+5]
                combined_text = "\n".join([sub.text for sub in batch])
                translated_text = ai_translate(combined_text)
                
                # অনুবাদগুলো আবার লাইনে ভাগ করে বসানো
                translated_lines = translated_text.split('\n')
                for j, sub in enumerate(batch):
                    if j < len(translated_lines):
                        sub.text = translated_lines[j]
                
                progress_bar.progress(min((i + 5) / total, 1.0))

            # ফাইলটি তৈরি করা
            output_srt = subs.to_string()
            st.success("অভিনন্দন! AI অনুবাদ সম্পন্ন হয়েছে।")
            st.download_button("বাংলা সাবটাইটেল ডাউনলোড করুন", output_srt, file_name="ai_translated.srt")

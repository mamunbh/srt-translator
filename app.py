import streamlit as st
import google.generativeai as genai
import pysrt

# আপনার API Key এখানে বসান
GEN_AI_KEY = "AIzaSyAnBG1-WCtEygZbgNbUqP7xs-ZKb24mpTI"

genai.configure(api_key=GEN_AI_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="AI Subtitle Translator", page_icon="🎬")
st.title("🎬 AI Smart SRT Translator")
st.write("Gemini AI দিয়ে মুভির আসল ফিল নিয়ে অনুবাদ করুন।")

def ai_translate(text):
    prompt = f"Translate the following movie subtitle text into natural, conversational Bengali. Keep the emotion and context intact. Don't do literal translation. Return only the translated Bengali text: \n\n{text}"
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
            raw_content = uploaded_file.read().decode("utf-8", errors='ignore')
            subs = pysrt.from_string(raw_content)
            
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
                        sub.text = translated_lines[j].strip()
                
                progress_bar.progress(min((i + 5) / total, 1.0))

            # এরর ফিক্স: টেক্সট জেনারেট করার সহজ পদ্ধতি
            output_srt = ""
            for sub in subs:
                output_srt += f"{sub.index}\n{sub.start} --> {sub.end}\n{sub.text}\n\n"
            
            st.success("অভিনন্দন! AI অনুবাদ সম্পন্ন হয়েছে।")
            st.download_button("বাংলা সাবটাইটেল ডাউনলোড করুন", output_srt, file_name="ai_translated_bangla.srt")

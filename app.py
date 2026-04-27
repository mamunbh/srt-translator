import streamlit as st
from googletrans import Translator
import re

st.set_page_config(page_title="SRT Translator", page_icon="📝")

st.title("🌐 SRT Subtitle Translator")
st.subheader("যেকোনো ভাষার সাবটাইটেল বাংলায় অনুবাদ করুন")

def translate_srt(content, target_lang='bn'):
    translator = Translator()
    # SRT pattern: Index, Time, Text
    lines = content.split('\n')
    translated_lines = []
    
    progress_bar = st.progress(0)
    total_lines = len(lines)

    for i, line in enumerate(lines):
        # যদি লাইনটি টেক্সট হয় (সময় বা নাম্বার না হয়), তবে অনুবাদ হবে
        if line.strip() and not line.strip().isdigit() and '-->' not in line:
            try:
                translated = translator.translate(line, dest=target_lang).text
                translated_lines.append(translated)
            except:
                translated_lines.append(line)
        else:
            translated_lines.append(line)
        
        # প্রগ্রেস আপডেট
        if i % 10 == 0:
            progress_bar.progress(i / total_lines)
            
    progress_bar.progress(1.0)
    return '\n'.join(translated_lines)

uploaded_file = st.file_uploader("আপনার .srt ফাইলটি এখানে আপলোড করুন", type=["srt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    
    if st.button("Translate to Bengali"):
        with st.spinner('অনুবাদ হচ্ছে... দয়া করে অপেক্ষা করুন।'):
            result = translate_srt(content)
            st.success("অনুবাদ সম্পন্ন হয়েছে!")
            
            st.download_button(
                label="অনুবাদ করা ফাইলটি ডাউনলোড করুন",
                data=result,
                file_name="translated_subtitle.srt",
                mime="text/plain"
            )
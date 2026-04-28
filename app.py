import streamlit as st
from googletrans import Translator
import time

st.set_page_config(page_title="Fast SRT Translator", page_icon="⚡")

st.title("⚡ Fast & Smart SRT Translator")
st.write("এখন অনুবাদ হবে আরও দ্রুত এবং নিখুঁত!")

def batch_translate(text_list, target_lang='bn'):
    translator = Translator()
    try:
        # অনেকগুলো লাইন একসাথে অনুবাদ করার চেষ্টা করবে
        translations = translator.translate(text_list, dest=target_lang)
        return [t.text for t in translations]
    except:
        return text_list

def process_srt(content):
    lines = content.split('\n')
    translated_lines = []
    text_to_translate = []
    indices_to_replace = []
    
    progress_bar = st.progress(0)
    
    for i, line in enumerate(lines):
        # সময় বা নাম্বার বাদে শুধু কথাগুলো আলাদা করা
        if line.strip() and not line.strip().isdigit() and '-->' not in line:
            text_to_translate.append(line)
            indices_to_replace.append(i)
        translated_lines.append(line)

    # একবারে ২০টি করে লাইন অনুবাদ হবে (যাতে গতি বাড়ে)
    batch_size = 20
    for i in range(0, len(text_to_translate), batch_size):
        batch = text_to_translate[i : i + batch_size]
        translated_batch = batch_translate(batch)
        
        for j, translated_text in enumerate(translated_batch):
            original_index = indices_to_replace[i + j]
            translated_lines[original_index] = translated_text
            
        progress_bar.progress(min((i + batch_size) / len(text_to_translate), 1.0))
        
    return '\n'.join(translated_lines)

uploaded_file = st.file_uploader("আপনার .srt ফাইলটি দিন", type=["srt"])

if uploaded_file is not None:
    if st.button("স্মার্ট অনুবাদ শুরু করুন"):
        with st.spinner('কাজ চলছে... দ্রুত শেষ হবে!'):
            content = uploaded_file.read().decode("utf-8")
            result = process_srt(content)
            st.success("কাজ শেষ!")
            st.download_button("ডাউনলোড করুন", result, "translated_bn.srt")

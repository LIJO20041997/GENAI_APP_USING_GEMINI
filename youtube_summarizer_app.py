import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))

prompt = """You are a Youtube video summarizer. You will taking the transcript text and 
summarizing the entire vedio and providing the important summary in points within 250 word.Please give 
the summary of the text given here  """

def extract_transcript_details(youtube_vedio_url):
    try:
        vedio_id = youtube_vedio_url.split("=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(vedio_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter Youtube Vedio link: ")

if youtube_link:
    vedio_id = youtube_link.split("=")[1].split("&")[0]
    st.image(f"http://img.youtube.com/vi/{vedio_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(prompt, transcript_text)
        st.markdown("## Detailed Notes: ")
        st.write(summary)

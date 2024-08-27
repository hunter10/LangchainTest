import streamlit as st
import subprocess
import math
from pydub import AudioSegment
import glob
import openai
import os

# 샘플영상
# https://www.youtube.com/watch?v=CWvOKHNeLMI

has_transcript = os.path.exists("./.cache/podcast.txt")

# 비디오에서 오디오 추출
@st.cache_data()
def extract_audio_from_video(video_path):
    if has_transcript:
        return
    audio_path = video_path.replace("mp4", "mp3")
    command = [
        "ffmpeg", 
        "-y",           # 질문자한테 물을때 y응답
        "-i",           # 인풋
        video_path, 
        "-vn",          # 비디오 없이
        audio_path,
    ]
    subprocess.run(command)

# 오디오에서 10분 단위로 자르기
@st.cache_data()
def cut_audio_in_chunk(audio_path, chunk_size, chunk_folder):
    if has_transcript:
        return
    track = AudioSegment.from_mp3(audio_path)
    chunk_len = chunk_size * 60 * 1000
    chunks = math.ceil(len(track) / chunk_len)

    for i in range(chunks):
        start_time = i * chunk_len
        end_time = (i + 1) * chunk_len
        chunk = track[start_time:end_time]
        chunk.export(f"{chunk_folder}/chunk_{i}.mp3", format="mp3")

# 오디오 파일에서 텍스트로 추출하기
@st.cache_data()
def transcribe_chunks(chunk_folder, destination):
    if has_transcript:
        return
    files = glob.glob(f"{chunk_folder}/*.mp3")
    files.sort()
    for file in files:
        with open(file, "rb") as audio_file, open(destination, "a") as text_file:
            transcript = openai.Audio.transcribe(
                "whisper-1", 
                audio_file, 
            )
            text_file.write(transcript["text"])

st.set_page_config(
    page_title="MeetingGPT",
    page_icon="☢",
)

st.markdown(
    """
# MeetingGPT
            
Welcome to MeetingGPT, upload a video and I will give you a transcript, a summary and a chat bot to ask any questions about it.

Get started by uploading a video file in the sidebar.
"""
)

with st.sidebar:
    video = st.file_uploader("Video", type=["mp4", "avi", "mkv", "mov"],)

if video:
    chunks_folder = "./.cache/chunks"

    with st.status("Loading video..."):
        video_content = video.read()
        video_path = f"./.cache/{video.name}"
        audio_path = video_path.replace("mp4", "mp3")
        transcript_path = video_path.replace("mp4", "txt")
        print(video_path)
        with open(video_path, "wb") as f:
            f.write(video_content)
    with st.status("Extracting audio..."):
        extract_audio_from_video(video_path)
    with st.status("Cutting audio segments..."):
        cut_audio_in_chunk(audio_path, 10, chunks_folder)
    with st.status("Transcribing audio..."):
        transcribe_chunks(chunks_folder, transcript_path)
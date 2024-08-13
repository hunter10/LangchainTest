# playwright install 으로 chromiumloader를 설치해줘야 함.(가상환경에서)
from langchain.document_loaders import SitemapLoader
import streamlit as st
import asyncio
import sys

@st.cache_data(show_spinner="Loading website...")
def load_website(url):
    loader = SitemapLoader(url)
    loader.requests_per_second = 1
    docs = loader.load()
    return docs

st.set_page_config(
    page_title="SiteGPT",
    page_icon="🖥️",
)

# if 'win32' in sys.platform:
#     # Windows specific event-loop policy & cmd
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
#     cmds = [['C:/Windows/system32/HOSTNAME.EXE']]
# else:
#     # Unix default event-loop policy & cmds
#     cmds = [
#         ['du', '-sh', '/Users/fredrik/Desktop'],
#         ['du', '-sh', '/Users/fredrik'],
#         ['du', '-sh', '/Users/fredrik/Pictures']
#     ]

st.markdown(
    """
    # SiteGPT
            
    Ask questions about the content of a website.
            
    Start by writing the URL of the website on the sidebar.
"""
)


with st.sidebar:
    url = st.text_input(
        "Write down a URL",
        # https://openai.com/index/introducing-gpts/
        # https://openai.com/index/frontier-risk-and-preparedness/
        # https://www.naver.com/
        # https://openai.com/sitemap.xml
        # https://www.google.com/sitemap.xml
        placeholder="https://example.com",
    )


if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        docs = load_website(url)
        st.write(docs)
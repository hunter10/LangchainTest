from langchain.document_loaders import SitemapLoader, text
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st

def parse_page(soup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return (
        str(soup.get_text())
        .replace("\n", " ")
        .replace("\xa0", " ")
        .replace("CloseSearch Submit Blog", "")
    )

@st.cache_data(show_spinner="Loading website...")
def load_website(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )
    loader = SitemapLoader(
        url,
        filter_urls=[
            r"^(.*\/blog\/).*",
        ],
        parsing_function=parse_page,
    )
    loader.requests_per_second = 2
    docs = loader.load_and_split(text_splitter=splitter)
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
        # https://openai.com/sitemap.xml # 2024년 8월 14일 현재 정보 못가져옴
        # https://openai.com/index/data-partnerships/
        # https://openai.com/index/introducing-gpts/
        # https://openai.com/index/frontier-risk-and-preparedness/
        # https://www.naver.com/
        # https://www.google.com/sitemap.xml # 양이 엄청남 시도하지 말기
        # https://www.google.com/gmail/sitemap.xml # 이게 양이 좀 작음.
        # https://www.google.com/intl/ko/gmail/about/ 바로 윗줄의 사이트맵에서 정보가져오기
        placeholder="https://example.com",
    )


if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        docs = load_website(url)
        st.write(docs)
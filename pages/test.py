from langchain.document_loaders import SitemapLoader
import requests
import tempfile

# 사이트맵 URL
sitemap_url = "https://openai.com/sitemap.xml"

# 추가적인 헤더 정보
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

# 사이트맵을 미리 다운로드
response = requests.get(sitemap_url, headers=headers)
if response.status_code == 200:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmp_file:
        tmp_file.write(response.content)
        temp_file_path = tmp_file.name
        
    # SitemapLoader를 사용하여 로컬 파일 처리
    loader = SitemapLoader(web_path=temp_file_path)
    documents = loader.load()

    # 문서 수 출력
    print(f"Number of documents loaded: {len(documents)}")

    # 첫 번째 문서 출력
    if documents:
        print(documents[0])
else:
    print(f"Failed to retrieve sitemap: {response.status_code}")



'''
from requests_html import HTMLSession

# 세션 설정
session = HTMLSession()

# 사이트맵 URL
sitemap_url = "https://openai.com/sitemap.xml"

# 자바스크립트를 처리하는 요청
response = session.get(sitemap_url)
response.html.render()  # 자바스크립트를 실행하여 페이지 렌더링

if response.status_code == 200:
    root = ET.fromstring(response.text)
    
    # 사이트맵에서 URL 추출
    urls = [url.find('loc').text for url in root.findall('.//url')]
    print(f"Number of URLs found: {len(urls)}")
else:
    print(f"Failed to retrieve sitemap: {response.status_code}")
'''

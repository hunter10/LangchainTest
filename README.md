# 노마드의 랭체인 강좌 연습

## 파이썬 3.11.6 (중요)

## 강의 조건
- ChatGPT plus 유료 구독자여야 함.
- platform.openaio.com 계정에 꼭 금액 limit를 걸어야 함.
- 파이썬 가상환경으로 작업
- .gitignore 세팅할때 env/는 추가하기 때문에 새로 세팅하면 가상환경 세팅작업을 해줘야 함.
- 이 프로젝트를 세팅하는데 필요한 패키지들은 requirements.txt에 있다.
- 가상환경하에서 pip install -r requirements.txt를 실행한다.

### 가상환경 세업 (venv)
- 생성 : python -m venv ./env 
- 활성(맥) : source <venv>/bin/activate
- 활성(윈) : C:\> <venv>\Scripts\activate.bat
- 활성(PS) : PS C:\> <venv>\Scripts\Activate.ps1
- 비활성화 : deactivate

https://nomadcoders.co/fullstack-gpt/lobby

    
- https://blog.deeplink.kr/?p=942 에서 venv로 가상환경 세팅하는걸 알수있다.  
  
- 최초 구성시 https://platform.openai.com/ 에서 API 키값을 받아와서 
프로젝트 안에 env 파일 생성후에 OPEN_API_KEY="받아온 키" 세팅해야 함.

- streamlit을 이용한 웹을 띄우려면 streamlit run Home.py을 실행

from typing import Any, Dict
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Nicolacus Maximus Quote Giver",
    description="Get a real quote said by Nicolacus Maximus himself.",
    servers=[
        {"url":"https://textbooks-purchased-pledge-aberdeen.trycloudflare.com"}
    ]
)

class Quote(BaseModel):
    quote: str = Field(description="The quote that Nicolacus Maximus said.")
    year: int = Field(description="The year when Nicolacus Maximus said the quote.")

@app.get(
    "/quote", 
    summary="Returns a random quote by Nicolacus Maximus",
    description="Upon receiving a GET request this endpoint will return a real quiote said by Nicolacus Maximus himself.",
    response_description="A Quote object that contains the quote said by Nicolacus Maximus and the date when the quote was said.",
    response_model=Quote,
    # openapi_extra={
    #     "x-openai-isConsequential":True,
    # },
)

def get_quote(request: Request):
    print(request.headers)
    return {
        "quote": "Life is short so eat it all.",
        "year": 1950,
    }

# 가짜 DB
user_token_db = {
    "ABCDEF": "nico"
}

#https://textbooks-purchased-pledge-aberdeen.trycloudflare.com/authorize?
# response_type=code&
# client_id=client123&
# redirect_uri=https%3A%2F%2Fchat.openai.com%2Faip%2Fg-02a2ab8ee544d0544e6e84e87e8163caabb3907e%2Foauth%2Fcallback&state=2eb26ca7-8560-4172-b985-e2f7f860cf7b&
# scope=user%3Aread%2Cuser%3Adelete
@app.get("/authorize", response_class=HTMLResponse,)
def handle_authorize(client_id:str, redirect_uri:str, state:str):
    # print( 
    #       client_id, 
    #       redirect_uri,  
    #       state)
    # return {
    #     "ok": True,
    # }
    
    return f"""
    <html>
        <head>
            <title>Nicolacus Maximus Log In</title>
        </head>
        <body>
            <h1>Log Into Nicolacus Maximus</h1>
            <a href="{redirect_uri}?code=ABCDEF&state={state}">Authorize Nicolacus 
            Maximus GPT</a>
        </body>
    </html>
    """

@app.post("/token")
# 뭘 보내는지 확인하기 위함
# def handle_token(payload: Any = Body(None)):
#     print(payload)
#     return {"x":"x"}

def handle_token(code = Form(...)):
    print(code)
    return {
        "access_token": user_token_db[code]
    }
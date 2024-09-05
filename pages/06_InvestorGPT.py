from langchain.schema import SystemMessage
import streamlit as st
import os
import requests
from typing import Type
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.agents import initialize_agent, AgentType
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.tools import DuckDuckGoSearchResults

llm = ChatOpenAI(temperature=0.1, model_name="gpt-4o-mini")

alpha_vantage_api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")

class StockMarketSymbolSearchToolArgsSchema(BaseModel):
    query: str = Field(description="The query you will search for.Example query: Stock Market Symbol for Apple Company")

class StockMarketSymbolSearchTool(BaseTool):
    name = "StockMarketSymbolSearchTool"
    description = """
    Use this tool to find the stock market symbol for a company.
    It takes a query as an argument.
    """
    args_schema: Type[
        StockMarketSymbolSearchToolArgsSchema
    ] = StockMarketSymbolSearchToolArgsSchema

    def _run(self, query):
        #ddg = DuckDuckGoSearchAPIWrapper()
        ddg = DuckDuckGoSearchResults()
        return ddg.run(query)

class CompanyOverviewArgsSchema(BaseModel):
    symbol : str = Field(description="Stock symbol of the company.Example: AAPL, TSLA")

class CompanyOverviewTool(BaseTool):
    name = "CompanyOverview"
    description = """
    Use this to get an overview of the financials of the company.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema]=CompanyOverviewArgsSchema

    def _run(self, symbol):
        r = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_vantage_api_key}")
        return r.json()

class CompanyIncomeStatementTool(BaseTool):
    name = "CompanyIncomeStatement"
    description = """
    Use this to get the income statement of a company.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema]=CompanyOverviewArgsSchema

    def _run(self, symbol):
        r = requests.get(f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={alpha_vantage_api_key}")
        return r.json()["annualReports"]

class CompanyStockPerformanceTool(BaseTool):
    name = "CompanyStockPerformanceTool"
    description = """
    Use this to get the weekly performance of a company stock.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema]=CompanyOverviewArgsSchema

    def _run(self, symbol):
        r = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={alpha_vantage_api_key}")
        return r.json()

agent = initialize_agent(
    llm=llm, 
    verbose=True,
    agent=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True, # 영상과 달리 2024.9.2 현재 이 문장이 없어도 문법에러는 없음
    tools=[
        StockMarketSymbolSearchTool(),
        CompanyOverviewTool(),
        CompanyIncomeStatementTool(),
        CompanyStockPerformanceTool(),
    ],
    agent_kwargs={
        "system_message": SystemMessage(content="""
            You are a hedge fund manager.
            
            You evaluate a company and provide your opinion and reasons why the stock is a buy or not.
            
            Consider the performance of a stock, the company overview and the income statement.
            
            Be assertive in your judgement and recommend the stock or advise the user against it.
        """)
    }
    #저는 헤지펀드 매니저입니다.
    #회사를 평가하고, 주식을 사야 할지 여부에 대한 의견과 그 이유를 제공합니다.

    #주식의 성과, 회사 개요, 그리고 손익계산서를 고려하여 판단합니다.
    #명확하게 판단하여 주식을 추천하거나, 사지 말아야 할 이유를 사용자에게 조언합니다.

    #아래에 평가할 회사 정보를 제공해 주세요.
    #이를 바탕으로 회사의 현재 상황을 분석하고 투자에 대한 결정을 내리겠습니다.

)

st.set_page_config(
    page_title="InvestorGPT",
    page_icon="💼",
)

st.markdown(
    """
    # InvestorGPT
            
    Welcome to InvestorGPT.
            
    Write down the name of a company and our Agent will do the research for you.
"""
)

company = st.text_input("Write the name of the company you are interested on.")

if company:
    result = agent.invoke(company)

    st.write(result["output"].replace("$", "\$"))
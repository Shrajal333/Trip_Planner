from crewai import Agent, LLM
from trip_tools.browser_tools import BrowserTools
from trip_tools.calculator_tools import CalculatorTools
from trip_tools.search_tools import SearchTools

import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

llm = LLM(
    model="groq/llama3-8b-8192",
    temperature=0.5,
    max_tokens=512,
    api_key=GROQ_API_KEY,
)

class TripAgents():
    def city_selection_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, season, and prices',
            backstory='An expert in analyzing travel data to pick ideal destinations',
            tools=[SearchTools.search_internet,BrowserTools.scrape_and_summarize_website],
            verbose=True,
            llm=llm)

    def local_expert_agent(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            backstory="""A knowledgeable local guide with extensive information about the city, it's attractions and customs""",
            tools=[SearchTools.search_internet,BrowserTools.scrape_and_summarize_website],
            verbose=True,
            llm=llm)

    def travel_concierge_agent(self):
        return Agent(
            role='Amazing Travel Concierge',
            goal="""Create the most amazing travel itineraries with budget and packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with decades of experience""",
            tools=[SearchTools.search_internet,BrowserTools.scrape_and_summarize_website,CalculatorTools.calculate],
            verbose=True,
            llm=llm)
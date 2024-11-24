import os
import requests
from bs4 import BeautifulSoup
from crewai.tools import tool
from langchain_groq import ChatGroq
from langchain import PromptTemplate
from langchain.schema import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

class BrowserTools():

    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Designed to scrape the content of a given website and generate a concise, meaningful summary of the information present on the site. It is particularly useful for extracting and condensing large amounts of textual data into a shorter format that captures the key points."""

        response = requests.get(website)
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3'])
        content = " ".join([para.get_text() for para in paragraphs])

        documents = [Document(page_content=content)]
        final_documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50).split_documents(documents)

        template = """
                        Please summarize the following YouTube transcript segment:
                        Speech: {text}
                        Provide a detailed summary, highlighting key ideas and important points. 
                        Summary:
                """
        prompt = PromptTemplate(input_variables=['text'], template=template)

        model = ChatGroq(model="Gemma-7b-It", api_key=GROQ_API_KEY)
        summary_chain = load_summarize_chain(
            model, 
            chain_type="stuff", 
            prompt=prompt, 
            verbose=False)

        summary = summary_chain.invoke({'input_documents': final_documents})['output_text']
        return summary
import os
import json
import requests
from crewai.tools import tool

from dotenv import load_dotenv
load_dotenv()

class SearchTools():

    @tool("Search topic on the internet")
    def search_internet(query):
        """Useful to search the internet about a a given topic and return relevant results"""

        top_results = 1
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})

        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json',
            'User-Agent': os.environ['USER_AGENT']
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
                return f"Error: Unable to fetch results (status code: {response.status_code})"
        
        results = response.json()['organic']
        if not results:
                return "No results found."
        
        output = []
        for result in results[:top_results]:
            title = result.get('title', 'No title available')
            link = result.get('link', 'No link available')
            snippet = result.get('snippet', 'No snippet available')
            output.append(f"Title: {title} \n Link: {link} \n Snippet: {snippet} \n-----------------")

        return '\n'.join(output)
import requests
from discord.ext import commands

API_KEY = "API_KEY"
CX = "CX"

class googleSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.apiKeys = {}
        self.getApiKeys()
        self.API_KEY = self.apiKeys.get(API_KEY, "")
        self.CX = self.apiKeys.get(CX, "")
        self.maxResults = 5

    def getApiKeys(self):
        with open('googleApiKeys.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                self.apiKeys[key] = value

    def search(self, query):
        BASE_URL = "https://www.googleapis.com/customsearch/v1"

        self.params = {
            "key": self.API_KEY,
            "cx": self.CX,
            "q": query,
            "num": self.maxResults
        }

        response = requests.get(BASE_URL, params=self.params)

        if response.status_code == 200:
            data = response.json()
            return data.get("items", [])
        else:
            return None
        
    @commands.command(name="ask", description="Asks google a question and returns the top 5 answers.")
    async def ask(self, ctx, *args):
        query = " ".join(args)
        search_results = self.search(query)
        if search_results:
            await ctx.send("Most relevant answers: ")
            for i, item in enumerate(search_results, start=1):
                await ctx.send(f"{i}. Answer: {item['snippet']}")
                await ctx.send(f"Source: <{item['link']}>")
        else:
            await ctx.send("Error: Unable to fetch search results.")
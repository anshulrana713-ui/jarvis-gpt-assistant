import requests
from config import NEWS_API_KEY

def get_news():
    api_key = NEWS_API_KEY

    url = f"http://api.mediastack.com/v1/news?access_key={api_key}&countries=in&languages=en&sort=published_desc&limit=3"

    try:
        data = requests.get(url).json()
        articles = data["data"]

        if not articles:
            return "No latest news found."

        result = ""

        for i, article in enumerate(articles, 1):
            result += f"{i}. {article['title']} "

        return result

    except Exception as e:
        print(e)
        return "Unable to fetch news."
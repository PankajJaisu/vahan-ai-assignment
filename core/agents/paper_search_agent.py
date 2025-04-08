import feedparser

class PaperSearchAgent:
    def search_arxiv(self, query, max_results=5):
        base_url = "http://export.arxiv.org/api/query?"
        query_url = f"search_query=all:{query}&start=0&max_results={max_results}"
        feed = feedparser.parse(base_url + query_url)
        return [{
            "title": entry.title,
            "summary": entry.summary,
            "link": entry.link,
            "published": entry.published,
            "citation": f"{entry.title} ({entry.published}) - {entry.link}"
        } for entry in feed.entries]

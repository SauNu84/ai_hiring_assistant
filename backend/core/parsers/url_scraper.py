"""JD ingestion from public URLs using Jina.ai reader (bot-resistant)."""
import httpx


JINA_READER_BASE = "https://r.jina.ai/"


async def scrape_jd_from_url(url: str, timeout: int = 30) -> str:
    """
    Fetch job description text from a public URL via Jina.ai reader.
    Jina converts the page to clean markdown, bypassing most scraper blocks.
    """
    reader_url = f"{JINA_READER_BASE}{url}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(
            reader_url,
            headers={"Accept": "text/plain"},
            follow_redirects=True,
        )
        response.raise_for_status()
        text = response.text.strip()
        if not text:
            raise ValueError("No content extracted from URL. Try uploading as PDF instead.")
        return text

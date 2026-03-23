"""JD ingestion from public URLs using Jina.ai reader (bot-resistant)."""
import httpx

from core.logging_config import get_logger

logger = get_logger(__name__)

JINA_READER_BASE = "https://r.jina.ai/"


async def scrape_jd_from_url(url: str, timeout: int = 30) -> str:
    """
    Fetch job description text from a public URL via Jina.ai reader.
    Jina converts the page to clean markdown, bypassing most scraper blocks.
    """
    logger.info("Scraping JD from URL", extra={"url": url})
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
            logger.warning("Empty response from Jina reader", extra={"url": url})
            raise ValueError("No content extracted from URL. Try uploading as PDF instead.")
        logger.debug("JD scraped successfully", extra={"url": url, "length": len(text)})
        return text

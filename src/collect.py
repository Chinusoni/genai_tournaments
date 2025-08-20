"""Data collection utilities.

This module demonstrates two approaches:
1) Web search + scraping (requires API keys / internet).
2) Local sample mode (uses bundled sample JSON).

Replace placeholder logic with real sources per sport (federation sites, BWF, AIFF, BCCI, etc.).
"""
import os, json, time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from .utils import parse_date, infer_level

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_tournaments.json")

def _summarize(desc: str) -> str:
    """50-word cap summary without external LLM (simple heuristic)."""
    words = (desc or "").split()
    return " ".join(words[:50])

def collect_from_sample() -> List[Dict]:
    with open(SAMPLE_PATH, "r") as f:
        items = json.load(f)
    return items

def scrape_generic(url: str) -> List[Dict]:
    """Very simple scraper stub; customize per site."""
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.title.text.strip() if soup.title else "Tournament"
    return [{
        "sport": "Unknown",
        "tournament_name": title,
        "level": infer_level(title) or "National",
        "start_date": "",
        "end_date": "",
        "official_url": url,
        "streaming": "",
        "image": "",
        "summary": _summarize(title)
    }]

def collect_all(mode: str = "sample") -> List[Dict]:
    if mode == "sample":
        return collect_from_sample()
    raise NotImplementedError("Real scraping/APIs not implemented in this environment; use mode='sample'.")

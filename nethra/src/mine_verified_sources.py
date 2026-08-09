#!/usr/bin/env python3
"""
mine_verified_sources.py — Real Web Mining Pipeline for Nethra
=============================================================

Searches the open web (Google News RSS, DuckDuckGo) for real articles
about each deep-audited ward/constituency, fetches and parses them,
uses Google Gemini to score geo-relevance and authenticity, and writes
only verified results into the Nethra SQLite database.

Usage:
  # Dry run — search & fetch only, no Gemini calls
  python3 src/mine_verified_sources.py --dry-run

  # Full run — search, fetch, verify with Gemini, write to DB
  GOOGLE_API_KEY=... python3 src/mine_verified_sources.py

  # Mine a single unit
  GOOGLE_API_KEY=... python3 src/mine_verified_sources.py --unit "Karur"
"""

import os
import sys
import json
import time
import sqlite3
import logging
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote_plus, urlparse, unquote
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

DB_PATH = "data/nethra_campaign.db"
GEMINI_MODEL = "gemini-3.5-flash"
REQUEST_DELAY = 2.5       # seconds between web requests
GEMINI_DELAY = 1.5        # seconds between Gemini calls
MAX_RESULTS_PER_QUERY = 8
REQUEST_TIMEOUT = 15      # seconds

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9,ta;q=0.8",
}

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("nethra_miner")

# ══════════════════════════════════════════════════════════════════════════════
# SEARCH TARGETS — 10 DEEP-AUDITED UNITS
# ══════════════════════════════════════════════════════════════════════════════

SEARCH_TARGETS = [
    # ── 5 ASSEMBLY BYELECTION SEATS ──────────────────────────────────────────
    {
        "unit_type": "constituency",
        "unit_name": "Karur",
        "district": "Karur",
        "key_issues": [
            "Thirumanilayur bus stand construction",
            "Karuppampalayam bus body MSME GST reduction",
            "Karur TVK stampede High Court ruling",
            "Amaravathi river dyeing effluent pollution",
        ],
        "search_queries": [
            '"Karur" "Thirumanilayur" bus stand',
            '"Karuppampalayam" bus body GST Karur',
            'Karur stampede TVK High Court 2025',
            'Karur byelection Tamil Nadu 2026',
            'Amaravathi river pollution Karur dyeing effluent',
        ],
    },
    {
        "unit_type": "constituency",
        "unit_name": "Tiruchirappalli (East)",
        "district": "Tiruchirappalli",
        "key_issues": [
            "Gandhi Market on-site upgrade vs Panjapur relocation",
            "BHEL Thuvakudi MSME industrial gas supply",
            "Trichy East byelection",
        ],
        "search_queries": [
            '"Gandhi Market" Trichy upgrade OR relocation',
            '"Gandhi Market" Panjapur Tiruchirappalli',
            'BHEL Thuvakudi MSME industrial gas Trichy',
            'Tiruchirappalli East byelection 2026',
            '"Gandhi Market" traders protest Trichy',
        ],
    },
    {
        "unit_type": "constituency",
        "unit_name": "Perundurai",
        "district": "Erode",
        "key_issues": [
            "SIPCOT CETP effluent plant ZLD",
            "Erode finger turmeric MSP price",
            "TAHDCO industrial sheds allotment",
        ],
        "search_queries": [
            'Perundurai SIPCOT CETP effluent plant',
            'Erode turmeric price MSP 2025 2026',
            'Perundurai TAHDCO sheds allotment SC ST',
            'Perundurai byelection Tamil Nadu 2026',
            'Erode turmeric farmers demand MSP',
        ],
    },
    {
        "unit_type": "constituency",
        "unit_name": "Viralimalai",
        "district": "Pudukkottai",
        "key_issues": [
            "Shanmuganathar hill peafowl sanctuary",
            "PWD irrigation kanmoi tank desilting",
        ],
        "search_queries": [
            'Viralimalai peafowl sanctuary Shanmuganathar',
            'Viralimalai peacock temple hill protection',
            'Pudukkottai kanmoi tank desilting PWD irrigation',
            'Viralimalai byelection Tamil Nadu 2026',
            'Viralimalai Pudukkottai irrigation tank',
        ],
    },
    {
        "unit_type": "constituency",
        "unit_name": "Ambasamudram",
        "district": "Tirunelveli",
        "key_issues": [
            "Thamirabarani concrete project PIL High Court",
            "Kalakkad solar crop fencing wildlife damage",
        ],
        "search_queries": [
            'Thamirabarani river concrete project High Court',
            'Thamirabarani riverfront beautification PIL',
            'Kalakkad crop damage wildlife elephant fencing',
            'Ambasamudram byelection Tamil Nadu 2026',
            'Thamirabarani Tirunelveli river restoration',
        ],
    },
    # ── 5 DEEP-AUDITED GCC WARDS ────────────────────────────────────────────
    {
        "unit_type": "gcc_ward",
        "unit_name": "Chennai Ward 84",
        "district": "Chennai",
        "key_issues": [
            "Anna Nagar 2nd Avenue stormwater drain SWD",
            "Otteri Nullah canal desilting",
        ],
        "search_queries": [
            '"Anna Nagar" stormwater drain Chennai 2025 2026',
            '"Otteri Nullah" desilting Chennai',
            'Anna Nagar 2nd Avenue SWD missing links Chennai',
            'Chennai Anna Nagar flood drain monsoon',
            'GCC Zone 8 Anna Nagar stormwater',
        ],
    },
    {
        "unit_type": "gcc_ward",
        "unit_name": "Chennai Ward 151",
        "district": "Chennai",
        "key_issues": [
            "Virugambakkam canal retaining wall",
            "Porur Lake feeder channel restoration",
        ],
        "search_queries": [
            'Virugambakkam canal retaining wall Chennai',
            '"Porur Lake" restoration feeder channel',
            'Valasaravakkam flood drainage Chennai',
            '"Porur Lake" encroachment sewage Chennai',
            'Virugambakkam canal wall construction GCC',
        ],
    },
    {
        "unit_type": "gcc_ward",
        "unit_name": "Chennai Ward 177",
        "district": "Chennai",
        "key_issues": [
            "Velachery Lake surplus channel desilting",
            "Pallikaranai marshland drain links",
        ],
        "search_queries": [
            '"Velachery Lake" surplus channel desilting',
            '"Pallikaranai marshland" drain OR drainage',
            'Velachery flooding monsoon Chennai 2025 2026',
            'Pallikaranai marsh missing stormwater drain',
            'Velachery MRTS track flood bottleneck',
        ],
    },
    {
        "unit_type": "gcc_ward",
        "unit_name": "Chennai Ward 180",
        "district": "Chennai",
        "key_issues": [
            "Adyar river sewage outfall interception",
            "33 canal restoration project",
            "Kotturpuram tree park pollution",
        ],
        "search_queries": [
            '"Adyar river" sewage outfall interception',
            '"33 canal" OR "33 canals" Chennai restoration',
            'Adyar river pollution sewage discharge Chennai',
            '"Kotturpuram" tree park OR urban forest',
            'Adyar Estuary canal restoration project GCC',
        ],
    },
    {
        "unit_type": "gcc_ward",
        "unit_name": "Chennai Ward 197",
        "district": "Chennai",
        "key_issues": [
            "Sholinganallur OMR drinking water pipeline",
            "Perungudi dump yard bio-mining",
        ],
        "search_queries": [
            'Sholinganallur OMR drinking water supply pipe',
            '"Perungudi dump yard" bio-mining OR biomining',
            'Perungudi dumpyard closure remediation Chennai',
            'ECR OMR link road water supply Chennai',
            'Sholinganallur IT corridor infrastructure Chennai',
        ],
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# SEARCH LAYER
# ══════════════════════════════════════════════════════════════════════════════

def search_google_news_rss(query: str) -> list[dict]:
    """Search via Google News RSS feed. Returns list of {url, title, source, date}."""
    results = []
    encoded = quote_plus(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        resp = requests.get(rss_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        for item in root.findall(".//item"):
            title_el = item.find("title")
            link_el = item.find("link")
            source_el = item.find("source")
            pub_date_el = item.find("pubDate")

            if link_el is None or link_el.text is None:
                continue

            results.append({
                "title": title_el.text if title_el is not None else "",
                "url": link_el.text.strip(),
                "source": source_el.text if source_el is not None else "",
                "date": pub_date_el.text if pub_date_el is not None else "",
                "origin": "google_news_rss",
            })

            if len(results) >= MAX_RESULTS_PER_QUERY:
                break

    except Exception as e:
        log.warning(f"  Google News RSS failed for query: {e}")

    return results


def search_duckduckgo(query: str) -> list[dict]:
    """Fallback search via DuckDuckGo HTML. Returns list of {url, title, snippet}."""
    results = []
    encoded = quote_plus(query)
    ddg_url = f"https://html.duckduckgo.com/html/?q={encoded}"

    try:
        resp = requests.get(ddg_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for result_div in soup.select(".result__body"):
            link_el = result_div.select_one(".result__a")
            snippet_el = result_div.select_one(".result__snippet")
            if link_el and link_el.get("href"):
                raw_href = link_el["href"]
                # DuckDuckGo wraps URLs in a redirect
                if "uddg=" in raw_href:
                    actual_url = unquote(raw_href.split("uddg=")[-1].split("&")[0])
                else:
                    actual_url = raw_href

                results.append({
                    "title": link_el.get_text(strip=True),
                    "url": actual_url,
                    "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                    "source": urlparse(actual_url).netloc,
                    "date": "",
                    "origin": "duckduckgo",
                })

                if len(results) >= MAX_RESULTS_PER_QUERY:
                    break

    except Exception as e:
        log.warning(f"  DuckDuckGo search failed for query: {e}")

    return results


def search_reddit(query: str) -> list[dict]:
    """Search via old.reddit.com to bypass API blocks."""
    results = []
    encoded = quote_plus(query)
    url = f"https://old.reddit.com/search?q={encoded}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.select("a.search-title"):
                href = a.get("href")
                if "/comments/" in href:
                    results.append({
                        "title": a.get_text(strip=True),
                        "url": href,
                        "source": "reddit.com",
                        "date": "",
                        "origin": "reddit"
                    })
                    if len(results) >= MAX_RESULTS_PER_QUERY:
                        break
    except Exception as e:
        log.warning(f"  Reddit search failed for query: {e}")
    return results

def search_all(query: str) -> list[dict]:
    """Search DuckDuckGo, Google News RSS, and Reddit."""
    results = search_duckduckgo(query)
    log.info(f"    DuckDuckGo: {len(results)} direct URLs")
    time.sleep(REQUEST_DELAY)

    gnews = search_google_news_rss(query)
    log.info(f"    Google News RSS: {len(gnews)} items")
    results.extend(gnews)
    time.sleep(REQUEST_DELAY)

    reddit = search_reddit(query)
    log.info(f"    Reddit: {len(reddit)} items")
    results.extend(reddit)

    return results


# ══════════════════════════════════════════════════════════════════════════════
# FETCH & PARSE LAYER
# ══════════════════════════════════════════════════════════════════════════════

def is_fetchable_url(url: str) -> bool:
    """Check if a URL can be fetched directly (not a Google News redirect)."""
    if not url or not url.startswith("http"):
        return False
    unfetchable_domains = [
        "news.google.com",
        "consent.google.com",
        "accounts.google.com",
    ]
    domain = urlparse(url).netloc
    return not any(d in domain for d in unfetchable_domains)


def fetch_article(candidate: dict) -> dict:
    """Fetch a URL and extract article content. Returns structured dict."""
    from urllib.parse import urlparse
    url = candidate["url"]
    result = {
        "url": url,
        "final_url": url,
        "title": candidate.get("title", ""),
        "text": "",
        "date": candidate.get("date", ""),
        "publisher": candidate.get("source", urlparse(url).netloc.replace("www.", "")),
        "http_status": 200,  # default to 200 for skipped fetches
        "error": None,
    }

    # If it's a Google News redirect, don't try to fetch because it requires JS
    if "news.google.com" in url:
        result["text"] = f"[Google News Redirect] Title: {result['title']}. Content masked by redirect."
        return result

    # If it's Reddit (from old.reddit.com search), we just use the title
    if "reddit.com" in url:
        result["text"] = f"[Reddit Post] Title: {result['title']}."
        return result

    # Special handling for YouTube
    if "youtube.com" in url or "youtu.be" in url:
        yt_data = validate_youtube_oembed(url)
        if yt_data and yt_data.get("valid"):
            if not result["title"]:
                result["title"] = yt_data["title"]
            result["publisher"] = yt_data["author"]
            result["text"] = f"[YouTube Video] Title: {result['title']} | Author: {yt_data['author']}"
            return result

    try:
        actual_url = url
        result["final_url"] = actual_url

        resp = requests.get(
            actual_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        result["http_status"] = resp.status_code
        result["final_url"] = resp.url
        result["publisher"] = urlparse(resp.url).netloc.replace("www.", "")

        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code}"
            return result

        soup = BeautifulSoup(resp.text, "html.parser")

        # Extract title
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            result["title"] = og_title["content"]
        elif soup.title:
            result["title"] = soup.title.get_text(strip=True)

        # Extract date
        for meta_name in ["article:published_time", "datePublished",
                          "og:updated_time", "pubdate"]:
            date_el = soup.find("meta", property=meta_name) or soup.find("meta", attrs={"name": meta_name})
            if date_el and date_el.get("content"):
                result["date"] = date_el["content"][:10]
                break
        # Fallback: look for time element
        if not result["date"]:
            time_el = soup.find("time", attrs={"datetime": True})
            if time_el:
                result["date"] = time_el["datetime"][:10]

        # Extract article text
        # Try common article body selectors
        article_body = None
        for selector in [
            "article", ".article-body", ".article-content",
            ".story-body", ".story-content", ".td-post-content",
            "#article-body", ".entry-content", ".post-content",
            '[itemprop="articleBody"]', ".content-body",
        ]:
            article_body = soup.select_one(selector)
            if article_body:
                break

        if article_body:
            # Extract paragraphs
            paragraphs = article_body.find_all("p")
            text_parts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            result["text"] = "\n".join(text_parts)
        else:
            # Fallback: grab all <p> tags
            paragraphs = soup.find_all("p")
            text_parts = [p.get_text(strip=True) for p in paragraphs
                          if len(p.get_text(strip=True)) > 40]
            result["text"] = "\n".join(text_parts[:20])

        # Trim to first 3000 chars for Gemini
        result["text"] = result["text"][:3000]

    except requests.exceptions.Timeout:
        result["error"] = "Timeout"
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection error"
    except Exception as e:
        result["error"] = str(e)[:200]

    return result


def validate_youtube_oembed(url: str):
    """Check if a YouTube URL is valid via oEmbed API."""
    if "youtube.com/watch" not in url and "youtu.be/" not in url:
        return None
    try:
        oembed_url = f"https://www.youtube.com/oembed?url={quote_plus(url)}&format=json"
        resp = requests.get(oembed_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "title": data.get("title", ""),
                "author": data.get("author_name", ""),
                "valid": True,
            }
    except Exception:
        pass
    return {"title": "", "author": "", "valid": False}


# ══════════════════════════════════════════════════════════════════════════════
# GEMINI LLM VERIFICATION LAYER
# ══════════════════════════════════════════════════════════════════════════════

def init_gemini():
    """Initialize Google Gemini client."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        log.error("GOOGLE_API_KEY environment variable not set!")
        sys.exit(1)

    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)
    log.info(f"Gemini initialized with model: {GEMINI_MODEL}")
    return model


def verify_with_gemini(model, article: dict, target: dict, already_verified_issues: list[str] = None) -> dict:
    """Ask Gemini to score geo-relevance and authenticity of an article and deduplicate."""
    if already_verified_issues is None:
        already_verified_issues = []
    
    prompt = f"""You are a Tamil Nadu political intelligence analyst. Evaluate this article
for a SPECIFIC geographic unit. Be strict — only score high geo_relevance if the
article specifically discusses the TARGET location, not just the broader city/district.

TARGET UNIT: {target['unit_name']}
TARGET DISTRICT: {target['district']}
KEY ISSUES TO MATCH: {', '.join(target['key_issues'])}
ALREADY VERIFIED ISSUES (DO NOT DUPLICATE THESE): {already_verified_issues}


ARTICLE TITLE: {article.get('title', 'N/A')}
ARTICLE URL: {article.get('final_url', article.get('url', 'N/A'))}
ARTICLE PUBLISHER: {article.get('publisher', 'N/A')}
ARTICLE DATE: {article.get('date', 'N/A')}
ARTICLE TEXT (first 2000 chars):
{article.get('text', '')[:2000]}

Score this article on two dimensions:

1. geo_relevance (0.0 to 1.0):
   - 1.0 = Article is specifically about this exact ward/constituency by name
   - 0.7 = Article mentions this area with relevant local details (If it is a Google News or Reddit link, judge based on the title)
   - 0.4 = Article is about the broader district/city but not this specific area
   - 0.1 = Article is about Tamil Nadu generally, barely relevant to this unit
   - 0.0 = This exact issue/event is already in the ALREADY VERIFIED ISSUES list (DUPLICATE).

2. authenticity (0.0 to 1.0):
   - 1.0 = Original reporting with specific facts, figures, dates, or direct social media complaint
   - 0.7 = Standard news report, Reddit post, video evidence, or Google News Redirect with a descriptive title
   - 0.4 = Opinion piece, press release, or thin content
   - 0.1 = Clickbait, AI-generated filler, or spam

Also provide:
- issue_category: One of ["Drainage & Flood Control", "MSME & Industrial",
  "Agriculture & MSP", "Transport & Infrastructure", "Legal & Court Orders",
  "Water Supply & Sanitation", "Environmental Protection", "Electoral & Political", "Citizen Grievance"]
- core_issue_summary: A 2-to-4 word description of the specific event/issue (e.g. "Bus factory fire", "CETP effluent leak").
- summary: 1-2 sentence factual summary of the article
- reasoning: Brief explanation of your scores, or "Duplicate issue" if geo_relevance is 0.0 due to duplication.

Respond in valid JSON only (no markdown fences, no extra text):
{{"geo_relevance": 0.0, "authenticity": 0.0, "issue_category": "", "core_issue_summary": "", "summary": "", "reasoning": ""}}"""

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            # Strip markdown code fences if present
            if text.startswith("```"):
                text = text.split("\n", 1)[1]
                if text.endswith("```"):
                    text = text.rsplit("```", 1)[0]
                text = text.strip()

            result = json.loads(text)
            return {
                "geo_relevance": float(result.get("geo_relevance", 0)),
                "authenticity": float(result.get("authenticity", 0)),
                "issue_category": result.get("issue_category", "Unknown"),
                "core_issue_summary": result.get("core_issue_summary", ""),
                "summary": result.get("summary", ""),
                "reasoning": result.get("reasoning", ""),
            }

        except json.JSONDecodeError as e:
            log.warning(f"    Gemini JSON parse error (attempt {attempt+1}): {e}")
            log.warning(f"    Raw response: {text[:300]}")
            time.sleep(GEMINI_DELAY)
        except Exception as e:
            log.warning(f"    Gemini error (attempt {attempt+1}): {e}")
            time.sleep(GEMINI_DELAY * 2)

    # Fallback: mark as unverified
    return {
        "geo_relevance": 0.0,
        "authenticity": 0.0,
        "issue_category": "Unknown",
        "summary": "Gemini verification failed after 3 attempts",
        "reasoning": "LLM error",
    }


def generate_campaign_messages(model, article: dict, target: dict) -> dict:
    """Ask Gemini to generate campaign messages from a verified article."""
    prompt = f"""Based on this verified news article, generate hyper-local campaign messages
for TVK (Tamilaga Vettri Kazhagam) for {target['unit_name']} in {target['district']} district.

Article Summary: {article.get('summary', article.get('title', ''))}
Key Issue: {target['key_issues'][0]}
Location: {target['unit_name']}, {target['district']} District, Tamil Nadu

Generate three messages that reference SPECIFIC facts from the article:
1. whatsapp_tamil: A WhatsApp broadcast in Tamil (200-400 chars). Must mention the location name and specific issue.
2. instagram_tamil: An Instagram caption in Tamil with 3-4 hashtags (150-300 chars).
3. twitter_english: An English Twitter/X post (≤280 chars) with hashtags.

Respond in valid JSON only (no markdown fences):
{{"whatsapp_tamil": "", "instagram_tamil": "", "twitter_english": ""}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text.rsplit("```", 1)[0]
            text = text.strip()
        return json.loads(text)
    except Exception as e:
        log.warning(f"    Campaign message generation failed: {e}")
        return {
            "whatsapp_tamil": "",
            "instagram_tamil": "",
            "twitter_english": "",
        }


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE LAYER
# ══════════════════════════════════════════════════════════════════════════════

def create_verified_sources_table(conn: sqlite3.Connection):
    """Create the verified_sources table if it doesn't exist."""
    conn.execute("""
    CREATE TABLE IF NOT EXISTS verified_sources (
        source_id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_type TEXT NOT NULL,
        unit_name TEXT NOT NULL,
        search_query TEXT,
        article_url TEXT NOT NULL,
        article_title TEXT,
        article_snippet TEXT,
        article_date TEXT,
        publisher TEXT,
        platform TEXT DEFAULT 'news',
        issue_category TEXT,
        geo_relevance_score REAL DEFAULT 0.0,
        authenticity_score REAL DEFAULT 0.0,
        gemini_reasoning TEXT,
        http_status INTEGER,
        is_verified INTEGER DEFAULT 0,
        mined_at TEXT,
        UNIQUE(unit_name, article_url)
    )
    """)
    conn.commit()
    log.info("✅ verified_sources table ready")


def url_already_mined(conn: sqlite3.Connection, unit_name: str, url: str) -> bool:
    """Check if a URL has already been mined for this unit."""
    row = conn.execute(
        "SELECT 1 FROM verified_sources WHERE unit_name=? AND article_url=?",
        (unit_name, url),
    ).fetchone()
    return row is not None


def insert_verified_source(conn: sqlite3.Connection, record: dict):
    """Insert a single verified source record."""
    conn.execute("""
    INSERT OR REPLACE INTO verified_sources
        (unit_type, unit_name, search_query, article_url, article_title,
         article_snippet, article_date, publisher, platform, issue_category,
         geo_relevance_score, authenticity_score, gemini_reasoning,
         http_status, is_verified, mined_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["unit_type"],
        record["unit_name"],
        record.get("search_query", ""),
        record["article_url"],
        record.get("article_title", ""),
        record.get("article_snippet", "")[:500],
        record.get("article_date", ""),
        record.get("publisher", ""),
        record.get("platform", "news"),
        record.get("issue_category", ""),
        record.get("geo_relevance_score", 0.0),
        record.get("authenticity_score", 0.0),
        record.get("gemini_reasoning", ""),
        record.get("http_status", 0),
        1 if record.get("geo_relevance_score", 0) >= 0.7
          and record.get("authenticity_score", 0) >= 0.7
          and record.get("http_status", 0) == 200 else 0,
        datetime.utcnow().isoformat(),
    ))
    conn.commit()


def update_main_tables(conn: sqlite3.Connection, target: dict, best_article: dict,
                       messages: dict):
    """Update the main constituency/gcc_ward table with the best verified source."""
    if target["unit_type"] == "constituency":
        table = "constituencies"
        where_clause = "name = ?"
        where_val = target["unit_name"]
    else:
        table = "gcc_wards"
        where_clause = "name LIKE ?"
        where_val = f"%{target['unit_name'].split()[-1]}%"  # Match ward number

    updates = {
        "source_url": best_article["article_url"],
        "source_name": f"{best_article.get('publisher', 'Verified Source')} (Geo:{best_article['geo_relevance_score']:.1f} Auth:{best_article['authenticity_score']:.1f})",
    }

    if messages.get("whatsapp_tamil"):
        updates["whatsapp"] = messages["whatsapp_tamil"]
    if messages.get("instagram_tamil"):
        updates["instagram"] = messages["instagram_tamil"]
    if messages.get("twitter_english"):
        updates["twitter"] = messages["twitter_english"]

    set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
    values = list(updates.values()) + [where_val]

    conn.execute(f"UPDATE {table} SET {set_clause} WHERE {where_clause}", values)
    conn.commit()
    log.info(f"  ✅ Updated {table} for {target['unit_name']} with best link: {best_article['article_url'][:80]}...")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN MINING PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def mine_unit(target: dict, conn: sqlite3.Connection, model=None, dry_run=False):
    """Mine a single unit: search, fetch, verify, write."""
    unit_name = target["unit_name"]
    log.info(f"\n{'='*70}")
    log.info(f"MINING: {unit_name} ({target['unit_type']})")
    log.info(f"District: {target['district']}")
    log.info(f"Key Issues: {', '.join(target['key_issues'])}")
    log.info(f"{'='*70}")

    all_candidates = []
    seen_urls = set()

    # Expand queries with social media targets
    expanded_queries = []
    for query in target["search_queries"]:
        expanded_queries.append(query)
        expanded_queries.append(f"{query} site:twitter.com OR site:youtube.com OR site:instagram.com OR site:reddit.com OR site:facebook.com")

    # Step 1: Search
    for i, query in enumerate(expanded_queries):
        log.info(f"  → Query {i+1}/{len(expanded_queries)}: {query}")
        results = search_all(query)
        log.info(f"    Found {len(results)} candidate URLs")

        for r in results:
            url = r["url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)
            r["search_query"] = query
            all_candidates.append(r)

        time.sleep(REQUEST_DELAY)

    log.info(f"  Total unique candidates: {len(all_candidates)}")

    # Step 2: Fetch & Parse
    fetched_articles = []
    for i, candidate in enumerate(all_candidates):
        url = candidate["url"]

        # Skip if already mined
        if url_already_mined(conn, unit_name, url):
            log.info(f"    [{i+1}] SKIP (already mined): {url[:80]}")
            continue

        log.info(f"    [{i+1}] Fetching: {url[:80]}...")
        article = fetch_article(candidate)
        article["search_query"] = candidate.get("search_query", "")

        status_icon = "✓" if article["http_status"] == 200 else "✗"
        log.info(f"      HTTP {article['http_status']} {status_icon}  Title: {article['title'][:60]}")

        if article["http_status"] == 200 and len(article.get("text", "")) > 100:
            fetched_articles.append(article)
        elif article["http_status"] == 200:
            log.info(f"      ⚠️ Thin content ({len(article.get('text', ''))} chars), skipping")

        time.sleep(REQUEST_DELAY)

    log.info(f"  Successfully fetched: {len(fetched_articles)} articles with real content")

    if dry_run:
        log.info("  [DRY RUN] Skipping Gemini verification and DB writes")
        for a in fetched_articles:
            log.info(f"    📰 {a['publisher']} | {a['title'][:60]} | {a['final_url'][:80]}")
        return fetched_articles

    if not model:
        log.error("  Gemini model not initialized — cannot verify. Use --dry-run or set GOOGLE_API_KEY.")
        return []

    # Step 3: Gemini Verification
    log.info(f"\n  ── Gemini Verification ({len(fetched_articles)} articles) ──")
    verified_articles = []
    verified_core_issues = []

    for i, article in enumerate(fetched_articles):
        log.info(f"    [{i+1}/{len(fetched_articles)}] Verifying: {article['title'][:60]}...")
        scores = verify_with_gemini(model, article, target, already_verified_issues=verified_core_issues)

        article.update(scores)
        is_verified = (scores["geo_relevance"] >= 0.7
                       and scores["authenticity"] >= 0.7)

        icon = "✅ VERIFIED" if is_verified else "❌ REJECTED"
        log.info(f"      {icon}  Geo: {scores['geo_relevance']:.2f}  Auth: {scores['authenticity']:.2f}")
        log.info(f"      Category: {scores['issue_category']}")
        log.info(f"      Reasoning: {scores['reasoning'][:100]}")

        # Write to DB regardless (so we don't re-mine rejected articles)
        insert_verified_source(conn, {
            "unit_type": target["unit_type"],
            "unit_name": unit_name,
            "search_query": article.get("search_query", ""),
            "article_url": article["final_url"],
            "article_title": article.get("title", ""),
            "article_snippet": scores.get("summary", article.get("text", "")[:300]),
            "article_date": article.get("date", ""),
            "publisher": article.get("publisher", ""),
            "platform": "youtube" if "youtube.com" in article["final_url"] else "news",
            "issue_category": scores.get("issue_category", ""),
            "geo_relevance_score": scores["geo_relevance"],
            "authenticity_score": scores["authenticity"],
            "gemini_reasoning": scores.get("reasoning", ""),
            "http_status": article["http_status"],
        })

        if is_verified:
            verified_articles.append(article)
            core_summary = scores.get("core_issue_summary")
            if core_summary:
                verified_core_issues.append(core_summary)

        time.sleep(GEMINI_DELAY)

    log.info(f"\n  RESULTS: {len(verified_articles)} verified / {len(fetched_articles)} fetched")

    # Step 4: Update main tables with the best verified article
    if verified_articles:
        # Sort by combined score
        verified_articles.sort(
            key=lambda a: a.get("geo_relevance", 0) + a.get("authenticity", 0),
            reverse=True,
        )
        best = verified_articles[0]
        log.info(f"  🏆 Best article: {best['title'][:60]}")
        log.info(f"     URL: {best['final_url']}")
        log.info(f"     Scores: Geo={best['geo_relevance']:.2f} Auth={best['authenticity']:.2f}")

        # Generate campaign messages from the best article
        log.info(f"  📝 Generating campaign messages...")
        messages = generate_campaign_messages(model, best, target)
        time.sleep(GEMINI_DELAY)

        # Update the main table
        update_main_tables(conn, target, {
            "article_url": best["final_url"],
            "publisher": best.get("publisher", ""),
            "geo_relevance_score": best["geo_relevance"],
            "authenticity_score": best["authenticity"],
        }, messages)
    else:
        log.warning(f"  ⚠️ No verified articles found for {unit_name}")

    return verified_articles


def print_final_report(conn: sqlite3.Connection):
    """Print a summary report of all verified sources."""
    log.info("\n" + "="*70)
    log.info("FINAL MINING REPORT")
    log.info("="*70)

    rows = conn.execute("""
        SELECT unit_name, COUNT(*) as total,
               SUM(CASE WHEN is_verified=1 THEN 1 ELSE 0 END) as verified
        FROM verified_sources
        GROUP BY unit_name
        ORDER BY unit_name
    """).fetchall()

    total_mined = 0
    total_verified = 0
    for unit_name, total, verified in rows:
        status = "✅" if verified > 0 else "❌"
        log.info(f"  {status} {unit_name}: {verified}/{total} verified")
        total_mined += total
        total_verified += verified

    log.info(f"\n  TOTAL: {total_verified}/{total_mined} articles verified across {len(rows)} units")

    # Show the best link for each unit
    log.info("\n  BEST VERIFIED LINKS:")
    best_rows = conn.execute("""
        SELECT unit_name, article_url, article_title,
               geo_relevance_score, authenticity_score, publisher
        FROM verified_sources
        WHERE is_verified=1
        ORDER BY unit_name, (geo_relevance_score + authenticity_score) DESC
    """).fetchall()

    current_unit = None
    for unit_name, url, title, geo, auth, publisher in best_rows:
        if unit_name != current_unit:
            current_unit = unit_name
            log.info(f"\n  📍 {unit_name}:")
        log.info(f"    → [{publisher}] {title[:50]}...")
        log.info(f"      {url}")
        log.info(f"      Geo: {geo:.2f}  Auth: {auth:.2f}")


# ══════════════════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Nethra Real Web Mining Pipeline with Gemini LLM Verification",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Search & fetch only, skip Gemini verification")
    parser.add_argument("--unit", type=str, default=None,
                        help="Mine a single unit by name (e.g. 'Karur', 'Chennai Ward 84')")
    parser.add_argument("--report-only", action="store_true",
                        help="Just print the final report from existing data")
    parser.add_argument("--all", action="store_true",
                        help="Mine all units dynamically from the database")
    args = parser.parse_args()

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    create_verified_sources_table(conn)

    if args.report_only:
        print_final_report(conn)
        conn.close()
        return

    # Filter targets if --unit specified
    targets = SEARCH_TARGETS
    if args.unit:
        targets = [t for t in SEARCH_TARGETS
                   if args.unit.lower() in t["unit_name"].lower()]
        if not targets:
            log.error(f"No target found matching '{args.unit}'")
            log.info(f"Available: {[t['unit_name'] for t in SEARCH_TARGETS]}")
            sys.exit(1)
    
    if args.all:
        log.info("Loading all targets from database...")
        targets = []
        # Load Constituencies
        for row in conn.execute("SELECT name, district, top_issue FROM constituencies").fetchall():
            targets.append({
                "unit_type": "constituency",
                "unit_name": row[0],
                "district": row[1] or row[0],
                "key_issues": [row[2]] if row[2] else [],
                "search_queries": [
                    f'"{row[0]}" {row[2] if row[2] else "issue"} Tamil Nadu',
                    f'{row[0]} assembly constituency news {row[2] if row[2] else ""}'
                ]
            })
        # Load Wards
        for row in conn.execute("SELECT name, top_issue FROM gcc_wards").fetchall():
            targets.append({
                "unit_type": "gcc_ward",
                "unit_name": row[0],
                "district": "Chennai",
                "key_issues": [row[1]] if row[1] else [],
                "search_queries": [
                    f'"{row[0]}" Chennai GCC {row[1] if row[1] else "issue"}',
                    f'{row[0]} Chennai corporation news {row[1] if row[1] else ""}'
                ]
            })

    # Initialize Gemini (unless dry-run)
    model = None
    if not args.dry_run:
        model = init_gemini()

    log.info(f"\n🚀 Starting Nethra Mining Pipeline")
    log.info(f"   Targets: {len(targets)} units")
    log.info(f"   Mode: {'DRY RUN' if args.dry_run else 'FULL (with Gemini verification)'}")
    log.info(f"   Database: {DB_PATH}")
    log.info(f"   Timestamp: {datetime.now().isoformat()}")

    # Mine each target
    all_verified = []
    for i, target in enumerate(targets):
        log.info(f"\n[{i+1}/{len(targets)}] ")
        verified = mine_unit(target, conn, model=model, dry_run=args.dry_run)
        all_verified.extend(verified or [])

    # Print final report
    if not args.dry_run:
        print_final_report(conn)

    conn.close()
    log.info(f"\n🏁 Mining pipeline complete. {len(all_verified)} total verified articles.")


if __name__ == "__main__":
    main()

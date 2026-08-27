#!/usr/bin/env python3
"""
Chinese News Spider — Scrapes headlines from 4 Chinese news websites.
Each site has a different structure and requires a different approach.

Usage:
  python3 spider.py                     # Crawl all 4 sites
  python3 spider.py --site cctv         # Only CCTV
  python3 spider.py --site ifeng        # Only Phoenix TV
  python3 spider.py --site ctinews      # Only CTi News
  python3 spider.py --site zaobao       # Only Lianhe Zaobao

Output: JSON lines, one story per line:
  {"source":"CCTV","title":"...","url":"...","date":"2026-05-14"}
"""

import sys
import json
import re
import subprocess
import html
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def curl(url, timeout=15):
    """Fetch a URL with curl."""
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", str(timeout), "-L", url,
             "-H", f"User-Agent: {USER_AGENT}",
             "-H", "Accept-Language: zh-CN,zh;q=0.9"],
            capture_output=True, text=True, timeout=timeout+5
        )
        return r.stdout
    except Exception as e:
        return f""

def today_str():
    return datetime.now().strftime("%Y/%m/%d")

def today_compact():
    return datetime.now().strftime("%Y%m%d")

def recent_dates(days=2):
    """Return list of date strings for the last N days in both / and _ formats."""
    from datetime import timedelta
    results_slash = []
    results_underscore = []
    for d in range(days):
        dt = datetime.now() - timedelta(days=d)
        results_slash.append(dt.strftime("%Y/%m/%d"))
        results_underscore.append(dt.strftime("%Y_%m_%d"))
    return results_slash, results_underscore


# ============================================================
# 1. CCTV / 央视 (news.cctv.com)
#    Strategy: Parse server-rendered HTML. Headlines in <a> tags
#    with URLs matching /YYYY/MM/DD/ARTI{id}.shtml
# ============================================================
def crawl_cctv():
    stories = []
    html_content = curl("https://news.cctv.com/")
    if not html_content:
        return stories

    # Extract article links with titles from the HTML
    # Pattern: <a href="https://news.cctv.com/2026/05/14/ARTI...shtml" ...>TITLE</a>
    slash_dates, _ = recent_dates(days=2)
    seen_urls = set()
    for today in slash_dates:
        escaped_today = today.replace("/", "\\/")
        pattern = rf'href="(https://news\.cctv\.com/{escaped_today}/ARTI[A-Za-z0-9]+\.shtml)"[^>]*>([^<]+)</a>'

        for match in re.finditer(pattern, html_content):
            url = match.group(1)
            title = html.unescape(match.group(2)).strip()
            title = re.sub(r'\s+', ' ', title)
            if url not in seen_urls and len(title) > 5 and len(title) < 200:
                seen_urls.add(url)
                stories.append({
                    "source": "CCTV",
                    "title": title,
                    "url": url,
                    "date": today.replace("/", "-")
                })

    # Also try the TV subdomain
    html_tv = curl("https://tv.cctv.com/")
    if html_tv:
        for today in slash_dates:
            escaped_today2 = today.replace("/", "\\/")
            pattern_tv = rf'href="(https://tv\.cctv\.com/{escaped_today2}/VIDE[A-Za-z0-9]+\.shtml)"[^>]*>([^<]+)</a>'
            for match in re.finditer(pattern_tv, html_tv):
                url = match.group(1)
                title = html.unescape(match.group(2)).strip()
                title = re.sub(r'\s+', ' ', title)
                if url not in seen_urls and len(title) > 5:
                    seen_urls.add(url)
                    stories.append({
                        "source": "CCTV",
                        "title": title,
                        "url": url,
                        "date": today.replace("/", "-")
                    })

    # Deduplicate by title similarity
    final = []
    titles_seen = set()
    for s in stories:
        key = s["title"][:30]
        if key not in titles_seen:
            titles_seen.add(key)
            final.append(s)

    return final[:10]


# ============================================================
# 2. 凤凰卫视 / Phoenix TV (ifeng.com)
#    Strategy: Extract headlines from embedded 'allData' JSON
#    in the HTML source. No JS execution needed.
# ============================================================
def crawl_ifeng():
    """Extract headlines from news.ifeng.com's embedded 'newsstream' JSON.

    The news channel homepage embeds a JSON array whose items carry correctly
    paired title/url/newsTime fields (unlike www.ifeng.com, where the title↔url
    pairing via regex fallback is unreliable and produces broken links).
    """
    stories = []
    html_content = curl("https://news.ifeng.com/")
    if not html_content:
        return stories

    idx = html_content.find('"newsstream":')
    if idx == -1:
        return stories
    start = html_content.find('[', idx)
    if start == -1:
        return stories

    # Locate the matching closing bracket (handles nested [] and strings).
    depth = 0
    end = start
    in_str = False
    esc = False
    while end < len(html_content):
        c = html_content[end]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    break
        end += 1

    try:
        arr = json.loads(html_content[start:end + 1])
    except (json.JSONDecodeError, TypeError):
        return stories

    seen = set()
    for item in arr:
        if not isinstance(item, dict):
            continue
        title = (item.get("title") or "").strip()
        url = (item.get("url") or "").strip()
        if item.get("type") != "article" or not title or not url:
            continue
        if url.startswith("//"):
            url = "https:" + url
        news_time = (item.get("newsTime") or "").strip()
        date = news_time.split(" ")[0] if news_time else datetime.now().strftime("%Y-%m-%d")
        key = title[:40]
        if key in seen:
            continue
        seen.add(key)
        stories.append({
            "source": "凤凰卫视",
            "title": html.unescape(title).strip(),
            "url": url,
            "date": date,
        })

    return stories[:10]


# ============================================================
# 3. 中天新闻 / CTi News (ctinews.com)
#    Strategy: Use the RSS feed at /rss/google-news.xml
#    (Easy mode: RSS gives titles, URLs, dates, descriptions)
# ============================================================
def crawl_ctinews():
    stories = []
    rss_xml = curl("https://ctinews.com/rss/google-news.xml")
    if not rss_xml:
        return stories

    # Parse RSS items with regex (simple, no XML parsing required)
    items = re.findall(r'<item>(.*?)</item>', rss_xml, re.DOTALL)
    for item in items:
        title_m = re.search(r'<title>(?:<!\[CDATA\[)?([^\]]+)(?:\]\]>)?</title>', item)
        link_m = re.search(r'<link>(.*?)</link>', item)
        desc_m = re.search(r'<description>(?:<!\[CDATA\[)?([^\]]+)(?:\]\]>)?</description>', item)
        date_m = re.search(r'<pubDate>(.*?)</pubDate>', item)

        if title_m and link_m:
            title = html.unescape(title_m.group(1)).strip()
            # Remove CDATA wrappers if any
            title = re.sub(r'^\s*<!\[CDATA\[|\]\]>\s*$', '', title).strip()
            url = link_m.group(1).strip()
            description = html.unescape(desc_m.group(1)).strip() if desc_m else ""
            description = re.sub(r'^\s*<!\[CDATA\[|\]\]>\s*$', '', description).strip()
            pub_date = date_m.group(1).strip() if date_m else ""

            if len(title) > 5 and len(title) < 300:
                stories.append({
                    "source": "中天新闻",
                    "title": title,
                    "url": url,
                    "date": pub_date,
                    "description": description[:300]
                })

    return stories[:15]


# ============================================================
# 4. 联合早报 / Lianhe Zaobao (zaobao.com.sg)
#    Strategy: Extract from embedded JSON in React Remix SPA.
#    Article data has fields _25 (title), _37 (url path).
#    Also use sitemap for URL discovery.
# ============================================================
def crawl_zaobao():
    stories = []
    html_content = curl("https://www.zaobao.com.sg/")
    if not html_content:
        return stories

    # Method: Match titles (>TITLE<) followed nearby by story URLs
    # In Zaobao's HTML, titles appear before their story URL paths
    pattern = r'>([^<]{10,80})<[\s\S]{0,600}?(/news/[a-z-]+/story\d{8}-\d+)'
    seen_titles = set()
    for match in re.finditer(pattern, html_content):
        title = html.unescape(match.group(1)).strip()
        title = re.sub(r'\s+', ' ', title)
        url_path = match.group(2)
        url = f"https://www.zaobao.com.sg{url_path}"

        # Dedup by first 30 chars of title
        key = title[:30]
        if key not in seen_titles and len(title) > 8:
            seen_titles.add(key)
            stories.append({
                "source": "联合早报",
                "title": title,
                "url": url,
                "date": datetime.now().strftime("%Y-%m-%d")
            })

    return stories[:10]


# ============================================================
# 5. 观察者网 (guancha.cn)
#    Strategy: Parses server-rendered HTML. Article URLs match
#    pattern /{section}/{YYYY}_{MM}_{DD}_{id}.shtml
#    Example: /politics/2026_05_14_817046.shtml
# ============================================================
def crawl_guancha():
    stories = []
    html_content = curl("https://www.guancha.cn/")
    if not html_content:
        return stories

    _, underscore_dates = recent_dates(days=2)
    seen = set()
    for date_str in underscore_dates:
        pattern = rf'href="(/([a-z]+)/{date_str}_(\d+)\.shtml)"[^>]*>([^<]+)'
        for match in re.finditer(pattern, html_content):
            path = match.group(1)
            title = html.unescape(match.group(4)).strip()
            title = re.sub(r'\s+', ' ', title)
            url = f"https://www.guancha.cn{path}"

            key = title[:30]
            if key not in seen and len(title) > 5 and "阅读" not in title:
                seen.add(key)
                stories.append({
                    "source": "观察者网",
                    "title": title,
                    "url": url,
                    "date": date_str.replace("_", "-")
                })

    return stories[:15]


# ============================================================
# 6. 参考消息 (cankaoxiaoxi.com)
#    Strategy: React SPA — all content loaded via JS.
#    API requires authentication headers.
#    FALLBACK: Use web_search in the cronjob.
# ============================================================
def crawl_cankaoxiaoxi():
    """参考消息 (cankaoxiaoxi.com)

    The website homepage is a React SPA with a protected config API, but the
    underlying channel content is served as public static JSON on the app
    domain (ckxxapp.ckxx.net). Each channel's article list is available at:
        https://ckxxapp.ckxx.net/json/channel/{alias}/list.json
    The channel aliases are stable, so we hardcode them and filter to recent
    articles (last 2 days).
    """
    from datetime import datetime, timedelta
    channels = {
        "gj": "国际",
        "zhongguo": "中国",
        "guandian": "观点",
    }
    recent = [(datetime.now() - timedelta(days=d)).strftime("%Y-%m-%d") for d in range(2)]
    seen = set()
    stories = []
    for alias in channels:
        raw = curl(f"https://ckxxapp.ckxx.net/json/channel/{alias}/list.json")
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue
        for item in data.get("list", []):
            d = item.get("data", {}) if isinstance(item, dict) else {}
            title = (d.get("title") or d.get("shorttitle") or "").strip()
            url = (d.get("url") or "").strip()
            pub = (d.get("publishTime") or d.get("createtime") or "").strip()
            if not title or not url:
                continue
            date_part = pub.split(" ")[0] if pub else ""
            if date_part and date_part not in recent:
                continue
            key = title[:30]
            if key in seen:
                continue
            seen.add(key)
            stories.append({
                "source": "参考消息",
                "title": title,
                "url": url,
                "date": date_part or datetime.now().strftime("%Y-%m-%d"),
            })
    return stories[:15]


# ============================================================
# Main
# ============================================================
def main():
    sites = {
        "cctv": ("CCTV / 央视", crawl_cctv),
        "ifeng": ("凤凰卫视 / Phoenix TV", crawl_ifeng),
        "ctinews": ("中天新闻 / CTi News", crawl_ctinews),
        "zaobao": ("联合早报 / Lianhe Zaobao", crawl_zaobao),
        "guancha": ("观察者网", crawl_guancha),
        "cankaoxiaoxi": ("参考消息", crawl_cankaoxiaoxi),
    }

    # Filter by --site argument
    if "--site" in sys.argv:
        idx = sys.argv.index("--site") + 1
        if idx < len(sys.argv):
            target = sys.argv[idx]
            sites = {k: v for k, v in sites.items() if k == target}

    total = 0
    for key, (name, crawler) in sites.items():
        try:
            print(f"--- {name} ---", file=sys.stderr)
            stories = crawler()
            for s in stories:
                print(json.dumps(s, ensure_ascii=False))
                total += 1
            print(f"  → {len(stories)} stories found", file=sys.stderr)
        except Exception as e:
            print(f"  → ERROR: {e}", file=sys.stderr)

    print(f"\nTotal: {total} stories", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build World News Brief with detailed article pages."""

import base64, json, re, html, subprocess, sys, random, os
from datetime import datetime
from collections import defaultdict

TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = "JimJian2023"
REPO = "world-news-brief"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
PROJECT_DIR = "/home/jianning/Hemers Agent/WorldNewsBrief"

def curl(url, timeout=10):
    try:
        r = subprocess.run(["curl", "-s", "--max-time", str(timeout), "-L", url, "-H", f"User-Agent: {UA}"], capture_output=True, text=True, timeout=timeout+5)
        return r.stdout
    except: return ""

def parse_rss(url, source):
    xml = curl(url)
    if not xml: return []
    items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
    results = []
    from datetime import timedelta
    allowable = [(datetime.now() - timedelta(days=d)).strftime("%d %b %Y") for d in range(2)]
    for item in items:
        title_m = re.search(r'<title>(?:<!\[CDATA\[)?([^\]>]+)', item)
        link_m = re.search(r'<link>(.*?)</link>', item)
        desc_m = re.search(r'<description>(?:<!\[CDATA\[)?([^\]>]+)', item)
        date_m = re.search(r'<pubDate>(.*?)</pubDate>', item)
        if title_m and link_m:
            title = re.sub(r'<!\[CDATA\[|\]\]>', '', title_m.group(1)).strip()
            url = link_m.group(1).strip()
            desc = re.sub(r'<!\[CDATA\[|\]\]>', '', desc_m.group(1)).strip()[:500] if desc_m else ""
            pubdate = date_m.group(1).strip() if date_m else ""
            if any(d in pubdate for d in allowable):
                results.append({"source": source, "headline": html.unescape(title), "url": url, "desc": html.unescape(desc), "date": pubdate})
    return results

def generate_article(item, lang="en"):
    headline = item["headline"]
    source = item["source"]
    desc = item.get("desc", "")
    if lang == "en":
        content = f"<p>{desc}</p>" if desc else f"<p>{headline}</p>"
        zh = f"<p>{headline}</p><p>（该新闻由{source}报道）</p>" if desc else ""
        return content, zh
    else:
        return f"<p>{headline}</p>"

def build_headline_html(articles, panel):
    items = []
    for art in articles:
        aid = art.get("id", f"a{len(items)}")
        items.append(f'<a href="#" onclick="openArticle(\'{panel}\',\'{aid}\');return false" class="headline-item flex items-center justify-between gap-3">'
                     f'<span class="font-semibold text-sm sm:text-base text-slate-900 dark:text-white">{art["headline"]}</span>'
                     f'<span class="text-xs text-slate-400 dark:text-slate-500 shrink-0 whitespace-nowrap">{art["source"]}</span>'
                     f'</a>')
    return "\n".join(items)

def sample_evenly(items, max_total, min_per_source=1):
    by_source = defaultdict(list)
    for item in items:
        by_source[item["source"]].append(item)
    result = []
    for src in by_source:
        src_items = by_source[src]
        random.shuffle(src_items)
        take = min(min_per_source, len(src_items))
        result.extend(src_items[:take])
        by_source[src] = src_items[take:]
    remaining = []
    for src in by_source:
        remaining.extend(by_source[src])
    random.shuffle(remaining)
    result.extend(remaining[:max_total - len(result)])
    return result[:max_total]

def main():
    print("Fetching RSS feeds...", file=sys.stderr)
    en_world = []
    en_tech = []
    for item in parse_rss("https://feeds.bbci.co.uk/news/world/rss.xml", "BBC"): en_world.append(item)
    for item in parse_rss("https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "New York Times"): en_world.append(item)
    for item in parse_rss("https://www.rt.com/rss/news/", "RT"): en_world.append(item)
    for item in parse_rss("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera"): en_world.append(item)
    for item in parse_rss("https://feeds.bbci.co.uk/news/technology/rss.xml", "BBC"): en_tech.append(item)
    for item in parse_rss("https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "New York Times"): en_tech.append(item)
    print(f"  EN World: {len(en_world)}, EN Tech: {len(en_tech)}", file=sys.stderr)

    print("Running spider...", file=sys.stderr)
    r = subprocess.run(["python3", f"{PROJECT_DIR}/spider.py"], capture_output=True, text=True, timeout=60)
    cn_raw = []
    for line in r.stdout.strip().split("\n"):
        if line.startswith("{"):
            try: cn_raw.append(json.loads(line))
            except: pass
    random.shuffle(cn_raw)
    cn_world = [s for s in cn_raw if not any(kw in s.get("title","") for kw in ["科技","AI","芯片","数字","量子","6G","5G","智能","数据","软件","华为","英伟达","苹果","特斯拉","微软","谷歌","自动驾驶","5G","6G"])]
    cn_tech = [s for s in cn_raw if any(kw in s.get("title","") for kw in ["科技","AI","芯片","数字","量子","6G","5G","智能","数据","软件","华为","英伟达","苹果","特斯拉","微软","谷歌","自动驾驶","5G","6G"])]
    if not cn_tech: cn_tech, cn_world = cn_world[-4:], cn_world[:-4]
    print(f"  CN World: {len(cn_world)}, CN Tech: {len(cn_tech)}", file=sys.stderr)

    MAX_WORLD, MAX_TECH = 12, 8
    en_world = sample_evenly(en_world, MAX_WORLD, min_per_source=2)
    en_tech = sample_evenly(en_tech, MAX_TECH, min_per_source=1)
    cn_world = sample_evenly(cn_world, MAX_WORLD, min_per_source=1)
    cn_tech = sample_evenly(cn_tech, MAX_TECH, min_per_source=1)

    for i, art in enumerate(en_world): art["id"] = f"ew{i}"
    for i, art in enumerate(en_tech): art["id"] = f"et{i}"
    for i, art in enumerate(cn_world): art["id"] = f"zw{i}"
    for i, art in enumerate(cn_tech): art["id"] = f"zt{i}"

    for art in en_world + en_tech:
        content, zh = generate_article(art, "en")
        art["content"] = content
        art["zh"] = zh
    for art in cn_world + cn_tech:
        title = art.get("title", "")
        desc = art.get("description", art.get("title", ""))
        art["headline"] = title
        art["content"] = f"<p>{desc}</p>"
        if "date" not in art: art["date"] = datetime.now().strftime("%Y-%m-%d")

    news_json = {
        "en_world": [{"id":a["id"],"source":a["source"],"headline":a["headline"],"date":a.get("date","")[:25],"content":a["content"],"zh":a.get("zh",""),"url":a["url"]} for a in en_world],
        "en_tech": [{"id":a["id"],"source":a["source"],"headline":a["headline"],"date":a.get("date","")[:25],"content":a["content"],"zh":a.get("zh",""),"url":a["url"]} for a in en_tech],
        "zh_world": [{"id":a["id"],"source":a["source"],"headline":a["headline"],"date":a.get("date","")[:25],"content":a["content"],"url":a.get("url","")} for a in cn_world],
        "zh_tech": [{"id":a["id"],"source":a["source"],"headline":a["headline"],"date":a.get("date","")[:25],"content":a["content"],"url":a.get("url","")} for a in cn_tech],
    }
    json_str = json.dumps(news_json, ensure_ascii=False)

    # Read template (with placeholders)
    template_path = f"{PROJECT_DIR}/index_template.html"
    if os.path.exists(template_path):
        with open(template_path, "r") as f: html = f.read()
    else:
        with open(f"{PROJECT_DIR}/index.html", "r") as f: html = f.read()

    date_str = datetime.now().strftime("%A, %d %B %Y") + " \u00b7 Auckland, NZ"
    html = html.replace("<!-- DATE_HERE -->", date_str)
    html = html.replace("<!-- NEWS_JSON -->", json_str)
    html = html.replace("<!-- EN_WORLD_COUNT -->", str(len(en_world)))
    html = html.replace("<!-- EN_TECH_COUNT -->", str(len(en_tech)))
    html = html.replace("<!-- ZH_WORLD_COUNT -->", str(len(cn_world)))
    html = html.replace("<!-- ZH_TECH_COUNT -->", str(len(cn_tech)))
    html = html.replace("<!-- EN_WORLD_LIST -->", build_headline_html(en_world, "en"))
    html = html.replace("<!-- EN_TECH_LIST -->", build_headline_html(en_tech, "en"))
    html = html.replace("<!-- ZH_WORLD_LIST -->", build_headline_html(cn_world, "zh"))
    html = html.replace("<!-- ZH_TECH_LIST -->", build_headline_html(cn_tech, "zh"))

    # Save generated HTML to index.html for GitHub Pages
    with open(f"{PROJECT_DIR}/index.html", "w") as f: f.write(html)
    print(f"Saved {len(html)} bytes to index.html", file=sys.stderr)
    print(f"EN: {len(en_world)}W+{len(en_tech)}T | ZH: {len(cn_world)}W+{len(cn_tech)}T", file=sys.stderr)

if __name__ == "__main__":
    main()

import feedparser
from datetime import datetime
import re

SITE_TITLE = "GLOBAL LIVE WIRE"

STREAMS = {
    "WORLD NEWS": "https://www.aljazeera.com/xml/rss/all.xml",
    "FINANCE": "https://www.investing.com/rss/news.rss",
    "TECH": "http://rss.cnn.com/rss/edition_technology.rss"
}

def get_backup_img(title, desc):
    text = (title + " " + desc).lower()
    if any(x in text for x in ['war', 'army', 'military', 'conflict']):
        return "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=500&q=30"
    elif any(x in text for x in ['crypto', 'bitcoin', 'stock', 'market']):
        return "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?w=500&q=30"
    return "https://images.unsplash.com/photo-1504711432869-efd597cdd042?w=500&q=30"

def create_site():
    all_posts_html = ""
    now = datetime.now().strftime("%B %d, %Y | %H:%M")
    for cat, url in STREAMS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:6]: 
            title = entry.title
            link = entry.link
            desc = re.sub('<[^<]+?>', '', entry.get('summary', entry.get('description', 'Full report on site.')))
            img = ""
            if 'media_content' in entry: img = entry.media_content[0]['url']
            elif 'media_thumbnail' in entry: img = entry.media_thumbnail[0]['url']
            if not img: img = get_backup_img(title, desc)
            all_posts_html += f"""
            <div style="max-width:600px; margin:0 auto 40px auto; background:#fff; border:2px solid #111; padding:20px; font-family: sans-serif;">
                <h2 style="font-size:24px; margin-bottom:10px;">{title}</h2>
                <img src="{img}" style="width:100%; height:300px; object-fit:cover; border:1px solid #ddd;" referrerpolicy="no-referrer">
                <p>{desc[:150]}...</p>
                <a href="{link}" target="_blank">Read More</a>
            </div>"""
    full_html = f"<html><body style='background:#f4f4f4; padding:20px;'><h1 style='text-align:center;'>{SITE_TITLE}</h1><p style='text-align:center;'>Sync: {now}</p>{all_posts_html}</body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

if __name__ == "__main__":
    create_site()

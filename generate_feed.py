import feedparser
from datetime import datetime
from email.utils import format_datetime

FEEDS = [
    ("Around the Nerd", "https://www.spreaker.com/show/3137940/episodes/feed"),
    ("Dungeon Mystery Theatre", "https://www.spreaker.com/show/4787378/episodes/feed"),
    ("Crit Happens!", "https://www.spreaker.com/show/6718900/episodes/feed"),
    ("Magic: The Talking", "https://www.spreaker.com/show/4144911/episodes/feed"),
]

items = []

for show_name, url in FEEDS:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        entry.show = show_name
        items.append(entry)

items.sort(
    key=lambda e: e.get("published_parsed", datetime.min.timetuple()),
    reverse=True
)

def esc(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

rss_items = ""

for e in items[:300]:
    pub_date = format_datetime(datetime(*e.published_parsed[:6]))
    enclosure = e.enclosures[0] if e.enclosures else None

    if not enclosure:
        continue

    rss_items += f"""
    <item>
      <title>[{esc(e.show)}] {esc(e.title)}</title>
      <description>{esc(e.summary)}</description>
      <pubDate>{pub_date}</pubDate>
      <guid>{esc(e.id)}</guid>
      <enclosure url="{enclosure.href}" length="{enclosure.length}" type="{enclosure.type}"/>
    </item>
    """

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
 xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel>
  <title>P3 Podcast Network</title>
  <link>https://sn0rlaxx92.github.io/p3pn-network-feed/</link>
  <description>All shows from the P3 Podcast Network.</description>
  <language>en-us</language>
  <itunes:author>P3 Podcast Network</itunes:author>
  <itunes:explicit>false</itunes:explicit>
  <itunes:image href="https://i.imgur.com/3zXCoJy.jpeg"/>
  {rss_items}
</channel>
</rss>
"""

with open("index.xml", "w", encoding="utf-8") as f:
    f.write(rss)

import feedparser
import openai
import json
import re
from datetime import datetime
from langdetect import detect

openai.api_key = "YOUR_OPENAI_API_KEY"

CHINESE_SOURCES = [
    "https://36kr.com/feed",
    "https://aixinzhijie.com/feed",
    "https://jiqizhixin.com/rss.xml",
    "https://qbitai.com/feed",
]

ENGLISH_SOURCES = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://www.technologyreview.com/feed/",
]

CHINESE_KEYWORDS = ["人工智能", "AI", "算法", "模型", "科技", "芯片", "机器学习", "深度学习", "大模型"]
ENGLISH_KEYWORDS = ["AI", "artificial intelligence", "model", "algorithm", "chip", "LLM", "tech", "robotics"]

def is_relevant(text, lang):
    keywords = CHINESE_KEYWORDS if lang == 'zh' else ENGLISH_KEYWORDS
    return any(k.lower() in text.lower() for k in keywords)

def generate_summary(text, lang):
    prompt = {
        "zh": f"请将以下内容摘要为不超过50字的新闻摘要：\n{text}",
        "en": f"Summarize the following in under 50 words:\n{text}"
    }
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt[lang]}],
            temperature=0.3
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "摘要生成失败"

def process_feed(url):
    entries = feedparser.parse(url).entries
    results = []
    for entry in entries[:15]:
        title = entry.get('title', '')
        summary = re.sub('<[^<]+?>', '', entry.get('summary', ''))
        link = entry.get('link', '')
        text = f"{title}\n{summary}"
        lang = detect(text)
        if lang not in ['zh', 'en']:
            continue
        if not is_relevant(text, lang):
            continue
        abstract = generate_summary(text, lang)
        results.append({
            "title": title,
            "summary": abstract,
            "link": link
        })
    return results

def main():
    zh_news, en_news = [], []
    for url in CHINESE_SOURCES:
        zh_news.extend(process_feed(url))
    for url in ENGLISH_SOURCES:
        en_news.extend(process_feed(url))

    final_output = {
        "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
        "zh": zh_news[:5],
        "en": en_news[:5]
    }

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

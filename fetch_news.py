
import feedparser
import json
import os
import time
import requests

def summarize(text):
    print("🚀 正在生成摘要...")
    print("📄 原文段落：", text[:100])
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ 未设置 DEEPSEEK_API_KEY 环境变量")
        return "【错误】缺少 API 密钥"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个AI科技新闻助手，请用简体中文（或英文）生成一句不超过50字的摘要"},
            {"role": "user", "content": text}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=data, timeout=10)
        print("📥 返回状态码：", response.status_code)
        if response.status_code == 200:
            summary = response.json()['choices'][0]['message']['content'].strip()
            print("📜 摘要结果：", summary)
            return summary
        else:
            return f"【API错误】状态码: {response.status_code}"
    except Exception as e:
        print("❌ 请求失败：", str(e))
        return "【错误】生成失败"

def fetch_news(feed_urls, lang):
    news = []
    for url in feed_urls:
        print(f"🌐 正在解析 {url}")
        try:
            feed = feedparser.parse(url)
            print(f"🔗 获取条数：{len(feed.entries)}")
            for entry in feed.entries[:5]:
                title = entry.title
                link = entry.link
                content = entry.get("summary", "")
                summary = summarize(content)
                news.append({
                    "title": title,
                    "summary": summary,
                    "link": link
                })
        except Exception as e:
            print(f"❌ 抓取失败：{url} 错误：{str(e)}")
    return news

feeds_zh = [
    "https://36kr.com/feed",
    "https://www.ithome.com/rss",
    "https://www.qbitai.com/feed",
    "https://www.jiqizhixin.com/rss"
]

feeds_en = [
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.technologyreview.com/feed/",
    "https://techcrunch.com/feed/"
]

print("📡 开始抓取中文新闻")
news_zh = fetch_news(feeds_zh, "zh")
print("📡 开始抓取英文新闻")
news_en = fetch_news(feeds_en, "en")

output = {
    "zh": news_zh,
    "en": news_en
}

import datetime

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump({
        "updated_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        "zh": zh_news,
        "en": en_news
    }, f, ensure_ascii=False, indent=2)


print("✅ 已写入 news.json，中文:", len(news_zh), "条，英文:", len(news_en), "条")

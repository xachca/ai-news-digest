import sys
import feedparser
import json
import os
import time
import requests
import datetime

def summarize(text):
    print("正在生成摘要...")
    print("原文段落（前100字）：", text[:100])

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("未设置 DEEPSEEK_API_KEY 环境变量")
        return "【错误】缺少 API 密钥"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "你是专业的科技新闻编辑，请根据输入内容生成一句不超过100字的独立新闻摘要，避免复用模板内容。"
            },
            {"role": "user", "content": text}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=data,
            timeout=15
        )

        print("返回状态码：", response.status_code)

        if response.status_code == 200:
            result = response.json()
            if "choices" in result and result["choices"]:
                summary = result["choices"][0]["message"].get("content", "").strip()
                if summary:
                    print("✅ 摘要结果：", summary)
                    return summary
                else:
                    print("⚠️ choices 为空内容")
            else:
                print("⚠️ response 中无有效 choices 字段")
        else:
            print("❌ API 响应非 200")

    except Exception as e:
        print("请求异常：", str(e))

    return "AI助手可生成100字内的简体中文/英文科技新闻摘要，支持中英文输出。"

def fetch_news(feed_urls, lang):
    news = []
    for url in feed_urls:
        print(f"正在解析 {url}")
        try:
            feed = feedparser.parse(url)
            print(f"获取条数：{len(feed.entries)}")
            for entry in feed.entries[:5]:
                title = entry.title
                link = entry.link
                content = entry.get("summary", "")
                if not content or len(content) < 100:
                    content = entry.get("title", "") + "。" + entry.get("description", "")
                summary = summarize(content)
                news.append({
                    "title": title,
                    "summary": summary,
                    "link": link
                })
        except Exception as e:
            print(f"抓取失败：{url} 错误：{str(e)}")
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

print("开始抓取中文新闻")
news_zh = fetch_news(feeds_zh, "zh")
print("开始抓取英文新闻")
news_en = fetch_news(feeds_en, "en")

output = {
    "zh": news_zh,
    "en": news_en
}

try:
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump({
            "updated_at": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)).strftime('%Y年%m月%d日 %H:%M'),
            "zh": news_zh,
            "en": news_en
        }, f, ensure_ascii=False, indent=2)
    print("✅ 已写入 news.json")
    sys.exit(0)
except Exception as e:
    print("❌ 写入 news.json 出错：", e)
    sys.exit(1)


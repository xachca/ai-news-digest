# 🧠 AI 科技头条速览

一个自动化系统，每天抓取全球中英文 AI 与科技新闻，生成摘要并通过 GitHub Pages 展示。

---

## ✨ 功能亮点

- 每天两次（08:50、17:50）自动更新
- 支持中英文新闻分栏显示
- 使用 Deepseek 模型自动生成摘要（≤50字）
- 自动部署，无需人工干预

---

## 📦 项目结构说明

| 文件/目录 | 描述 |
|-----------|------|
| `fetch_news.py` | 抓取 RSS、生成摘要并输出 `news.json` |
| `news.json`     | 存储最新 AI/科技新闻列表 |
| `index.html`    | 静态网页展示，读取 `news.json` |
| `requirements.txt` | 所需依赖（feedparser、langdetect、requests） |
| `.github/workflows/news-update.yml` | GitHub Actions 自动部署配置 |

---

## 🚀 快速部署指南

### 1️⃣ Fork 或克隆本仓库

```bash
git clone https://github.com/your-username/ai-news-digest.git
cd ai-news-digest
```

### 2️⃣ 设置 GitHub Secret

前往：

`Settings → Secrets and variables → Actions → New repository secret`

添加密钥：

- **Name**: `DEEPSEEK_API_KEY`
- **Value**: 你的 Deepseek API Key

### 3️⃣ 启用 GitHub Pages

进入 `Settings → Pages`：

- Source 选择：`main` 分支，目录：`/ (root)`
- 完成后会生成页面地址，如：
  ```
  https://your-username.github.io/ai-news-digest/
  ```

---

## 🧠 Deepseek API 接口说明

脚本使用 `https://api.deepseek.com/v1/chat/completions` 接口调用大模型。

摘要请求示例：

```json
{
  "model": "deepseek-chat",
  "messages": [
    {
      "role": "user",
      "content": "请将以下内容摘要为不超过50字：..."
    }
  ]
}
```

---

## 🔄 自动任务说明

由 GitHub Actions 定时触发：

```yaml
schedule:
  - cron: '50 0 * * *'  # 北京时间 08:50
  - cron: '50 9 * * *'  # 北京时间 17:50
```

也可手动触发 Actions 执行。

---

## 📷 示例页面展示（中文）

```
【OpenAI 推出 GPT-5 模型】
摘要：模型支持多模态输入，显著增强推理能力。
链接：[查看原文](https://openai.com/blog/gpt-5)
```

---

## 📄 License

MIT

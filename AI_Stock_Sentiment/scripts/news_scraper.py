from gnews import GNews
import pandas as pd
import os

os.makedirs('data', exist_ok=True)
google_news = GNews(language='zh-Hant', country='TW', period='7d', max_results=10)
news_list = google_news.get_news('台積電 2330')

news_data = []
for n in news_list:
    news_data.append({
        '日期': n['published date'],
        '標題': n['title'],
        '內容': n['description']
    })

df_news = pd.DataFrame(news_data)
df_news = df_news.dropna() # 清理資料 [cite: 24]
df_news.to_csv("data/news.csv", index=False) # 產出 news.csv [cite: 55]
print("新聞資料已儲存至 data/news.csv")

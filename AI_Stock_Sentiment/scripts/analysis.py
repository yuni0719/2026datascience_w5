from FinMind.data import DataLoader
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 抓取股價 (台積電 2330) 
dl = DataLoader()
# 為了對齊新聞，我們改抓最近一週的資料
df_stock = dl.taiwan_stock_daily(stock_id="2330", start_date="2026-03-18")

# 自動檢查並修正欄位名稱 
if 'date' not in df_stock.columns and 'Date' in df_stock.columns:
    df_stock = df_stock.rename(columns={'Date': 'date'})

# 儲存原始資料 
os.makedirs('data', exist_ok=True)
df_stock.to_csv("data/stock.csv", index=False)

# 2. 讀取與處理新聞資料 
df_news = pd.read_csv("data/news.csv")

# 確保日期欄位格式正確 
df_stock['date'] = pd.to_datetime(df_stock['date']).dt.date
df_news['date'] = pd.to_datetime(df_news['日期']).dt.date

# 3. 計算每日情緒總分 
daily_sentiment = df_news.groupby('date')['sentiment_score'].sum().reset_index()

# 4. 合併資料 (使用 outer join 避免日期沒對上就消失) 
merged = pd.merge(df_stock, daily_sentiment, on='date', how='outer').sort_values('date').fillna(0)

# 5. 繪製視覺化圖表 
fig, ax1 = plt.subplots(figsize=(12, 6))

# 股價趨勢 (左軸)
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Price (2330)', color='blue')
ax1.plot(merged['date'], merged['close'], color='blue', marker='o', label='Stock Price')

# 情緒趨勢 (右軸)
ax2 = ax1.twinx()
ax2.set_ylabel('Sentiment Score', color='orange')
ax2.bar(merged['date'], merged['sentiment_score'], color='orange', alpha=0.3, label='Sentiment Sum')

plt.title('2330 Stock Price vs. News Sentiment')
plt.xticks(rotation=45)
os.makedirs('output', exist_ok=True)
plt.savefig('output/result.png') 
plt.show()

print("分析腳本執行成功，已產出 result.png")

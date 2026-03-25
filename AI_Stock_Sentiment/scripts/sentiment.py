from transformers import pipeline
import pandas as pd

# 使用金融專用模型 (進階方式) [cite: 29]
classifier = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")
df_news = pd.read_csv("data/news.csv")

def get_sentiment_score(text):
    if pd.isna(text) or text == "": return 0
    result = classifier(text[:512])[0]
    label = result['label']
    if label == 'Positive': return 1   # Positive = +1 [cite: 34]
    if label == 'Negative': return -1  # Negative = -1 [cite: 36]
    return 0                           # Neutral = 0 [cite: 35]

df_news['sentiment_score'] = df_news['標題'].apply(get_sentiment_score)
df_news.to_csv("data/news.csv", index=False)
print("情緒分析完成並更新至 data/news.csv")

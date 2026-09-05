import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. Yahoo!ニュースのトップページを取得
url = "https://news.yahoo.co.jp/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}
response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding

# 2. HTMLの解析
soup = BeautifulSoup(response.text, "html.parser")

news_data = []

# トピックス一覧のリンク（aタグ）を検索
# Yahoo!ニュースの主要トピックスのURLパターン (/pickup/ や /news/ など) を含むリンクを取得
for link in soup.find_all("a"):
    href = link.get("href", "")
    title = link.text.strip()

    # 主要トピックス記事のURL条件に一致するものを抽出
    if "/pickup/" in href or ("news.yahoo.co.jp/articles/" in href):
        if title and len(title) > 5:  # 短すぎる記号などを除外
            news_data.append({"title": title, "url": href})
            
# 3. pandas DataFrameに変換してCSV保存
df = pd.DataFrame(news_data)

# 重複箇所の削除
if not df.empty:
    df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)

df.to_csv("news.csv", index=False, encoding="utf-8-sig")
print(f"取得完了: {len(df)}件のニュースを news.csv に保存しました。")
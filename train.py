import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

print("Loading datasets...")
df_sent = pd.read_csv("kobun_sentences.csv")
df_word = pd.read_csv("kobun_words.csv")

# 共通ベクトライザ（文字 n-gram）
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 4)
)

print("Training vectorizer...")
X_sent = vectorizer.fit_transform(df_sent["classical"])
X_word = vectorizer.transform(df_word["classical"])

# 保存
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("sentences.pkl", "wb") as f:
    pickle.dump(df_sent, f)

with open("words.pkl", "wb") as f:
    pickle.dump(df_word, f)

with open("X_sent.pkl", "wb") as f:
    pickle.dump(X_sent, f)

with open("X_word.pkl", "wb") as f:
    pickle.dump(X_word, f)

print("Training finished!")
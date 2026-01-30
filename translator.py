import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ======================
# CSV 読み込み
# ======================

def load_word_dict(path):
    word_dict = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                word_dict[row[0]] = row[1]
    return word_dict


def load_sentence_data(path):
    originals = []
    translations = []
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                originals.append(row[0])
                translations.append(row[1])
    return originals, translations


# ======================
# データ準備
# ======================

WORD_CSV = "kobun_words.csv"
SENTENCE_CSV = "kobun_sentences.csv"

word_dict = load_word_dict(WORD_CSV)
sentences, sentence_translations = load_sentence_data(SENTENCE_CSV)

vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 4)
)
sentence_vectors = vectorizer.fit_transform(sentences)

# ======================
# ★ 逆翻訳用データ準備（追加）
# ======================

# 単語辞書（現代語 → 古文）
reverse_word_dict = {v: k for k, v in word_dict.items()}

# 文データ（現代語 → 古文）
reverse_sentences = sentence_translations
reverse_sentence_translations = sentences

reverse_vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 4)
)
reverse_sentence_vectors = reverse_vectorizer.fit_transform(reverse_sentences)


# ======================
# 翻訳ロジック
# ======================

def translate(text):
    text = text.strip()

    # ---------- ① 単語 完全一致 ----------
    if text in word_dict:
        return word_dict[text]

    # ---------- ② 単語の組み合わせ判定 ----------
    results = []
    i = 0
    while i < len(text):
        matched = False
        # 長い単語を優先して探す
        for j in range(len(text), i, -1):
            part = text[i:j]
            if part in word_dict:
                results.append(word_dict[part])
                i = j
                matched = True
                break
        if not matched:
            break

    if results:
        return " ".join(results)

    # ---------- ③ 文章翻訳 ----------
    vec = vectorizer.transform([text])
    sims = cosine_similarity(vec, sentence_vectors)[0]

    best_idx = sims.argmax()
    best_score = sims[best_idx]

    if best_score < 0.2:
        return "翻訳できませんでした"

    return sentence_translations[best_idx]

# ======================
# ★ 現代語 → 古文（追加）
# ======================

def translate_reverse(text):
    text = text.strip()

    # ---------- ① 単語 完全一致 ----------
    if text in reverse_word_dict:
        return reverse_word_dict[text]

    # ---------- ② 単語の組み合わせ判定 ----------
    results = []
    i = 0
    while i < len(text):
        matched = False
        for j in range(len(text), i, -1):
            part = text[i:j]
            if part in reverse_word_dict:
                results.append(reverse_word_dict[part])
                i = j
                matched = True
                break
        if not matched:
            break

    if results:
        return "".join(results)  # 古文なのでスペースなし

    # ---------- ③ 文章翻訳 ----------
    vec = reverse_vectorizer.transform([text])
    sims = cosine_similarity(vec, reverse_sentence_vectors)[0]

    best_idx = sims.argmax()
    best_score = sims[best_idx]

    if best_score < 0.2:
        return "翻訳できませんでした"

    return reverse_sentence_translations[best_idx]

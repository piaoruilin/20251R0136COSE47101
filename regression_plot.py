# Re-import the uploaded movie data and cleaned keyword list
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import ast

df = pd.read_csv("자료폴더/top-10_with_genres_keywords.csv")
summary_df = pd.read_csv("keyword_analysis_summary_cleaned.csv")

# Create cleaned keyword set
clean_keywords_set = set(summary_df["keyword"].str.lower())

# Clean and filter keywords per movie
df["keywords"] = df["keywords"].fillna("[]").apply(ast.literal_eval)
df["filtered_keywords"] = df["keywords"].apply(
    lambda kws: [kw.strip().lower().replace(" ", "_") for kw in kws if kw.strip().lower() in clean_keywords_set]
)
df["keywords_text"] = df["filtered_keywords"].apply(lambda kws: " ".join(kws))
df["is_hit"] = df["weekly_views"] >= 10000000
y = df["is_hit"].astype(int)

# Vectorize keyword text
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["keywords_text"])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression model
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)

# Extract keyword coefficients
coefficients = logreg.coef_[0]
feature_names = np.array(vectorizer.get_feature_names_out())

# Top 10 positive and top 10 negative coefficients
top_positive_indices = np.argsort(coefficients)[-10:][::-1]
top_negative_indices = np.argsort(coefficients)[:10]

top_keywords = feature_names[np.concatenate([top_negative_indices, top_positive_indices])]
top_values = coefficients[np.concatenate([top_negative_indices, top_positive_indices])]

# Plot
plt.figure(figsize=(12, 6))
colors = ['red'] * 10 + ['green'] * 10
plt.barh(top_keywords[::-1], top_values[::-1], color=colors[::-1])
plt.xlabel("Coefficient Value")
plt.title("Top 10 Positive and Negative Keyword Effects (Logistic Regression)")
plt.tight_layout()
plt.show()

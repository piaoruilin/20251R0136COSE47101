from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import pandas as pd
from collections import Counter
import ast

# Load original dataset
df = pd.read_csv("자료폴더/top-10_with_genres_keywords.csv")

# Load cleaned keyword list
clean_keywords_df = pd.read_csv("keyword_analysis_summary_cleaned.csv")
clean_keywords_set = set(clean_keywords_df["keyword"].str.lower())

# Preprocess keywords: filter out non-English ones
df["keywords"] = df["keywords"].fillna("[]").apply(ast.literal_eval)
df["filtered_keywords"] = df["keywords"].apply(
    lambda kws: [kw.strip().lower().replace(" ", "_") for kw in kws if kw.strip().lower() in clean_keywords_set]
)

# Convert to text for vectorization
df["keywords_text"] = df["filtered_keywords"].apply(lambda kws: " ".join(kws))

# Target variable
df["is_hit"] = df["weekly_views"] >= 10000000
y = df["is_hit"].astype(int)

# Vectorize keywords
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["keywords_text"])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train decision tree classifier
tree_model = DecisionTreeClassifier(max_depth=5, random_state=42)
tree_model.fit(X_train, y_train)

# Plot the decision tree
plt.figure(figsize=(20, 10))
plot_tree(tree_model, feature_names=vectorizer.get_feature_names_out(), class_names=["Non-Hit", "Hit"],
          filled=True, rounded=True, max_depth=3, fontsize=10)
plt.tight_layout()
plt.show()
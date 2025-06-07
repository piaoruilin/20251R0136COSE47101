from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import pandas as pd
from collections import Counter
import ast
import matplotlib.pyplot as plt

# Reload the full dataset
df = pd.read_csv("자료폴더/top-10_with_genres_keywords.csv")

# Preprocess keywords
df["keywords"] = df["keywords"].fillna("[]").apply(ast.literal_eval)
df["is_hit"] = df["weekly_views"] >= 10000000

# Join keywords into a single string per movie
df["keywords_text"] = df["keywords"].apply(lambda kws: " ".join([kw.strip().lower().replace(" ", "_") for kw in kws]))

# Vectorize keywords
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["keywords_text"])
y = df["is_hit"].astype(int)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred, output_dict=True)
conf_matrix = confusion_matrix(y_test, y_pred)

# Get top positive and negative keyword coefficients
feature_names = np.array(vectorizer.get_feature_names_out())
coefs = model.coef_[0]
top_positive = feature_names[np.argsort(coefs)[-10:]][::-1]
top_negative = feature_names[np.argsort(coefs)[:10]]

print(top_positive, top_negative, report, conf_matrix)

# Load the reuploaded cleaned keyword summary file
file_path1 = "keyword_files/keyword_analysis_summary_cleaned.csv"
summary_df1 = pd.read_csv(file_path1)

# Filter keywords that appeared in at least 1 hit movie
filtered_keywords = summary_df1[summary_df1["hit_count"] > 0]

# Sort by hit_ratio descending and select top 20
top_keywords = filtered_keywords.sort_values(by="hit_ratio", ascending=False).head(20)

# Plot with values annotated
plt.figure(figsize=(12, 8))
bars = plt.barh(top_keywords["keyword"][::-1], top_keywords["hit_ratio"][::-1])
plt.xlabel("Hit Ratio")
plt.title("Top 20 Keywords by Hit Ratio")

# Annotate hit ratios on the bars
for bar, ratio in zip(bars, top_keywords["hit_ratio"][::-1]):
    plt.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
             f"{ratio:.2f}", va="center", fontsize=9)

plt.tight_layout()
plt.show()

# Reload the cleaned keyword summary CSV
summary_df = pd.read_csv("keyword_files/keyword_analysis_summary_cleaned.csv")

# Filter to remove infinite lift and require at least 1 hit and 1 non-hit occurrence
filtered_for_lift = summary_df[
    (summary_df["hit_count"] > 0) &
    (summary_df["non_hit_count"] > 0) &
    (summary_df["lift"] != float("inf"))
]

# Sort by lift score and take top 20
top_lift_keywords = filtered_for_lift.sort_values(by="lift", ascending=False).head(20)

plt.figure(figsize=(12, 8))
bars = plt.barh(top_lift_keywords["keyword"][::-1], top_lift_keywords["lift"][::-1])
plt.xlabel("Lift Score")
plt.title("Top 20 Keywords by Lift Score")

# Annotate lift values on the bars
for bar, lift in zip(bars, top_lift_keywords["lift"][::-1]):
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
             f"{lift:.2f}", va="center", fontsize=9)

plt.tight_layout()
plt.show()
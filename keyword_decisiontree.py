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

# Predict using the decision tree model
y_pred_tree = tree_model.predict(X_test)

# Generate classification report and confusion matrix
tree_report = classification_report(y_test, y_pred_tree, output_dict=True)
tree_conf_matrix = confusion_matrix(y_test, y_pred_tree)

from sklearn.utils import resample

# Combine X and y for easier resampling
df_balanced = df[["keywords_text", "is_hit"]].copy()

# Separate majority and minority classes
df_majority = df_balanced[df_balanced["is_hit"] == 0]
df_minority = df_balanced[df_balanced["is_hit"] == 1]

# Upsample minority class
df_minority_upsampled = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)

# Combine majority and upsampled minority class
df_upsampled = pd.concat([df_majority, df_minority_upsampled])

# Re-vectorize after resampling
X_up = vectorizer.fit_transform(df_upsampled["keywords_text"])
y_up = df_upsampled["is_hit"]

# Train-test split
X_train_up, X_test_up, y_train_up, y_test_up = train_test_split(X_up, y_up, test_size=0.2, random_state=42)

# Train a new decision tree
tree_model_up = DecisionTreeClassifier(max_depth=5, random_state=42)
tree_model_up.fit(X_train_up, y_train_up)

# Predict and evaluate
y_pred_up = tree_model_up.predict(X_test_up)
report_up = classification_report(y_test_up, y_pred_up, output_dict=True)
conf_matrix_up = confusion_matrix(y_test_up, y_pred_up)

print(report_up, conf_matrix_up)

# Train a deeper decision tree
deep_tree_model = DecisionTreeClassifier(max_depth=15, random_state=42)
deep_tree_model.fit(X_train_up, y_train_up)

# Predict and evaluate
y_pred_deep = deep_tree_model.predict(X_test_up)
report_deep = classification_report(y_test_up, y_pred_deep, output_dict=True)
conf_matrix_deep = confusion_matrix(y_test_up, y_pred_deep)

report_deep, conf_matrix_deep
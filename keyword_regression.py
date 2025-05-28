from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import pandas as pd
from collections import Counter
import ast

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

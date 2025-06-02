import pandas as pd
from collections import Counter
import ast

# Load the dataset
df = pd.read_csv("자료폴더/top-10_with_genres_keywords.csv")

# Convert stringified lists to actual lists
df["keywords"] = df["keywords"].fillna("[]").apply(ast.literal_eval)

# Define "hit" movies (custom threshold – adjust as needed)
df["is_hit"] = df["weekly_views"] >= 10000000  # e.g., 10 million weekly views

# Filter hit and non-hit movies
hit_df = df[df["is_hit"] == True]
non_hit_df = df[df["is_hit"] == False]

# Count keyword frequencies
hit_keywords = Counter([kw.lower().strip() for kws in hit_df["keywords"] for kw in kws])
non_hit_keywords = Counter([kw.lower().strip() for kws in non_hit_df["keywords"] for kw in kws])

# Total number of hit and non-hit movies
total_hit = len(hit_df)
total_non_hit = len(non_hit_df)

# Create summary DataFrame
keywords = set(hit_keywords.keys()).union(non_hit_keywords.keys())
summary = []

for kw in keywords:
    hit_count = hit_keywords[kw]
    non_hit_count = non_hit_keywords[kw]
    hit_ratio = hit_count / total_hit if total_hit else 0
    non_hit_ratio = non_hit_count / total_non_hit if total_non_hit else 0
    lift = (hit_ratio / non_hit_ratio) if non_hit_ratio > 0 else float("inf")
    summary.append({
        "keyword": kw,
        "hit_count": hit_count,
        "hit_ratio": round(hit_ratio, 4),
        "non_hit_count": non_hit_count,
        "non_hit_ratio": round(non_hit_ratio, 4),
        "lift": round(lift, 2)
    })

# Create DataFrame
summary_df = pd.DataFrame(summary).sort_values(by="lift", ascending=False)

# Save to CSV
output_path = "keyword_analysis_summary.csv"
summary_df.to_csv(output_path, index=False)

# Load the reuploaded cleaned keyword summary file
file_path1 = "keyword_analysis_summary_cleaned.csv"
summary_df1 = pd.read_csv(file_path1)

# Filter keywords that appeared in at least 1 hit movie
filtered_keywords = summary_df1[summary_df1["hit_count"] > 0]

# Sort by hit_ratio descending and select top 20
top_keywords = filtered_keywords.sort_values(by="hit_ratio", ascending=False).head(20)

# Save to new CSV
top_keywords_path = "top_20_hit_keywords.csv"
top_keywords.to_csv(top_keywords_path, index=False)

top_keywords_path

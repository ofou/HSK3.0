import pandas as pd
import ast

# Read the CSV
df = pd.read_csv("./output/guide.csv")

# Convert string representation of lists to actual lists
df["new_words"] = df["new_words"].apply(ast.literal_eval)


# Count words per level
def count_words(word_list):
    return len(word_list) if isinstance(word_list, list) else 0


df["word_count"] = df["new_words"].apply(count_words)

# Group by level and calculate average
level_stats = df.groupby("level")["word_count"].agg(["sum", "count", "mean"])

print("Average words per level:")
print(level_stats)

import json

import pandas as pd

class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)
            all_tags = self.df["tags"].apply(lambda x : x).sum()
            self.unique_tags = set(list(all_tags))

    def categorize_length(self,line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"
    def get_tags(self):
        return self.unique_tags

    def get_filtered_posts(self, length, language, tag):
        print("👉 Input values:")
        print("Length:", length)
        print("Language:", language)
        print("Tag:", tag)

        print("\n👉 Available data in DataFrame:")
        print("Languages:", self.df['language'].unique())
        print("Lengths:", self.df['length'].unique())
        print("Sample tags:", self.df['tags'].head())

        df_filtered = self.df[
            (self.df['language'].str.lower() == language.lower()) &
            (self.df['length'].str.lower() == length.lower()) &
            (self.df['tags'].apply(lambda x: tag.lower() in [t.lower() for t in x]))
            ]

        print("\n👉 Filtered result:")
        print(df_filtered)

        return df_filtered.to_dict(orient="records")


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts("Short","Hinglish","Motivation")
    print("Final Output:", posts)





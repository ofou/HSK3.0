# pip install wordfreq jieba pandas
import pandas as pd
from typing import Tuple, List, Set, Dict
from dataclasses import dataclass
from pathlib import Path
from wordfreq import word_frequency
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ChineseCharacterAnalyzer:
    """Analyzes Chinese characters and vocabulary relationships."""

    chars_path: Path
    vocab_path: Path
    output_dir: Path

    def get_char_frequency(self, char: str) -> float:
        """Get frequency for a single character in simplified Chinese."""
        try:
            return word_frequency(char, "zh")
        except:
            logger.warning(f"Could not get frequency for character: {char}")
            return 0.0

    def __post_init__(self):
        """Initialize the analyzer by loading data and creating output directory."""
        self.chars_df = pd.read_csv(self.chars_path, encoding="utf-8")
        self.vocab_df = pd.read_csv(self.vocab_path, encoding="utf-8")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Define standard level ordering
        self.level_order = ["一级", "二级", "三级", "四级", "五级", "六级", "高等"]
        self.level_map = {level: i + 1 for i, level in enumerate(self.level_order)}

        # Add frequency information
        self.chars_df["frequency"] = self.chars_df["汉字"].apply(
            self.get_char_frequency
        )

    def process_characters(self) -> pd.DataFrame:
        """Process characters and create initial dataframe with cumulative characters."""
        # Sort by level first, then by frequency within each level
        sorted_chars = self.chars_df.assign(
            level_num=self.chars_df["级别"].map(self.level_map)
        ).sort_values(["level_num", "frequency"], ascending=[True, False])

        df = pd.DataFrame(
            {
                "page": range(1, len(sorted_chars) + 1),
                "chars": sorted_chars["汉字"],
                "level": pd.Categorical(sorted_chars["级别"], self.level_order),
                "pinyin": sorted_chars["拼音"],
                "frequency": sorted_chars["frequency"],
            }
        )

        # Calculate cumulative characters
        df["old_chars"] = df["chars"].cumsum().str.split("")
        return df

    def find_words(
        self, df: pd.DataFrame, char_range: Tuple[int, int] = (2, 10)
    ) -> pd.DataFrame:
        """Find valid words that can be formed from cumulative characters."""
        min_chars, max_chars = char_range

        def get_valid_words(chars_set: Set[str]) -> List[str]:
            """Get valid words for a given set of characters."""
            return [
                word
                for word in self.vocab_df["词语"]
                if min_chars <= len(word) <= max_chars
                and all(char in chars_set for char in word)
            ]

        # Process words more efficiently using vectorized operations
        char_sets = [set("".join(chars)) for chars in df["old_chars"]]
        df["词语"] = [set(get_valid_words(char_set)) for char_set in char_sets]
        return df

    def find_new_words(self, df: pd.DataFrame) -> pd.DataFrame:
        """Find new words introduced with each character."""

        # Initialize empty list to store cumulative words
        cumulative_words = []
        seen_words = set()

        # Process each row to find new words
        for idx, row in df.iterrows():
            current_words = row["词语"]
            new_words = [
                word
                for word in current_words
                if row["chars"] in word and word not in seen_words
            ]
            cumulative_words.append(new_words)
            seen_words.update(current_words)

        # Update DataFrame
        result_df = df[["level", "chars", "pinyin"]].copy()
        result_df["new_words"] = cumulative_words

        return result_df

    def find_homophones(self, df: pd.DataFrame) -> pd.DataFrame:
        """Identify characters with same form but different pronunciations."""
        homophones = df[df.duplicated(subset=["chars"], keep=False)].copy()
        return homophones.sort_values(["chars", "level"])

    def save_by_level(self, df: pd.DataFrame) -> None:
        """Save separate CSV files for each proficiency level."""
        for level_name, level_num in self.level_map.items():
            level_df = df[df["level"] == level_name]
            output_path = self.output_dir / f"guide_{level_num}.csv"
            level_df.to_csv(output_path, index=False, encoding="utf-8")

    def process_all(self) -> None:
        """Execute complete processing pipeline."""
        df = self.process_characters()
        df = self.find_words(df)
        result_df = self.find_new_words(df)

        # Save main results
        result_df.to_csv(self.output_dir / "guide.csv", index=False, encoding="utf-8")

        # Save level-specific files
        self.save_by_level(result_df)

        # Generate and save homophones
        homophones = self.find_homophones(result_df)
        homophones.to_csv(
            self.output_dir / "homophones.csv", index=False, encoding="utf-8"
        )


# Usage example:
if __name__ == "__main__":
    analyzer = ChineseCharacterAnalyzer(
        chars_path=Path("./汉字.csv"),
        vocab_path=Path("./词汇.csv"),
        output_dir=Path("./output"),
    )
    analyzer.process_all()

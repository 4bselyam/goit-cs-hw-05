import requests
import re
import collections
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor


def download_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def map_words(text):
    words = re.findall(r"\b\w+\b", text.lower())
    return collections.Counter(words)


def reduce_counts(counts_list):
    total_counts = collections.Counter()
    for counts in counts_list:
        total_counts.update(counts)
    return total_counts


def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color="skyblue")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title(f"Top {top_n} Words by Frequency")
    plt.xticks(rotation=45)
    plt.show()


def main(url, top_n=10):
    text = download_text(url)

    chunk_size = len(text) // 4
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    with ThreadPoolExecutor() as executor:
        map_results = list(executor.map(map_words, chunks))

    word_counts = reduce_counts(map_results)

    visualize_top_words(word_counts, top_n)


if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    main(url, top_n=10)

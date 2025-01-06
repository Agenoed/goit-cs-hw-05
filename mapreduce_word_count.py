import matplotlib.pyplot as plt
import operator
from collections import Counter
import urllib.request
from multiprocessing import Pool
import re
from functools import reduce

def chunkify(data, chunk_size):
    """Розбиває дані на частини (chunks)."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def map_words(chunk):
    """Рахує слова у фрагменті тексту."""
    return Counter(chunk)

def reduce_counts(counts1, counts2):
    """Об'єднує два словники з кількістю слів."""
    counts1.update(counts2)
    return counts1

def map_reduce(text, num_processes):
    """Застосовує парадигму MapReduce для підрахунку слів."""
    words = re.findall(r'\b\w+\b', text.lower())

    chunk_size = len(words) // num_processes
    chunks = list(chunkify(words, chunk_size))

    with Pool(num_processes) as pool:
        mapped_values = pool.map(map_words, chunks)
        reduced_counts = reduce(reduce_counts, mapped_values)
    return reduced_counts

def visualize_top_words(word_counts, top_n=10):
    """Візуалізує топ-слова."""
    sorted_word_counts = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
    top_words = sorted_word_counts[:top_n]
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.title(f"Топ-{top_n} найчастіше вживаних слів")
    plt.xticks()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    with urllib.request.urlopen(url) as response:
        text = response.read().decode('utf-8')

    word_counts = map_reduce(text, num_processes=4)
    visualize_top_words(word_counts)
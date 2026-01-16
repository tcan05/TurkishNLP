import os
import json
import math
import random
from collections import Counter, defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "syllables.json")

with open(filepath, "r", encoding="utf-8") as f:
    syllable_list = json.load(f)


#-----------------------------
# DATA SPLITTING
#-----------------------------
train_size = int(0.95 * len(syllable_list))
train_data = syllable_list[:train_size]
test_data = syllable_list[train_size:]


#-----------------------------
# BUILD N-GRAMS
#-----------------------------

# Generate N-Grams
def generate_ngrams(data, n):

    ngrams = [tuple(data[i:i + n]) for i in range(len(data) - n + 1)]
    return ngrams

# N-Gram Counter
def count_ngrams(data, n):

    ngrams = generate_ngrams(data, n)
    ngram_counts = Counter(ngrams)

    prefix_counts = Counter()

    for ngram in ngrams:

        prefix = ngram[:-1]
        prefix_counts[prefix] += 1

    return ngram_counts, prefix_counts

# Normalize N-Grams
def normalize_ngrams(ngram_counts, prefix_counts):
    probs = defaultdict(dict)

    for ngram, count in ngram_counts.items():

        prefix = ngram[:-1]
        next_token = ngram[-1]
        probs[prefix][next_token] = count / prefix_counts[prefix]

    return probs

# Generate Normalized N-Grams
def generate_ngram_model(data, n):

    ngram_counts, prefix_counts = count_ngrams(data, n)
    probs = normalize_ngrams(ngram_counts, prefix_counts)

    return probs

unigram = generate_ngram_model(train_data, 1)
bigram = generate_ngram_model(train_data, 2)
trigram = generate_ngram_model(train_data, 3)


#-----------------------------
# CALCULATE PERPLEXITY
#-----------------------------

def calc_perplexity(probs, data, n):

    log_prob_sum = 0
    N = 0

    for i in range(n - 1, len(data)):

        prefix = tuple(data[i - n + 1:i]) if n > 1 else ()
        
        syll = data[i]
        prob = probs.get(prefix, {}).get(syll, 1e-6)
        log_prob_sum += math.log(prob)
        N += 1

    return math.exp(-log_prob_sum / N)

unigram_pp = calc_perplexity(unigram, test_data, 1)
bigram_pp = calc_perplexity(bigram, test_data, 2)
trigram_pp = calc_perplexity(trigram, test_data, 3)

print("Unigram Perplexity: ", unigram_pp)
print("Bigram Perplexity : ",bigram_pp)
print("Trigram Perplexity: ",trigram_pp)


#-----------------------------
# RANDOM SENTENCES
#-----------------------------

def generate_sentence(probs, n, length = 10):

    if n == 1:
        prefix = ()
    else:
        prefix = random.choice(list(probs.keys()))

    sentence = list(prefix)

    for _ in range(length):

        next_prefix = probs.get(prefix)

        if not next_prefix:
            break

        syllables = list(next_prefix.keys())
        weights   = list(next_prefix.values())
        next_syll = random.choices(syllables, weights = weights, k = 1)[0]
        
        sentence.append(next_syll)

        if n > 1:
            prefix = tuple(sentence[-(n - 1):])

    text = "".join(sentence)
    text = text.replace("_", " ")

    return text

print("Unigram Sentence:", generate_sentence(unigram, 1, 10))
print("Bigram Sentence:", generate_sentence(bigram, 2, 10))
print("Trigram Sentence:", generate_sentence(trigram, 3, 10))
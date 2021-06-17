from nltk.corpus import stopwords
from heapq import nlargest
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS
from rouge import Rouge
import spacy

import nltk
nltk.download("stopwords")


def summarize(text):
    listStopwords = set(stopwords.words("indonesian"))
    _stopwords = list(STOP_WORDS)
    _stopwords.append(listStopwords)

    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    tokens = [token.text for token in doc]

    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n'

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in _stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency

    sentence_tokens = [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] = word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens)*0.3)

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    selected = []
    for sent in sentence_tokens:
        if sent in summary:
            selected += sent

    final_summary = [word.text for word in selected]

    summary = ' '.join(final_summary)

    len_text = len(text)
    len_summary = len(summary)
    return {'summary': summary,  'len_text': len_text, 'len_summary': len_summary}


def calculate_rouge(text, summary):
    rouge = Rouge()
    scores = rouge.get_scores(summary, text)
    return scores[0]

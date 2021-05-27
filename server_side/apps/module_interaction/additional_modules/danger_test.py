import re
import nltk
import numpy as np
import pandas as pd
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from server_side.apps.module_interaction.additional_modules import constants
from server_side.apps.data_interaction import crud


def find_danger(id_disaster, language):
    disaster = crud.read_disaster_id(id_disaster)
    if disaster == '':
        return ''
    quantity_indicator = find_quantity_indicator(disaster)
    peak = np.random.normal(find_center_distribution(quantity_indicator, disaster.term))
    content_analysis = make_content_analysis(disaster.about, language, disaster.id)
    return peak * content_analysis


def find_quantity_indicator(disaster):
    intensity_list = [constants.MIN_INTENSITY, disaster.intensity, constants.MAX_INTENSITY]
    intensity = [float(i) / max(intensity_list) for i in intensity_list][1]
    readiness_list = [constants.MIN_READINESS, disaster.readiness_degree, constants.MAX_READINESS]
    readiness = [float(i) / max(readiness_list) for i in readiness_list][1]
    return intensity / readiness


def find_center_distribution(indicator, term):
    indicator_list = [constants.MIN_INDICATOR, indicator, constants.MAX_INDICATOR]
    indicator = [float(i) / max(indicator_list) for i in indicator_list][1]
    return term / indicator


def make_content_analysis(text, language, id_disaster):
    sid = SentimentIntensityAnalyzer()
    text = clean_text(text)
    text = process_text(text, language)
    crud.update_disaster_about(id_disaster, text)
    dictionary = make_dictionary(id_disaster)
    dictionary.insert(0, text)
    tfidf_vectorizer = TfidfVectorizer()
    values = tfidf_vectorizer.fit_transform(dictionary)
    feature_names = tfidf_vectorizer.get_feature_names()
    data = pd.DataFrame(values.toarray(), columns=feature_names)
    data = data.T[data.T[0] != 0]
    words = list(data.index)
    sum_ = 0
    sum_f = 0
    for word in words:
        polarity = sid.polarity_scores(word)['compound']
        frequency = data[0][word]
        sum_f += frequency
        sum_ += polarity * frequency
    return sum_ + sum_f


def clean_text(text):
    pattern = r"[\W\d_]"
    return re.sub(pattern, " ", text)


def process_text(text, language):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words(get_language_name(language)))
    sentences = nltk.sent_tokenize(text)
    sentences_processed = []
    for sentence in sentences:
        words_processed = []
        words = nltk.word_tokenize(sentence)
        words = [word for word in words if word not in stop_words]
        for word in words:
            word = stemmer.stem(word)
            word = lemmatizer.lemmatize(word)
            words_processed.append(word)
        words = [word for word in words_processed if word not in stop_words]
        sentences_processed.append(" ".join(words))
    text_processed = " ".join(sentences_processed)
    return text_processed


def make_dictionary(id_disaster):
    disasters = crud.read_disasters()
    dictionary = []
    for disaster in disasters:
        if disaster.about_clean != "" and disaster.id != id_disaster:
            dictionary.append(disaster.about_clean)
    return dictionary


def get_language_name(language):
    if language == "en":
        return "english"
    if language == "de":
        return "german"
    if language == "ru" or language == "be" or language == "uk":
        return "russian"

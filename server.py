import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')


def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    # Reconstruct text
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text


def analyze_sentiment(text):
    # Preprocess text
    preprocessed_text = preprocess_text(text)
    # Initialize sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    # Get sentiment score
    sentiment_score = sia.polarity_scores(preprocessed_text)['compound']
    # Classify sentiment
    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


# server

from socket import *
from threading import Thread


s = socket(AF_INET, SOCK_STREAM)
host = '127.0.0.1'
port = 8000
s.bind((host, port))


def client_server(c, addr):
    while True:
        data = c.recv(1024)
        if not data:
            break
        data = data.decode('utf-8')

        sentiment = analyze_sentiment(data)
        c.sendall(sentiment.encode())



while True:
    s.listen()
    c, addr = s.accept()
    thread = Thread(target=client_server, args=(c, addr))
    thread.start()

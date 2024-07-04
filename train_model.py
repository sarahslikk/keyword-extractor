import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """
    Function to clean the text by lemmatizing and removing stopwords and punctuation.
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def train_and_save_vectorizer(sentences, filename='vectorizer.pkl'):
    """
    Train a TF-IDF vectorizer and save it to a file.
    """
    cleaned_sentences = [clean_text(sentence) for sentence in sentences]
    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit(cleaned_sentences)
    joblib.dump(vectorizer, filename)
    print(f"Vectorizer saved to {filename}")

# Example usage
sentences = [
    "Machine learning is fascinating and powerful.",
    "Natural language processing enables computers to understand human language.",
    "Artificial intelligence is transforming various industries."
]
train_and_save_vectorizer(sentences)

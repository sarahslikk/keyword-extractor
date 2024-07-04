import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    """
    Function to clean the text by lemmatizing and removing stopwords and punctuation.
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def extract_keywords(sentences, top_n=5):
    """
    Function to extract keywords using TF-IDF.
    """
    cleaned_sentences = [clean_text(sentence) for sentence in sentences]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(cleaned_sentences)
    feature_names = vectorizer.get_feature_names_out()
    sorted_items = sorted(zip(X.toarray()[0], feature_names), reverse=True)
    keywords = [item[1] for item in sorted_items[:top_n]]
    return keywords

# Example usage for testing
if __name__ == "__main__":
    sentences = ["Machine learning is fascinating and powerful."]
    print(extract_keywords(sentences))

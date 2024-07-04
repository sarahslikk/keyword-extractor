from flask import Flask, request, jsonify
import joblib
import spacy

# Ensure the model is loaded
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Downloading the spaCy model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load the trained vectorizer
vectorizer = joblib.load('vectorizer.pkl')

app = Flask(__name__)

def clean_text(text):
    """
    Clean the text by lemmatizing and removing stopwords and punctuation.
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def extract_keywords(sentence):
    """
    Extract keywords from a single sentence.
    """
    cleaned_sentence = clean_text(sentence)
    vectorized = vectorizer.transform([cleaned_sentence])
    sorted_items = sorted(zip(vectorized.toarray()[0], vectorizer.get_feature_names_out()), reverse=True)
    keywords = [item[1] for item in sorted_items[:5]]
    return keywords

@app.route('/extract_keywords', methods=['POST'])
def extract_keywords_api():
    """
    API endpoint to extract keywords from given sentences.
    """
    data = request.json
    sentences = data['sentences']
    keywords = [extract_keywords(sentence) for sentence in sentences]
    return jsonify({'keywords': keywords})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

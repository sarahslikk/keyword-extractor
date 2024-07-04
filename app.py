from flask import Flask, request, jsonify
import joblib
import spacy
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Ensure the model is loaded
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load the trained vectorizer
try:
    vectorizer = joblib.load('vectorizer.pkl')
except FileNotFoundError:
    print("Error: The 'vectorizer.pkl' file is not found. Make sure it is included in the project.")
    exit(1)

app = Flask(__name__)

def clean_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def extract_keywords(sentence, top_n=5):
    cleaned_sentence = clean_text(sentence)
    vectorized = vectorizer.transform([cleaned_sentence])
    sorted_items = sorted(zip(vectorized.toarray()[0], vectorizer.get_feature_names_out()), reverse=True)
    
    # Filter out keywords with very low scores and remove non-English characters
    keywords = [item[1].capitalize() for item in sorted_items if item[0] > 0.1 and item[1].isalpha()]
    
    # Return only the top_n keywords
    return keywords[:top_n]

@app.route('/extract_keywords', methods=['POST'])
def extract_keywords_api():
    data = request.json
    sentences = data['sentences']
    keywords = [extract_keywords(sentence) for sentence in sentences]
    return jsonify({'keywords': keywords})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

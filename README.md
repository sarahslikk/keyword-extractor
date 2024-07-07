Project for extracting keywords, trained from a customer service dataset.

This is a project I've been working on to combine my knowledge in data science and machine learning with Servicenow. I first trained a python model with TDIFVectorizer on customer service data I got from Kaggle (file is in the repository). The model still needs tuning, but it performs basic functions of a keywords extractor. I pushed it to an app on Heroku so I could integrate it into Servicenow as an outbound REST Message API, and the extract_keyword function is what actually extracts keywords. 

I haven't included the REST Message record in this repository because Heroku costs $$ to make a certain amount of requests, but I have included all of the files you need to replicate this. The only files you need to upload to heroku or whatever api server you want to use is the trained model (app.py), the vectorizer (vectorizer.pkl) and the requirements.txt (contains all the libraries I used that trained the model and extract keywords). 

In Heroku, you also need a Procfile, and runtime file (the python version, mine is 3.12). The training for the model is in train_model.py, which you can add hypertuning parameters to or change however you want. The data I used is in the csv file, I used customer service data specifically because that's the kind of stuff you'd see in Servicenow in incidents, etc. 

The other Javascript files (UI action, and Auto Tagger Script Include) contain the logic you need to actually automatically tag any table which you apply the UI action to. In order to work, you'll need a separate record for the outbound REST message called Keyword Extractor, with one POST method, linked to the keyword extractor API. Below contains the stuff you'll need to put into the REST message record. 


Format for calling the api and creating REST message: Example Endpoint: https://myappname.herokuapp.com/extract_keywords (extract_keywords) is the important part, make sure you put that
Method: POST, 
Headers: Content-type application/json, 
Body: { "sentences": ["Example sentence"] }

Response: (parse with JSON) {
    "keywords": [
        [
            "Example"
        ]
    ]
}

The body and response is handled in the script, while the Header and Method and Endpoint I configured in the REST Message record, to avoid hardcoding. I'm working to have this API be hosted on AWS Lambda instead, but right now I'm having trouble uploading the files because the python libaries are very large. Once I have it uploaded to Lambda then I will reupload with the REST message record, since AWS Lambda has free API requests up to 1 million requests. 



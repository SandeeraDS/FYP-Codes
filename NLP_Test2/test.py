# Import spaCy and load the language library
import spacy
#load small version of english library
nlp = spacy.load('en_core_web_sm')
# Create a Doc object
doc = nlp(u'Tesla is looking at buying U.S. startup for $6 million')
# Print each token separately-parse the entire stream into seperate components
for token in doc:
    print(token.text)
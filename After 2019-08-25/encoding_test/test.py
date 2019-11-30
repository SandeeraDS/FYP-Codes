import re
import nltk
# to install contractions - pip install contractions
from contractions import contractions_dict


def expand_contractions(text, contractions_dict):
    contractions_pattern = re.compile('({})'.format('|'.join(contractions_dict.keys())))

    def expand_match(contraction):
        # print(contraction)
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contractions_dict.get(match) \
            if contractions_dict.get(match) \
            else contractions_dict.get(match.lower())
        expanded_contraction = expanded_contraction
        print(expanded_contraction)
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    print(expanded_text)
    return expanded_text



# for the transcript
with open('2.txt', 'r', encoding="utf-8") as file:
    data = file.read()
    data = expand_contractions(data, contractions_dict)
sentence = nltk.sent_tokenize(data)
tokenized_sentences = [nltk.word_tokenize(sentences) for sentences in sentence]
print(tokenized_sentences)




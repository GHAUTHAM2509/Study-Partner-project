samplechunk = {'id': 'FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-25_Introduction-to-AI_chunk_010', 'source_document': 'FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-25_Introduction-to-AI.pptx', 'page_number': 10, 'keywords': [], 'text': 'Cont…\nAI in Data Security\nThe security of data is crucial for every company and cyber-attacks are growing very rapidly in the digital world. AI can be used to make your data more safe and secure. Some examples such as AEG bot, AI2 Platform,are used to determine software bug and cyber-attacks in a better way.\n AI in Social Media\nSocial Media sites such as Facebook, Twitter, and Snapchat contain billions of user profiles, which need to be stored and managed in a very efficient way. AI can organize and manage massive amounts of data. AI can analyze lots of data to identify the latest trends, hashtag, and requirement of different users.\nAI in Travel & Transport\nAI is becoming highly demanding for travel industries. AI is capable of doing various travel related works such as from making travel arrangement to suggesting the hotels, flights, and best routes to the customers. Travel industries are using AI-powered chatbots which can make human-like interaction with customers for better and fast response.', 'embedding': None}

import yake
import spacy
import pytextrank

def extract_keywords(chunk):
    text = chunk['text']

    # YAKE keyword extraction
    kw_extractor = yake.KeywordExtractor(lan="en", n=3, top=5)
    yake_keywords = [kw for kw, score in kw_extractor.extract_keywords(text)]

    # spaCy + pytextrank keyword extraction
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    doc = nlp(text)
    textrank_keywords = [phrase.text for phrase in doc._.phrases[:5]]

    # Combine and remove duplicates
    combined_keywords = list(dict.fromkeys(yake_keywords + textrank_keywords))
    
    chunk['keywords'] = combined_keywords
    return chunk

def extract_keywords_from_chunks(chunks):
    return [extract_keywords(chunk) for chunk in chunks]

if __name__ == "__main__":
    print(samplechunk)
    print() 
    print()
    keywords = extract_keywords(samplechunk)
    
# TChatBot
Own attempt to implement a question/answer chatbot with command line... Using for example: gensim doc2vec, spacy_udpipe nlp lemmatizer.  

At first, you need to install gensim and spacy_udpipe ( **pip3 install gensim**, **pip3 install spacy_udpipe** )

Then you need to download language for spacy_udpipe:

> spacy_udpipe.download("en")

## Input data format:
1. intents for questions
2. intents for answers
3. structure context (intent is dependent on another intent)

Data of intents are from some kaggle.com dataset. 

The sample **doc2vec model** is loading automaticaly (see the config. class). 

To force model training is necessary to set **FORCE_TRAINING** in config class to **True**. Note that training could take some time (see the bulgarian constants when creating . 

## Running

> python3 demo.py

Enjoy chatting!

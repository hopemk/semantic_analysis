import pandas as pd
import numpy as np # linear algebra
import regex as re

import nltk

import ssl

from textblob.classifiers import NaiveBayesClassifier

from nltk.tokenize import word_tokenize
from nltk import pos_tag

from nltk.corpus import stopwords

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('omw-1.4')
nltk.download('punkt')

nltk.download('stopwords')

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class MyClassifier:
    data = []
    
    def __init__(self):
        self.pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}
        self.wordnet_lemmatizer = WordNetLemmatizer()
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download('omw-1.4')
        nltk.download('punkt')

        nltk.download('stopwords')

        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')

    def read_file(self):
        # Creating a pandas dataframe from reviews.txt file
        print("Opening data file.")
        data = pd.read_csv('women_reviews.csv', sep=',')
        #print(data)
        #data.head()
        print("Done.\nThe table below shows the structure of the data.\n")
        print(data.head())
        return data
    def num_missing(self, df):
        return sum(df.isnull())

    def clean_data(self, data):
        data.apply(self.num_missing, axis=0)

        data = data.dropna()
        print("\nStarting text processing....\nRemoving the unnamed column")
        mydata = data.drop('Unnamed: 0', axis=1)
        return mydata
    #print(mydata.head())


    # Define a function to clean the text
    def clean(self, text):
    # Removes all special characters and numericals leaving the alphabets
        if type(text) == str:
            text = re.sub('[^A-Za-z]+', ' ', text)
            #print(text)
            return text
        else:
            return ' '
    
    def token_stop_pos(self, text):
        tags = pos_tag(word_tokenize(text))
        newlist = []
        for word, tag in tags:
            if word.lower() not in set(stopwords.words('english')):
                newlist.append(tuple([word, self.pos_dict.get(tag[0])]))
        return newlist

    
    def lemmatize(self, pos_data):
        lemma_rew = " "
        for word, pos in pos_data:
            if not pos:
                lemma = word
                lemma_rew = lemma_rew + " " + lemma
            else:
                lemma = self.wordnet_lemmatizer.lemmatize(word, pos=pos)
                lemma_rew = lemma_rew + " " + lemma
        return lemma_rew
    

    # function to calculate subjectivity
    def getSubjectivity(review):
        return TextBlob(review).sentiment.subjectivity
        # function to calculate polarity
    def getPolarity(self, review):
        return TextBlob(review).sentiment.polarity

    # function to analyze the reviews
    def analysis(self, score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    #fin_data = pd.DataFrame(mydata[['Complete Review', 'Lemma']])
    
    def make_predictions(self, tuples_test, cl, predicted_classifications):
        for i in range(len(tuples_test)):
            classification = cl.classify(tuples_test[i][0])
            predicted_classifications.append(classification)
            #print(tuples_test[i][0] + '\t' + str(classification))
    #make_predictions()
    
    #print(predicted_classifications[0:9])

    def _classify(self, text, num_of_rows):
        data = self.read_file()
        mydata = self.clean_data(data)
        #num_of_rows = int(input("Please enter the number of rows you would want to use : "))
        mydata = mydata[:num_of_rows]

        print("Joining Title and Review Text columns.")
        mydata['Complete Review'] = mydata['Title'] + ' ' + mydata['Review Text']
        # Cleaning the text in the review column
        mydata['Cleaned Reviews'] = mydata['Complete Review'].apply(self.clean)
        #print(mydata.head())

        # POS tagger dictionary
        #pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}

        print("Parts of speech tagging....")
        mydata['POS tagged'] = mydata['Cleaned Reviews'].apply(self.token_stop_pos)
        print(mydata.head())


        #wordnet_lemmatizer = WordNetLemmatizer()

        print("Lemmatizing....")
        mydata['Lemma'] = mydata['POS tagged'].apply(self.lemmatize)
        mydata.head()

        print("Calculating polarity indices....")
        # fin_data['Subjectivity'] = fin_data['Lemma'].apply(getSubjectivity) 
        mydata['Polarity'] = mydata['Lemma'].apply(self.getPolarity) 
        mydata['Analysis'] = mydata['Polarity'].apply(self.analysis)
        print(mydata.head())

        tb_counts = mydata.Analysis.value_counts()

        print(tb_counts)

        '''
        #for data in fin_data.:
        train_set = fin_data[['Review Text', 'Analysis']]
        fin_data_ls = [tuple(x) for x in train_set.values]
        print(fin_data_ls.head())
        #train = train_set.to_numpy()
        #print(train)
        cl = NaiveBayesClassifier(fin_data_ls)
        print(cl.classify("This is an amazing library!"))
        '''

        df = mydata
        #print(df.Titlevalue_counts())
        print(df.head())
        np.random.seed(0)
        msk = np.random.rand(len(df)) < 0.8
        train = df[msk]
        test = df[~msk]

        subset_train = train[['Complete Review', 'Recommended IND']]
        #tuples_train = subset_train1[]
        tuples_train = [tuple(x) for x in subset_train.values]
        subset_test = test[['Complete Review', 'Recommended IND']]
        tuples_test = [tuple(x) for x in subset_test.values]

        #print(tuples_train[0:1000])
        print("\nTraining the naive bayes classifier for classification")
        cl = NaiveBayesClassifier(tuples_train)
        print("\nRunning text predictions with parts of the dataset.")
        predicted_classifications = []

        self.make_predictions(tuples_test, cl, predicted_classifications)
        print("Done, everything working well. You can run your classifications now.")
        #text = input("\nEnter your review text : ")
        if cl.classify(text) == 1:
            print("\nCustomer shows positive behavior.")
        else:
            print("\nCustomer shows negative behavior")
        var = input("\nDo you want to classify again?, type y/n : ")
        if var =='y':
            _classify()
        else:
            exit()

#sent = MyClassifier()
#sent._classify("i hate it", 3000)
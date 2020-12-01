from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize
import gensim
import numpy as np


def calculateMark(answer, answerKey, mark):  #function takes array of strings of recognized texts,  original answer key and the maximum mark for the question
           fullAnswerString = ""
           for i in answer:
                  if i != "," and i!= '.':
                        fullStringAnswer += " "
                  fullAnswerString +=i
           print(fullAnswerString)

           tokenizedAnswer = sent_tokenize(fullAnswerString)  #sentence tokenising

           gen_docs = [[w.lower() for w in word_tokenize(text)] for text in tokenizedAnswer]  #word tokenizing

           dictionary = gensim.corpora.Dictionary(gen_docs)

           corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
           print(corpus)

           tf_idf = gensim.models.TfidfModel(corpus)

           for doc in tf_idf[corpus]:
                  print([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])

           # building the index
           sims = gensim.similarities.Similarity('workdir/',tf_idf[corpus], num_features=len(dictionary))


           #Create Query Document Once the index is built, we are going to calculate how similar is this query document to each document in the index.
           answerKeyDocs = []
           avg_sims = []

           tokenizedAnswerKey = sent_tokenize(answerKey)  #sentence tokenising

           for line in tokenizedAnswerKey:
                      answerKeyDocs.append(line)

           for line in answerKeyDocs:
                      query_doc = [w.lower() for w in word_tokenize(line)]
                      query_doc_bow = dictionary.doc2bow(query_doc) #update an existing dictionary and create bag of words

                      # find similarity for each document
                      query_doc_tf_idf = tf_idf[query_doc_bow]

                      # calculate sum of similarities for each query doc
                      sum_of_sims =(np.sum(sims[query_doc_tf_idf], dtype=np.float32))

                      # calculate average of similarity for each query doc
                      avg = sum_of_sims / len(file_docs)

                      # print average of similarity for each query doc
                      print(f'avg: {sum_of_sims / len(file_docs)}')

                      # add average values into array
                      avg_sims.append(avg)  


            # calculate total average
            total_avg = np.sum(avg_sims, dtype=np.float)

            # round the value and multiply by 100 to format it as percentage
            percentage_of_similarity = round(float(total_avg) * 100)
            # if percentage is greater than 100
            # that means documents are almost same
            if percentage_of_similarity >= 100:
                percentage_of_similarity = 100
                
                
            x = percentage_of_similarity/100
            total_mark = mark * x;
            
            return total_mark
   
   

    
   
   
   
   
   
   
        

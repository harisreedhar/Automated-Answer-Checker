import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import gensim

 #function takes array of strings of recognized texts... and original answer key
    
def answerForSingleQuestion(answer, answerKey, mark): 
            fullAnswerString = ""
            for i in answer:
                    if i != "," and i!= '.':
                         fullAnswerString += " "
                    fullAnswerString +=i
            print(fullAnswerString)

            tokenizedAnswer = sent_tokenize(fullAnswerString)  #sentence tokenising
            
            print(tokenizedAnswer)

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
            
            fullAnswerKeyString = ""
            for i in answerKey:
                    if i != "," and i!= '.':
                         fullAnswerKeyString += " "
                    fullAnswerKeyString +=i
            print(fullAnswerKeyString)


            tokenizedAnswerKey = sent_tokenize(fullAnswerKeyString)  #sentence tokenising of answerKey
            print("hello")
            print(tokenizedAnswerKey)

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
                    avg = sum_of_sims / len(answerKeyDocs)

                    # print average of similarity for each query doc
                    print(f'avg: {sum_of_sims / len(answerKeyDocs)}')

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
                    
            print(percentage_of_similarity)


            x = percentage_of_similarity/100
            total_mark = mark * x;

            return round(total_mark)

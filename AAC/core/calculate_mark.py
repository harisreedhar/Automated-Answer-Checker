from core.HandWriting_Recognition.src.imageToText import photoToText

def getWordsFromImage(imagePath):
       wordList, accuracyList = photoToText(imagePath)
       return wordList

def decomposeDictionary(answerKey, includeMarks = False):
       words = []
       marks = []
       for i in range(len(answerKey)):
              key = 'Qn'+str(i+1)
              answer_and_mark = answerKey.get(key)
              words.append(answer_and_mark[0])
              marks.append(answer_and_mark[1])
       if includeMarks:
              return words, marks
       return words

def calculateMark():
       imagePath = '/home/hari/Documents/College_Project/test_project/core/HandWriting_Recognition/data/test.jpg'
       words_from_answersheet = getWordsFromImage(imagePath)

       answerKey = {'Qn1':[("test1", "test1"), 10],
                    'Qn2':[("test2", "test2"), 20],
                    'Qn3':[("test3", "test3"), 30]}
       words_from_answerkey = decomposeDictionary(answerKey)

       ####### Do similarity checking code here #######

       print("Answer sheet:\n", words_from_answersheet)
       print("Answer key:\n", words_from_answerkey)
       return

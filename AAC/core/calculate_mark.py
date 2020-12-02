from core.HandWriting_Recognition.src.imageToText import pdfToText
import re

def getWordsFromPdf(imagePath, splitAnswers = False):
       wordList, accuracyList = pdfToText(imagePath)

       if splitAnswers:
              # split by keyword 'answer'
              text = re.split("answer", wordList)
              if len(text) > 1:
                     text = text[1:]
              return text
       return wordList

def decomposeDictionary(answerKey, includeMarks = False):
       words = []
       marks = []
       for i in range(len(answerKey)):
              key = 'Qn'+str(i+1)
              answer_and_mark = answerKey.get(key)
              words.append(answer_and_mark[0])
              marks.append(answer_and_mark[1])

       # convert individual string elements to a single string list
       words = [' '.join(w) for w in words]
       if includeMarks:
              return words, marks
       return words

def calculateMark():
       imagePath = '/home/hari/Downloads/htr_test.pdf'
       words_from_answersheet = getWordsFromPdf(imagePath, splitAnswers = True)

       answerKey = {'Qn1':[("test1", "test1"), 10],
                    'Qn2':[("test2", "test2"), 20],
                    'Qn3':[("test3", "test3"), 30]}
       words_from_answerkey = decomposeDictionary(answerKey)

       ####### Do similarity checking code here #######

       print("Answer sheet:\n", words_from_answersheet)
       print("Answer key:\n", words_from_answerkey)
       return
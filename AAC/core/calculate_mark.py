from core.HandWriting_Recognition.src.imageToText import pdfToText
from core.grading import answerForSingleQuestion
from pprint import pprint
import numpy as np
import bisect
import spacy
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

def seperateQuestionAnswer(words_from_answersheet):

       qn = ["answer", "answer2", "answer3"]
       nI = len(qn)
       answerFromStudent = {}
       last = len(words_from_answersheet)
       pos1 = bisect.bisect_right(words_from_answersheet, "answer")
       for i in range(1, nI):
              fullanswer = ""
              if i == nI-1:
                     pos2 =  bisect.bisect_right(words_from_answersheet, qn(i))
                     ans = words_from_answersheet[pos1: pos2]
                     for j in ans:
                            fullanswer += j
                            fullanswer += " "
                     answerFromStudent[qn[i-1]: fullanswer]

                     ans = words_from_answersheet[pos2: last-1]
                     for j in ans:
                            fullanswer += j
                            fullanswer += " "
                     answerFromStudent[qn[i]: fullanswer]

              else:
                     pos2 =  bisect.bisect_right(words_from_answersheet, qn(i))
                     ans = words_from_answersheet[pos1: pos2]
                     for j in ans:
                            fullanswer += j
                            fullanswer += " "
                     answerFromStudent[qn[i-1]: fullanswer]
                     pos1 = pos2


       return answerFromStudent


def decomposeDictionary(answerKey, includeMarks = False):
       words = []
       marks = []
       for i in range(len(answerKey)):
              key = 'Q'+str(i+1)
              answer_and_mark = answerKey.get(key)
              if isinstance(answer_and_mark[0], (list, tuple)):
                     temp = ' '.join(answer_and_mark[0])
                     words.append(temp)
              elif isinstance(answer_and_mark[0], str):
                     words.append(answer_and_mark[0])
              marks.append(answer_and_mark[1])

       # convert individual string elements to a single string list
       if includeMarks:
              return words, marks
       return words

def temporarySimilarityChecking(answer, answerKey, mark):
       #nlp = spacy.load('en_core_web_md')
       nlp = spacy.load('en')
       doc1 = nlp(answer)
       doc2 = nlp(answerKey)
       similarity = doc1.similarity(doc2)

       # simple maprange
       value = similarity
       leftMin = 0
       leftMax = 1
       rightMin = 0
       rightMax = mark
       leftSpan = leftMax - leftMin
       rightSpan = rightMax - rightMin
       valueScaled = float(value - leftMin) / float(leftSpan)
       newValue = rightMin + (valueScaled * rightSpan)

       return round(newValue)

def calculateMark(answerSheet, answerKey):
       words_from_answersheet = getWordsFromPdf(answerSheet, splitAnswers = True)


       words_from_answerkey, marks = decomposeDictionary(answerKey, includeMarks=True)

       computedMarks = []
       if len(words_from_answersheet) == len(words_from_answerkey):
              for anskey, ans, mrk in zip(words_from_answerkey, words_from_answersheet, marks):
                     #ans = re.split('\s+', ans)
                     #anskey = re.split('\s+', anskey)
                     #computedMarks.append(answerForSingleQuestion(ans, anskey, mrk))
                     computedMarks.append(temporarySimilarityChecking(ans, anskey, mrk))
       else:
              print("Handwriting Detection error! length of answerkeys and answer doesn't match")

       print(chr(27)+'[2j')
       print('\033c')
       print('\x1bc')

       print('\n**************** Answer Key ****************')
       pprint(words_from_answerkey)
       print('\n************** Detected Answer **************')
       pprint(words_from_answersheet)
       print('\n*************** Total Marks ****************\n', marks, '\n')
       print('************** Computed Marks **************\n', computedMarks, '\n')

       actual_mark = sum(marks)
       computed_mark = sum(computedMarks)

       return actual_mark, computed_mark

def computeGrade(mark):
       if 0.85 <= mark <= 1:
              return 'A'
       elif 0.75 <= mark < 0.85:
              return 'B'
       elif 0.65 <= mark < 0.75:
              return 'C'
       elif 0.55 <= mark < 0.65:
              return 'D'
       elif 0.45 <= mark < 0.55:
              return 'E'
       else:
              return 'F'


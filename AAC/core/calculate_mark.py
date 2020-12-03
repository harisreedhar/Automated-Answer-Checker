from core.HandWriting_Recognition.src.imageToText import pdfToText
from core.grading import answerForSingleQuestion
import re
import bisect
import spacy

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
              key = 'Qn'+str(i+1)
              answer_and_mark = answerKey.get(key)
              words.append(answer_and_mark[0])
              marks.append(answer_and_mark[1])

       # convert individual string elements to a single string list
       #words = [' '.join(w) for w in words]
       if includeMarks:
              return words, marks
       return words

def temporarySimilarityChecking(answer, answerKey, mark):
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
       print(words_from_answersheet)
       words_from_answerkey, marks = decomposeDictionary(answerKey, includeMarks=True)
       print(words_from_answerkey)

       computedMarks = []
       if len(words_from_answersheet) == len(words_from_answerkey):
              for anskey, ans, mrk in zip(words_from_answerkey, words_from_answersheet, marks):
                     #ans = re.split('\s+', ans)
                     #anskey = re.split('\s+', anskey)
                     #computedMarks.append(answerForSingleQuestion(ans, anskey, mrk))
                     computedMarks.append(temporarySimilarityChecking(ans, anskey, mrk))
       else:
              print("Handwriting Detection error! length of answerkeys and answer doesn't match")

       actual_mark = sum(marks)
       computed_mark = sum(computedMarks)

       return actual_mark, computed_mark

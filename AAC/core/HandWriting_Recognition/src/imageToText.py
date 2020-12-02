from __future__ import division
from __future__ import print_function

import os
import sys
import cv2
import argparse
import numpy as np
import editdistance
from core.HandWriting_Recognition.src.Model import Model, DecoderType
from core.HandWriting_Recognition.src.DataLoader import DataLoader, Batch
from core.HandWriting_Recognition.src.SamplePreprocessor import preprocess
from core.HandWriting_Recognition.src.WordSegmentation import wordSegmentation, prepareImg

from core.HandWriting_Recognition.src import page
from core.HandWriting_Recognition.src import words
from core.HandWriting_Recognition.src.utils import pdf_to_image
#from PIL import Image
from autocorrect import Speller
spell = Speller()

from pathlib import Path
def mypath():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	return str(Path(dir_path).parents[0])


class FilePaths:
	"filenames and paths to data"
	fnCharList = mypath() + '/model/charList.txt'
	fnAccuracy = mypath() + '/model/accuracy.txt'
	fnTrain = mypath() + '/data/'
	fnInfer = mypath() + '/data/test.png'
	fnCorpus = mypath() + '/data/corpus.txt'

def infer(model, fnImg):
	img = preprocess(fnImg, Model.imgSize)
	batch = Batch(None, [img])
	(recognized, probability) = model.inferBatch(batch, True)
	return  probability[0], recognized[0]


def linePhotoToTextList(path):
	img = prepareImg(cv2.imread(path), 50)

	res = wordSegmentation(img, kernelSize=25, sigma=11, theta=7, minArea=100)
	stringList = []
	accuracyList = []

	model = Model(open(FilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True)
	for (j, w) in enumerate(res):
		(wordBox, wordImg) = w
		accuracy, text = infer(model, wordImg)

		stringList.append(text)
		accuracyList.append(accuracy)

	return stringList, accuracyList

model = Model(open(FilePaths.fnCharList).read(), DecoderType.BeamSearch, mustRestore=True)

def photoToText(imageArr, autoCorrection = True):
	#image = cv2.cvtColor(cv2.imread(imagePath), cv2.COLOR_BGR2RGB)
	image = cv2.cvtColor(np.asarray(imageArr), cv2.COLOR_BGR2RGB)

	# Crop image and get bounding boxes
	crop = page.detection(image)
	boxes = words.detection(crop)
	lines = words.sort_words(boxes)

	wordImageList = []
    # Saving the bounded words from the page image in sorted way
	i = 0
	for line in lines:
		text = crop.copy()
		for (x1, y1, x2, y2) in line:
			#imageChunk = Image.fromarray(text[y1:y2, x1:x2])
			imageChunk = np.asarray(text[y1:y2, x1:x2])
			wordImageList.append(cv2.cvtColor(imageChunk, cv2.COLOR_BGR2GRAY))
			i += 1

	answer = ""
	accuracyList = []
	for wordImage in wordImageList:
		#wordImage = prepareImg(wordImage, 50)
		accuracy, text = infer(model, wordImage)
		if autoCorrection:
			if accuracy < 0.5:
				text = spell(text)
		answer = answer + " " + text
		accuracyList.append(accuracy)

	return answer, accuracyList

def pdfToText(path):
	images = pdf_to_image(path)
	answer = ""
	accuracyList = []
	for img in images:
		temp1, temp2 = photoToText(img)
		answer = answer + " " + temp1
		accuracyList.extend(temp2)
	return answer, accuracyList

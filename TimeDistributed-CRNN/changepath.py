import os 
import csv
import numpy as np
import cv2
label = []
text = []

with open(r'E:\Code\Test\TimeDistributed-CRNN\Data\unicodefinal.txt', newline = '', encoding="utf-16") as games:                                                                                          
    	game_reader = csv.reader(games, delimiter='\t')
    	for game in game_reader:
            label.append(game[0])
            text.append(game[1])
#print(label)
#print(text)
path1 = "./Data/images_final/"
with open(r'E:\Code\Test\TimeDistributed-CRNN\Data\unicodefinal.txt', newline = '', encoding="utf-16") as games:
    with open(r'E:\Code\Test\TimeDistributed-CRNN\Data\colab.txt', "wt", encoding="utf-16") as fout:
        for line, i in zip(games, range(len(label))):
            fout.write(line.replace(label[i], path1 + label[i]))
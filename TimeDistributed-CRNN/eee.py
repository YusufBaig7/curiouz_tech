import pandas as pd
infile = pd.read_csv(r"E:\Code\Test\TimeDistributed-CRNN\Data\out2.txt", encoding= 'utf-8')
print(infile["Path"])

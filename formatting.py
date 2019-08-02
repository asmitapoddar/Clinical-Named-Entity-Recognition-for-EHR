from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
import pandas as pd
import re

#df = pd.read_csv('Patient1.txt')
file_object = open("/home/asmita/NER/data/Patient1.con",'r')
f = file_object.read()

file_object1 = open("/home/asmita/NER/data/Patient1.txt",'r')
patients = file_object1.read()

#lines = f.readlines()

wordList = re.sub("[^\w]", " ",  f).split()

l = len(f)
print(l)
start = 0
condition_word_list = [""]
conditions = []
tags = []

for i in range(l):
    if f[i]=='\n':
        end = i
        sub = f[start:end]
        sub.find('\"')
        slasharr = [pos for pos, char in enumerate(sub) if char == "\""]
        #find location of quotation marks and subset it
        condition = sub[3:slasharr[1]]
        tag = sub[slasharr[2]+1:slasharr[3]]

        conditions.append(condition)
        tags.append(tag)
        #print('condition=', condition, ' tag = ', tag)

        condition_words = re.sub("[^\w]", " ",  condition).split()
        #print(condition_words)
        condition_word_list.extend(condition_words)
        start=i+1

print(condition_word_list)
print(conditions[0])
print(conditions[0] in condition_word_list)

indices = map(patients.lower().find, conditions)
length_of_conditions = [len(con) for con in conditions]
print(length_of_conditions)
#indices = patients.find(i for i in conditions)
print(conditions)
index_list = list(indices)
print(index_list)
print(len(conditions), len(index_list))

mydict = {}
for i in range(len(length_of_conditions)):
    mydict[conditions[i]]=tags[i]

print('mydict', mydict)


z = index_list.count(-1)
print(z)
print(patients[0:320])
print(min(length_of_conditions))
for i in range(len(length_of_conditions)):
    print(length_of_conditions[i])
    toreplace = '*'*length_of_conditions[i]
    patients = patients.replace( patients[index_list[i]:index_list[i]+length_of_conditions[i]], toreplace)
    #print(patients[index_list[i]:index_list[i] + length_of_conditions[i]])
print(patients[index_list[0]:index_list[0]+length_of_conditions[0]])
print(patients[0:320])

print(patients[400:410])
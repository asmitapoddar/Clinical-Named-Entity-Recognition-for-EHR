from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
import pandas as pd
import re

#df = pd.read_csv('Patient1.txt')
file_object = open("Patient1.txt",'r')
f = file_object.read()

string = str(f)
string_words = string.split()
sentences = f.split('\n')
cleaned_sentences = [e for e in sentences if e not in ('')]
list_of_sen = [e.split() for e in cleaned_sentences]

path = get_tmpfile("word2vec.model")
#model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)
#model.save("word2vec.model")

sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
			['this', 'is', 'the', 'second', 'sentence', 'for'],
			['yet', 'another', 'sentence', 'for'],
			['one', 'more', 'sentence', 'for'],
			['and', 'the', 'final', 'sentence']]

fullFile = re.sub("(\!|\?|\.) ","\\1<BRK>",f)
sentences = fullFile.split("<BRK>")
cleaned_sentence = [[re.sub("\n"," ",line)] for line in sentences]
#list_of_sen = [[e.split()] for e in cleaned_sentence]
print('cleaned_sentence', cleaned_sentence[0])
print('listof_sentence', list_of_sen)
final_sentences = cleaned_sentence


print(final_sentences)
#print(get_tmpfile(sentences[0][0]))

model = Word2Vec(list_of_sen, size=100, window=5, min_count=1, workers=4)
model.train(list_of_sen, total_examples=len(sentences), epochs=10)
#model.train([["hello", "world"]], total_examples=1, epochs=1)
print(model)
words = list(model.wv.vocab)
print('length=', len(words))
print('Unique length', len(set(words)))

#print(model['second'])
print(words)
#print(model.wv['sentence'])
#print('final embedding', model.wv['Admission'])

#print(model.wv.most_similar(positive='Surgical',topn=10))

words_list = [line.split() for line in sentences]
word_flat_list = [item for sublist in words_list for item in sublist]
print('len(word_flat_list)', len(word_flat_list))
print(set(word_flat_list))
print('len(set(word_flat_list))', len(set(word_flat_list)))
wordFile = open("./words.out_Patient1", "w+")
sentFile = open("./sentences.out", "w+")
for line in sentences:
	sentFile.write(line)
	sentFile.write("\n\n")
sentFile.close

for word in word_flat_list:
	wordFile.write(word)
	wordFile.write(" ")
	for item in model.wv[word]:
		wordFile.write(str(item))
		wordFile.write(" ")
	#wordFile.write(str(model.wv[word]))
	wordFile.write("\n")
sentFile.close


print('1. Heart, fracture', model.wv.similarity(w1='heart',w2='fracture'))
print('2. surgery date', model.wv.similarity(w1='surgery',w2='Date'))
print('3. cerebellar encephalomalacia', model.wv.similarity(w1='cerebellar',w2='ventricular'))
#print('4. Surgical elevation', model.wv.similarity(w1='Surgical',w2='augmentation'))


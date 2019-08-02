import re

file_object = open("/home/asmita/NER/data/Patient2.con",'r')
f = file_object.read()  #this contains the dictionary of phrases

file_object1 = open("/home/asmita/NER/data/Patient2.txt",'r')
patients = file_object1.read() #this contains the string
P = patients
patients = patients.replace('.', ' . ')

wordList = re.sub("[^\w].,!", " ",  patients).split()
print(wordList)
l = len(f)
start = 0
condition_word_list = [""]
conditions = []
tags = []

fff = open("tokenized.txt", "w+")
wordlist = patients.split()
for word in wordlist:
    fff.write("( ")
    fff.write(word)
    fff.write(("), ()\n"))
fff.close()


'''
doing some processing to get the dictionary of phrases as a list, the starting index and length of phrases [ O(n) ]
'''
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

#print(conditions) #this is the dictionary of phrases

''' *** This is the part at which you need to take a look *** '''

index_list = list(map(patients.lower().find, conditions) )  #this is the list of starting indices of the phrases
length_of_conditions = [len(con) for con in conditions]  #this is the list of lengths of the phrases


dict_tag = {}
for i in range(len(conditions)):
    dict_tag[conditions[i]] = tags[i]

conditions = list(set(conditions))

for c in conditions:
    if (len(c)<3):
        conditions.remove(c)
        del(dict_tag[c])
#print(dict_tag)
length_of_conditions = [len(con) for con in conditions]  #print(min(length_of_conditions)) = 3

my_dict = {}
my_dict_tag = {}
counter = 1
for c in conditions:
    my_dict[c] = '***'+str(counter)+'***'
    counter+=1

for i in range(len(conditions)):
    #print(conditions[i], length_of_conditions[i])
    #toreplace = '*'*len(conditions[i])
    r = patients.lower().replace(conditions[i], my_dict[conditions[i]])
    #r = r.strip()
    #for q in r:
    #    if q[0:2]=='***'
    patients=r

#print(patients[400:410])
#print(patients)

#split_p = re.findall(r"[\w']+|[.,!?;]", patients)
split_p = patients.split()
final_dict = {}


for k, v in my_dict.items():
    #replacing stars with the conditions
    for n, i in enumerate(split_p):
        if i == v:
            split_p[n] = k

print('AAAAAAAA')
print(split_p)
print('heehaw')


ff = open("split_patients.txt","w+")
for word in split_p:
    if word in conditions:
        #print('okkkkk')
        lll = word.split()
        #print('word list', lll)
        for r in lll:
            final_dict[word] = dict_tag[word]
        s = word + " NNP" + " B-NP " + dict_tag[word]
        ff.write("%s\n" % s)
        #print(s)
    else:
        #print('holy cow')
        s = word + " NNP" + " B-NP " + 'O'
        ff.write("%s\n" % s)
        #print(s)
        final_dict[word] = 'O'

ff.close()

'''
ff = open("/home/asmita/Downloads/Named-Entity-Recognition-with-Bidirectional-LSTM-CNNs-master/data/train.txt","w+")
for k,v in final_dict.items():
    s = k + " NNP" + " B-NP " + v
    print(s)
    ff.write("%s\n" % s)
    #ff.write("\n")
    #ff.write("\n")
ff.close()
print(len(final_dict))

#print('\ufeff' in P.split())
#f=open("train_patient.txt", "r")
#contents = f.read()

'''

import re

file_object = open("/home/asmita/NER/data/Patient2.con",'r')
f = file_object.read()  #this contains the dictionary of phrases

file_object1 = open("/home/asmita/NER/data/patients_sub.txt",'r')
patients = file_object1.read() #this contains the string
P = patients
wordList = re.sub("[^\w]", " ",  f).split()

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

#print(length_of_conditions)
#print(index_list)
#print(patients[0:320])
#print(min(length_of_conditions))

dict_tag = {}
for i in range(len(conditions)):
    dict_tag[conditions[i]] = tags[i]

conditions = list(set(conditions))

for c in conditions:
    if (len(c)<3):
        conditions.remove(c)
        del(dict_tag[c])

length_of_conditions = [len(con) for con in conditions]  #print(min(length_of_conditions)) = 3
print('dict_tag', dict_tag)
tag_dict={}
for i in range(len(conditions)):
    #print(conditions[i], length_of_conditions[i])
    #toreplace = '*'*len(conditions[i])
    lll = conditions[i].split()
    print('word list', lll)
    for r in lll:
        tag_dict[r] = dict_tag[conditions[i]]

split_p = patients.split()
final_dict = {}

print(split_p)
print('heehaw')

for word in split_p:
    if word in list(tag_dict.keys()):
        final_dict[word] = tag_dict[word]
    else:
        final_dict[word] = 'O'

print(final_dict)
print(len(final_dict))

ff = open("patients_sub.txt","w+")
for k,v in final_dict.items():
    s = "('" + k + "' , '" + v + "')"
    print(s)
    ff.write(" %s" % s)
    ff.write("\n")
    #ff.write("\n")
ff.close()
print(len(final_dict))



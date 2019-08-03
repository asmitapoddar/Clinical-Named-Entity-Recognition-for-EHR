import pandas as pd
import re

file_object = open("/home/asmita/Downloads/CliNER/data/examples/Patient2.con",'r')
f = file_object.read()

file_object1 = open("/home/asmita/Downloads/CliNER/data/examples/Patient2.txt",'r')
patients = file_object1.read()

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

print(conditions[0])
#print(conditions[0] in condition_word_list) 

indices = map(patients.lower().find, conditions)
length_of_conditions = [len(con) for con in conditions]
print(length_of_conditions)
#indices = patients.find(i for i in conditions)
print(conditions)
index_list = list(indices)
print(index_list)
print(len(conditions), len(index_list))

print('len(conditions;', len(conditions))
dict_tag = {}
for i in range(len(conditions)):
    dict_tag[conditions[i]] = tags[i]

tests = []
for k,v in dict_tag.items():
    if v=='treatment':
        tests.append(k)
print('length of treatment', len(tests))
ff = open("treatment_exploration.txt","w+")

notin=[23,73,84,148,150,238,404,405,432,434,470,575,663,817,839,850,927]
for i in range(len(tests)):
    if i in notin:
        continue
    result = [m.start() for m in re.finditer(tests[i], patients.lower())]
    print(i, tests[i], result)
    if len(result)!=0:
        for ind in result:
            #print(patients[ind:ind+len(tests[i])])
            pre_words = []
            count=0
            p = ind - 1
            while(count<6):

                for j in range(p-1, 0, -1):
                    if ( patients[j]==' ' or patients[j]=='\n'):
                        sub = patients[j:p]
                        p=j
                        break
                count=count+1
                pre_words.append(sub)
            pre_words = list(reversed(pre_words))

            post_words = []
            count = 0
            p = ind + len(tests[i])
            while (count < 6):
                for j in range(p+1,len(patients),1):
                    if ( patients[j] == ' ' or patients[j]=='\n' ):
                        sub = patients[p:j]
                        p = j
                        break
                count = count + 1
                post_words.append(sub)
            #print(pre_words) #print(tests[i]) #print(post_words)

            ff.write(str(pre_words))
            ff.write("\n")
            ff.write(tests[i])
            ff.write("\n")
            ff.write(str(post_words))
            ff.write("\n\n")
ff.close()

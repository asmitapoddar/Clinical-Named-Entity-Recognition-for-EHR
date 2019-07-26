import pandas as pd
import re
import collections

'''
### Creating a smaller subfile to play with
df = pd.read_csv('/home/asmita/EHR/NOTEEVENTS.csv')
#df.head(1000)
df.head(1000).to_csv('/home/asmita/EHR/subfile.csv')
'''

df = pd.read_csv('/home/asmita/EHR/subfile.csv')
df = pd.read_csv('/home/asmita/EHR/NOTEEVENTS.csv')

'''
firsttext = df['TEXT'][1]
print('Row ID:', df['ROW_ID'][1])
print('Subject ID:', df['SUBJECT_ID'][1])
print('HADM ID:', df['HADM_ID'][1])
print('CHARTDATE:', df['CHARTDATE'][1])
print('CHARTTIME:', df['CHARTTIME'][1])
print('STORETIME:', df['STORETIME'][1])
print('CATEGORY:', df['CATEGORY'][1])
print('DESCRIPTION:', df['DESCRIPTION'][1])
print('CGID:', df['CGID'][1])
print('ISERROR:', df['ISERROR'][1])
print( firsttext )
'''

type(df['TEXT'][1])  # str
list(df)  #['ROW_ID', 'SUBJECT_ID', 'HADM_ID', 'CHARTDATE', 'CHARTTIME', 'STORETIME', 'CATEGORY', 'DESCRIPTION', 'CGID', 'ISERROR', 'TEXT']

len(df['ROW_ID'].unique())   #2083180 unique entries (visits)
len(df['SUBJECT_ID'].unique())   # 46146 unique patients

#print('Dates:', df['CHARTDATE'].head(20) )

df.shape   # (2083180, 11)
'''
print('Unique descriptions:', df['DESCRIPTION'].unique())
print('Unique categories:', df['CATEGORY'].unique())

Unique descriptions: ['Report' 'Addendum' 'Nursing Transfer Note' ...
 'PLACE CATH CAROTID/INOM ART' 'L US MSK ASPIRATE/INJ GANGLION CYST LEFT' 'RO HIP NAILING IN OR W/FILMS & FLUORO RIGHT IN O.R.']
 
Unique categories: ['Discharge summary' 'Echo' 'ECG' 'Nursing' 'Physician ' 'Rehab Services' 'Case Management ' 'Respiratory ' 'Nutrition' 'General' 'Social Work'
 'Pharmacy' 'Consult' 'Radiology' 'Nursing/other']
 '''
cnt = collections.Counter()
for word in df['CATEGORY']:
    cnt[word] += 1

most_common = cnt.most_common()
print('Counters for category:', most_common)      #('Discharge summary', 59652)

#nursing = df[df['CATEGORY']=='Nursing/other'] print('NURSING', nursing['TEXT'].iloc[0])
ds = df[df['CATEGORY']=='Discharge summary']  #59652

dsc = collections.Counter()
for patient in ds['SUBJECT_ID']:
    dsc[patient] += 1

'''
Top patients of discharge summaries
[(13033, 47),
 (109, 34),
 (11861, 32),
 (5060, 29),
 (11318, 28),
 (20643, 27),
 (23707, 24),
 (19213, 23)
 '''

p13033 = ds[ds['SUBJECT_ID']==13033]

#wordList = re.sub("[^\w]", " ", df['TEXT'][14]).split()
service = []
#print(wordList)

ds['SERVICE']=None
for i in range(0,2000):  #Taking part of the discharge summaries to tag them
    wordList = re.sub("[^\w]", " ", ds['TEXT'].iloc[i]).split()
    wordList = [x.upper() for x in wordList]
    if 'SERVICE' in wordList:
        s = wordList[wordList.index('SERVICE')+1]
        ds['SERVICE'].iloc[i]=s
        service.append(s)
unique_service = set(service)
print(unique_service)

#Services for Discharge summaries
us = collections.Counter()
for item in service:
    us[item] += 1

#

common_service = us.most_common()  #Medicine
print(common_service)

#for item in unique_service:
#    print(item, service.count(item))

#valuecounte = df.SUBJECT_ID.value_counts()

'''
nursing = df[df['CATEGORY']=='Nursing/other']
print('Nursing/other---', nursing['TEXT'].iloc[0])
print('Nursing/other', nursing['TEXT'].iloc[1])

Radiology = df[df['CATEGORY']=='Radiology']
print('Radiology---', Radiology['TEXT'].iloc[0])
print('Radiology', Radiology['TEXT'].iloc[1])

Nursing = df[df['CATEGORY']=='Nursing']
print('Nursing---', Nursing['TEXT'].iloc[0])
print('Nursing', Nursing['TEXT'].iloc[1])

ECG = df[df['CATEGORY']=='ECG']
print('ECG----', ECG['TEXT'].iloc[0])
print('ECG', ECG['TEXT'].iloc[1])

#Physician = df[df['CATEGORY']=='Physician']
#print('Physician---', Physician['TEXT'].iloc[0])
#print('Physician', Physician['TEXT'].iloc[1])

Discharge_summary = df[df['CATEGORY']=='Discharge summary']
print('Discharge summary---', Discharge_summary['TEXT'].iloc[0])
print('Discharge summary', Discharge_summary['TEXT'].iloc[1])

Echo = df[df['CATEGORY']=='Echo']
print('Echo---', Echo['TEXT'].iloc[0])
print('Echo', Echo['TEXT'].iloc[1])

Respiratory = df[df['CATEGORY']=='Respiratory']
print('Respiratory---', Respiratory['TEXT'].iloc[0])
print('Respiratory', Respiratory['TEXT'].iloc[1])

Nutrition = df[df['CATEGORY']=='Nutrition']
print('Nutrition---', Nutrition['TEXT'].iloc[0])
print('Nutrition', Nutrition['TEXT'].iloc[1])

General = df[df['CATEGORY']=='General']
print('General---', General['TEXT'].iloc[0])
print('General', General['TEXT'].iloc[1])

Rehab_Services = df[df['CATEGORY']=='Rehab Services']
print('Rehab Services---', Rehab_Services['TEXT'].iloc[0])
'''

medicine = ds[ds['SERVICE']=='MEDICINE']
print(len(medicine))

file = open("folder/medicinesub.txt","w")
for i in range(0,len(medicine)):
    file.write(medicine['TEXT'].iloc[i])
    if(i%100==0):
        print(i)
file.close()
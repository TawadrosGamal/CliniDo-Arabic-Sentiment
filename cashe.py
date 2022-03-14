# coding=utf-8
import json
#Load Sentiment Model
#from transformers import pipeline1
# initialize pipline
#pipe = pipeline("sentiment-analysis", model="/content/drive/MyDrive/Arabic_Sentiment_Analysis", device=0, return_all_scores=True)
#Load Data for Search

 

Arabic_specalities=[]
English_specalities=[]
with open("Arabic_fixed_specalities.txt","r", encoding="utf8") as f1,open("English_fixed_specalities.txt","r", encoding="utf8") as f2:
  Arabic_specalities_raw=f1.read()
  English_specalities_raw=f2.read()
f1.close()
f2.close()
#loading in lists
for ara_spec,eng_spec in zip(Arabic_specalities_raw.splitlines(),English_specalities_raw.splitlines()):
  Arabic_specalities.append(ara_spec)
  English_specalities.append(eng_spec)
Arabic_area_city=[]
English_area_city=[]
Arabic_city=[]
English_city=[]
Arabic_area=[]
English_area=[]
with open("Arabic_city_area.txt","r", encoding="utf8") as f1,open("English_city_area.txt","r", encoding="utf8") as f2:
  Arabic__area_city_raw=f1.read()
  English_area_city_raw=f2.read()
f1.close()
f2.close()
for ara_row,eng_row in zip(Arabic__area_city_raw.splitlines(),English_area_city_raw.splitlines()):
  Arabic_area_city.append((ara_row.split(",")[0],ara_row.split(",")[1]))
  English_area_city.append((eng_row.split(",")[0],eng_row.split(",")[1]))
  Arabic_city.append(ara_row.split(",")[1])
  Arabic_area.append(ara_row.split(",")[0])
  English_city.append(eng_row.split(",")[1])
  English_area.append(eng_row.split(",")[0])
#loading all words in words set
words=set()
#loading bigger words than 1 phrase
specalities_biger=[]
cities_biger=[]
areas_biger=[]
'''
for sentence in Arabic_specalities:
  if len(sentence.split(" "))>1:
    specalities_biger.append(sentence)
  for word in sentence.split(" "):
    words.add(word)
'''
Arabic_specalities_one_phrase=[]
Arabic_areas_one_phrase=[]

# Opening JSON file
with open('arabic_specalities.json', encoding="utf8") as json_file:
    specalities = json.load(json_file)

with open('arabic_areas.json', encoding="utf8") as json_file2:
    areas = json.load(json_file2)

for va_list in specalities.values():
  for sentence in va_list:
    if len(sentence.split(" "))>1 : 
      specalities_biger.append(sentence)
    else:
      Arabic_specalities_one_phrase.append(sentence)

    for word in sentence.split(" "):
        words.add(word)

for sentence in Arabic_city:
  if len(sentence.split(" "))>1:
    cities_biger.append(sentence)
  for word in sentence.split(" "):
    words.add(word)

for va_list in areas.values():
  for sentence in va_list:
    if len(sentence.split(" "))>1 : 
      areas_biger.append(sentence)
    else:
      Arabic_areas_one_phrase.append(sentence)

    for word in sentence.split(" "):
        words.add(word)


key_words=["انا","عاوز","اكشف","هاكشف","علي","في","هاستشير","ابحث"]

for word in key_words:
  words.add(word)



words_excluded=['الجديدة','جراحة','مدينة','القاهرة',"(التجمع)"]
for word in words_excluded:
  words.remove(word)
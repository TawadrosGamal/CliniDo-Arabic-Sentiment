# -*- coding: utf-8 -*-
from cashe import Arabic_specalities,Arabic_area_city,English_specalities,English_area_city,Arabic_city,English_city
from cashe import Arabic_area,English_area,words,specalities_biger,cities_biger,areas_biger,areas,Arabic_areas_one_phrase,specalities,Arabic_specalities_one_phrase
from difflib import get_close_matches
from nltk.tokenize import MWETokenizer
from flask import Flask, request, jsonify
import time

def closeMatches(patterns, word): 
    return get_close_matches(word, patterns, n=1, cutoff=0.8)

app = Flask("CliniDoSmartSearch")




@app.route('/',methods=["GET"])
def hello_world():
    return "This API is for CliniDo's Smart Search!"

@app.route('/Search', methods=["POST"])
def SearchText():
  time.time()
  timestamp1 = time.time()
  try :


    input_json = request.get_json(force=True)
    values=input_json['text'].encode('utf-8')
    ar_inputs=values.decode('utf-8')
    ar_inputs_list=ar_inputs.split(" ")
    out_sentence=""
    for word in ar_inputs_list:
      match=closeMatches(words,word)
      if len(match)>0:
        out_sentence+=match[0]+" "
        #select 1 word phrases
        if match[0] in Arabic_specalities_one_phrase and match[0] in speckey_list:
          found_specalities.add(match[0])

        elif match[0] in Arabic_specalities_one_phrase and match[0] not in speckey_list:
          for ind,spec_list in enumerate(specval_list):
            if match[0] in spec_list:
              found_specalities.add(speckey_list[ind])

        elif match[0] in Arabic_areas_one_phrase and  match[0]  in areaskey_list:
          found_areas.add(match[0])

        elif match[0] in Arabic_areas_one_phrase and match[0] not in areaskey_list:
          for ind,area_list in enumerate(areasval_list):
            if match[0] in area_list:
              found_areas.add(areaskey_list[ind])

        elif match[0] in Arabic_city:
          found_cities.add(match[0])

      #correct input text  
      else:
        out_sentence+=word+" "
    #select two or more words phrases
    Specality_tokenizer = MWETokenizer()
    for spe in specalities_biger:
      Specality_tokenizer.add_mwe(spe.split())

    City_tokenizer = MWETokenizer()
    for cit in cities_biger:
      City_tokenizer.add_mwe(cit.split())

    Area_tokenizer = MWETokenizer()
    for are in areas_biger:
      Area_tokenizer.add_mwe(are.split())
    
    spec=set(Specality_tokenizer.tokenize(out_sentence.split()))
    city=set(City_tokenizer.tokenize(out_sentence.split()))
    area=set(Area_tokenizer.tokenize(out_sentence.split()))
    #adding two or more words phrases 
    for s in spec:
      if "_" in s:
        specality_value=s.replace("_"," ")
        for ind,spec_list in enumerate(specval_list):
          if specality_value in spec_list:
              found_specalities.add(speckey_list[ind])
          if specality_value in found_specalities and  specality_value not in speckey_list:
              found_specalities.remove(specality_value)

    for c in city:
      if "_" in c:
        found_cities.add(c.replace("_"," "))

    for a in area:
      if "_" in a:
        area_value=a.replace("_"," ")
        for ind,area_list in enumerate(areasval_list):
          if area_value in area_list:
              found_areas.add(areaskey_list[ind])
          if area_value in found_areas and  area_value not in areaskey_list:
              found_areas.remove(area_value)

    #matching city with area  
    for area in found_areas:
      area_index=Arabic_area.index(area)
      indexed_city=Arabic_city[area_index]
      if indexed_city in found_cities:
        print(indexed_city)
      else:
        found_cities.add(indexed_city)
    Sfound_not_remove=['جراحه وجه و فكين','جراحه اورام','جراحة سمنه ومناظير','جراحة مخ وأعصاب','جراحه قلب وصدر','جراحه اوعيه دمويه','جراحة عمود فقرى','جراحة تجميل','جراحه أطفال']
    AFound_and_remove=['شبرا']
    #keep valied specalities
    for spec in Sfound_not_remove:
      if spec in found_specalities:
        found_specalities.clear()
        found_specalities.add(spec)
    #remove unvalid areas
    for area in AFound_and_remove:
      if area in found_areas:
        found_areas.remove(area)
    timestamp2 = time.time()
    timetext="This took %.2f seconds" % (timestamp2 - timestamp1)
    dictToReturn1 = {"Speciality":str(found_specalities),"City":str(found_cities),"Area":str(found_areas),"ExecutionTime":str(timetext),"CorrextedText":str(out_sentence)}
    return jsonify(dictToReturn1)

  except Exception as E:
    text_exp="Theres is a problem in the request or the JSON format and the exception caught is  "
    print(text_exp+str(E))
    dictToReturn_err_exp = {'Error':text_exp+str(E)}
    return jsonify(dictToReturn_err_exp)

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(E):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(E), 404


@app.errorhandler(500)
def server_error(E):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(E), 500

if __name__ == '__main__':
  found_specalities=set()
  found_areas=set()
  found_cities=set()
  speckey_list = list(specalities.keys())
  specval_list = list(specalities.values())
  areaskey_list = list(areas.keys())
  areasval_list = list(areas.values())
  app.run(host='0.0.0.0', port=20000)

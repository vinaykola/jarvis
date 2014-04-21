import urllib2
import json

import csv

COMIC_VINE_API_KEY = "37a0f6cdbe5752b2f272373ba6a21491ea2629eb"
DATA_DIR = "../data/"
graph_file = "output1.csv"
#from common.writers import CSVWriter
class util:
    def __init__(self,typeOfFeature,features):
        self.typeOfFeatureNeeded = typeOfFeature
        self.listoffeatures = features

    def getFeatures(self,name):
        url = self.char_url_generator (name)
        json_data = self.get_json_response (url)
        relevantUrl = self.get_character_url (json_data)
        #Now we have got the url for the person we are searching for
        urlForCharacter = self.get_char_url_generator_specific(relevantUrl)
        dataForCharacter = self.get_json_response(urlForCharacter)
        return dataForCharacter

    def getURLFeatures(self,url):
        json_data = self.get_json_response (url)
        relevantUrl = self.get_character_url (json_data)
        urlForCharacter = self.get_char_url_generator_specific(relevantUrl)
        dataForCharacter = self.get_json_response(urlForCharacter)
        return dataForCharacter

    def extractFeatureNames(self,dataForCharacter,featureName):
        names = map (lambda x:(x["name"], x["api_detail_url"]), dataForCharacter["results"][featureName])
        return names

    def char_url_generator (self,name):
        base_url = "http://www.comicvine.com/api/"+self.typeOfFeatureNeeded
        api_key= "api_key" + "=" + COMIC_VINE_API_KEY
        filter_string ="filter" + "=" + "name:" + name
        format_string = "format" + "=" + "json"
        suffix_url = "&".join ([api_key, filter_string, format_string])
        query_url = base_url + "?" + suffix_url
        print query_url
        return query_url

    def get_json_response (self,url):
        response = urllib2.urlopen (url)
        response_string = response.read()
        js_object =  json.loads (response_string)
        return js_object

    def get_character_url (self,js_object):
        character_url = js_object["results"][0]["api_detail_url"]
        return character_url

    def get_char_url_generator_specific (self,base_url):
        api_key = "api_key" + "=" + COMIC_VINE_API_KEY
        fields = "field_list="+",".join(self.listoffeatures)
        format_string = "format=json"
        suffix_url = "&".join ([api_key, fields, format_string])
        query_url = base_url + "?" + suffix_url
        return query_url

    def get_ascii (string):
        return string.encode ("ascii", "ignore")
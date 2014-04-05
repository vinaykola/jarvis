import urllib2
import json

from common.writers import CSVWriter

COMIC_VINE_API_KEY = "37a0f6cdbe5752b2f272373ba6a21491ea2629eb"
DATA_DIR = "../data/"

graph_file = DATA_DIR + "output1.csv"

def char_url_generator (name):
    base_url = "http://www.comicvine.com/api/characters/"
    api_key= "api_key" + "=" + COMIC_VINE_API_KEY
    filter_string ="filter" + "=" + "name:" + name
    format_string = "format" + "=" + "json"
    suffix_url = "&".join ([api_key, filter_string, format_string])
    query_url = base_url + "?" + suffix_url
    return query_url

def char_url_generator (name):
    base_url = "http://www.comicvine.com/api/characters/"
    api_key= "api_key" + "=" + COMIC_VINE_API_KEY
    filter_string ="filter" + "=" + "name:" + name
    format_string = "format" + "=" + "json"
    suffix_url = "&".join ([api_key, filter_string, format_string])
    query_url = base_url + "?" + suffix_url
    return query_url

def get_json_response (url):
    response = urllib2.urlopen (url)
    response_string = response.read()
    js_object =  json.loads (response_string)
    return js_object

def get_character_url (js_object):
    character_url = js_object["results"][0]["api_detail_url"]
    return character_url

def get_char_url_generator_specific (base_url):
    api_key = "api_key" + "=" + COMIC_VINE_API_KEY
    fields = "field_list=name,character_enemies,character_friends"
    format_string = "format=json"
    suffix_url = "&".join ([api_key, fields, format_string])
    query_url = base_url + "?" + suffix_url
    return query_url

def get_enemies (char_js_object):
    enemies = map (lambda x:(x["name"], x["api_detail_url"]), char_js_object["results"]["character_enemies"])
    return enemies

def get_friends (char_js_object):
    friends = map (lambda x:(x["name"], x["api_detail_url"]), char_js_object["results"]["character_friends"])
    return friends

def get_ascii (string):
    return string.encode ("ascii", "ignore")

url = char_url_generator("batman")
js_object = get_json_response (url)
base_character_url = get_character_url (js_object)
char_url = get_char_url_generator_specific (base_character_url)
char_js_object = get_json_response (char_url)

enemies = get_enemies (char_js_object)
friends = get_friends (char_js_object)

items = [("Batman", "http://www.comicvine.com/api/character/4005-1699/")]

csv_writer = CSVWriter(graph_file, "w")

for name, url in items:
    char_url = get_char_url_generator_specific (url)
    char_js_object = get_json_response (char_url)
    enemies = get_enemies (char_js_object)
    friends = get_friends (char_js_object)
    
    for enemy, _url in enemies:
        csv_writer.writerow ([get_ascii (name.lower()), get_ascii (enemy.lower()), "0"])
        enemy_json = get_json_response (get_char_url_generator_specific (_url))
        more_enemies = get_enemies (enemy_json)
        more_friends = get_friends (enemy_json)
        for more_enemy, _ in more_enemies:
            csv_writer.writerow([get_ascii (enemy.lower()), get_ascii (more_enemy.lower()), "0"])
        for more_friend, _ in more_friends:
            csv_writer.writerow([get_ascii (enemy.lower()), get_ascii (more_friend.lower()), "1"])
        
    for friend, _url in friends:
        csv_writer.writerow ([get_ascii (name.lower()), get_ascii (friend.lower()), "1"])
        friend_json = get_json_response (get_char_url_generator_specific (_url))
        more_enemies = get_enemies (friend_json)
        more_friends = get_friends (friend_json)
        for more_enemy, _ in more_enemies:
            csv_writer.writerow([get_ascii (friend.lower()), get_ascii (more_enemy.lower()), "0"])
        for more_friend, _ in more_friends:
            csv_writer.writerow([get_ascii (friend.lower()), get_ascii (more_friend.lower()), "1"])
            
csv_writer.close()

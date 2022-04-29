import requests
import json
# can import the API Key from a module file to make the program safe.
import secrets_keys
# from printTree import printTree
from flask import Flask, render_template, request
from datetime import date
from build_tree import thetree
from readtree import read_tree_from_json


# the functions for the APIs
# weather API
def weather_API(location):
    url_weather = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q": location, "days": "3"}
    apikey = secrets_keys.apikey_weatherapi

    headers = {
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        "X-RapidAPI-Key": apikey
    }
    # caching
    request_key = construct_unique_key(url_weather, querystring)
    if request_key in CACHE_DICT_weather.keys():
        print("cache hit!", request_key)
        # return CACHE_DICT_weather[request_key]
    else:
        print("cache miss!", request_key)
        # CACHE_DICT_weather[request_key] = make_request(baseurl, params)
        weather_response = requests.request("GET", url_weather, headers=headers, params=querystring)
        weather_json = weather_response.json()
        CACHE_DICT_weather[request_key] = weather_json
        save_cache(CACHE_DICT_weather, cache_weather_name)

    # print(CACHE_DICT_weather[request_key]['location']['name'])
    return CACHE_DICT_weather[request_key]


def covid_API(coordinates):
    # covid API
    url_covid = "https://geocovid-19.p.rapidapi.com/geocovid"
    querystring = {"coordinates": coordinates}

    headers = {
        "X-RapidAPI-Host": "geocovid-19.p.rapidapi.com",
        "X-RapidAPI-Key": secrets_keys.apikey_covidapi
    }

    # caching
    request_key = construct_unique_key(url_covid, querystring)
    if request_key in CACHE_DICT_covid.keys():
        print("cache hit!", request_key)
    else:
        print("cache miss!", request_key)
        covid_response = requests.request("GET", url_covid, headers=headers, params=querystring)
        covid_json = covid_response.json()
        CACHE_DICT_covid[request_key] = covid_json
        save_cache(CACHE_DICT_covid, cache_covid_name)


    # print(CACHE_DICT_covid[request_key]['response']['data']['place_name'])
    # print(CACHE_DICT_covid[request_key]['response']['data']['last_7_days_trend'])

    return CACHE_DICT_covid[request_key]


def yelp_API(params):
    apikey = secrets_keys.apikey_yelpfusionapi
    headers = {'Authorization': 'Bearer ' + apikey}
    baseurl = 'https://api.yelp.com/v3/businesses/search?'


    # caching
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT_yelp.keys():
        print("cache hit!", request_key)
    else:
        print("cache miss!", request_key)
        yelp_response = requests.get(baseurl, params, headers=headers)
        # print('yelp response code', yelp_response.status_code)
        yelp_json = yelp_response.json()
        CACHE_DICT_yelp[request_key] = yelp_json
        save_cache(CACHE_DICT_yelp, cache_yelp_name)
    # print(CACHE_DICT_yelp[request_key])
    return CACHE_DICT_yelp[request_key]


###########################################################################################
# the caching part
def open_cache(cache_filename):
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(cache_filename, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}

    return cache_dict


def save_cache(cache_dict, cache_filename):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(cache_filename,"w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and
    repeatably identify an API request by its baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the unique key as a string
    '''
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()

    today = date.today()
    today_str = str(today)

    unique_key = baseurl + connector + connector.join(param_strings) + today_str
    return unique_key



####################################################################################
# functions for the tree
def yes(prompt):
    while True:
        content = input(prompt)
        if content in ['yes', 'y', 'yup', 'sure']:
            return True
        elif content in ['no', 'n', 'nope']:
            return False
        else:
            print("Not a valid input, please enter \"yes\" or \"no\": ")


def simplePlay(tree):
    """DOCSTRING!"""
    # 1. If the tree is a leaf, print the content in the first iterm of the lesf,
    # ask the user whether they want to explore the details of the businesses by the urls.

    # 2. If the tree is not a leaf, ask the questions in the tree, that is tree[0],
    # which asks the user to choose a condition,
    # If the user answers "former", call yourself recursively on the subtree that is the second element in the triple.
    # If the user answers "latter", recur on the subtree that is the third element in the triple.
    if isLeaf(tree):
        businesses_name = [x['name'] for x in tree[0][1]]
        businesses_details = [[x['name'], x['url']] for x in tree[0][1]]  # check format
        print(tree[0][0], businesses_name)
        # covid_trend = covid_content['response']['data']['last_7_days_trend']
        # print(f'By the way, the COVID trend in the last 7 days there is {covid_trend}')
        ans = yes('Do you want to explore the details? ')
        if ans:
            for details in businesses_details:
                print(details)
        else:
            print('Thank you!')

    else:
        sort2 = request.form["sort"]
        try:
            weather_condi1 = tree[0][0].split()
            weather_condi2 = weather_condi1[-4]
        except:
            weather_condi2 = 'any_value'
        if sort2 == "rating" or sort2 == weather_condi2:
            content = 'former'
        else:
            content = 'latter'
        # content = input(f'{tree[0]} Enter \"former\" or \"latter\": ')

        if content == 'former':
            tree = tree[1]
            return simplePlay(tree)  # there is no return value when recursively call the function itself, so return the function
        elif content == 'latter':
            tree = tree[2]
            return simplePlay(tree)



def isLeaf(tree):
    if (tree[1] == None) and (tree[2] == None):
        return True
    else:
        return False

def testprint():
    location2 = request.form["location"]
    print(location2)
    return location2


# store the tree to a list
def printTree_file(tree, prefix = '', bend = '', answer = ''):
    """Recursively print a 20 Questions tree in a human-friendly form.
       TREE is the tree (or subtree) to be printed.
       PREFIX holds characters to be prepended to each printed line.
       BEND is a character string used to print the "corner" of a tree branch.
       ANSWER is a string giving "Yes" or "No" for the current branch."""
    # newfilename = "printed_tree.txt"
    # treefile = open(newfilename, 'w')

    text, left, right = tree
    if left is None  and  right is None:
        tree_list.append(f'{prefix}{bend}{answer} {text}')
    else:
        tree_list.append(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree_file(left, prefix, '+-', "former: ")
        printTree_file(right, prefix, '`-', "latter:  ")


# flask app
app = Flask(__name__)


# homepage
@app.route('/')
def home_page():
    return render_template('qst.html')


@app.route('/builddata', methods=['POST'])
def api_page():
    # call the weather api
    location = request.form["location"]
    weather_content = weather_API(location)
    weather_cond = weather_content['current']['condition']['text']

    # wind_kph = weather_content['current']['wind_kph']
    # print(weather_content['current']['condition']['text'])
    # print(f'the wind is: {wind_kph} kph')

    # call the covid api
    coordinates = f'{weather_content["location"]["lat"]},{weather_content["location"]["lon"]}'
    covid_content = covid_API(coordinates)
    global covid_trend

    covid_trend = covid_content['response']['data']['last_7_days_trend']

    # call the yelp api
    params = {'term': 'food', 'location': location}
    content_yelp = yelp_API(params)

    ####################################################################################
    # build a tree
    weathercond_today = weather_content['forecast']['forecastday'][0]['day']['condition']['text']
    weathercond_tomorrow = weather_content['forecast']['forecastday'][1]['day']['condition']['text']
    degree_sign = u'\N{DEGREE SIGN}'
    tem_today = str(weather_content['forecast']['forecastday'][0]['day']["mintemp_c"])+degree_sign+'C - ' + str(weather_content['forecast']['forecastday'][0]['day']["maxtemp_c"])+degree_sign+'C'
    tem_tomorrow = str(weather_content['forecast']['forecastday'][1]['day']["mintemp_c"]) + degree_sign + 'C - ' + \
                str(weather_content['forecast']['forecastday'][1]['day']["maxtemp_c"]) + degree_sign + 'C'
    global weather_today
    global weather_tomorrow
    weather_today = weathercond_today+', '+tem_today
    weather_tomorrow = weathercond_tomorrow + ', ' + tem_tomorrow

    weather_qst = f'Do you like {weather_today} or {weather_tomorrow}?'

    list_businesses_rating = content_yelp['businesses']
    list_businesses_rating.sort(key=lambda x: x['rating'], reverse=True)
    list_businesses_rating = list_businesses_rating[0:5]

    list_businesses_price = content_yelp['businesses']
    list_businesses_price.sort(key=lambda x: x['rating'], reverse=False)
    list_businesses_price = list_businesses_price[0:5]

    global finalTree

    # finalTree = \
    #     ("Would you like to sort by rating or price?",
    #      (weather_qst,
    #       (['I suggest you go today, this is the 5 restaurants sorted by rating:', list_businesses_rating], None, None),
    #       (['I suggest  you go tomorrow, this is the 5 restaurants sorted by rating:', list_businesses_rating], None,
    #        None)),
    #      (weather_qst,
    #       (['I suggest you go today, this is the 5 restaurants sorted by price:', list_businesses_price], None, None),
    #       (['I suggest you go tomorrow, this is the 5 restaurants sorted by price:', list_businesses_price], None,
    #        None)))

    finalTree_obj = thetree(weather_qst, list_businesses_rating, list_businesses_price)
    finalTree = finalTree_obj.final_tree
    finalTree_obj.save_tree_json()

    tree_list.clear()
    printTree_file(finalTree)


    return render_template('selections.html', weather_cond=weather_cond, tree=finalTree, weather_today=weather_today, weather_tomorrow=weather_tomorrow, tree_list=tree_list)


@app.route('/results', methods=['POST'])
def results_page():
    sortstd = request.form["sort"]
    weather = request.form["weather"]

    # tree1 = finalTree
    tree1 = read_tree_from_json('finalTree.json')

    if sortstd == 'former':
        trees = tree1[1]
    else:
        trees = tree1[2]

    if weather == 'former':
        leaf = trees[1]
        weather_cod = weather_today
    else:
        leaf = trees[2]
        weather_cod = weather_tomorrow

    businesses_name = [x['name'] for x in leaf[0][1]]
    businesses_details = [[x['name'], x['url']] for x in leaf[0][1]]  # check format
    suggestion = leaf[0][0]

    # tree_from_json = read_tree_from_json('finalTree.json')

    return render_template('results_new.html', businesses_name=businesses_name, businesses_details=businesses_details, suggestion=suggestion, businesses=leaf[0][1], tree_list=tree_list, covid_trend=covid_trend, weather_cod=weather_cod)


@app.route('/tree')
def tree():
    return render_template('tree.html', tree_list=tree_list)







if __name__ == "__main__":
    global tree_list
    tree_list =[]

    CACHE_DICT_weather = {}
    cache_weather_name = 'cache_weather.json'
    CACHE_DICT_weather = open_cache(cache_weather_name)

    CACHE_DICT_covid = {}
    cache_covid_name = 'cache_covid.json'
    CACHE_DICT_covid = open_cache(cache_covid_name)

    CACHE_DICT_yelp = {}
    cache_yelp_name = 'cache_yelp.json'
    CACHE_DICT_yelp = open_cache(cache_yelp_name)

    finalTree = None

    ####################################################################################
    # # preprocess the data from the yelp API
    # list_businesses = content_yelp['businesses']
    # list_businesses.sort(key=lambda x: x['rating'], reverse=True)
    # print('sort', list_businesses)
    # high_rate_list = list_businesses[0:5]
    # print(high_rate_list[-1])



    app.run(debug=True)













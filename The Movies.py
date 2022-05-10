
import requests
from selenium import webdriver   
import json

API_KEY = 'YOUR_API_KEY'
LOGIN = 'LOGIN'
PASSWORD = 'PASSWORD'


#To understand how the api works and why each step within this code, consult the api documentation through this link: https://developers.themoviedb.org/3/getting-started/introduction 


# Make a request via get to generate a new token id
response = requests.get(f'https://api.themoviedb.org/3/authentication/token/new?api_key={API_KEY}')

request_token_generate = (response.json())
request_token = request_token_generate['request_token']


# For you to be able to get your account information, after getting the new request_token,
# you need to allow the Third Party Authentication Request through the url: https://www.themoviedb.org/authenticate/newtokenid
# So i use selenium to do that auto authentication for me

op = webdriver.ChromeOptions()
op.add_argument('--headless')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
op.add_argument('user-agent={0}'.format(user_agent))
driver = webdriver.Chrome(options=op)
driver = webdriver.Chrome('PATH/TO/WEBDRIVER',options=op)

driver.get(f'https://www.themoviedb.org/login')

driver.find_element_by_xpath('//*[@id="username"]').send_keys(f'{LOGIN}')

driver.find_element_by_id('password').send_keys(f'{PASSWORD}')

driver.find_element_by_id('login_button').click()


driver.get(f'https://www.themoviedb.org/authenticate/{request_token}')
driver.find_element_by_xpath('//*[@id="allow_authentication"]').click()


# Make a request via get to generate a session id
get_session_id =  requests.get(f'https://api.themoviedb.org/3/authentication/session/new?api_key={API_KEY}&request_token={request_token}')

session_id_generate = (get_session_id.json())
session_id = session_id_generate['session_id']

# Make a request via get to get a user_id from user
get_user_id = requests.get(f'https://api.themoviedb.org/3/account?api_key={API_KEY}&session_id={session_id}')

info_user = get_user_id.json()
user_id = info_user['id']
username = info_user['username']

print('API DATA INFORMATION')
print('*'*100)
print(f'Username: {username}')
print(f'User ID: {user_id}')
print(f'Session: {session_id}')
print(f'Request_token: {request_token}')
print('*'*100)


# Get the favorite movies from account
favorites_movies = requests.get(f'https://api.themoviedb.org/3/account/{user_id}/favorite/movies?api_key={API_KEY}&language=en-US&sort_by=created_at.asc&page=1&session_id={session_id}')
favorites_movies_info_dict = favorites_movies.json()

# Will turn python dictionary into a json file
favorites_movies_info_json = json.dumps(favorites_movies_info_dict, indent = 4) 
print(favorites_movies_info_json)

print('*'*100)
for movie in favorites_movies_info_dict['results']:
         
    original_title = movie['original_title']
    vote_average = movie['vote_average']
    vote_count = movie['vote_count']
    overview = movie['overview']
    poster_path = movie['poster_path']
    backdrop_path = movie['backdrop_path']
    
    
    

 # If you want to see specifically some data, just uncomment the code
 
 
    print(f'Nome do filme: {original_title}')
    print(f'Avaliação dos usuários: {vote_average}')
    print(f'Contagem dos votos: {vote_count}')
    print(f'Descrição do filme: {overview}')
    print(f'poster_path: https://image.tmdb.org/t/p/w300_and_h450_bestv2{poster_path}')
    print(f'backdrop_path: https://image.tmdb.org/t/p/w300_and_h450_bestv2{backdrop_path}')
    print('*'*100) 
    
    
'''
# Get the Rated Movies from account
rated_movies = requests.get(f'https://api.themoviedb.org/3/account/{user_id}/rated/movies?api_key={API_KEY}&language=pt-br&sort_by=created_at.asc&page=1&session_id={session_id}')

movies_info_rated = rated_movies.json()

# Will turn python dictionary into a json file
movies_info_rated_json = json.dumps(movies_info_rated, indent = 4) 
print(movies_info_rated_json)


for movie in movies_info_rated['results']:
         
    original_title = movie['original_title']
    vote_average = movie['vote_average']
    vote_count = movie['vote_count']
    overview = movie['overview']
    poster_path = movie['poster_path']
    backdrop_path = movie['backdrop_path']
    
    
# If you want to see specifically some data, just uncomment the code 
"""     print(f'Nome do filme: {original_title}')
    print(f'Avaliação dos usuários: {vote_average}')
    print(f'Contagem dos votos: {vote_count}')
    print(f'Descrição do filme: {overview}')
    print(f'poster_path: https://image.tmdb.org/t/p/w300_and_h450_bestv2{poster_path}')
    print(f'backdrop_path: https://image.tmdb.org/t/p/w300_and_h450_bestv2{backdrop_path}')
    print('*'*100) """
'''    
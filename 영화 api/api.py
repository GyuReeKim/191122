import requests
# from decouple import config

url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
key = '660f73acbf0225280f5db341b9f4e840'
movie_url = f'{url}?key={key}'

res = requests.get(movie_url).json()
print(res)
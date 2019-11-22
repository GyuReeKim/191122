from datetime import datetime, timedelta
import requests

today = datetime.today()

for i in range(2):
    targetDt = (today + timedelta(days=-(i+1)*7)).strftime('%Y%m%d')
    # print(targetDt)

    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
    key = '660f73acbf0225280f5db341b9f4e840'
    movie_url = f'{url}?key={key}&targetDt={targetDt}'

    res = requests.get(movie_url).json()
    print(res)
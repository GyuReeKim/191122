```python
class Movie(models.Model):
    title = models.CharField(max_length=150) # movieNm
    summary = models.TextField() # 크롤링
    director = models.CharField(max_length=45) # director
    genre = models.ManyToManyField(Genre, related_name='movies') # 크롤링?

    title_en = models.CharField(max_length=150) # subtitle
    score = models.FloatField() # userRating
    audience = models.IntegerField() # audiCnt
    poster_url = models.CharField(max_length=500) # image
    video_url = models.CharField(max_length=500, null=True) # image
    ost_url = models.CharField(max_length=500, null=True) # image
    # like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")
    # 영화 좋아요
```



### 영화진흥api key

```
660f73acbf0225280f5db341b9f4e840
```



### 일별 박스오피스

````
http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=660f73acbf0225280f5db341b9f4e840&targetDt=20191121
````



### 영화 상세정보

```
http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=660f73acbf0225280f5db341b9f4e840&movieCd=20197803
```



### datetime 영화 정보 가져오기

```python
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
```



### string -> json

> https://ourcstory.tistory.com/106 



### 네이버 영화 검색 크롤링 참고

>  [http://ehpub.co.kr/30-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-naver-open-api-%ED%99%9C%EC%9A%A9%ED%95%98%EA%B8%B0-%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0%EB%8F%84%EC%84%9C-%EA%B2%80%EC%83%89/](http://ehpub.co.kr/30-파이썬을-이용한-naver-open-api-활용하기-시작하기도서-검색/) 

```python
#import
import urllib.request
import json
 
#애플리케이션 클라이언트 id 및 secret
client_id = "hG6O_G7PA_2DCtQbUri0" 
client_secret = "fsSh41QFYc"
 
#영화검색 url

url = "https://openapi.naver.com/v1/search/movie.json"
option = "&display=1"
query = "?query="+urllib.parse.quote('겨울왕국')
url_query = url + query + option
 
#Open API 검색 요청 개체 설정
request = urllib.request.Request(url_query)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
 
#검색 요청 및 처리
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode == 200):
    response_body = response.read()
    str_info = response_body.decode('utf-8')
    # print(type(temp))
    dict_info = json.loads(str_info)
    print(dict_info.get('items')[0].get('link'))
else:
    print("Error code:"+rescode)
```



### 네이버 영화 줄거리 크롤링

>  [https://somjang.tistory.com/entry/Python%EC%98%81%ED%99%94-%ED%8F%89%EC%A0%90-%EC%A4%84%EA%B1%B0%EB%A6%AC%EB%A5%BC-%EA%B0%80%EC%A7%80%EA%B3%A0-%ED%8F%89%EC%A0%90-%EC%98%88%EC%B8%A1-%EB%AA%A8%EB%8D%B8-%EB%A7%8C%EB%93%A4%EC%96%B4%EB%B3%B4%EA%B8%B0feat-Keras](https://somjang.tistory.com/entry/Python영화-평점-줄거리를-가지고-평점-예측-모델-만들어보기feat-Keras) 

>  [https://somjang.tistory.com/entry/Python%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%98%81%ED%99%94-%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0](https://somjang.tistory.com/entry/Python네이버-영화-데이터-크롤링하기) 

```python
import requests
from bs4 import BeautifulSoup

# 영화 주소 링크 필요
response = requests.get("https://movie.naver.com/movie/bi/mi/basic.nhn?code=136873").text
soup = BeautifulSoup(response, 'html.parser')


contents = soup.select('div.story_area > p.con_tx')
# print(contents)

# 줄거리
movie_info = []
if len(contents) == 0:
    movie_info.append("줄거리 없음")
else:
    for c in contents:
        temp = c.text
        temp = temp.replace('\r', '')
        temp = temp.replace('\xa0', '')
        movie_info.append(temp)
print(movie_info)
```



### Django 크롤링 데이터 저장

>  https://beomi.github.io/2017/03/01/HowToMakeWebCrawler-Save-with-Django/ 


from bs4 import BeautifulSoup
from urllib.request import urlopen

url = urlopen('https://movie.naver.com/movie/bi/mi/basic.nhn?code=136873')
bs = BeautifulSoup(url, 'html.parser')
body = bs.body

target = body.find(class_="con_tx")
print(target.text)

#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div > p
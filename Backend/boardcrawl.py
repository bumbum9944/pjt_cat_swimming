import requests
from bs4 import BeautifulSoup
from decouple import config
import urllib
import os
base_url = "https://cafe.naver.com/joonggonara"
headers = { # 헤더를 넣지 않아도 작동하는 것을 확인했습니다.
'Content-Type': 'application/json; charset=utf-8',
'Accept-Language': 'ko-KR,ko;q=0.9,en-US',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}
keyword='닌텐도'
newKeyword = str(keyword.encode('ms949')).lstrip("b'").rstrip("'").replace("\\x","%")
url = base_url + f"/ArticleSearchList.nhn?search.clubid=10050146&search.searchdate=all&search.page={1}&search.searchBy=0&search.query={newKeyword}&search.includeAll=&search.exclude=&search.include=&search.exact=&"
html = requests.get(url, headers = headers)
soup = BeautifulSoup(html.text, 'html.parser')
soup = soup.select_one('#divSearchMenuTop>ul')
soup = soup.find_all('li')
board = {}
for li in soup:
    a= li.select_one('a')
    if ('폐쇄' not in a.text and '종료' not in a.text and '[구]' not in a.text and '미사용' not in a.text and '예정' not in a.text and '[임시]' not in a.text and '레드카드' not in a.text):
        bnum = a['onclick'].lstrip("applySearchOption('searchmenuTop', '").split('_')[0]
        if a.text != '전체 게시판':
            board[a.text]= bnum
basedir2 = os.path.abspath(os.path.dirname(__file__))
with open(basedir2+'/boardlist.txt','w',encoding='utf8') as f:
    f.write('##board dictionary url: /search/<int:menu_id>/<str:keyword>/<int:page> , menu_id로 0을 넣으면 전체검색 ##\n')
    f.write(str(board))

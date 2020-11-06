import requests
from bs4 import BeautifulSoup
from decouple import config
import urllib

def MaskingTemplateText(text):
    TT = [
        '[거래 전에 꼭! 확인하세요]',
        '- 해당 상품은 ',
        '중고나라 공식앱을 통해 카페에 함께 등록한 상품',
        '- 카톡이나 다른 링크(안전거래사칭,블로그)를 통해 거래를 요구할 경우 거래를 피해주세요',
        '[빠르고 안전한 중고나라 앱으로 해당 상품 구매하러가기]',
    ]
    for T in TT:
        if T in text:
            text = text.replace(T,'')
    return text
    # return True if text in TT else False

def search(menu, keyword, page):
    base_url = "https://cafe.naver.com/joonggonara"
    headers = { # 헤더를 넣지 않아도 작동하는 것을 확인했습니다.
    "cookie" : config("cookie"),
    'Content-Type': 'application/json; charset=utf-8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }

    def get_article_data():
        newKeyword = str(keyword.encode('ms949')).lstrip("b'").rstrip("'").replace("\\x","%")
        if menu == 0:
            url = base_url + f"/ArticleSearchList.nhn?search.clubid=10050146&search.searchdate=all&search.page={page}&search.searchBy=0&search.query={newKeyword}&search.includeAll=&search.exclude=&search.include=&search.exact=&"
        else:
            url = base_url + f"/ArticleSearchList.nhn?search.clubid=10050146&search.searchdate=all&search.page={page}&search.searchBy=0&search.query={newKeyword}&search.defaultValue=1&search.includeAll=&search.exclude=&search.include=&search.exact=&search.sortBy=date&userDisplay=15&search.media=0&search.option=0&search.menuid={menu}"
            print(url)
        html = requests.get(url, headers = headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        soup = soup.select('#main-area > div.article-board > table > tbody> tr')
        if (soup[0].select('div.nodata')):
            return []
        return soup

    def get_text_data(url):
        try:
            html = requests.get(base_url+url, headers = headers)
            soup = BeautifulSoup(html.text, 'html.parser')
            data = soup.select_one('html>body>#basisElement>#content-area>#main-area>div.list-blog>div.inbox')
        except:
            print("data error")
        if not data:
            data = soup
        try:
            title = data.select_one("div.tit-box")
            titleps = title.find_all('p')
            titlespans = title.find_all('span')
            title = []
            if (titleps!=[]):
                title = list(map(lambda x : x.text, titleps))
            if (titlespans!=[]):
                title = title + list(map(lambda x : x.text, titlespans))
            title = ' '.join(title)
        except:
            title="error!"
        try:
            category = data.select_one("div.tit-box>div.fl>table>tr>td>a.m-tcol-c").text
        except:
            category = "error!"
        try:
            user = data.select_one("div.etc-box > div.fl > table > tr > td > table > tr > td.p-nick > a").text
        except:
            user= "error!"
        try:
            price = data.select_one("span.cost").text
        except:
            price="error!"
        try :
            content = data.select_one("#tbody")
            if content.find(class_="comm-foreign"):
                content.find(class_="comm-foreign").decompose()
            if content.find(class_="comm-detail"):
                content.find(class_="comm-detail").decompose()
            if content.find(class_="notice_manager"):
                content.find(class_="notice_manager").decompose()
            ps = content.find_all('p')
            spans = content.find_all('span')
            content = []
            if (ps!=[]):
                content = list(map(lambda x :MaskingTemplateText(x.text), ps))
            if (spans!=[]):
                content = content + list(map(lambda x : MaskingTemplateText(x.text), spans))
            
            if len(content) and "* 거래전 필독! 주의하세요!" in content[0]:
                content.pop(0)
        except Exception as e:
            print(f'content error! {str(e)} {title}')
            content = []
        try: 
            date = data.select_one("div.tit-box > div.fr > table > tbody > tr > td.m-tcol-c.date").text
        except:
            date="2020. 04. 24"
        one = {"title": title, "user": user, "category": category, "price": price, "content": content, "date": date, "url": base_url+url}
        return one

    # 저장되어있는 id 목록 불러오기
    # article_id_list = list(np.load("./article_id_list.npy", allow_pickle=True).tolist())
    # 저장되어있던 process된 data목록 불러오기
    process_datas = []
    data = get_article_data()
    if not len(data):
        return process_datas
    for tr in data:
        process_datas.append(get_text_data(tr.select_one('a.article')['href']))    

    return process_datas

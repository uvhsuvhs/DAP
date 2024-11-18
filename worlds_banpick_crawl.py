import requests
from bs4 import BeautifulSoup
import json

def crawl(base_url, pages):
    data = []

    for page in range(1, pages + 1):
        url = f"{base_url}?pg={page}&iskin=lol&category2=192"

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
    
        db = soup.find("pick", class_="listframe") 
        if not db:
            print("find 실패")
            continue

    return data

if __name__ == "__main__":
    base_url = "https://lol.inven.co.kr/dataninfo/match/teamList.php"
    pages = 4 # 페이지 4까지 크롤링

    data = crawl(base_url, pages)

    with open("worlds_banpick_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)\

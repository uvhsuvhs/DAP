import requests
from bs4 import BeautifulSoup
import json

# 월즈 데이터 크롤링
def worlds_crawl():
    worlds_data = []

    for page in range(1, 5):
        url = "https://lol.inven.co.kr/dataninfo/match/teamList.php?pg={page}&iskin=lol&category2=192"
        print(f"페이지 {page} 크롤링")

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        matchlist = soup.find_all("div", class_="listFrame")

        for match in matchlist:
            match_data = {}

            # 날짜 
            date_tag = match.find("div", class_="date")
            match_data["date"] = date_tag.text.strip() 

            # 토너먼트명 및 세트 숫자 추출
            stage_tag = match.find("div", class_="stage")
            match_data["stage"] = stage_tag.text.strip()

            # wTeam 추출
            wteam_tag = match.find("div", class_="wTeam")
            if wteam_tag:
                w_team_name = wteam_tag.find("a", class_="teamname")
                match_data["wTeam"] = w_team_name.text.strip() 

            # lTeam 추출
            lteam_tag = match.find("div", class_="lTeam")
            if lteam_tag:
                l_team_name = lteam_tag.find("a", class_="teamname")
                match_data["lTeam"] = l_team_name.text.strip() 

            worlds_data.append(match_data)

    return worlds_data

if __name__ == "__main__":
    worlds_data = worlds_crawl()

    with open("worlds_banpick_data.json", "w", encoding="utf-8") as f:
        json.dump(worlds_data, f, ensure_ascii=False, indent=4)

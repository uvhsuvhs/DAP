import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm

# inven html 구조상 밴픽 데이터가 한국어와 숫자로만 적혀 있으므로
# 정규표현식으로 한국어와 숫자만 추출
def extract(onmouseover_text):
    korean_text = re.findall(r"[\uac00-\ud7a30-9]+", onmouseover_text)
    return " ".join(korean_text)

# 월즈 데이터 크롤링
def worlds_crawl():
    worlds_data = []

    for page in tqdm(range(1, 5), desc="inven crawling"):
        url = f"https://lol.inven.co.kr/dataninfo/match/teamList.php?pg={page}&iskin=lol&category2=192"

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        matchlist = soup.find_all("div", class_="listFrame")

        # div 태그의 listFrame 클래스 하위에 존재하는 데이터 추출 반복문
        for match in matchlist:
            match_data = {}

            # 날짜 추출
            date_tag = match.find("div", class_="date")
            match_data["date"] = date_tag.text.strip()

            # 토너먼트명 및 세트 숫자 추출
            stage_tag = match.find("div", class_="stage")
            match_data["stage"] = stage_tag.text.strip()

            # wTeam / lTeam 데이터 추출
            for team_class in ["wTeam", "lTeam"]:
                team_tag = match.find("div", class_=team_class)
                if team_tag:
                    team_name = team_tag.find("a", class_="teamname")
                    match_data[team_class] = team_name.text.strip()

                    # 픽 데이터 추출
                    picks = []
                    pick_tag = team_tag.find("ul", class_="pick")
                    if pick_tag:
                        for li in pick_tag.find_all("li"):
                            img_tag = li.find("img")
                            if img_tag and "onmouseover" in img_tag.attrs:
                                pick_text = extract(img_tag["onmouseover"])
                                picks.append(pick_text)
                    match_data[f"{team_class}_picks"] = picks

                    # 밴 데이터 추출
                    bans = []
                    ban_tag = team_tag.find("ul", class_="ban")
                    if ban_tag:
                        for li in ban_tag.find_all("li"):
                            img_tag = li.find("img")
                            if img_tag and "onmouseover" in img_tag.attrs:
                                ban_text = extract(img_tag["onmouseover"])
                                bans.append(ban_text)
                    match_data[f"{team_class}_bans"] = bans
                    
            worlds_data.append(match_data)

    return worlds_data

if __name__ == "__main__":
    worlds_data = worlds_crawl()

    with open("worlds_banpick_data.json", "w", encoding="utf-8") as f:
        json.dump(worlds_data, f, ensure_ascii=False, indent=4)

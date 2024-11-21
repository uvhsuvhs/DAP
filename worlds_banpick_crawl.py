import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm

# inven html 구조상 챔피언 이름이 한국어와 숫자로만 적혀 있음
# 정규표현식으로 추출
def extract_champion_name(onmouseover_text):
    korean_text = re.findall(r"[\uac00-\ud7a30-9]+", onmouseover_text)
    return " ".join(korean_text)

# 팀별 데이터 추출 함수
def extract_team_data(team_tag, team_class, result_class):
    team_data = {}
    if team_tag:
        # 팀 이름 추출
        team_name = team_tag.find("a", class_="teamname")
        team_data[f"{team_class}_name"] = team_name.text.strip()

        # 팀 이름 오류 수정
        if team_data[f"{team_class}_name"] == "Bilibili Gaming":
            team_data[f"{team_class}_name"] = "BILIBILI GAMING DREAMSMART"

        # 승패 추출
        result_tag = team_tag.find("div", class_=result_class)
        team_data[f"{team_class}_result"] = result_tag.text.strip()

        # 픽 데이터 추출
        picks = []
        pick_tag = team_tag.find("ul", class_="pick")
        if pick_tag:
            for li in pick_tag.find_all("li"):
                img_tag = li.find("img")
                if img_tag and "onmouseover" in img_tag.attrs:
                    pick_text = extract_champion_name(img_tag["onmouseover"])
                    picks.append(pick_text)
        team_data[f"{team_class}_picks"] = picks

        # 밴 데이터 추출
        bans = []
        ban_tag = team_tag.find("ul", class_="ban")
        if ban_tag:
            for li in ban_tag.find_all("li"):
                img_tag = li.find("img")
                if img_tag and "onmouseover" in img_tag.attrs:
                    ban_text = extract_champion_name(img_tag["onmouseover"])
                    bans.append(ban_text)
        team_data[f"{team_class}_bans"] = bans

    return team_data

# 월즈 데이터 크롤링
def worlds_crawl():
    worlds_data = []
    for page in tqdm(range(1, 5), desc="inven crawling"):
        url = f"https://lol.inven.co.kr/dataninfo/match/teamList.php?pg={page}&iskin=lol&category2=192"

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        matchlist = soup.find_all("div", class_="listFrame")

        # listFrame class에서 가져온 데이터를 바탕으로
        # 각 경기 데이터를 크롤링
        for match in matchlist:
            match_data = {}

            # 날짜 추출
            date_tag = match.find("div", class_="date")
            match_data["date"] = date_tag.text.strip() 

            # 토너먼트명 및 세트 숫자 추출
            stage_tag = match.find("div", class_="stage")
            match_data["stage"] = stage_tag.text.strip() 

            # wTeam / lTeam 데이터 추출
            match_data.update(
                extract_team_data(
                    match.find("div", class_="wTeam"), 
                    "wTeam", 
                    "color1 tx5"
                )
            )
            match_data.update(
                extract_team_data(
                    match.find("div", class_="lTeam"), 
                    "lTeam", 
                    "color2 tx5"
                )
            )
            
            worlds_data.append(match_data)
        
    return worlds_data

if __name__ == "__main__":
    worlds_data = worlds_crawl()

    with open("worlds_banpick_data.json", "w", encoding="utf-8") as f:
        json.dump(worlds_data, f, ensure_ascii=False, indent=4)
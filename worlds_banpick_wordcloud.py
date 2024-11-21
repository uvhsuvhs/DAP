import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import json

# JSON 파일 읽어오기
with open("worlds_banpick_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

t1_picks = []
t1_bans = []
other_teams_picks = []
other_teams_bans = []

# T1의 경기 데이터를 기준으로 T1과 상대팀의 밴픽 데이터 필터링
for match in data:
    if match["wTeam_name"] == "T1":
        t1_picks.extend(match["wTeam_picks"])
        t1_bans.extend(match["wTeam_bans"])
        other_teams_picks.extend(match["lTeam_picks"])
        other_teams_bans.extend(match["lTeam_bans"])
    elif match["lTeam_name"] == "T1":
        t1_picks.extend(match["lTeam_picks"])
        t1_bans.extend(match["lTeam_bans"])
        other_teams_picks.extend(match["wTeam_picks"])
        other_teams_bans.extend(match["wTeam_bans"])

# 밴픽 빈도 계산
t1_pick_counts = Counter(t1_picks)
t1_ban_counts = Counter(t1_bans)
other_teams_pick_counts = Counter(other_teams_picks)
other_teams_ban_counts = Counter(other_teams_bans)

# 워드클라우드 생성 함수
def create_wordcloud(data, title, color):
    wordcloud = WordCloud(
        width=800, height=400, 
        background_color='white', 
        font_path="C:/Users/user/Downloads/S-Core_Dream_OTF/SCDream5.otf",
        colormap=color
    ).generate_from_frequencies(data)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=30, pad=15)
    plt.show()

# T1 픽 워드클라우드
create_wordcloud(t1_pick_counts, "T1 Picks", 'gist_heat')

# T1 상대 팀 픽 워드클라우드
create_wordcloud(other_teams_pick_counts, "T1 Opponents Picks", 'winter')

# T1 밴 워드클라우드
create_wordcloud(t1_ban_counts, "T1 Bans", 'gist_heat')

# T1 상대 팀 밴 워드클라우드
create_wordcloud(other_teams_ban_counts, "T1 Opponents Bans", 'winter')
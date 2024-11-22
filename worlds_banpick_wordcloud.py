import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import json

# JSON 파일 읽어오기
with open("worlds_banpick_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 빈도 저장 리스트 초기화
t1_picks = []
t1_bans = []
oppo_picks = []
oppo_bans = []
all_picks = []
all_bans = []

# all : 모든 팀의 밴픽 데이터 
# t1, oppo: T1의 경기 데이터를 기준으로 T1과 상대팀의 밴픽 데이터 필터링
for match in data:
    all_picks.extend(match["wTeam_picks"])
    all_picks.extend(match["lTeam_picks"])
    all_bans.extend(match["wTeam_bans"])
    all_bans.extend(match["lTeam_bans"])
    if match["wTeam_name"] == "T1":
        t1_picks.extend(match["wTeam_picks"])
        t1_bans.extend(match["wTeam_bans"])
        oppo_picks.extend(match["lTeam_picks"])
        oppo_bans.extend(match["lTeam_bans"])
    elif match["lTeam_name"] == "T1":
        t1_picks.extend(match["lTeam_picks"])
        t1_bans.extend(match["lTeam_bans"])
        oppo_picks.extend(match["wTeam_picks"])
        oppo_bans.extend(match["wTeam_bans"])

# 밴픽 빈도 계산
t1_pick_counts = Counter(t1_picks)
t1_ban_counts = Counter(t1_bans)
oppo_pick_counts = Counter(oppo_picks)
oppo_ban_counts = Counter(oppo_bans)
all_pick_counts = Counter(all_picks)
all_ban_counts = Counter(all_bans)

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

# 워드클라우드 생성
# 전체 팀 색상 : 다른 데이터에 사용되지 않은 핑크 / 옐로우 계열의 spring
# T1 색상 : 상징색인 레드 / 블랙을 기반으로 한 gist_heat
# T1 상대팀 색상 : T1과 구별되도록 정반대 계열의 색상을 기반으로 한 winter

# 픽 워드클라우드
create_wordcloud(all_pick_counts, "All Picks", 'spring')
create_wordcloud(t1_pick_counts, "T1 Picks", 'gist_heat')
create_wordcloud(oppo_pick_counts, "T1 Opponents Picks", 'winter')

# 밴 워드클라우드
create_wordcloud(all_ban_counts, "All Bans", 'spring')
create_wordcloud(t1_ban_counts, "T1 Bans", 'gist_heat')
create_wordcloud(oppo_ban_counts, "T1 Opponents Bans", 'winter')
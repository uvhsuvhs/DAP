import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# JSON 데이터 읽어오기
with open("worlds_banpick_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# T1 승리/패배 데이터 리스트 초기화
t1_win_picks = []
t1_win_bans = []
t1_lose_picks = []
t1_lose_bans = []

# T1 승리/패배 데이터 필터링
for match in data:
    if match["wTeam_name"] == "T1" and match["wTeam_result"] == "W":
        t1_win_picks.extend(match["wTeam_picks"])
        t1_win_bans.extend(match["wTeam_bans"])
    elif match["lTeam_name"] == "T1" and match["lTeam_result"] == "L":
        t1_lose_picks.extend(match["lTeam_picks"])
        t1_lose_bans.extend(match["lTeam_bans"])

    if match["lTeam_name"] == "T1" and match["lTeam_result"] == "W":
        t1_win_picks.extend(match["lTeam_picks"])
        t1_win_bans.extend(match["lTeam_bans"])
    elif match["wTeam_name"] == "T1" and match["wTeam_result"] == "L":
        t1_lose_picks.extend(match["wTeam_picks"])
        t1_lose_bans.extend(match["wTeam_bans"])

# T1 승리/패배 시 픽/밴 빈도 계산
t1_win_pick_counts = Counter(t1_win_picks)
t1_win_ban_counts = Counter(t1_win_bans)
t1_lose_pick_counts = Counter(t1_lose_picks)
t1_lose_ban_counts = Counter(t1_lose_bans)

# 승리 데이터 필터링
picks_only_win = set(t1_win_pick_counts.keys()) - set(t1_win_ban_counts.keys())
bans_only_win = set(t1_win_ban_counts.keys()) - set(t1_win_pick_counts.keys())
pick_and_ban_win = set(t1_win_pick_counts.keys()) & set(t1_win_ban_counts.keys())

# 패배 데이터 필터링
picks_only_lose = set(t1_lose_pick_counts.keys()) - set(t1_lose_ban_counts.keys())
bans_only_lose = set(t1_lose_ban_counts.keys()) - set(t1_lose_pick_counts.keys())
pick_and_ban_lose = set(t1_lose_pick_counts.keys()) & set(t1_lose_ban_counts.keys())

# 스택드 바 차트 데이터 처리 함수
def prepare_stacked_data(pick_counts, ban_counts, champions):
    return pd.DataFrame({
        "champion": list(champions),
        "pick_count": [pick_counts.get(champ, 0) for champ in champions],
        "ban_count": [ban_counts.get(champ, 0) for champ in champions],
    })

df_win_stacked = prepare_stacked_data(t1_win_pick_counts, t1_win_ban_counts, pick_and_ban_win)
df_lose_stacked = prepare_stacked_data(t1_lose_pick_counts, t1_lose_ban_counts, pick_and_ban_lose)

plt.rc('font', family='Malgun Gothic')

# 승리: 픽 또는 밴만 된 챔피언
# 픽된 챔피언은 초록 / 밴된 챔피언은 빨강 계열의 색상으로 대비
plt.figure(figsize=(14, 8))
sns.barplot(x=list(picks_only_win), y=[t1_win_pick_counts[ch] for ch in picks_only_win], color='olivedrab', label="Picks only win")
sns.barplot(x=list(bans_only_win), y=[t1_win_ban_counts[ch] for ch in bans_only_win], color='firebrick', label="Bans only win")
plt.title("T1 Win : Picks or Bans Only")
plt.xticks(rotation=90)
plt.xlabel("Champion")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()

# 승리: 픽과 밴된 챔피언
# 픽된 챔피언은 초록 / 밴된 챔피언은 빨강 계열의 색상으로 대비
df_win_stacked.set_index("champion")[["pick_count", "ban_count"]].plot(
    kind="bar", stacked=True, figsize=(14, 8), color=["olivedrab", "firebrick"])
plt.title("T1 Win : Picks and Bans")
plt.xticks(rotation=90)
plt.xlabel("Champion")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# 패배: 픽 또는 밴만 된 챔피언
# 픽된 챔피언은 노랑 / 밴된 챔피언은 파랑 계열의 색상으로 대비
plt.figure(figsize=(14, 8))
sns.barplot(x=list(picks_only_lose), y=[t1_lose_pick_counts[ch] for ch in picks_only_lose], color='gold', label="Picks only lose")
sns.barplot(x=list(bans_only_lose), y=[t1_lose_ban_counts[ch] for ch in bans_only_lose], color='darkblue', label="Bans only lose")
plt.title("T1 Lose : Picks or Bans Only")
plt.xticks(rotation=90)
plt.xlabel("Champion")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()

# 패배: 픽과 밴된 챔피언
# 픽된 챔피언은 노랑 / 밴된 챔피언은 파랑 계열의 색상으로 대비
df_lose_stacked.set_index("champion")[["pick_count", "ban_count"]].plot(
    kind="bar", stacked=True, figsize=(14, 8), color=["gold", "darkblue"])
plt.title("T1 Lose : Picks and Bans")
plt.xticks(rotation=90)
plt.xlabel("Champion")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# JSON 데이터 읽기
with open("worlds_banpick_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# T1과 상대팀의 밴픽 데이터 분리
t1_picks = []
t1_bans = []
oppo_picks = []
oppo_bans = []

for match in data:
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

# 빈도 계산
t1_pick_counts = Counter(t1_picks)
t1_ban_counts = Counter(t1_bans)
oppo_pick_counts = Counter(oppo_picks)
oppo_ban_counts = Counter(oppo_bans)

# 전체 챔피언 리스트 생성
all_champions = list(set(t1_picks + t1_bans + oppo_picks + oppo_bans))

# T1 픽 비율 계산
t1_pick_ratio = {}
for champ in all_champions:
    total_picks = t1_pick_counts.get(champ, 0) + oppo_pick_counts.get(champ, 0)
    if total_picks > 0:
        t1_pick_ratio[champ] = t1_pick_counts.get(champ, 0) / total_picks
    else:
        t1_pick_ratio[champ] = 0

# T1 밴 비율 계산
t1_ban_ratio = {}
for champ in all_champions:
    total_bans = t1_ban_counts.get(champ, 0) + oppo_ban_counts.get(champ, 0)
    if total_bans > 0:
        t1_ban_ratio[champ] = t1_ban_counts.get(champ, 0) / total_bans
    else:
        t1_ban_ratio[champ] = 0

# T1 상대팀 픽 비율 계산
oppo_pick_ratio = {}
for champ in all_champions:
    total_picks = t1_pick_counts.get(champ, 0) + oppo_pick_counts.get(champ, 0)
    if total_picks > 0:
        oppo_pick_ratio[champ] = oppo_pick_counts.get(champ, 0) / total_picks
    else:
        oppo_pick_ratio[champ] = 0

# T1 상대팀 밴 비율 계산
oppo_ban_ratio = {}
for champ in all_champions:
    total_bans = t1_ban_counts.get(champ, 0) + oppo_ban_counts.get(champ, 0)
    if total_bans > 0:
        oppo_ban_ratio[champ] = oppo_ban_counts.get(champ, 0) / total_bans
    else:
        oppo_ban_ratio[champ] = 0

# 픽 데이터프레임 생성
df_picks = pd.DataFrame({
    "T1 Pick Ratio": [t1_pick_ratio.get(champ, 0) for champ in all_champions],
    "Opponent Pick Ratio": [oppo_pick_ratio.get(champ, 0) for champ in all_champions],
}, index=all_champions)

# 밴 데이터프레임 생성
df_bans = pd.DataFrame({
    "T1 Ban Ratio": [t1_ban_ratio.get(champ, 0) for champ in all_champions],
    "Opponent Ban Ratio": [oppo_ban_ratio.get(champ, 0) for champ in all_champions],
}, index=all_champions)

# 픽 비율 히트맵
plt.figure(figsize=(14, 12))
plt.rc('font', family='Malgun Gothic')
sns.heatmap(df_picks, annot=True, cmap="Blues", linewidths=0.3, linecolor='black', fmt=".2f")
plt.title("T1 vs Opponent Pick Ratios", fontsize=16, pad=20)
plt.xlabel("Pick Ratios", fontsize=10)
plt.ylabel("Champions", fontsize=10)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 밴 비율 히트맵
plt.figure(figsize=(14, 12))
plt.rc('font', family='Malgun Gothic')
sns.heatmap(df_bans, annot=True, cmap="Reds", linewidths=0.3, linecolor='black', fmt=".2f")
plt.title("T1 vs Opponent Ban Ratios", fontsize=16, pad=20)
plt.xlabel("Ban Ratios", fontsize=10)
plt.ylabel("Champions", fontsize=10)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
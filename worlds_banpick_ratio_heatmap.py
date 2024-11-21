import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# 비율 계산 함수
def calculate_ratio(numerator_counts, denominator_counts):
    ratios = {}
    for champ in denominator_counts:
        total = denominator_counts[champ]
        if total > 0:
            ratios[champ] = numerator_counts.get(champ, 0) / total
        else:
            ratios[champ] = 0
    return ratios

# JSON 데이터 읽어오기
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

# 전체 챔피언 리스트
all_champions = list(set(t1_picks + t1_bans + oppo_picks + oppo_bans))

# 각 챔피언 총 픽 횟수, 총 밴 횟수 딕셔너리
total_pick_counts = {}
total_ban_counts = {}

# 총 픽 횟수
for champ in all_champions:
    total_pick_counts[champ] = t1_pick_counts.get(champ, 0) + oppo_pick_counts.get(champ, 0)

# 총 밴 횟수
for champ in all_champions:
    total_ban_counts[champ] = t1_ban_counts.get(champ, 0) + oppo_ban_counts.get(champ, 0)

# 비율 계산
t1_pick_ratio = calculate_ratio(t1_pick_counts, total_pick_counts)
t1_ban_ratio = calculate_ratio(t1_ban_counts, total_ban_counts)
oppo_pick_ratio = calculate_ratio(oppo_pick_counts, total_pick_counts)
oppo_ban_ratio = calculate_ratio(oppo_ban_counts, total_ban_counts)

# 데이터프레임 생성

# 픽 데이터프레임 
df_picks = pd.DataFrame({
    "T1 Pick Ratio": [t1_pick_ratio.get(champ, 0) for champ in all_champions],
    "Opponents Pick Ratio": [oppo_pick_ratio.get(champ, 0) for champ in all_champions],
}, index=all_champions)
# 밴 데이터프레임 
df_bans = pd.DataFrame({
    "T1 Ban Ratio": [t1_ban_ratio.get(champ, 0) for champ in all_champions],
    "Opponents Ban Ratio": [oppo_ban_ratio
    .get(champ, 0) for champ in all_champions],
}, index=all_champions)

# T1과 상대 모두 서로와의 경기에서
# 픽 또는 밴한 적 없는 챔피언 데이터 배제
df_picks = df_picks[(df_picks['T1 Pick Ratio'] > 0) | (df_picks['Opponents Pick Ratio'] > 0)]
df_bans = df_bans[(df_bans['T1 Ban Ratio'] > 0) | (df_bans['Opponents Ban Ratio'] > 0)]

# 픽 비율 히트맵
plt.figure(figsize=(14, 9.8))
plt.rc('font', family='Malgun Gothic')
sns.heatmap(
    df_picks, 
    annot=True, 
    cmap="Blues", 
    linewidths=0.35, 
    linecolor='black', 
    fmt=".2f"
)
plt.title("T1 vs Opponents Pick Ratios", fontsize=16, pad=20)
plt.xlabel("Pick Ratios", fontsize=12)
plt.ylabel("Champions", fontsize=12)
plt.tight_layout()
plt.show()

# 밴 비율 히트맵
plt.figure(figsize=(14, 9))
plt.rc('font', family='Malgun Gothic')
sns.heatmap(
    df_bans, 
    annot=True, 
    cmap="Reds", 
    linewidths=0.35, 
    linecolor='black', 
    fmt=".2f"
)
plt.title("T1 vs Opponents Ban Ratios", fontsize=16, pad=20)
plt.xlabel("Ban Ratios", fontsize=12)
plt.ylabel("Champions", fontsize=12)
plt.tight_layout()
plt.show()
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

# T1 승리/패배 시 픽/밴 빈도 
t1_win_pick_counts = Counter(t1_win_picks)
t1_win_ban_counts = Counter(t1_win_bans)
t1_loss_pick_counts = Counter(t1_lose_picks)
t1_loss_ban_counts = Counter(t1_lose_bans)

# 데이터프레임 변환
df_win = pd.DataFrame({
    'champion': list(t1_win_pick_counts.keys()) + list(t1_win_ban_counts.keys()),
    'count': list(t1_win_pick_counts.values()) + list(t1_win_ban_counts.values()),
    'type': ['pick'] * len(t1_win_pick_counts) + ['ban'] * len(t1_win_ban_counts)
})

df_loss = pd.DataFrame({
    'champion': list(t1_loss_pick_counts.keys()) + list(t1_loss_ban_counts.keys()),
    'count': list(t1_loss_pick_counts.values()) + list(t1_loss_ban_counts.values()),
    'type': ['pick'] * len(t1_loss_pick_counts) + ['ban'] * len(t1_loss_ban_counts)
})


# 승리 픽/밴 막대그래프
plt.figure(figsize=(14, 9))
plt.rc('font', family='Malgun gothic')
sns.barplot(x='champion', y='count', hue='type', data=df_win, palette='Blues_d')
plt.title("T1 Win - Champion Picks and Bans")
plt.xticks(rotation=90)
plt.xlabel("Champion")
plt.ylabel("Frequency")
plt.show()

# 패배 픽/밴 막대그래프
plt.figure(figsize=(14, 9))
plt.rc('font', family='Malgun gothic')
sns.barplot(x='champion', y='count', hue='type', data=df_loss, palette='Reds_d')
plt.title("T1 Lose - Champion Picks and Bans")
plt.xticks(rotation=90)
plt.xlabel("Champion")
plt.ylabel("Frequency")
plt.show()
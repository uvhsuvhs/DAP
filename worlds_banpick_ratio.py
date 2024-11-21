import json
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
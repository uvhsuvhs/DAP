import json
import matplotlib.pyplot as plt

# JSON 데이터 읽어오기
with open("worlds_banpick_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 레나타 전체 픽 / T1 픽 횟수 계산
renata_total_picks = 0
renata_t1_picks = 0

for match in data:
    # 전체 레나타 픽 횟수 카운트
    renata_total_picks += match["wTeam_picks"].count("레나타 글라스크")
    renata_total_picks += match["lTeam_picks"].count("레나타 글라스크")
    
    # T1 레나타 픽 횟수 카운트
    if match["wTeam_name"] == "T1":
        renata_t1_picks += match["wTeam_picks"].count("레나타 글라스크")
    if match["lTeam_name"] == "T1":
        renata_t1_picks += match["lTeam_picks"].count("레나타 글라스크")

renata_oppo_picks = renata_total_picks - renata_t1_picks
labels = ["T1 Picks", "Oppo' Picks"]
sizes = [renata_t1_picks, renata_oppo_picks]
colors = ["red", "lightgray"]

# 파이 차트 생성
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct="%.1f%%", startangle=140, colors=colors)
plt.title("Renata Glasc Picks")
plt.tight_layout()
plt.show()
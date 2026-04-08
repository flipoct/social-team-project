import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

baseline_deaths = 152

scenarios = [
    {"시나리오": "기준(도입 전)", "보급률": 0.00, "위험감지율": 0.00, "개입효과": 0.00},
    {"시나리오": "보수적", "보급률": 0.40, "위험감지율": 0.60, "개입효과": 0.50},
    {"시나리오": "기준 시뮬레이션", "보급률": 0.60, "위험감지율": 0.70, "개입효과": 0.60},
    {"시나리오": "공격적", "보급률": 0.80, "위험감지율": 0.80, "개입효과": 0.70},
]

rows = []
for s in scenarios:
    prevented_share = s["보급률"] * s["위험감지율"] * s["개입효과"]
    expected_deaths = round(baseline_deaths * (1 - prevented_share))
    reduction_count = baseline_deaths - expected_deaths
    mortality_index = round(expected_deaths / baseline_deaths * 100, 1)
    rows.append({
        "시나리오": s["시나리오"],
        "보급률": s["보급률"],
        "위험감지율": s["위험감지율"],
        "개입효과": s["개입효과"],
        "예방가능비율": prevented_share,
        "예상사망자수": expected_deaths,
        "감소인원": reduction_count,
        "사망지수(기준=100)": mortality_index
    })

df = pd.DataFrame(rows)

csv_path = "heatwatch_simulation.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

plt.figure(figsize=(8, 5))
plt.bar(df["시나리오"], df["예상사망자수"])
plt.title("스마트워치 도입 시나리오별 예상 온열질환 사망자 수")
plt.ylabel("예상 사망자 수(명)")
plt.xlabel("시나리오")

for i, v in enumerate(df["예상사망자수"]):
    plt.text(i, v + 2, str(v), ha="center")

plt.tight_layout()
chart1 = "heatwatch_expected_deaths.png"
plt.savefig(chart1, dpi=200, bbox_inches="tight")
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(df["시나리오"], df["사망지수(기준=100)"], marker="o")
plt.title("스마트워치 도입 시나리오별 사망지수 변화")
plt.ylabel("사망지수(기준 시나리오=100)")
plt.xlabel("시나리오")

for i, v in enumerate(df["사망지수(기준=100)"]):
    plt.text(i, v + 1.5, f"{v}", ha="center")

plt.tight_layout()
chart2 = "heatwatch_mortality_index.png"
plt.savefig(chart2, dpi=200, bbox_inches="tight")
plt.show()

print("저장된 파일:")
print(chart1)
print(chart2)
print(csv_path)
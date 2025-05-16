import pandas as pd
import matplotlib.pyplot as plt
import csv
from collections import defaultdict

# === Step 1: Read all judge CSVs and aggregate rankings by index ===
gemini_csv_files = ['BackEnd/user_logs/user6.csv', 'BackEnd/user_logs/user8.csv', 'BackEnd/user_logs/user9.csv']
gpt_csv_files = ['BackEnd/user_logs/shirley.csv', 'BackEnd/user_logs/user1.csv', 'BackEnd/user_logs/user2.csv']
claude_csv_files = ['BackEnd/user_logs/user3.csv', 'BackEnd/user_logs/user4.csv', 'BackEnd/user_logs/user5.csv','BackEnd/user_logs/user10.csv']


all_rankings = defaultdict(list)
borda_points = [2, 1, 0]

for file in csv_files:
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        ranking_col_index = header.index("ranking") if "ranking" in header else 1

        for row in reader:
            if len(row) <= ranking_col_index or not row[ranking_col_index]:
                continue
            index = row[0].strip()
            systems = [s.strip().lower() for s in row[ranking_col_index].split(',')[:3]]
            if len(systems) < 3:
                continue
            all_rankings[index].append(systems)

# === Step 2: Aggregate scores per index across judges ===
results = {
    'maats_vs_single_agent': {'win': 0, 'tie': 0, 'loss': 0},
    'maats_vs_zero_shot': {'win': 0, 'tie': 0, 'loss': 0},
}

for index, system_lists in all_rankings.items():
    score_map = defaultdict(int)
    for systems in system_lists:
        for i, sys in enumerate(systems[:3]):
            score_map[sys] += borda_points[i]

    # Compare MAATS vs SINGLE_AGENT
    if score_map['maats'] > score_map['single_agent']:
        results['maats_vs_single_agent']['win'] += 1
    elif score_map['maats'] == score_map['single_agent']:
        results['maats_vs_single_agent']['tie'] += 1
    else:
        results['maats_vs_single_agent']['loss'] += 1

    # Compare MAATS vs ZERO_SHOT
    if score_map['maats'] > score_map['zero_shot']:
        results['maats_vs_zero_shot']['win'] += 1
    elif score_map['maats'] == score_map['zero_shot']:
        results['maats_vs_zero_shot']['tie'] += 1
    else:
        results['maats_vs_zero_shot']['loss'] += 1

# === Step 3: Convert to percentages ===
percent_results = {}
for matchup, outcome in results.items():
    total = sum(outcome.values())
    percent_results[matchup] = {k: round(v / total * 100, 2) for k, v in outcome.items()}

# === Step 4: Pie Charts with actual percentage numbers ===
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

labels = ['Win', 'Tie', 'Loss']

# Pie 1: MAATS vs SINGLE_AGENT
values1 = [percent_results['maats_vs_single_agent'][k.lower()] for k in labels]
axs[0].pie(values1, labels=labels, autopct='%1.2f%%', startangle=140)
axs[0].set_title('MAATS vs Single Agent')

# Pie 2: MAATS vs ZERO_SHOT
values2 = [percent_results['maats_vs_zero_shot'][k.lower()] for k in labels]
axs[1].pie(values2, labels=labels, autopct='%1.2f%%', startangle=140)
axs[1].set_title('MAATS vs Zero Shot')

plt.tight_layout()
plt.savefig('analysis/gemini_maats_pie_comparison.png')
plt.close()

# === Step 5: Print Results ===
print("Percentage Results:")
for matchup, scores in percent_results.items():
    print(f"{matchup}: {scores}")

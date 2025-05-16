import matplotlib.pyplot as plt
import csv
from collections import defaultdict
from matplotlib.patches import Patch

# === Define judge CSVs grouped by model ===
csv_groups = {
    "GPT": ['BackEnd/user_logs/shirley.csv', 'BackEnd/user_logs/user1.csv', 'BackEnd/user_logs/user2.csv'],
    "Claude": ['BackEnd/user_logs/user3.csv', 'BackEnd/user_logs/user4.csv', 'BackEnd/user_logs/user5.csv', 'BackEnd/user_logs/user10.csv'],
    "Gemini": ['BackEnd/user_logs/user6.csv', 'BackEnd/user_logs/user8.csv', 'BackEnd/user_logs/user9.csv'],
}

borda_points = [2, 1, 0]
labels = ['Win', 'Tie', 'Loss']
colors = ["#1F77B4", "#FFC107", "#D62728"]  # Green, Yellow, Red

# === Prepare 2x3 subplots (row 0: vs Single Agent, row 1: vs Zero Shot) ===
fig, axs = plt.subplots(2, 3, figsize=(12, 8))
fig.subplots_adjust(hspace=0.3)
# fig.suptitle('MAATS Comparison Results Across Models', fontsize=16)

# === Process each model group and fill the charts ===
for col_idx, (model_name, csv_files) in enumerate(csv_groups.items()):
    all_rankings = defaultdict(list)

    # === Step 1: Collect all rankings per index ===
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

    # === Step 2: Aggregate Borda scores ===
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
        percent_results[matchup] = [round(outcome[k] / total * 100, 2) for k in ['win', 'tie', 'loss']]

    # === Step 4: Draw pies ===
    axs[0, col_idx].pie(percent_results['maats_vs_single_agent'], autopct='%1.1f%%', colors=colors, startangle=140)
    axs[1, col_idx].pie(percent_results['maats_vs_zero_shot'], autopct='%1.1f%%', colors=colors, startangle=140)

    # === Column titles (top) ===
    axs[0, col_idx].set_title(model_name, fontsize=14)

# === Row titles (left) ===
axs[0, 0].text(-1.2, 0, 'MAATS vs\nSingle Agent', va='center', ha='right', fontsize=12)
axs[1, 0].text(-1.2, 0, 'MAATS vs\nZero Shot', va='center', ha='right', fontsize=12)

# === Legend at the bottom ===
# === Custom legend at the bottom ===
# === Create manual legend from color patches ===
legend_handles = [
    Patch(facecolor=colors[0], label='MAATS Win'),
    Patch(facecolor=colors[1], label='MAATS Tie'),
    Patch(facecolor=colors[2], label='MAATS Loss'),
]

# === Add legend BELOW the entire figure ===
fig.legend(handles=legend_handles, loc='lower center', ncol=3, fontsize=12)

# === Adjust layout to leave space for legend ===
plt.subplots_adjust(bottom=0.15, top=0.9)

# === Save the figure ===
plt.savefig('analysis/maats_model_comparison_grid.png', bbox_inches='tight')
plt.close()


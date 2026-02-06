#!/usr/bin/env python3
"""
Generate figures for Chapter 4 (Exploring Categorical Data) exercises.
Creates synthetic/representative plots based on the exercise descriptions in _04-ex-explore-categorical.qmd
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Set style for cleaner plots
plt.style.use('seaborn-v0_8-whitegrid')

# Create output directory if it doesn't exist
output_dir = "source/images/exercises"
os.makedirs(output_dir, exist_ok=True)

# Color scheme similar to OpenIntro
COLORS = {
    'blue': '#569BBD',
    'red': '#F05133',
    'green': '#4C9A2A',
    'pink': '#F4A5A5',
    'yellow': '#FDB515',
    'lgray': '#CCCCCC',
    'purple': '#9370DB'
}

print("="*60)
print("Generating Chapter 4 Exercise Figures")
print("="*60)

# Exercise 1: Antibiotic use in children - Bar plot and pie chart
print("\n1. Generating Exercise 1: Antibiotic use in children...")
conditions = ['Cardiac', 'Prematurity', 'Pulmonary', 'Trauma']
counts = [12, 15, 22, 11]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Bar plot
colors_list = [COLORS['blue'], COLORS['red'], COLORS['green'], COLORS['pink']]
ax1.barh(conditions, counts, color=colors_list)
ax1.set_xlabel('Count', fontsize=11)
ax1.set_ylabel('Condition', fontsize=11)
ax1.set_title('Bar plot', fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Pie chart
ax2.pie(counts, labels=conditions, colors=colors_list, autopct='%1.1f%%', startangle=90)
ax2.set_title('Pie chart', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_04-ex-01-antibiotic-use.png'), dpi=150, bbox_inches='tight')
print(f"   ✓ Saved {os.path.join(output_dir, '_04-ex-01-antibiotic-use.png')}")
plt.close()

# Exercise 2: Views on immigration - Table (will be created as text in PTX)
print("\n2. Exercise 2 uses a table - will be added directly in PTX")

# Exercise 3: Black Lives Matter - Stacked bar plot by age
print("\n3. Generating Exercise 3: Black Lives Matter survey...")
ages = ['18-29', '30-39', '40-49', '50-64', '65+']
opinions = {
    'Strongly support': [55, 42, 51, 45, 42],
    'Somewhat support': [26, 35, 26, 29, 21],
    'Somewhat oppose': [13, 13, 9, 10, 10],
    'Strongly oppose': [5, 9, 13, 17, 24],
    'No opinion': [0, 1, 1, 0, 2]
}

fig, ax = plt.subplots(figsize=(10, 5))
left = np.zeros(len(ages))
colors_opinions = [COLORS['green'], COLORS['blue'], COLORS['lgray'], COLORS['pink'], COLORS['red']]

for i, (opinion, values) in enumerate(opinions.items()):
    proportions = [v / 100 for v in values]
    ax.barh(ages, proportions, left=left, label=opinion, color=colors_opinions[i])
    left += proportions

ax.set_xlabel('Proportion', fontsize=11)
ax.set_ylabel('Age', fontsize=11)
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False)
ax.set_title('Support for protests following George Floyd\'s killing by age group', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_04-ex-03-blm-survey.png'), dpi=150, bbox_inches='tight')
print(f"   ✓ Saved {os.path.join(output_dir, '_04-ex-03-blm-survey.png')}")
plt.close()

# Exercise 4: Raise taxes - Stacked bar plot by party
print("\n4. Generating Exercise 4: Raise taxes survey...")
parties = ['Democrat', 'Republican', 'Independent/Other']
tax_opinions = {
    'Raise taxes on the rich': [91, 47, 49],
    'Raise taxes on the poor': [4, 10, 11],
    'Not sure': [5, 43, 40]
}

fig, ax = plt.subplots(figsize=(10, 4.5))
left = np.zeros(len(parties))
colors_tax = [COLORS['blue'], COLORS['red'], COLORS['lgray']]

for i, (opinion, values) in enumerate(tax_opinions.items()):
    proportions = [v / 100 for v in values]
    ax.barh(parties, proportions, left=left, label=opinion, color=colors_tax[i])
    left += proportions

ax.set_xlabel('Proportion', fontsize=11)
ax.set_ylabel('Political affiliation', fontsize=11)
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, frameon=False)
ax.set_title('Views on raising taxes by political affiliation', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_04-ex-04-raise-taxes.png'), dpi=150, bbox_inches='tight')
print(f"   ✓ Saved {os.path.join(output_dir, '_04-ex-04-raise-taxes.png')}")
plt.close()

# Exercise 5: Heart transplant - Two bar plots (counts and proportions)
print("\n5. Generating Exercise 5: Heart transplant study...")
groups = ['Control', 'Treatment']
deceased = [30, 45]
alive = [4, 24]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Stacked bar plot (counts)
width = 0.5
ax1.barh(groups, deceased, label='Deceased', color=COLORS['blue'], height=width)
ax1.barh(groups, alive, left=deceased, label='Alive', color=COLORS['red'], height=width)
ax1.set_xlabel('Count', fontsize=11)
ax1.set_ylabel('Group', fontsize=11)
ax1.set_title('Counts', fontsize=12, fontweight='bold')
ax1.legend(loc='right')
ax1.grid(axis='x', alpha=0.3)

# Standardized bar plot (proportions)
total_control = deceased[0] + alive[0]
total_treatment = deceased[1] + alive[1]
prop_deceased = [deceased[0]/total_control, deceased[1]/total_treatment]
prop_alive = [alive[0]/total_control, alive[1]/total_treatment]

ax2.barh(groups, prop_deceased, label='Deceased', color=COLORS['blue'], height=width)
ax2.barh(groups, prop_alive, left=prop_deceased, label='Alive', color=COLORS['red'], height=width)
ax2.set_xlabel('Proportion', fontsize=11)
ax2.set_title('Proportions', fontsize=12, fontweight='bold')
ax2.set_xlim(0, 1)
ax2.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
ax2.legend(loc='right')
ax2.grid(axis='x', alpha=0.3)

plt.suptitle('Heart Transplant Study Outcomes', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_04-ex-05-heart-transplant.png'), dpi=150, bbox_inches='tight')
print(f"   ✓ Saved {os.path.join(output_dir, '_04-ex-05-heart-transplant.png')}")
plt.close()

# Exercise 6: Shipping holiday gifts - Two stacked bar plots
print("\n6. Generating Exercise 6: Shipping holiday gifts...")
shipping_methods = ['USPS', 'UPS', 'FedEx', 'Something else', 'Not sure']
age_groups = ['18-34', '35-54', '55+']

# Data for plot 1: shipping method by age
data_by_age = {
    '18-34': [72, 52, 31, 7, 3],
    '35-54': [97, 76, 24, 6, 6],
    '55+': [76, 34, 9, 3, 4]
}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot 1: Age distribution within each shipping method
colors_age = [COLORS['blue'], COLORS['red'], COLORS['pink']]
for i, method in enumerate(shipping_methods):
    values = [data_by_age[age][i] for age in age_groups]
    total = sum(values)
    proportions = [v/total for v in values]
    
    left = 0
    for j, age in enumerate(age_groups):
        ax1.barh(len(shipping_methods)-1-i, proportions[j], left=left, 
                color=colors_age[j], label=age if i == 0 else "")
        left += proportions[j]

ax1.set_yticks(range(len(shipping_methods)))
ax1.set_yticklabels(shipping_methods[::-1])
ax1.set_xlabel('Proportion', fontsize=11)
ax1.set_ylabel('Shipping method', fontsize=11)
ax1.set_xlim(0, 1)
ax1.set_title('Age distribution by shipping method', fontsize=12, fontweight='bold')
ax1.legend(title='Age', loc='lower right')

# Plot 2: Shipping method distribution within each age group
colors_shipping = [COLORS['blue'], COLORS['red'], COLORS['pink'], COLORS['yellow'], COLORS['green']]
for i, age in enumerate(age_groups):
    values = data_by_age[age]
    total = sum(values)
    proportions = [v/total for v in values]
    
    left = 0
    for j, method in enumerate(shipping_methods):
        ax2.barh(len(age_groups)-1-i, proportions[j], left=left,
                color=colors_shipping[j], label=method if i == 0 else "")
        left += proportions[j]

ax2.set_yticks(range(len(age_groups)))
ax2.set_yticklabels(age_groups[::-1])
ax2.set_xlabel('Proportion', fontsize=11)
ax2.set_ylabel('Age', fontsize=11)
ax2.set_xlim(0, 1)
ax2.set_title('Shipping method distribution by age', fontsize=12, fontweight='bold')
ax2.legend(title='Shipping method', loc='lower right', ncol=2)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_04-ex-06-shipping-gifts.png'), dpi=150, bbox_inches='tight')
print(f"   ✓ Saved {os.path.join(output_dir, '_04-ex-06-shipping-gifts.png')}")
plt.close()

# Exercise 7: Meat consumption and life expectancy - Ridge plots
print("\n7. Generating Exercise 7: Meat consumption and life expectancy...")
income_levels = ['High income', 'Middle income', 'Low income']

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

# Ridge plot 1: Meat consumption
np.random.seed(42)
meat_data = {
    'High income': np.random.gamma(8, 8, 50),
    'Middle income': np.random.gamma(5, 6, 50),
    'Low income': np.random.gamma(3, 5, 50)
}

for i, (level, data) in enumerate(meat_data.items()):
    y_offset = i * 0.5
    counts, bins = np.histogram(data, bins=20, density=True)
    bins_center = (bins[:-1] + bins[1:]) / 2
    ax1.fill_between(bins_center, y_offset, counts * 0.4 + y_offset, 
                     alpha=0.7, color=[COLORS['blue'], COLORS['red'], COLORS['green']][i])
    ax1.plot(bins_center, counts * 0.4 + y_offset, 
            color=[COLORS['blue'], COLORS['red'], COLORS['green']][i], linewidth=2)

ax1.set_yticks([0.5, 1.0, 1.5])
ax1.set_yticklabels(income_levels[::-1])
ax1.set_xlabel('Meat consumption (kg per capita)', fontsize=11)
ax1.set_ylabel('', fontsize=11)
ax1.set_xlim(0, 120)
ax1.set_title('Meat consumption by income level', fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Ridge plot 2: Life expectancy
life_data = {
    'High income': np.random.normal(78, 3, 50),
    'Middle income': np.random.normal(72, 4, 50),
    'Low income': np.random.normal(65, 5, 50)
}

for i, (level, data) in enumerate(life_data.items()):
    y_offset = i * 0.5
    counts, bins = np.histogram(data, bins=20, density=True)
    bins_center = (bins[:-1] + bins[1:]) / 2
    ax2.fill_between(bins_center, y_offset, counts * 0.4 + y_offset,
                     alpha=0.7, color=[COLORS['blue'], COLORS['red'], COLORS['green']][i])
    ax2.plot(bins_center, counts * 0.4 + y_offset,
            color=[COLORS['blue'], COLORS['red'], COLORS['green']][i], linewidth=2)

ax2.set_yticks([0.5, 1.0, 1.5])
ax2.set_yticklabels(income_levels[::-1])
ax2.set_xlabel('Life expectancy (years)', fontsize=11)
ax2.set_ylabel('', fontsize=11)
ax2.set_xlim(50, 90)
ax2.set_title('Life expectancy by income level', fontsize=12, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_04-ex-07-meat-life-expectancy.png'), dpi=150, bbox_inches='tight')
print(f"   ✓ Saved {os.path.join(output_dir, '_04-ex-07-meat-life-expectancy.png')}")
plt.close()

# Exercise 8: Florence Nightingale - No figure needed (text-based)
print("\n8. Exercise 8 is text-based - no figure needed")

# Exercise 9: On-time arrivals - Table (will be created as text in PTX)
print("\n9. Exercise 9 uses a table - will be added directly in PTX")

# Exercise 10: US House of Representatives - No figure needed (text-based)
print("\n10. Exercise 10 is text-based - no figure needed")

print("\n" + "="*60)
print("✓ All Chapter 4 exercise figures generated successfully!")
print("="*60)

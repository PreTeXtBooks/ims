#!/usr/bin/env python3
"""
Generate figures for Chapter 7 exercises.
Since we don't have access to R/Quarto, we'll create representative plots
based on the exercise descriptions using matplotlib.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
np.random.seed(42)

# Create output directory
output_dir = "source/images/exercises"
os.makedirs(output_dir, exist_ok=True)

print("Generating Chapter 7 exercise figures...")

# Exercise 1: Visualizing residuals - 2 panel plot
print("\n1. Visualizing residuals...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Panel (a) - linear relationship
x1 = np.linspace(1, 100, 100)
y1 = 3 * x1 + 5 + np.random.normal(0, 20, 100)
ax1.scatter(x1, y1, alpha=0.6, s=20)
# Fit line
z1 = np.polyfit(x1, y1, 1)
p1 = np.poly1d(z1)
ax1.plot(x1, p1(x1), 'r-', linewidth=2)
ax1.set_title('(a)')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_xticks([])
ax1.set_yticks([])

# Panel (b) - fan shape (heteroscedastic)
x2 = np.linspace(1, 100, 100)
noise = np.sort(np.abs(np.random.normal(0, 1.3, 100)) * x2, axis=0)[::-1]
y2 = 4 * x2 + 5 + noise
ax2.scatter(x2, y2, alpha=0.6, s=20)
z2 = np.polyfit(x2, y2, 1)
p2 = np.poly1d(z2)
ax2.plot(x2, p2(x2), 'r-', linewidth=2)
ax2.set_title('(b)')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_xticks([])
ax2.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-01.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 2: Trends in residuals - 2 panel residual plots
print("2. Trends in residuals...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Panel (a) - fan pattern in residuals
x1 = np.linspace(1, 300, 300)
y1 = 4 * x1 + 5 + np.random.normal(0, 1, 300) * (1.3 * x1)
fitted1 = 4 * x1 + 5
residuals1 = y1 - fitted1
ax1.scatter(fitted1, residuals1, alpha=0.4, s=10)
ax1.axhline(y=0, color='k', linestyle='--', linewidth=1)
ax1.set_title('(a)')
ax1.set_xlabel('Predicted values')
ax1.set_ylabel('Residuals')
ax1.set_xticks([])
ax1.set_yticks([])

# Panel (b) - curved pattern
x2 = np.linspace(1, 300, 300)
y2 = np.log(x2) + np.random.normal(0, 0.5, 300)
z = np.polyfit(x2, y2, 1)
p = np.poly1d(z)
residuals2 = y2 - p(x2)
ax2.scatter(p(x2), residuals2, alpha=0.4, s=10)
ax2.axhline(y=0, color='k', linestyle='--', linewidth=1)
ax2.set_title('(b)')
ax2.set_xlabel('Predicted values')
ax2.set_ylabel('Residuals')
ax2.set_xticks([])
ax2.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-02.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 3: Identify relationships I - 6 panel plot
print("3. Identify relationships I...")
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

x = np.linspace(0, 6, 121)

# (a) U-shaped
y_a = (x - 3)**2 - 4 + np.random.normal(0, 1, 121)
axes[0].scatter(x, y_a, alpha=0.5, s=15)
axes[0].set_title('(a)')
axes[0].set_xticks([])
axes[0].set_yticks([])

# (b) Strong positive linear
y_b = 3 * x + 10 + np.random.normal(0, 2, 121)
axes[1].scatter(x, y_b, alpha=0.5, s=15)
axes[1].set_title('(b)')
axes[1].set_xticks([])
axes[1].set_yticks([])

# (c) Weak positive linear
y_c = 3 * x + 10 + np.random.normal(0, 20, 121)
axes[2].scatter(x, y_c, alpha=0.5, s=15)
axes[2].set_title('(c)')
axes[2].set_xticks([])
axes[2].set_yticks([])

x2 = np.linspace(-8, -2, 121)

# (d) Inverted U-shaped
y_d = -(x2 + 5)**2 + 1 + np.random.normal(0, 2, 121)
axes[3].scatter(x2, y_d, alpha=0.5, s=15)
axes[3].set_title('(d)')
axes[3].set_xticks([])
axes[3].set_yticks([])

# (e) Strong negative linear
y_e = -5 * x2 + 3 + np.random.normal(0, 2, 121)
axes[4].scatter(x2, y_e, alpha=0.5, s=15)
axes[4].set_title('(e)')
axes[4].set_xticks([])
axes[4].set_yticks([])

# (f) No relationship
y_f = np.random.normal(0, 10, 121)
axes[5].scatter(x2, y_f, alpha=0.5, s=15)
axes[5].set_title('(f)')
axes[5].set_xticks([])
axes[5].set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-03.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 4: Identify relationships II - similar 6 panel plot
print("4. Identify relationships II...")
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

x = np.linspace(0, 6, 121)

# Create 6 different patterns
patterns = [
    (3 * x + np.random.normal(0, 5, 121), '(a)'),  # moderate positive
    (-2 * x + np.random.normal(0, 3, 121), '(b)'),  # moderate negative
    (np.sin(x) * 5 + np.random.normal(0, 1, 121), '(c)'),  # sinusoidal
    (np.random.normal(0, 5, 121), '(d)'),  # no relationship
    (5 * x + np.random.normal(0, 2, 121), '(e)'),  # strong positive
    (np.exp(x/3) + np.random.normal(0, 2, 121), '(f)')  # exponential
]

for ax, (y, title) in zip(axes, patterns):
    ax.scatter(x, y, alpha=0.5, s=15)
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-04.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 5: Midterms and final - 2 scatterplots
print("5. Midterms and final...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Exam 1 vs Course Grade (stronger correlation)
exam1 = np.random.uniform(60, 100, 233)
course = 0.7 * exam1 + np.random.normal(0, 5, 233) + 20
ax1.scatter(exam1, course, alpha=0.5, s=20)
ax1.set_xlabel('Exam 1')
ax1.set_ylabel('Course Grade')
ax1.set_title('Exam 1 vs Course Grade')
ax1.set_xlim(55, 105)
ax1.set_ylim(55, 105)

# Exam 2 vs Course Grade (weaker correlation)
exam2 = np.random.uniform(60, 100, 233)
course2 = 0.5 * exam2 + np.random.normal(0, 10, 233) + 30
ax2.scatter(exam2, course2, alpha=0.5, s=20)
ax2.set_xlabel('Exam 2')
ax2.set_ylabel('Course Grade')
ax2.set_title('Exam 2 vs Course Grade')
ax2.set_xlim(55, 105)
ax2.set_ylim(55, 105)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-05.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 6: Meat consumption and life expectancy - 2 scatterplots
print("6. Meat consumption and life expectancy...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Meat vs Life Expectancy (positive, leveling off)
meat = np.random.uniform(10, 120, 175)
life_exp = 50 + 25 * (1 - np.exp(-meat / 40)) + np.random.normal(0, 3, 175)
ax1.scatter(meat, life_exp, alpha=0.5, s=20)
ax1.set_xlabel('Meat consumption (kg/capita/year)')
ax1.set_ylabel('Life expectancy (years)')
ax1.set_title('Life Expectancy vs Meat')
ax1.set_xlim(0, 130)
ax1.set_ylim(45, 85)

# Meat vs Carbohydrates (negative)
carbs = 200 - 0.8 * meat + np.random.normal(0, 20, 175)
ax2.scatter(meat, carbs, alpha=0.5, s=20)
ax2.set_xlabel('Meat consumption (kg/capita/year)')
ax2.set_ylabel('Carbohydrate consumption (kg/capita/year)')
ax2.set_title('Carbohydrates vs Meat')
ax2.set_xlim(0, 130)
ax2.set_ylim(50, 250)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-06.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 7: Match the correlation I - 4 scatterplots
print("7. Match the correlation I...")
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

n = 100
x = np.random.uniform(0, 10, n)

# Create plots with specific correlations
correlations = [-0.7, 0.45, 0.06, 0.92]
titles = ['(a)', '(b)', '(c)', '(d)']

for ax, r, title in zip(axes, correlations, titles):
    # Generate correlated data
    y = r * x + np.random.normal(0, np.sqrt(1 - r**2) * 3, n)
    ax.scatter(x, y, alpha=0.5, s=20)
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-07.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 8: Match the correlation II - 4 scatterplots
print("8. Match the correlation II...")
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

correlations = [0.49, -0.48, -0.03, -0.85]
titles = ['(a)', '(b)', '(c)', '(d)']

for ax, r, title in zip(axes, correlations, titles):
    y = r * x + np.random.normal(0, np.sqrt(abs(1 - r**2)) * 3, n)
    ax.scatter(x, y, alpha=0.5, s=20)
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-08.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 9: Body measurements correlation - shoulder girth vs height
print("9. Body measurements correlation...")
fig, ax = plt.subplots(figsize=(8, 6))
shoulder = np.random.normal(107.2, 10.37, 507)
height = 0.67 * ((shoulder - 107.2) / 10.37) * 9.41 + 171.14 + np.random.normal(0, 7, 507)
ax.scatter(shoulder, height, alpha=0.4, s=15)
ax.set_xlabel('Shoulder girth (cm)')
ax.set_ylabel('Height (cm)')
ax.set_title('Height vs Shoulder Girth')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-09.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 11: The Coast Starlight correlation
print("11. The Coast Starlight correlation...")
fig, ax = plt.subplots(figsize=(8, 6))
distance = np.random.uniform(10, 250, 30)
time = 0.636 * ((distance - 108) / 99) * 113 + 129 + np.random.normal(0, 60, 30)
ax.scatter(distance, time, alpha=0.6, s=40)
ax.set_xlabel('Distance (miles)')
ax.set_ylabel('Travel time (minutes)')
ax.set_title('Travel Time vs Distance')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-11.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 12: Crawling babies correlation
print("12. Crawling babies correlation...")
fig, ax = plt.subplots(figsize=(8, 6))
temp = np.linspace(30, 80, 12)  # 12 months
age = 33 - 0.7 * ((temp - 55) / 15) * 5 + np.random.normal(0, 1.5, 12)
ax.scatter(temp, age, alpha=0.6, s=60)
ax.set_xlabel('Temperature (°F)')
ax.set_ylabel('Average crawling age (weeks)')
ax.set_title('Crawling Age vs Temperature')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-12.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 19: Starbucks calories and protein
print("19. Starbucks calories and protein...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
calories = np.random.uniform(80, 500, 77)
protein = 0.05 * calories + np.random.normal(0, 3, 77)
protein = np.clip(protein, 0, 30)
ax1.scatter(calories, protein, alpha=0.5, s=30)
ax1.set_xlabel('Calories')
ax1.set_ylabel('Protein (g)')
ax1.set_title('Protein vs Calories')

# Residual plot
fitted = 0.05 * calories
residuals = protein - fitted
ax2.scatter(fitted, residuals, alpha=0.5, s=30)
ax2.axhline(y=0, color='k', linestyle='--', linewidth=1)
ax2.set_xlabel('Predicted protein')
ax2.set_ylabel('Residuals')
ax2.set_title('Residuals vs Predicted')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-19.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 20: Starbucks calories and carbs
print("20. Starbucks calories and carbs...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
carbs = 0.12 * calories + np.random.normal(0, 5, 77)
carbs = np.clip(carbs, 5, 80)
ax1.scatter(calories, carbs, alpha=0.5, s=30)
ax1.set_xlabel('Calories')
ax1.set_ylabel('Carbohydrates (g)')
ax1.set_title('Carbs vs Calories')

# Residual plot
fitted = 0.12 * calories
residuals = carbs - fitted
ax2.scatter(fitted, residuals, alpha=0.5, s=30)
ax2.axhline(y=0, color='k', linestyle='--', linewidth=1)
ax2.set_xlabel('Predicted carbs')
ax2.set_ylabel('Residuals')
ax2.set_title('Residuals vs Predicted')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-20.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 21: The Coast Starlight regression (single plot)
print("21. The Coast Starlight regression...")
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(distance, time, alpha=0.6, s=40)
# Add regression line
z = np.polyfit(distance, time, 1)
p = np.poly1d(z)
x_line = np.linspace(distance.min(), distance.max(), 100)
ax.plot(x_line, p(x_line), 'r-', linewidth=2)
ax.set_xlabel('Distance (miles)')
ax.set_ylabel('Travel time (minutes)')
ax.set_title('Travel Time vs Distance (with regression line)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-21.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 22: Body measurements regression
print("22. Body measurements regression...")
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(shoulder, height, alpha=0.4, s=15)
# Add regression line
z = np.polyfit(shoulder, height, 1)
p = np.poly1d(z)
x_line = np.linspace(shoulder.min(), shoulder.max(), 100)
ax.plot(x_line, p(x_line), 'r-', linewidth=2)
ax.set_xlabel('Shoulder girth (cm)')
ax.set_ylabel('Height (cm)')
ax.set_title('Height vs Shoulder Girth (with regression line)')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-22.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 23: Poverty and unemployment
print("23. Poverty and unemployment...")
fig, ax = plt.subplots(figsize=(8, 6))
unemployment = np.random.uniform(2, 20, 3000)
poverty = 8 + 0.7 * unemployment + np.random.normal(0, 3, 3000)
ax.scatter(unemployment, poverty, alpha=0.2, s=10)
z = np.polyfit(unemployment, poverty, 1)
p = np.poly1d(z)
x_line = np.linspace(unemployment.min(), unemployment.max(), 100)
ax.plot(x_line, p(x_line), 'r-', linewidth=2)
ax.set_xlabel('Unemployment rate (%)')
ax.set_ylabel('Poverty (%)')
ax.set_title('Poverty vs Unemployment Rate')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-23.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 25: Outliers I - multiple scatterplots showing different outlier types
print("25. Outliers I...")
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

x_base = np.random.uniform(0, 10, 50)
y_base = 2 * x_base + np.random.normal(0, 1, 50)

# (a) Outlier in y
x1 = np.append(x_base, 5)
y1 = np.append(y_base, 20)
axes[0].scatter(x1, y1, alpha=0.5, s=30)
axes[0].set_title('(a)')
axes[0].set_xticks([])
axes[0].set_yticks([])

# (b) Outlier in x (leverage point)
x2 = np.append(x_base, 15)
y2 = np.append(y_base, 2 * 15 + 1)
axes[1].scatter(x2, y2, alpha=0.5, s=30)
axes[1].set_title('(b)')
axes[1].set_xticks([])
axes[1].set_yticks([])

# (c) Influential point
x3 = np.append(x_base, 15)
y3 = np.append(y_base, 5)
axes[2].scatter(x3, y3, alpha=0.5, s=30)
axes[2].set_title('(c)')
axes[2].set_xticks([])
axes[2].set_yticks([])

# (d) No outliers
axes[3].scatter(x_base, y_base, alpha=0.5, s=30)
axes[3].set_title('(d)')
axes[3].set_xticks([])
axes[3].set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-25.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 26: Outliers II - similar plots
print("26. Outliers II...")
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

for i, ax in enumerate(axes):
    x = np.random.uniform(0, 10, 50)
    y = 2 * x + np.random.normal(0, 1, 50)
    if i == 0:  # Add y-outlier
        x = np.append(x, 5)
        y = np.append(y, -5)
    elif i == 1:  # Add leverage point
        x = np.append(x, 14)
        y = np.append(y, 2 * 14)
    elif i == 2:  # Add influential point
        x = np.append(x, 13)
        y = np.append(y, 8)
    ax.scatter(x, y, alpha=0.5, s=30)
    ax.set_title(f'({chr(97+i)})')
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-26.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 27: Urban homeowners outliers
print("27. Urban homeowners outliers...")
fig, ax = plt.subplots(figsize=(8, 6))
urban = np.random.uniform(30, 100, 51)
homeowners = 75 - 0.3 * urban + np.random.normal(0, 5, 51)
# Add DC as outlier
urban = np.append(urban, 100)
homeowners = np.append(homeowners, 42)  # DC has low homeownership
ax.scatter(urban[:-1], homeowners[:-1], alpha=0.5, s=30)
ax.scatter(urban[-1], homeowners[-1], color='red', s=100, alpha=0.7, label='DC')
ax.set_xlabel('% Urban')
ax.set_ylabel('% Homeowners')
ax.set_title('Homeownership vs Urban Population')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-27.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 28: Crawling babies outliers
print("28. Crawling babies outliers...")
fig, ax = plt.subplots(figsize=(8, 6))
temp = np.linspace(30, 80, 11)
age = 33 - 0.7 * ((temp - 55) / 15) * 5 + np.random.normal(0, 1.5, 11)
# Add outlier
temp = np.append(temp, 53)
age = np.append(age, 28.5)
ax.scatter(temp[:-1], age[:-1], alpha=0.6, s=60)
ax.scatter(temp[-1], age[-1], color='red', s=100, alpha=0.7, label='Outlier')
ax.set_xlabel('Temperature (°F) at 6 months')
ax.set_ylabel('Average crawling age (weeks)')
ax.set_title('Crawling Age vs Temperature')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-28.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 30: Cherry trees - 3 scatterplots
print("30. Cherry trees...")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

n_trees = 31
height = np.random.uniform(60, 85, n_trees)
diameter = np.random.uniform(8, 20, n_trees)
volume = 0.3 * diameter**2 * height / 100 + np.random.normal(0, 3, n_trees)

# Volume vs Height
axes[0].scatter(height, volume, alpha=0.6, s=40)
axes[0].set_xlabel('Height (ft)')
axes[0].set_ylabel('Volume (cubic ft)')
axes[0].set_title('Volume vs Height')

# Volume vs Diameter
axes[1].scatter(diameter, volume, alpha=0.6, s=40)
axes[1].set_xlabel('Diameter (inches)')
axes[1].set_ylabel('Volume (cubic ft)')
axes[1].set_title('Volume vs Diameter')

# Height vs Diameter
axes[2].scatter(diameter, height, alpha=0.6, s=40)
axes[2].set_xlabel('Diameter (inches)')
axes[2].set_ylabel('Height (ft)')
axes[2].set_title('Height vs Diameter')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-30.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 31: Match the correlation III
print("31. Match the correlation III...")
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

correlations = [0.35, -0.62, 0.88, -0.15]
titles = ['(a)', '(b)', '(c)', '(d)']

for ax, r, title in zip(axes, correlations, titles):
    x_temp = np.random.uniform(0, 10, 100)
    y = r * x_temp + np.random.normal(0, np.sqrt(abs(1 - r**2)) * 3, 100)
    ax.scatter(x_temp, y, alpha=0.5, s=20)
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-31.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 32: Helmets and lunches
print("32. Helmets and lunches...")
fig, ax = plt.subplots(figsize=(8, 6))
lunch = np.random.uniform(0, 80, 30)
helmet = 60 - 0.7 * lunch + np.random.normal(0, 8, 30)
helmet = np.clip(helmet, 5, 95)
ax.scatter(lunch, helmet, alpha=0.6, s=40)
z = np.polyfit(lunch, helmet, 1)
p = np.poly1d(z)
x_line = np.linspace(lunch.min(), lunch.max(), 100)
ax.plot(x_line, p(x_line), 'r-', linewidth=2)
ax.set_xlabel('% receiving reduced-fee lunch')
ax.set_ylabel('% wearing helmets')
ax.set_title('Helmet Usage vs Reduced-Fee Lunch')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_07-ex-model-slr-32.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n✓ All exercise figures generated successfully!")
print(f"✓ Figures saved to {output_dir}/")

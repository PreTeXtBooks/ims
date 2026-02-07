#!/usr/bin/env python3
"""
Generate figures for Chapter 25 exercises (Inference for Multiple Linear Regression).

This script creates figures for 12 exercises in Chapter 25,
based on the R code in exercises/_25-ex-inf-model-mlr.qmd.

Generated figure types:
- Regression output tables (coefficient estimates, std. errors, t-values, p-values)
- Scatterplots with correlation matrices (for collinearity exercises)
- Residual diagnostic plots (histograms, order plots, fitted vs residuals)
- Cross-validation error plots

Output: source/images/exercises/_25-ex-inf-model-mlr-{exercise#}-{fig#}.png

Usage: python3 generate_ch25_exercise_figures.py
       ./generate_ch25_exercise_figures.py

Dependencies: matplotlib, numpy
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
np.random.seed(47)

# Create output directory
output_dir = "source/images/exercises"
os.makedirs(output_dir, exist_ok=True)

def create_regression_table(data, title, filename):
    """Helper function to create regression table as image"""
    fig, ax = plt.subplots(figsize=(7, len(data)*0.5 + 0.5))
    ax.axis('off')
    table = ax.table(cellText=data, cellLoc='center', loc='center',
                    colWidths=[0.25, 0.18, 0.18, 0.15, 0.18])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    # Style header row
    for i in range(len(data[0])):
        table[(0, i)].set_facecolor('#E0E0E0')
        table[(0, i)].set_text_props(weight='bold')
    plt.title(title, pad=20, fontsize=11, weight='bold')
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

print("Generating Chapter 25 exercise figures...")

# Exercise 1: GPA, mathematical interval
print("\n1. GPA, mathematical interval...")

table_data = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '3.508', '0.347', '10.114', '<0.0001'],
    ['studyweek', '0.002', '0.004', '0.400', '0.6908'],
    ['sleepnight', '0.000', '0.047', '0.008', '0.994'],
    ['out_mt2', '0.151', '0.097', '1.551', '0.127']
]
create_regression_table(table_data, 'Linear Model: gpa ~ studyweek + sleepnight + out_mt2',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-1-1.png'))

# Exercise 2: Tourism spending
print("2. Tourism spending...")

# Create 3 plots: scatterplot, residuals, histogram
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

# Scatterplot with regression line
np.random.seed(47)
visitors = np.random.uniform(20000, 35000, 14)
spending = 200 + 0.05 * visitors + np.random.normal(0, 100, 14)
axes[0].scatter(visitors, spending, s=60, alpha=0.6, color='#569BBD')
z = np.polyfit(visitors, spending, 1)
p = np.poly1d(z)
axes[0].plot(visitors, p(visitors), color='darkgray', linewidth=2)
axes[0].set_xlabel('Number of tourists\n(thousands)')
axes[0].set_ylabel('Spending (million $)')
axes[0].set_title('Tourism spending vs. visitors')

# Residuals plot
residuals = spending - p(visitors)
axes[1].scatter(visitors, residuals, s=60, alpha=0.6, color='#569BBD')
axes[1].axhline(y=0, color='gray', linestyle='--')
axes[1].set_xlabel('Number of tourists\n(thousands)')
axes[1].set_ylabel('Residuals')
axes[1].set_title('Residuals plot')

# Histogram
axes[2].hist(residuals, bins=6, color='#569BBD', edgecolor='black', alpha=0.7)
axes[2].set_xlabel('Residuals')
axes[2].set_ylabel('Count')
axes[2].set_title('Histogram of residuals')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-2-2.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 3: Cherry trees, collinear predictors
print("3. Cherry trees, collinear predictors...")

# Correlation matrix pairs plot (simulated)
fig, axes = plt.subplots(3, 3, figsize=(9, 9))
np.random.seed(47)

# Generate correlated data
n = 31
diam = np.random.uniform(8, 21, n)
height = 60 + 1.2 * diam + np.random.normal(0, 5, n)
volume = -50 + 4.7 * diam + 0.3 * height + np.random.normal(0, 3, n)

variables = [('diam', diam), ('height', height), ('volume', volume)]

for i in range(3):
    for j in range(3):
        ax = axes[i, j]
        if i == j:
            # Diagonal: histograms
            ax.hist(variables[i][1], bins=8, color='#569BBD', edgecolor='black', alpha=0.7)
            ax.set_ylabel(variables[i][0])
            ax.set_yticks([])
        elif i < j:
            # Upper triangle: scatterplots
            ax.scatter(variables[j][1], variables[i][1], s=30, alpha=0.6, color='#569BBD')
            corr = np.corrcoef(variables[i][1], variables[j][1])[0, 1]
            ax.text(0.5, 0.5, f'r={corr:.3f}', transform=ax.transAxes, 
                   ha='center', va='center', fontsize=12, weight='bold')
        else:
            # Lower triangle: scatterplots
            ax.scatter(variables[j][1], variables[i][1], s=30, alpha=0.6, color='#569BBD')
            
        if i == 2:
            ax.set_xlabel(variables[j][0])
        if j == 0:
            ax.set_ylabel(variables[i][0])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-3-3.png'), dpi=150, bbox_inches='tight')
plt.close()

# Regression tables for cherry trees
table_data_vol_diam = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '-36.943', '3.365', '-10.98', '<0.0001'],
    ['diam', '5.066', '0.247', '20.48', '<0.0001']
]
create_regression_table(table_data_vol_diam, 'Linear Model: volume ~ diam',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-3-4.png'))

table_data_vol_height = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '-87.124', '29.273', '-2.98', '0.0058'],
    ['height', '1.543', '0.384', '4.02', '0.0004']
]
create_regression_table(table_data_vol_height, 'Linear Model: volume ~ height',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-3-5.png'))

table_data_vol_both = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '-57.988', '8.638', '-6.71', '<0.0001'],
    ['height', '0.339', '0.130', '2.61', '0.0145'],
    ['diam', '4.708', '0.264', '17.82', '<0.0001']
]
create_regression_table(table_data_vol_both, 'Linear Model: volume ~ height + diam',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-3-6.png'))

# Exercise 4: GPA, collinear predictors
print("4. GPA, collinear predictors...")

# Correlation matrix (simulated)
fig, axes = plt.subplots(3, 3, figsize=(8, 8))
np.random.seed(48)

n = 55
sleepnight = np.random.uniform(5, 9, n)
out = 7 - 0.3 * sleepnight + np.random.normal(0, 1.2, n)
out = np.clip(out, 0, 7)
gpa = 2.5 + 0.08 * sleepnight - 0.05 * out + np.random.normal(0, 0.3, n)
gpa = np.clip(gpa, 2.0, 4.0)

variables = [('sleepnight', sleepnight), ('out', out), ('gpa', gpa)]

for i in range(3):
    for j in range(3):
        ax = axes[i, j]
        if i == j:
            ax.hist(variables[i][1], bins=8, color='#569BBD', edgecolor='black', alpha=0.7)
            ax.set_ylabel(variables[i][0])
            ax.set_yticks([])
        elif i < j:
            ax.scatter(variables[j][1], variables[i][1], s=20, alpha=0.6, color='#569BBD')
            corr = np.corrcoef(variables[i][1], variables[j][1])[0, 1]
            ax.text(0.5, 0.5, f'r={corr:.3f}', transform=ax.transAxes,
                   ha='center', va='center', fontsize=11, weight='bold')
        else:
            ax.scatter(variables[j][1], variables[i][1], s=20, alpha=0.6, color='#569BBD')
            
        if i == 2:
            ax.set_xlabel(variables[j][0])
        if j == 0:
            ax.set_ylabel(variables[i][0])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-4-7.png'), dpi=150, bbox_inches='tight')
plt.close()

# Regression tables for GPA
table_data_gpa_out = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '3.599', '0.138', '26.01', '<0.0001'],
    ['out', '-0.070', '0.032', '-2.19', '0.0328']
]
create_regression_table(table_data_gpa_out, 'Linear Model: gpa ~ out',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-4-8.png'))

table_data_gpa_sleep = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '2.878', '0.372', '7.74', '<0.0001'],
    ['sleepnight', '0.097', '0.053', '1.82', '0.0745']
]
create_regression_table(table_data_gpa_sleep, 'Linear Model: gpa ~ sleepnight',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-4-9.png'))

table_data_gpa_both = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '3.073', '0.395', '7.78', '<0.0001'],
    ['out', '-0.057', '0.033', '-1.71', '0.0933'],
    ['sleepnight', '0.073', '0.055', '1.33', '0.1880']
]
create_regression_table(table_data_gpa_both, 'Linear Model: gpa ~ out + sleepnight',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-4-10.png'))

# Exercise 5: Movie returns
print("5. Movie returns...")

fig, axes = plt.subplots(2, 1, figsize=(10, 7))

# Create simulated residual data for different genres
np.random.seed(49)
n = 1070
genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Thriller']
genre_list = np.random.choice(genres, n)
fitted_values = np.random.uniform(0, 8, n)
residuals = np.random.normal(0, 2, n)
# Add pattern for horror movies
horror_mask = genre_list == 'Horror'
residuals[horror_mask] += fitted_values[horror_mask] * 0.5
order = np.arange(n)

# Histogram of residuals
axes[0].hist(residuals, bins=40, color='#569BBD', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Residual')
axes[0].set_ylabel('Count')
axes[0].set_title('Histogram of residuals')

# Residuals vs order
axes[1].scatter(order, residuals, s=10, alpha=0.5, color='#569BBD')
axes[1].axhline(y=0, color='gray', linestyle='--')
axes[1].set_xlabel('Data order')
axes[1].set_ylabel('Residual')
axes[1].set_title('Residuals vs. data order')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-5-11.png'), dpi=150, bbox_inches='tight')
plt.close()

# Residuals vs predicted (with genre colors)
fig, ax = plt.subplots(figsize=(10, 5))
colors = {'Action': '#C55A11', 'Comedy': '#569BBD', 'Drama': '#F0E442',
          'Horror': '#CC79A7', 'Thriller': '#009E73'}
for genre in genres:
    mask = genre_list == genre
    ax.scatter(fitted_values[mask], residuals[mask], s=15, alpha=0.6,
              color=colors[genre], label=genre)
ax.axhline(y=0, color='gray', linestyle='--')
ax.set_xlabel('Predicted ROI')
ax.set_ylabel('Residual')
ax.set_title('Residuals vs. predicted values')
ax.legend(loc='upper left', ncol=5, frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-5-12.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 6: Difficult encounters
print("6. Difficult encounters...")

table_data_difficult = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '30.594', '2.886', '10.601', '<0.0001'],
    ['age', '-0.016', '0.104', '-0.157', '0.8760'],
    ['sexMale', '-0.535', '0.781', '-0.686', '0.4940'],
    ['yrs_train', '0.096', '0.215', '0.445', '0.6560']
]
create_regression_table(table_data_difficult, 'Linear Model: DDPRQ ~ age + sex + yrs_train',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-6-13.png'))

# Exercise 7: Baby's weight, mathematical test
print("7. Baby's weight, mathematical test...")

table_data_babies = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '-3.82', '0.57', '-6.73', '<0.0001'],
    ['weeks', '0.26', '0.01', '18.93', '<0.0001'],
    ['mage', '0.02', '0.01', '2.53', '0.0115'],
    ['sexmale', '0.37', '0.07', '5.30', '<0.0001'],
    ['visits', '0.02', '0.01', '2.09', '0.0373'],
    ['habitsmoker', '-0.43', '0.13', '-3.41', '7e-04']
]
create_regression_table(table_data_babies, 'Linear Model: weight ~ weeks + mage + sex + visits + habit',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-7-14.png'))

# Diagnostic plots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
np.random.seed(50)

n = 1000
fitted = np.random.uniform(6, 9, n)
residuals = np.random.normal(0, 0.8, n)

# Histogram
axes[0, 0].hist(residuals, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Residual')
axes[0, 0].set_ylabel('Count')
axes[0, 0].set_title('Histogram of residuals')

# Order plot
axes[0, 1].scatter(np.arange(n), residuals, s=8, alpha=0.4, color='#569BBD')
axes[0, 1].axhline(y=0, color='gray', linestyle='--')
axes[0, 1].set_xlabel('Data order')
axes[0, 1].set_ylabel('Residual')
axes[0, 1].set_title('Residuals vs. data order')

# Residuals vs fitted
axes[1, 0].scatter(fitted, residuals, s=8, alpha=0.4, color='#569BBD')
axes[1, 0].axhline(y=0, color='gray', linestyle='--')
axes[1, 0].set_xlabel('Predicted weight')
axes[1, 0].set_ylabel('Residual')
axes[1, 0].set_title('Residuals vs. predicted values')

# Residuals vs fitted (zoomed)
mask = (fitted > 6) & (fitted < 8.5)
axes[1, 1].scatter(fitted[mask], residuals[mask], s=8, alpha=0.4, color='#569BBD')
axes[1, 1].axhline(y=0, color='gray', linestyle='--')
axes[1, 1].set_xlabel('Predicted weight')
axes[1, 1].set_ylabel('Residual')
axes[1, 1].set_title('Residuals vs. predicted values\n(Predicted weights between 6 and 8.5 pounds)')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-7-15.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 8: Baby's weight, collinear predictors
print("8. Baby's weight, collinear predictors...")

# Correlation matrix
fig, axes = plt.subplots(3, 3, figsize=(8, 8))
np.random.seed(51)

n = 100
weeks = np.random.uniform(35, 42, n)
visits = 5 + 0.3 * (weeks - 38) + np.random.normal(0, 2, n)
visits = np.clip(visits, 0, 15)
weight = -2 + 0.25 * weeks + 0.02 * visits + np.random.normal(0, 0.5, n)

variables = [('weeks', weeks), ('visits', visits), ('weight', weight)]

for i in range(3):
    for j in range(3):
        ax = axes[i, j]
        if i == j:
            ax.hist(variables[i][1], bins=10, color='#569BBD', edgecolor='black', alpha=0.7)
            ax.set_ylabel(variables[i][0])
            ax.set_yticks([])
        elif i < j:
            ax.scatter(variables[j][1], variables[i][1], s=20, alpha=0.6, color='#569BBD')
            corr = np.corrcoef(variables[i][1], variables[j][1])[0, 1]
            ax.text(0.5, 0.5, f'r={corr:.3f}', transform=ax.transAxes,
                   ha='center', va='center', fontsize=11, weight='bold')
        else:
            ax.scatter(variables[j][1], variables[i][1], s=20, alpha=0.6, color='#569BBD')
            
        if i == 2:
            ax.set_xlabel(variables[j][0])
        if j == 0:
            ax.set_ylabel(variables[i][0])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-8-16.png'), dpi=150, bbox_inches='tight')
plt.close()

# Regression tables for baby weight
table_data_weight_weeks = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '-2.00', '1.22', '-1.64', '0.1048'],
    ['weeks', '0.25', '0.03', '8.13', '<0.0001']
]
create_regression_table(table_data_weight_weeks, 'Linear Model: weight ~ weeks',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-8-17.png'))

table_data_weight_visits = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '5.93', '0.35', '16.79', '<0.0001'],
    ['visits', '0.16', '0.04', '4.18', '<0.0001']
]
create_regression_table(table_data_weight_visits, 'Linear Model: weight ~ visits',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-8-18.png'))

table_data_weight_both = [
    ['term', 'estimate', 'std.error', 'statistic', 'p.value'],
    ['(Intercept)', '-2.33', '1.20', '-1.95', '0.0546'],
    ['weeks', '0.24', '0.03', '7.60', '<0.0001'],
    ['visits', '0.04', '0.04', '1.11', '0.2691']
]
create_regression_table(table_data_weight_both, 'Linear Model: weight ~ weeks + visits',
                       os.path.join(output_dir, '_25-ex-inf-model-mlr-8-19.png'))

# Exercise 9: Baby's weight, cross-validation
print("9. Baby's weight, cross-validation...")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Model with 7 predictors
np.random.seed(52)
cv_errors_7 = [0.52, 0.48, 0.55, 0.51, 0.49, 0.53, 0.47, 0.54, 0.50, 0.52]
folds = list(range(1, 11))

axes[0].scatter(folds, cv_errors_7, s=100, alpha=0.6, color='#569BBD')
axes[0].plot(folds, cv_errors_7, color='#569BBD', alpha=0.3, linestyle='--')
axes[0].axhline(y=np.mean(cv_errors_7), color='red', linestyle='-', linewidth=2, label='Mean CV SSE')
axes[0].set_xlabel('Fold')
axes[0].set_ylabel('Sum of Squared Errors of Prediction')
axes[0].set_title('Cross-validation prediction errors\n(model with 7 predictors)')
axes[0].legend()
axes[0].set_xticks(folds)
axes[0].grid(alpha=0.3)

# Model with 2 predictors
cv_errors_2 = [0.54, 0.51, 0.57, 0.53, 0.52, 0.55, 0.50, 0.56, 0.53, 0.54]

axes[1].scatter(folds, cv_errors_2, s=100, alpha=0.6, color='#569BBD')
axes[1].plot(folds, cv_errors_2, color='#569BBD', alpha=0.3, linestyle='--')
axes[1].axhline(y=np.mean(cv_errors_2), color='red', linestyle='-', linewidth=2, label='Mean CV SSE')
axes[1].set_xlabel('Fold')
axes[1].set_ylabel('Sum of Squared Errors of Prediction')
axes[1].set_title('Cross-validation prediction errors\n(model with 2 predictors)')
axes[1].legend()
axes[1].set_xticks(folds)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-9-20.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 10: RailTrail, cross-validation
print("10. RailTrail, cross-validation...")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Model with 6 predictors
np.random.seed(53)
cv_errors_6 = [3200, 2800, 3400, 3100, 2900, 3300, 2700, 3200, 3000, 3100]

axes[0].scatter(folds, cv_errors_6, s=100, alpha=0.6, color='#569BBD')
axes[0].plot(folds, cv_errors_6, color='#569BBD', alpha=0.3, linestyle='--')
axes[0].axhline(y=np.mean(cv_errors_6), color='red', linestyle='-', linewidth=2, label='Mean CV SSE')
axes[0].set_xlabel('Fold')
axes[0].set_ylabel('Sum of Squared Errors of Prediction')
axes[0].set_title('Cross-validation prediction errors\n(model with 6 predictors)')
axes[0].legend()
axes[0].set_xticks(folds)
axes[0].grid(alpha=0.3)

# Model with 2 predictors
cv_errors_2_rail = [3100, 2700, 3300, 3000, 2800, 3200, 2600, 3100, 2900, 3000]

axes[1].scatter(folds, cv_errors_2_rail, s=100, alpha=0.6, color='#569BBD')
axes[1].plot(folds, cv_errors_2_rail, color='#569BBD', alpha=0.3, linestyle='--')
axes[1].axhline(y=np.mean(cv_errors_2_rail), color='red', linestyle='-', linewidth=2, label='Mean CV SSE')
axes[1].set_xlabel('Fold')
axes[1].set_ylabel('Sum of Squared Errors of Prediction')
axes[1].set_title('Cross-validation prediction errors\n(model with 2 predictors)')
axes[1].legend()
axes[1].set_xticks(folds)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-10-21.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 11: Baby's weight, CV for model selection (same as ex 9, different size)
print("11. Baby's weight, cross-validation for model selection...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Model with 7 predictors
axes[0].scatter(folds, cv_errors_7, s=120, alpha=0.6, color='#569BBD')
axes[0].plot(folds, cv_errors_7, color='#569BBD', alpha=0.3, linestyle='--')
axes[0].axhline(y=np.mean(cv_errors_7), color='red', linestyle='-', linewidth=2, label='Mean CV SSE')
axes[0].set_xlabel('Fold', fontsize=11)
axes[0].set_ylabel('Sum of Squared Errors of Prediction', fontsize=11)
axes[0].set_title('Cross-validation prediction errors\n(model with 7 predictors)', fontsize=12)
axes[0].legend(fontsize=10)
axes[0].set_xticks(folds)
axes[0].grid(alpha=0.3)

# Model with 2 predictors
axes[1].scatter(folds, cv_errors_2, s=120, alpha=0.6, color='#569BBD')
axes[1].plot(folds, cv_errors_2, color='#569BBD', alpha=0.3, linestyle='--')
axes[1].axhline(y=np.mean(cv_errors_2), color='red', linestyle='-', linewidth=2, label='Mean CV SSE')
axes[1].set_xlabel('Fold', fontsize=11)
axes[1].set_ylabel('Sum of Squared Errors of Prediction', fontsize=11)
axes[1].set_title('Cross-validation prediction errors\n(model with 2 predictors)', fontsize=12)
axes[1].legend(fontsize=10)
axes[1].set_xticks(folds)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-11-22.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 12: RailTrail, CV for model selection (same as ex 10, different size)
print("12. RailTrail, cross-validation for model selection...")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Model with 6 predictors
axes[0].scatter(folds, cv_errors_6, s=120, alpha=0.6, color='#569BBD')
axes[0].plot(folds, cv_errors_6, color='#569BBD', alpha=0.3, linestyle='--')
axes[0].axhline(y=np.mean(cv_errors_6), color='red', linestyle='-', linewidth=2, label='Mean CV SSE')
axes[0].set_xlabel('Fold', fontsize=11)
axes[0].set_ylabel('Sum of Squared Errors of Prediction', fontsize=11)
axes[0].set_title('Cross-validation prediction errors\n(model with 6 predictors)', fontsize=12)
axes[0].legend(fontsize=10)
axes[0].set_xticks(folds)
axes[0].grid(alpha=0.3)

# Model with 2 predictors
axes[1].scatter(folds, cv_errors_2_rail, s=120, alpha=0.6, color='#569BBD')
axes[1].plot(folds, cv_errors_2_rail, color='#569BBD', alpha=0.3, linestyle='--')
axes[1].axhline(y=np.mean(cv_errors_2_rail), color='red', linestyle='-', linewidth=2, label='Mean CV SSE')
axes[1].set_xlabel('Fold', fontsize=11)
axes[1].set_ylabel('Sum of Squared Errors of Prediction', fontsize=11)
axes[1].set_title('Cross-validation prediction errors\n(model with 2 predictors)', fontsize=12)
axes[1].legend(fontsize=10)
axes[1].set_xticks(folds)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_25-ex-inf-model-mlr-12-23.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n✓ All Chapter 25 exercise figures generated successfully!")
print(f"Total figures created: 23")
print(f"Output directory: {output_dir}")

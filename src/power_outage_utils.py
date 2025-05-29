# -*- coding: utf-8 -*-
"""
Created on Wed May  7 08:30:33 2025

@author: Tim with Janet
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.ticker as ticker

# === FILE PATH ===
FILE_PATH = 'data/power-outage-history.csv'

# === LOAD AND PREP OUTAGE DATA ===
def load_outage_data(filepath=FILE_PATH):
    df = pd.read_csv(filepath)

    # Parse dates (date-only)
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce').dt.date
    df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce').dt.date

    # Parse times (time-only)
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce').dt.time
    df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce').dt.time

    # Combine into full datetime if both parts are available
    df['Start Datetime'] = combine_datetime(df, 'Start Date', 'Start Time')
    df['End Datetime'] = combine_datetime(df, 'End Date', 'End Time')

    # Sort by Start Date
    df = df.sort_values(by=['Start Date']).reset_index(drop=True)

    return df

# === COMBINE DATE AND TIME TO DATETIME ===
def combine_datetime(df, date_col, time_col):
    return [
        datetime.combine(d, t) if pd.notnull(d) and pd.notnull(t) else pd.NaT
        for d, t in zip(df[date_col], df[time_col])
    ]

# === PLOT: OUTAGES BY YEAR ===
def plot_outages_by_year(df):
    # Extract year from Start Date
    df['Year'] = pd.to_datetime(df['Start Date'], errors='coerce').dt.year

    # Create complete year range from min to max year
    all_years = list(range(df['Year'].min(), df['Year'].max() + 1))

    # Count outages per year, reindex to include all years - even those w/o any outages
    year_counts = df['Year'].value_counts().reindex(all_years, fill_value=0).sort_index()

    # Plot bars
    fig, ax = plt.subplots(figsize=(8, 5))
    year_counts.plot(kind='bar', color='darkcyan', ax=ax)

    # Aesthetics
    ax.set_title('Number of Power Outages by Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Outages')
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Compute Averages
    pre2020_years = [year for year in all_years if year < 2020]
    post2020_years = [year for year in all_years if 2020 <= year <= 2024]  # exclude 2025

    pre2020_avg = year_counts.loc[pre2020_years].mean()
    post2020_avg = year_counts.loc[post2020_years].mean()

    # Draw Horizontal Segments for Averages
    # Pre-2020 avg line
    pre_start = all_years.index(pre2020_years[0]) - 0.4
    pre_end = all_years.index(pre2020_years[-1]) + 0.4
    ax.hlines(pre2020_avg, xmin=pre_start, xmax=pre_end, color='orangered', linestyle='--', alpha=0.8)

    # 2020–2024 avg line
    post_start = all_years.index(post2020_years[0]) - 0.4
    post_end = all_years.index(post2020_years[-1]) + 0.4
    ax.hlines(post2020_avg, xmin=post_start, xmax=post_end, color='orangered', linestyle='--', alpha=0.8)

    # Pre-2020 avg label near 2018 (good choice—empty space)
    pre2020_label_x = all_years.index(2018)
    ax.text(pre2020_label_x, pre2020_avg + 0.1, f'Avg: {pre2020_avg:.2f}', color='orangered', ha='center')
    
    # 2020–2024 avg label near 2023 (less crowded)
    post2020_label_x = all_years.index(2023)
    ax.text(post2020_label_x, post2020_avg + 0.1, f'Avg: {post2020_avg:.2f}', color='orangered', ha='center')

    # --- Add '?' Above 2025 Bar ---
    if 2025 in year_counts.index:
        bar_height = year_counts.loc[2025]
        ax.text(year_counts.index.get_loc(2025), bar_height + 0.05, '?', ha='center', va='bottom', fontsize=12, color='black')

    plt.tight_layout()
    plt.show()


# === PLOT: OUTAGES BY MONTH ===
def plot_outages_by_month(df):
    # Use 'Month' column if it exists; otherwise extract from 'Start Date'
    if 'Month' in df.columns:
        month_series = df['Month']
    else:
        month_series = pd.to_datetime(df['Start Date'], errors='coerce').dt.month

    # Full month range with labels
    all_months = list(range(1, 13))
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Count outages by month
    month_counts = month_series.value_counts().reindex(all_months, fill_value=0)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    month_counts.plot(kind='bar', color='darkcyan', ax=ax)
    ax.set_title('Number of Power Outages by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Outages')
    ax.set_xticks(range(12))
    ax.set_xticklabels(month_names)
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # integer ticks only
    plt.tight_layout()
    plt.show()

# === PLOT: OUTAGE DURATIONS AS NUMBER LINE WITH ANNOTATIONS ===
def plot_outage_durations_number_line(df):
    durations = df['Duration Hours'].dropna()
    duration_counts = durations.value_counts().sort_index()

    # Compute summary stats
    max_val = durations.max()
    span_limit = max_val + 5

    fig, ax = plt.subplots(figsize=(10, 4))

    # Spoilage risk zones (extend to span_limit for emphasis)
    fridge_patch  = ax.axvspan( 4, span_limit, color='orange', alpha=0.2, label='Fridge Spoilage Risk (4+ hours)')
    freezer_patch = ax.axvspan(24, span_limit, color='red',    alpha=0.2, label='Freezer Spoilage Risk (24+ hours)')

    # Bars
    ax.bar(duration_counts.index, duration_counts.values, width=0.3, color='darkcyan')

    # Final polish
    ax.set_xlim(left=0, right=span_limit)
    ax.set_title('Power Outage Duration (Hours)')
    ax.set_xlabel('Duration (hours)')
    ax.set_ylabel('Count')
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    ax.set_yticks(range(1, duration_counts.max() + 2))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Legend below the plot
    fig.legend(handles=[fridge_patch, freezer_patch], loc='lower center', ncol=2, fontsize=10, frameon=False, bbox_to_anchor=(0.5, -0.05))

    plt.tight_layout()
    plt.show()


# === PLOT: TIME OF DAY (START OR END) ===
def plot_time_of_day(df, column_label):
    # Filter out null values
    time_series = df[column_label].dropna()

    # Convert to float hour of day
    times = pd.to_datetime(time_series.astype(str), format='%H:%M:%S', errors='coerce')
    float_hours = times.dt.hour + times.dt.minute / 60

    counts = float_hours.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 4))

    # Background shading: Asleep = dark gray, Awake = yellow
    ax.axvspan(0, 5, color='dimgray', alpha=0.4)
    ax.axvspan(5, 22, color='yellow', alpha=0.4)
    ax.axvspan(22, 24, color='dimgray', alpha=0.4)

    # Bars
    ax.bar(counts.index, counts.values, width=0.1, color='darkcyan')

    # Labels & ticks
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 2))
    ax.set_title(f'Outage {column_label}')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Count')
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Simplified legend: Awake vs Asleep
    fig.legend(labels=['Asleep (10pm–5am)', 'Awake (5am–10pm)'],
               loc='lower center', ncol=2, fontsize=10, frameon=False,
               bbox_to_anchor=(0.5, -0.05))

    plt.tight_layout()
    plt.show()


# === PLOT: CUMULATIVE DURATION OVER TIME ===
def plot_cumulative_duration_by_year(df):
    df['Year'] = pd.to_datetime(df['Start Date'], errors='coerce').dt.year
    durations_by_year = df.groupby('Year')['Duration Hours'].sum().sort_index()

    fig, ax = plt.subplots(figsize=(8, 3))
    durations_by_year.cumsum().plot(ax=ax, marker='o', color='darkcyan')

    ax.set_title('Cumulative Power Outage Duration Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Hours Without Power')
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    plt.tight_layout()
    plt.show()



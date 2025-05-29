# -*- coding: utf-8 -*-
"""
Created on Wed May  7 08:12:44 2025

@author: Tim Graettinger with Janet
"""

from src.power_outage_utils import (load_outage_data, 
                                plot_outages_by_year, 
                                plot_outages_by_month,
                                plot_outage_durations_number_line,
                                plot_time_of_day,
                                plot_cumulative_duration_by_year
                                )


# Load data
outage_df = load_outage_data()

# Plot outages by year
plot_outages_by_year(outage_df)

# Plot outages by month
plot_outages_by_month(outage_df)

# Plot outage durations as a number line
plot_outage_durations_number_line(outage_df)

# Plot time-of-day for the start and the end of the outages
plot_time_of_day(outage_df, 'Start Time')

# Plot cumulative duration over time
plot_cumulative_duration_by_year(outage_df)

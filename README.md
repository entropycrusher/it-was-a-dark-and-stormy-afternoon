
# It Was a Dark and Stormy Afternoon: How We Used Data to Prepare for Our Next Power Outage

This repository contains the data, code, and visualizations for the article:
["It Was a Dark and Stormy Afternoon"](https://timgraettinger.com/articles/it-was-a-dark-and-stormy-afternoon/)  
published on May 25, 2025.

## 🌱 Project Summary

This project explores eight years of home power outage history 
using personal logs and NOAA wind data 
to uncover patterns in outage timing, duration, seasonality, and wind-related triggers. 
Through Python-based visualizations and practical interpretation, 
it reveals how data helped reshape our readiness strategy — 
from reactive to confident and prepared. 
The repository includes all data, code, and charts 
referenced in the article “It Was a Dark and Stormy Afternoon.”

## 📁 Contents

- `data/` — Source datasets (power outage history, NOAA wind speed data)
- `docs/` — The PDF version of the article
- `figs/` — Final visualizations
- `src/`  — Code used to generate the charts
- `README.md` — This file
- `LICENSE` — License info

## 📊 Running the Code

To regenerate the plots:

```bash
python src/create-power-outage-visuals.py

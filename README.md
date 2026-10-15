# 🎬 YouTube Global Trends Analytics

A **Big Data Analytics** dashboard that analyzes trending YouTube video patterns across **113 countries** using **Apache Spark** and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat&logo=streamlit)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-PySpark-orange?style=flat&logo=apachespark)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-purple?style=flat&logo=plotly)

## 🔗 Live Demo

**[View Dashboard →](https://hemanthraj09-youtube-data-analytics.streamlit.app)**

---

## 📊 Project Overview

This project processes and visualizes a **5.5GB+ dataset** of YouTube trending videos from 113 countries. The dashboard provides insights into:

- 🌍 **Geographic Distribution** — Which countries have the most viral content
- 🗣️ **Language Analysis** — Content language patterns across regions
- 📈 **Engagement Metrics** — View counts, likes, and engagement rates
- 🏆 **Top Performers** — Leading channels and trending creators

### Why Apache Spark?

The original dataset contains **~4.3M trending records (5.5GB)**. Apache Spark was used for:
- Distributed data processing
- Efficient sampling and aggregation
- Handling large-scale data transformations

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Interactive Filters** | Filter by country and language |
| **Real-time Aggregation** | Charts update dynamically based on filters |
| **Noise Reduction** | Minimum threshold filtering removes outliers |
| **Key Insights** | Auto-generated highlights (top region, dominant language, etc.) |
| **Responsive Design** | Professional dark theme optimized for presentation |

---

## 🛠️ Tech Stack

- **Data Processing:** Apache Spark (PySpark), Parquet
- **Machine Learning:** Spark MLlib (Random Forest view-count forecast)
- **Backend:** Python, Pandas, NumPy
- **Visualization:** Plotly
- **Frontend:** Streamlit
- **Deployment:** Streamlit Cloud

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Hemanthraj09/Youtube-data-Analytics.git
cd Youtube-data-Analytics

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 📁 Project Structure

```
Youtube-data-Analytics/
├── app.py                    # Main Streamlit application
├── yt_trending_sample.csv    # Sampled dataset (5.4MB)
├── spark_session.py          # Shared local SparkSession setup
├── spark_prepare.py          # Raw CSV → Parquet (one-time)
├── spark_forecast.py         # View-count forecast (Spark MLlib)
├── BigData_pipeline.md       # End-to-end pipeline documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

---

## 📈 Data Pipeline

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Raw Dataset    │────▶│ Apache Spark │────▶│ Sampled Dataset │
│  (5.5GB, 4.3M)  │     │  Processing  │     │  (5.4MB, 42K)   │
└─────────────────┘     └──────────────┘     └─────────────────┘
                                                      │
                                                      ▼
                               ┌─────────────────────────────────┐
                               │     Streamlit Dashboard         │
                               │  • Interactive Visualizations   │
                               │  • Real-time Filtering          │
                               │  • Key Insights Generation      │
                               └─────────────────────────────────┘
```

---

## 📊 Key Insights

The dashboard automatically generates insights such as:
- **Top Region** — Country with highest total views
- **Dominant Language** — Most common content language
- **Highest Engagement** — Language with best engagement rate

---

## 🔮 View-Count Forecasting (Spark MLlib)

A Spark MLlib model forecasts a trending video's view count **1 or 3 days ahead**, trained on the full 4.3M-record dataset. Features are built with Spark window functions over each video's trending history (recent growth, days on trending, country spread, rank movement) plus past-only channel history, video age and content signals. The model is tested on later dates than it was trained on (from August 2025).

| Horizon | Model | R² (log views) | R² (growth) | Median error |
|---------|-------|----------------|-------------|--------------|
| 1 day  | "No change" baseline | 0.952 | — | 9.6% |
| 1 day  | **Random Forest** | **0.988** | **0.62** | **1.6%** |
| 3 days | "No change" baseline | 0.877 | — | 20.4% |
| 3 days | **Random Forest** | **0.973** | **0.63** | **3.7%** |

Run it locally (requires Java 17 and PySpark; see [BigData_pipeline.md](BigData_pipeline.md) for details):

```bash
python spark_prepare.py                 # one-time: raw CSV → Parquet
python spark_forecast.py --horizon 1    # build features, train and evaluate
```

---

## 🤝 Contact

**Hemanth Raj**

[![GitHub](https://img.shields.io/badge/GitHub-Hemanthraj09-black?style=flat&logo=github)](https://github.com/Hemanthraj09)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-hemanthrajmv-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/hemanthrajmv)

---

## 📄 License

This project is for educational and portfolio purposes.

---

<p align="center">
  <b>⭐ If you found this project useful, please give it a star!</b>
</p>

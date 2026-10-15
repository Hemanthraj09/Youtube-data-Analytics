# YouTube Global Trends Analytics: End-to-End Pipeline

This document outlines the complete end-to-end workflow of the YouTube Global Trends Analytics project. The pipeline encompasses data ingestion, cleaning, feature engineering, a view-count forecasting model built with Apache Spark, and interactive visualization using Streamlit.

## 1. Data Ingestion
- **Source Dataset**: `trending_yt_videos_113_countries.csv`
- **Volume**: Over **5.5 GB** of data spanning ~4.3 million trending records across 113 countries.
- **Tool Used**: **Apache Spark (PySpark)** is utilized because the data volume exceeds standard single-machine memory capacities (like Pandas). Spark's distributed computing logic efficiently loads the dataset.

## 2. Storage & Preprocessing (`spark_prepare.py`)
- **Parsing**: The CSV is read with an explicit schema and `multiLine` / `escape` options, because video descriptions contain line breaks and quotes. All 4,258,851 records parse with the expected 18 fields.
- **Columnar storage**: The data is written once to **Parquet** (~0.9 GB, 48 partitions). Every later Spark job reads Parquet instead of re-parsing the 5.5 GB CSV.
- **Slimming**: `thumbnail_url` is dropped and the description text is replaced by its length, the only part the pipeline uses.

## 3. Forecasting Dataset (`spark_forecast.py`)
- **Task**: for a video on the trending list on day *t*, forecast its view count on day *t + H* (H = 1 or 3 days), using only information available on day *t*.
- **One row per video per day**: view counts are global per video, so the per-country rows for the same day are aggregated (max views, number of countries, best and average rank).
- **Label**: views on day *t + H*, obtained by joining each video-day to the same video's snapshot *H* days later. The model predicts the log growth `log1p(views[t+H]) − log1p(views[t])` and converts back to a view count.
- **Coverage**: a video is only recorded while it is trending. 76.6% of video-days are still trending one day later, 49.0% after three days and 22.9% after seven, which is why short horizons are used.

## 4. Feature Engineering (Spark window functions)
- **Current state**: log views, likes and comments; like and comment rates; video age in days.
- **Trending history** (window over each video's snapshots): previous snapshot's views, recent growth rates, days on trending, days since first trending, number of countries today and the maximum so far, best/average rank and rank movements.
- **Channel history**: mean log views of the channel's earlier video-days and the number of its videos seen before, computed with a window that ends the day before *t*, so no future information is used.
- **Content and timing**: title length, tag count (tags are comma-separated), description length, publish weekday and hour, language (top 30, rest grouped).
- Like and comment rates divide by **today's** views, which are known on day *t*; nothing involves the future views being predicted. (The earlier same-day model leaked here: its `engagement_rate` feature was derived from the very view count it was predicting.)

## 5. Time-Based Split (Leakage Prevention)
- The latest 15% of snapshot days (from 2025-08-01) form the test set. Training rows must have their label day before that date, so no training label overlaps the test period.
- Every feature is computed from data up to day *t*, so the test set reflects a real forecast of unseen future days.

## 6. Forecasting Model & Results
- **Model**: Spark MLlib **RandomForestRegressor** (80 trees, max depth 14). A 50-tree forest and **GBTRegressor** were also compared; gradient boosting was slightly worse and six times slower.
- **Baseline**: "no change" (tomorrow's views = today's views). Because views change little day to day, this baseline already scores a high R², so the model is judged by how much it beats it.
- **Metrics**: R² on views and log views, R² on log growth (the part that is genuinely hard to predict), and median absolute percentage error.

| Horizon | Model | R² views | R² log views | R² growth | Median % error |
|---|---|---|---|---|---|
| 1 day | No-change baseline | 0.9935 | 0.952 | −0.47 | 9.61% |
| 1 day | Random Forest (50 trees, depth 10) | 0.9969 | 0.986 | 0.582 | 1.71% |
| 1 day | **Random Forest (80 trees, depth 14)** | **0.9970** | **0.988** | **0.623** | **1.55%** |
| 3 days | No-change baseline | 0.9710 | 0.877 | −0.71 | 20.44% |
| 3 days | Random Forest (50 trees, depth 10) | 0.9877 | 0.970 | 0.583 | 4.02% |
| 3 days | **Random Forest (80 trees, depth 14)** | **0.9880** | **0.973** | **0.627** | **3.73%** |

- **Reading the results**: the forecast cuts the typical error from 9.6% to 1.6% (1 day) and from 20.4% to 3.7% (3 days), and explains about 62% of the variation in growth, the part a "no change" guess cannot capture.
- **Most important features**: recent growth rate, days on trending, days since first trending, video age, and the previous snapshot's views.

## 7. Downsampling & UI Preparation
- **Dataset Sampling**: To provide a snappy, real-time dashboard on Streamlit Cloud, a random sample of the processed output data is generated (`yt_trending_sample.csv`).
- **Noise Filtering**: A logical threshold (e.g., threshold set at `view_count > 5000`) is applied to keep focus on genuinely "trending" data and remove unrepresentative noise.

## 8. Interactive Dashboard & Visualization (Streamlit)
- **State management & UI**: Streamlit provides a highly interactive portal into the data.
- **Visual Analytics**: **Plotly** powers dynamic, real-time charts including:
  - Geographic performance mapping (Views by Country).
  - Categorizing views and determining dominant languages.
  - Scatter plots correlating Engagement against Popularity.
  - Analyzing trending activity across months.
- **Dynamic Filtering**: Users can slice and analyze views dynamically based on **Region** and **Language**.

## Summary 
The pipeline scales rigorously from heavy-duty **Big Data processing (PySpark)** down to a highly optimized, light-footprint **web application (Streamlit)** resulting in a fully interactive, full-stack analytics tracker.

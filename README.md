# 🏨 Hotel Business Intelligence Dashboard

An interactive Streamlit dashboard designed to analyse hotel booking demand, cancellation behaviour, stay duration, booking lead time, and seasonal booking patterns.

## 📊 Project Overview

The Hotel Business Intelligence Dashboard transforms hotel booking data into an interactive business analytics application.

The dashboard helps users understand:

- Hotel booking demand
- City Hotel vs Resort Hotel performance
- Cancellation behaviour
- Cancellation risk by hotel type
- Relationship between stay duration and cancellations
- Relationship between booking lead time and cancellations
- Monthly booking trends
- Seasonal demand patterns
- Key business insights
- Business recommendations

## 🎯 Project Objective

The objective of this project is to analyse hotel booking demand and cancellation behaviour using data visualisation and convert the findings into practical business recommendations.

The analysis focuses particularly on:

- Hotel type
- Stay duration
- Booking lead time
- Cancellation behaviour
- Monthly booking demand

## 📈 Dashboard Features

### Executive Overview
Provides a high-level summary of the selected booking data, including:

- Total bookings
- City Hotel booking share
- Overall cancellation rate
- Peak booking month

### Hotel Demand
Analyses booking distribution between:

- City Hotel
- Resort Hotel

### Cancellation Risk
Examines cancellation behaviour based on:

- Hotel type
- Stay duration
- Booking lead time

### Seasonality & Booking Trends
Visualises monthly booking patterns and compares demand between City Hotel and Resort Hotel.

### Key Business Insights
Automatically highlights important findings from the selected dataset.

### Business Interpretation
Provides practical recommendations based on the observed booking and cancellation patterns.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- GitHub

## 📂 Project Structure

```text
hotel-business-intelligence/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── hotel_bookings_cleaned.csv

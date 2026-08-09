import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hotel Business Intelligence",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD DATA (WITH SAFETY CHECK)
# ============================================================

DATA_PATH = "data/hotel_bookings_cleaned.csv"

if not os.path.exists(DATA_PATH):
  st.error(
      f"⚠️ Dataset not found at `{DATA_PATH}`. Please make sure you have a"
      " 'data' folder containing 'hotel_bookings_cleaned.csv'."
  )
  st.stop()

df = pd.read_csv(DATA_PATH)


# ============================================================
# DATA PREPARATION
# ============================================================

# Total stay duration
df["total_stay"] = df["stays_in_weekend_nights"] + df["stays_in_weekdays_nights"]


# Stay duration groups
df["stay_duration_group"] = pd.cut(
    df["total_stay"],
    bins=[-1, 2, 5, 7, float("inf")],
    labels=[
        "Short stay (0–2 nights)",
        "Medium stay (3–5 nights)",
        "Week-long stay (6–7 nights)",
        "Long stay (8+ nights)",
    ],
)


# Lead time groups
df["lead_time_group"] = pd.cut(
    df["lead_time"],
    bins=[-1, 7, 30, 90, 180, float("inf")],
    labels=[
        "Last-minute (0–7 days)",
        "Short-term (8–30 days)",
        "Medium-term (31–90 days)",
        "Long-term (91–180 days)",
        "Far in advance (181+ days)",
    ],
)


# Month order
month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


# ============================================================
# PREMIUM DASHBOARD THEME & FONT STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ---------------- GENERAL PAGE & FONT ---------------- */

    .stApp {
        background-color: #F7F4EE;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* ---------------- SIDEBAR ---------------- */

    [data-testid="stSidebar"] {
        background-color: #17212B;
    }

    [data-testid="stSidebar"] * {
        color: #F7F4EE !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }


    /* ---------------- MAIN TITLE ---------------- */

    .dashboard-title {
        font-size: 42px;
        font-weight: 700;
        color: #17212B !important;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .dashboard-subtitle {
        font-size: 17px;
        color: #6B6B63 !important;
        margin-bottom: 28px;
    }


    /* ---------------- SECTION HEADINGS ---------------- */

    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: #17212B !important;
        margin-top: 32px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        font-size: 14px;
        color: #77766F !important;
        margin-bottom: 18px;
    }


    /* ---------------- GRAPH HEADINGS ---------------- */

    .chart-title {
        font-size: 18px;
        font-weight: 700;
        color: #17212B !important;
        margin-top: 10px;
        margin-bottom: 4px;
    }

    .chart-caption {
        font-size: 12px;
        color: #77766F !important;
        margin-top: -8px;
        margin-bottom: 20px;
        line-height: 1.5;
    }


    /* ---------------- KPI CARDS ---------------- */

    .kpi-card {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #E5E0D7;
        box-shadow: 0px 4px 14px rgba(23, 33, 43, 0.06);
        min-height: 125px;
    }

    .kpi-label {
        color: #77766F !important;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #17212B !important;
        font-size: 30px;
        font-weight: 700;
    }

    .kpi-description {
        color: #9A978E !important;
        font-size: 12px;
        margin-top: 5px;
    }


    /* ---------------- INSIGHT CARDS ---------------- */

    .insight-card {
        background-color: #FFFFFF;
        border-left: 4px solid #B89B5E;
        padding: 18px 20px;
        border-radius: 10px;
        margin-bottom: 14px;
        box-shadow: 0px 3px 10px rgba(23, 33, 43, 0.05);
        min-height: 125px;
    }

    .insight-title {
        color: #17212B !important;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 7px;
    }

    .insight-text {
        color: #66645E !important;
        font-size: 14px;
        line-height: 1.55;
    }


    /* ---------------- RECOMMENDATION CARDS ---------------- */

    .recommendation-card {
        background-color: #FFFDF8;
        border: 1px solid #E5E0D7;
        border-left: 4px solid #B89B5E;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 14px;
        box-shadow: 0px 3px 10px rgba(23, 33, 43, 0.04);
    }

    .recommendation-title {
        color: #17212B !important;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .recommendation-text {
        color: #66645E !important;
        font-size: 14px;
        line-height: 1.55;
    }


    /* ---------------- EXPANDER FIX ---------------- */

    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E0D7 !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] summary p {
        color: #17212B !important;
        font-weight: 600 !important;
    }

    [data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p, 
    [data-testid="stExpander"] div[data-testid="stMarkdownContainer"] li {
        color: #17212B !important;
    }


    /* ---------------- FOOTER ---------------- */

    .footer {
        text-align: center;
        padding: 35px 0 10px 0;
        color: #8A877F !important;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PLOTLY THEME
# ============================================================


def premium_chart(fig):
  fig.update_layout(
      title=None,
      paper_bgcolor="#FFFFFF",
      plot_bgcolor="#FFFFFF",
      font=dict(family="Segoe UI, Roboto, sans-serif", color="#17212B"),
      margin=dict(t=30, b=55, l=60, r=30),
      hoverlabel=dict(bgcolor="#17212B", font_color="#FFFFFF"),
      legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#17212B")),
  )

  fig.update_xaxes(
      showgrid=False,
      linecolor="#E5E0D7",
      tickfont=dict(color="#66645E"),
      title_font=dict(color="#17212B"),
  )

  fig.update_yaxes(
      gridcolor="#EEEAE2",
      zeroline=False,
      linecolor="#E5E0D7",
      tickfont=dict(color="#66645E"),
      title_font=dict(color="#17212B"),
  )

  return fig


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">Hotel Business Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="dashboard-subtitle">Understanding booking demand, cancellation'
    " behaviour & seasonal patterns</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR NAVIGATION & FILTERS
# ============================================================

nav_selection = st.sidebar.radio(
    "Go to section",
    [
        "All Sections (Full View)",
        "Overview & Context",
        "Hotel Demand",
        "Cancellation Risk",
        "Seasonality & Trends",
        "Insights & Recommendations",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("## Dashboard Filters")

hotel_options = ["All Hotels"] + sorted(df["hotel"].dropna().unique().tolist())
selected_hotel = st.sidebar.selectbox("Hotel Type", hotel_options)

if selected_hotel != "All Hotels":
  filtered_df = df[df["hotel"] == selected_hotel].copy()
else:
  filtered_df = df.copy()

st.sidebar.markdown("---")
st.sidebar.caption(
    "Use the selection above to jump between sections, or filter by hotel type."
)


# Helper flags for navigation display
show_all = nav_selection == "All Sections (Full View)"


# ============================================================
# SECTION 1: OVERVIEW & CONTEXT
# ============================================================

if show_all or nav_selection == "Overview & Context":
  st.markdown(
      '<div class="section-title">Project Context & Objectives</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      """<div class="insight-card">
<div class="insight-title">🎯 Why Customer Behaviour Analysis Matters</div>
<div class="insight-text">
Understanding customer booking behaviour allows hotel management to anticipate market demand, optimize room inventory, and minimize revenue loss from cancellations. It directly improves decisions regarding dynamic pricing, staffing allocation, marketing campaigns, and cancellation policies.
</div>
</div>""",
      unsafe_allow_html=True,
  )

  with st.expander("Data Preprocessing & Cleaning Details"):
    st.markdown("""
        * **Dataset Overview:** Covers hotel bookings from 2017–2019 containing around 119k rows and 29 columns.
        * **Missing Values Handled:** Columns like company and agent missing values indicate direct bookings or corporate stays without third-party agents. Missing values in children were filled with zero, and missing country values were marked as unknown.
        * **Duplicate Rows:** Checked and removed duplicate entries to prevent skewing analytical metrics.
        * **Inconsistent Values:** Recategorized unclear entries (such as 'Undefined' values in the meal category) into standard meal plans (Bed & Breakfast, Half Board, etc.).
        * **Anomalies Checked:** Filtered out extreme or negative Average Daily Rate (adr) anomalies and bookings recording zero guests to maintain analysis accuracy.
        """)

  # KPI Calculations
  total_bookings = len(filtered_df)
  city_bookings = filtered_df["hotel"].eq("City Hotel").sum()
  city_share = (
      (city_bookings / total_bookings * 100) if total_bookings > 0 else 0
  )
  cancellation_rate = (
      (filtered_df["is_canceled"].mean() * 100) if total_bookings > 0 else 0
  )
  monthly_kpi = filtered_df.groupby("arrival_date_month").size()
  if len(monthly_kpi) > 0:
    peak_month = monthly_kpi.idxmax()
    peak_bookings = int(monthly_kpi.max())
  else:
    peak_month = "N/A"
    peak_bookings = 0

  st.markdown(
      '<div class="section-title">Executive Overview</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="section-subtitle">A snapshot of the current booking'
      " portfolio</div>",
      unsafe_allow_html=True,
  )

  kpi1, kpi2, kpi3, kpi4 = st.columns(4)

  with kpi1:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-label">TOTAL BOOKINGS</div>
                <div class="kpi-value">{total_bookings:,}</div>
                <div class="kpi-description">Bookings in selected view</div>
            </div>
            """,
        unsafe_allow_html=True,
    )
  with kpi2:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-label">CITY HOTEL SHARE</div>
                <div class="kpi-value">{city_share:.2f}%</div>
                <div class="kpi-description">Share of selected bookings</div>
            </div>
            """,
        unsafe_allow_html=True,
    )
  with kpi3:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-label">CANCELLATION RATE</div>
                <div class="kpi-value">{cancellation_rate:.2f}%</div>
                <div class="kpi-description">Bookings cancelled</div>
            </div>
            """,
        unsafe_allow_html=True,
    )
  with kpi4:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-label">PEAK MONTH</div>
                <div class="kpi-value">{peak_month}</div>
                <div class="kpi-description">{peak_bookings:,} bookings</div>
            </div>
            """,
        unsafe_allow_html=True,
    )


# ============================================================
# SECTION 2: HOTEL DEMAND
# ============================================================

if show_all or nav_selection == "Hotel Demand":
  st.markdown(
      '<div class="section-title">Hotel Demand</div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="section-subtitle">Which hotel type is booked most often and'
      " how demand is distributed.</div>",
      unsafe_allow_html=True,
  )

  hotel_counts = filtered_df["hotel"].value_counts().reset_index()
  hotel_counts.columns = ["hotel", "bookings"]
  hotel_counts["share"] = (
      hotel_counts["bookings"] / hotel_counts["bookings"].sum() * 100
  )

  st.markdown(
      '<div class="chart-title">Hotel Type Booking Share</div>',
      unsafe_allow_html=True,
  )
  fig_share = px.pie(
      hotel_counts,
      names="hotel",
      values="bookings",
      hole=0.62,
      color="hotel",
      color_discrete_map={"City Hotel": "#17212B", "Resort Hotel": "#B89B5E"},
  )
  fig_share.update_traces(
      textposition="inside",
      textinfo="percent",
      hovertemplate=(
          "<b>%{label}</b><br>Bookings: %{value:,}<br>Share:"
          " %{percent}<extra></extra>"
      ),
  )
  fig_share.update_layout(
      showlegend=True, height=360, margin=dict(t=20, b=20, l=10, r=10)
  )
  fig_share = premium_chart(fig_share)
  st.plotly_chart(
      fig_share, use_container_width=True, key="hotel_share_chart_nav"
  )
  st.markdown(
      '<div class="chart-caption">City Hotel represents the larger share of'
      " bookings in the overall portfolio.</div>",
      unsafe_allow_html=True,
  )

  st.markdown(
      '<div class="chart-title">Booking Volume by Hotel Type</div>',
      unsafe_allow_html=True,
  )
  fig_hotel = px.bar(
      hotel_counts,
      x="hotel",
      y="bookings",
      text="bookings",
      color="hotel",
      color_discrete_map={"City Hotel": "#17212B", "Resort Hotel": "#B89B5E"},
      labels={"hotel": "Hotel Type", "bookings": "Number of Bookings"},
  )
  fig_hotel.update_traces(
      texttemplate="%{text:,}",
      textposition="outside",
      hovertemplate=(
          "<b>%{x}</b><br>Bookings: %{y:,}<br>Share:"
          " %{customdata:.2f}%<extra></extra>"
      ),
      customdata=hotel_counts["share"],
  )
  fig_hotel.update_layout(
      showlegend=False,
      xaxis_title="Hotel Type",
      yaxis_title="Number of Bookings",
      height=360,
      margin=dict(t=40, b=50, l=50, r=20),
  )
  fig_hotel = premium_chart(fig_hotel)
  st.plotly_chart(
      fig_hotel, use_container_width=True, key="hotel_booking_chart_nav"
  )
  st.markdown(
      '<div class="chart-caption">The chart compares the number of bookings'
      " received by City Hotel and Resort Hotel.</div>",
      unsafe_allow_html=True,
  )


# ============================================================
# SECTION 3: CANCELLATION RISK
# ============================================================

if show_all or nav_selection == "Cancellation Risk":
  st.markdown(
      '<div class="section-title">Cancellation Risk</div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="section-subtitle">Understanding how hotel type, stay duration'
      " and booking lead time are associated with cancellation behaviour.</div>",
      unsafe_allow_html=True,
  )

  cancellation_hotel = (
      filtered_df.groupby("hotel")["is_canceled"].mean().reset_index()
  )
  cancellation_hotel["cancellation_rate"] = (
      cancellation_hotel["is_canceled"] * 100
  )

  st.markdown(
      '<div class="chart-title">Cancellation Rate by Hotel Type</div>',
      unsafe_allow_html=True,
  )
  fig_cancel_hotel = px.bar(
      cancellation_hotel,
      x="hotel",
      y="cancellation_rate",
      text="cancellation_rate",
      color="hotel",
      color_discrete_map={"City Hotel": "#17212B", "Resort Hotel": "#B89B5E"},
      labels={
          "hotel": "Hotel Type",
          "cancellation_rate": "Cancellation Rate (%)",
      },
  )
  fig_cancel_hotel.update_traces(
      texttemplate="%{text:.1f}%",
      textposition="outside",
      hovertemplate="<b>%{x}</b><br>Cancellation Rate: %{y:.2f}%<extra></extra>",
  )
  fig_cancel_hotel.update_layout(
      showlegend=False,
      xaxis_title="Hotel Type",
      yaxis_title="Cancellation Rate (%)",
      height=380,
      margin=dict(t=40, b=50, l=50, r=20),
  )
  fig_cancel_hotel = premium_chart(fig_cancel_hotel)
  st.plotly_chart(
      fig_cancel_hotel,
      use_container_width=True,
      key="cancellation_hotel_chart_nav",
  )
  st.markdown(
      '<div class="chart-caption">City Hotel has a higher overall cancellation'
      " rate than Resort Hotel in the cleaned dataset.</div>",
      unsafe_allow_html=True,
  )

  stay_analysis = (
      filtered_df.groupby(["stay_duration_group", "hotel"], observed=True)[
          "is_canceled"
      ]
      .mean()
      .reset_index()
  )
  stay_analysis["cancellation_rate"] = stay_analysis["is_canceled"] * 100

  st.markdown(
      '<div class="chart-title">Stay Duration vs Cancellation</div>',
      unsafe_allow_html=True,
  )
  fig_stay = px.line(
      stay_analysis,
      x="stay_duration_group",
      y="cancellation_rate",
      color="hotel",
      markers=True,
      text="cancellation_rate",
      color_discrete_map={"City Hotel": "#17212B", "Resort Hotel": "#B89B5E"},
      labels={
          "stay_duration_group": "Stay Duration",
          "cancellation_rate": "Cancellation Rate (%)",
          "hotel": "Hotel Type",
      },
  )
  fig_stay.update_traces(
      texttemplate="%{text:.1f}%",
      textposition="top center",
      hovertemplate=(
          "<b>%{fullData.name}</b><br>Stay: %{x}<br>Cancellation Rate:"
          " %{y:.2f}%<extra></extra>"
      ),
  )
  fig_stay.update_layout(
      xaxis_title="Stay Duration",
      yaxis_title="Cancellation Rate (%)",
      height=410,
      hovermode="x unified",
  )
  fig_stay = premium_chart(fig_stay)
  st.plotly_chart(
      fig_stay, use_container_width=True, key="cancellation_stay_chart_nav"
  )
  st.markdown(
      '<div class="chart-caption">Cancellation risk generally rises for longer'
      " stays, with the pattern differing between hotel types.</div>",
      unsafe_allow_html=True,
  )

  lead_analysis = (
      filtered_df.groupby(["hotel", "lead_time_group"], observed=True)[
          "is_canceled"
      ]
      .mean()
      .reset_index()
  )
  lead_analysis["cancellation_rate"] = lead_analysis["is_canceled"] * 100

  st.markdown(
      '<div class="chart-title">Lead Time vs Cancellation</div>',
      unsafe_allow_html=True,
  )
  fig_lead = px.line(
      lead_analysis,
      x="lead_time_group",
      y="cancellation_rate",
      color="hotel",
      markers=True,
      text="cancellation_rate",
      color_discrete_map={"City Hotel": "#17212B", "Resort Hotel": "#B89B5E"},
      labels={
          "lead_time_group": "Booking Lead Time",
          "cancellation_rate": "Cancellation Rate (%)",
          "hotel": "Hotel Type",
      },
  )
  fig_lead.update_traces(
      texttemplate="%{text:.1f}%",
      textposition="top center",
      hovertemplate=(
          "<b>%{fullData.name}</b><br>Lead Time: %{x}<br>Cancellation Rate:"
          " %{y:.2f}%<extra></extra>"
      ),
  )
  fig_lead.update_layout(
      xaxis_title="Booking Lead Time",
      yaxis_title="Cancellation Rate (%)",
      height=410,
      hovermode="x unified",
  )
  fig_lead = premium_chart(fig_lead)
  st.plotly_chart(
      fig_lead, use_container_width=True, key="cancellation_lead_chart_nav"
  )
  st.markdown(
      '<div class="chart-caption">Cancellation rates generally increase as'
      " bookings are made further in advance, especially for City Hotel.</div>",
      unsafe_allow_html=True,
  )


# ============================================================
# SECTION 4: SEASONALITY & TRENDS
# ============================================================

if show_all or nav_selection == "Seasonality & Trends":
  st.markdown(
      '<div class="section-title">Seasonality & Booking Trends</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="section-subtitle">Monthly booking patterns reveal periods of'
      " high and low demand across the year.</div>",
      unsafe_allow_html=True,
  )

  monthly_bookings = (
      filtered_df.groupby("arrival_date_month")
      .size()
      .reindex(month_order, fill_value=0)
      .reset_index(name="bookings")
  )
  monthly_bookings["month_order"] = pd.Categorical(
      monthly_bookings["arrival_date_month"],
      categories=month_order,
      ordered=True,
  )
  monthly_bookings = monthly_bookings.sort_values("month_order")

  st.markdown(
      '<div class="chart-title">Monthly Booking Trend</div>',
      unsafe_allow_html=True,
  )
  fig_monthly = px.line(
      monthly_bookings,
      x="arrival_date_month",
      y="bookings",
      markers=True,
      text="bookings",
      labels={
          "arrival_date_month": "Arrival Month",
          "bookings": "Number of Bookings",
      },
  )
  fig_monthly.update_traces(
      texttemplate="%{text:,}",
      textposition="top center",
      line_width=3,
      hovertemplate="<b>%{x}</b><br>Bookings: %{y:,}<extra></extra>",
  )
  fig_monthly.update_layout(
      xaxis=dict(
          title="Arrival Month", categoryorder="array", categoryarray=month_order
      ),
      yaxis_title="Number of Bookings",
      height=420,
  )
  fig_monthly = premium_chart(fig_monthly)
  st.plotly_chart(
      fig_monthly, use_container_width=True, key="seasonality_overall_chart_nav"
  )
  st.markdown(
      '<div class="chart-caption">October records the highest booking volume,'
      " while March records the lowest in the overall cleaned dataset.</div>",
      unsafe_allow_html=True,
  )

  monthly_hotel = (
      filtered_df.groupby(["arrival_date_month", "hotel"])
      .size()
      .reset_index(name="bookings")
  )
  monthly_hotel["month_order"] = pd.Categorical(
      monthly_hotel["arrival_date_month"], categories=month_order, ordered=True
  )
  monthly_hotel = monthly_hotel.sort_values("month_order")

  st.markdown(
      '<div class="chart-title">City Hotel vs Resort Hotel — Monthly'
      " Pattern</div>",
      unsafe_allow_html=True,
  )
  fig_hotel_month = px.line(
      monthly_hotel,
      x="arrival_date_month",
      y="bookings",
      color="hotel",
      markers=True,
      color_discrete_map={"City Hotel": "#17212B", "Resort Hotel": "#B89B5E"},
      labels={
          "arrival_date_month": "Arrival Month",
          "bookings": "Number of Bookings",
          "hotel": "Hotel Type",
      },
  )
  fig_hotel_month.update_traces(
      hovertemplate=(
          "<b>%{fullData.name}</b><br>Month: %{x}<br>Bookings:"
          " %{y:,}<extra></extra>"
      )
  )
  fig_hotel_month.update_layout(
      xaxis=dict(
          title="Arrival Month", categoryorder="array", categoryarray=month_order
      ),
      yaxis_title="Number of Bookings",
      height=420,
  )
  fig_hotel_month = premium_chart(fig_hotel_month)
  st.plotly_chart(
      fig_hotel_month, use_container_width=True, key="seasonality_hotel_chart_nav"
  )
  st.markdown(
      '<div class="chart-caption">The monthly pattern shows how City Hotel and'
      " Resort Hotel demand changes across the year.</div>",
      unsafe_allow_html=True,
  )


# ============================================================
# SECTION 5: INSIGHTS & RECOMMENDATIONS
# ============================================================

if show_all or nav_selection == "Insights & Recommendations":
  st.markdown(
      '<div class="section-title">Key Business Insights</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="section-subtitle">Key findings derived directly from the'
      " booking and cancellation analysis.</div>",
      unsafe_allow_html=True,
  )

  hotel_booking_counts = filtered_df["hotel"].value_counts()
  city_bookings = hotel_booking_counts.get("City Hotel", 0)
  total_filtered = len(filtered_df)
  city_percentage = (
      (city_bookings / total_filtered * 100) if total_filtered > 0 else 0
  )
  cancel_rate_values = (
      filtered_df.groupby("hotel")["is_canceled"].mean() * 100
  )
  city_cancel_rate = cancel_rate_values.get("City Hotel", 0)
  resort_cancel_rate = cancel_rate_values.get("Resort Hotel", 0)
  monthly_insight = filtered_df.groupby("arrival_date_month").size()
  if len(monthly_insight) > 0:
    busiest_month = monthly_insight.idxmax()
    busiest_bookings = int(monthly_insight.max())
    quietest_month = monthly_insight.idxmin()
    quietest_bookings = int(monthly_insight.min())
  else:
    busiest_month = "N/A"
    busiest_bookings = 0
    quietest_month = "N/A"
    quietest_bookings = 0

  col1, col2 = st.columns(2)
  with col1:
    st.markdown(
        f"""<div class="insight-card">
<div class="insight-title">🏨 City Hotel Leads Overall Demand</div>
<div class="insight-text">
City Hotel accounts for approximately <strong>{city_percentage:.2f}%</strong> of bookings in the selected view. This makes it the dominant hotel type in the portfolio.
</div>
</div>""",
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""<div class="insight-card">
<div class="insight-title">⚠️ City Hotel Shows Higher Cancellation Risk</div>
<div class="insight-text">
The cancellation rate is approximately <strong>{city_cancel_rate:.2f}%</strong> for City Hotel and <strong>{resort_cancel_rate:.2f}%</strong> for Resort Hotel.
</div>
</div>""",
        unsafe_allow_html=True,
    )

  col3, col4 = st.columns(2)
  with col3:
    st.markdown(
        f"""<div class="insight-card">
<div class="insight-title">📅 {busiest_month} is the Peak Booking Month</div>
<div class="insight-text">
{busiest_month} records the highest booking volume with <strong>{busiest_bookings:,}</strong> bookings in the selected view.
</div>
</div>""",
        unsafe_allow_html=True,
    )
  with col4:
    st.markdown(
        f"""<div class="insight-card">
<div class="insight-title">🌿 {quietest_month} is the Quietest Month</div>
<div class="insight-text">
{quietest_month} has the lowest booking volume, with <strong>{quietest_bookings:,}</strong> bookings in the selected view.
</div>
</div>""",
        unsafe_allow_html=True,
    )

  st.markdown(
      '<div class="section-title">Business Interpretation</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="section-subtitle">What the observed patterns can mean for'
      " hotel management.</div>",
      unsafe_allow_html=True,
  )

  st.markdown(
      """<div class="recommendation-card">
<div class="recommendation-title">📊 Seasonal Demand Planning</div>
<div class="recommendation-text">
Hotels can use the monthly demand pattern to prepare staffing, room inventory, pricing and promotional campaigns ahead of high-demand periods. Lower-demand months can be targeted with promotional packages and demand-building campaigns.
</div>
</div>""",
      unsafe_allow_html=True,
  )

  st.markdown(
      """<div class="recommendation-card">
<div class="recommendation-title">🏨 Hotel Type Strategy</div>
<div class="recommendation-text">
Since City Hotel contributes the larger share of bookings, management can protect this strong demand while using targeted campaigns and differentiated packages to strengthen Resort Hotel demand during weaker periods.
</div>
</div>""",
      unsafe_allow_html=True,
  )

  st.markdown(
      """<div class="recommendation-card">
<div class="recommendation-title">🛎️ Longer-Stay Cancellation Management</div>
<div class="recommendation-text">
Longer stays show higher cancellation risk in the analysis. Hotels could consider stronger cancellation terms, deposits, flexible rebooking options or minimum-stay policies for higher-risk long-duration bookings.
</div>
</div>""",
      unsafe_allow_html=True,
  )

  st.markdown(
      """<div class="recommendation-card">
<div class="recommendation-title">📩 Managing Far-Ahead Bookings</div>
<div class="recommendation-text">
Bookings made far in advance show higher cancellation risk. Reminder messages, confirmation requests, deposits and flexible rescheduling options can help reduce avoidable cancellations.
</div>
</div>""",
      unsafe_allow_html=True,
  )

  st.markdown(
      '<div class="section-title">Recommended Priority Action</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      """<div class="recommendation-card">
<div class="recommendation-title">⭐ Focus on reducing cancellations among high-risk bookings</div>
<div class="recommendation-text">
The strongest priority is to introduce proactive cancellation management for bookings with longer lead times and longer stays. The analysis shows that cancellation risk increases across these higher-risk booking segments. Targeted reminders, deposits and flexible rescheduling can help protect expected room revenue while maintaining customer flexibility.
</div>
</div>""",
      unsafe_allow_html=True,
  )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div class="footer">
Hotel Business Intelligence Dashboard
<br>
Booking Demand • Cancellation Risk • Seasonal Analysis
</div>""",
    unsafe_allow_html=True,
)
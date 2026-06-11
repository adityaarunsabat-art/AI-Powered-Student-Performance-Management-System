import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Student Performance Dashboard")

# Load Data
df = pd.read_csv("students.csv")

# Calculate Total and Average
subjects = ["Math", "Science", "English", "Computer"]

df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1)

# Sidebar
st.sidebar.header("Filters")

student = st.sidebar.selectbox(
    "Select Student",
    ["All"] + list(df["Name"])
)

if student != "All":
    df = df[df["Name"] == student]

# KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Students", len(df))

with col2:
    st.metric("Highest Average", round(df["Average"].max(),2))

with col3:
    st.metric("Class Average", round(df["Average"].mean(),2))

st.divider()

# Data Table
st.subheader("Student Data")

st.dataframe(df)

# Subject Average
st.subheader("Subject Wise Average")

subject_avg = pd.DataFrame({
    "Subject": subjects,
    "Average Marks": [df[sub].mean() for sub in subjects]
})

fig1 = px.bar(
    subject_avg,
    x="Subject",
    y="Average Marks",
    title="Average Marks by Subject"
)

st.plotly_chart(fig1, use_container_width=True)

# Top Performers
st.subheader("Top Performers")

top_students = df.sort_values(
    by="Average",
    ascending=False
)

fig2 = px.bar(
    top_students,
    x="Name",
    y="Average",
    title="Top Students"
)

st.plotly_chart(fig2, use_container_width=True)

# Pie Chart
st.subheader("Pass / Fail Analysis")

df["Status"] = df["Average"].apply(
    lambda x: "Pass" if x >= 40 else "Fail"
)

status_count = df["Status"].value_counts()

fig3 = px.pie(
    values=status_count.values,
    names=status_count.index,
    title="Pass vs Fail"
)

st.plotly_chart(fig3, use_container_width=True)

# Student Performance Comparison
st.subheader("Student Comparison")

fig4 = px.line(
    df,
    x="Name",
    y=subjects,
    markers=True,
    title="Performance Comparison"
)

st.plotly_chart(fig4, use_container_width=True)

# Student Details
st.subheader("Student Ranking")

rank_df = df.sort_values(
    by="Average",
    ascending=False
)[["Name", "Total", "Average"]]

rank_df.index = range(1, len(rank_df)+1)

st.dataframe(rank_df)
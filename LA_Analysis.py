import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Approval Data Analysis", layout="wide")

st.title("📊 Loan Approval Data Analysis using Streamlit + Plotly")

# Upload CSV
uploaded_file = st.file_uploader("Upload your Loan Prediction CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Preprocessing
    df = df.dropna()
    df['Dependents'] = df['Dependents'].replace("3+", "3").astype('float64')
    df['CoapplicantIncome'] = df['CoapplicantIncome'].astype('int64')
    df['Loan_Status'] = df['Loan_Status'].replace({'Y': 'Yes', 'N': 'No'})
    df['TotalIncome'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['IsHighIncome'] = df['TotalIncome'] > 5000
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].astype('int64')
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].replace({
        360: 36, 120: 12, 180: 18, 60: 6, 300: 30, 480: 48, 240: 24
    })

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.subheader("📉 Descriptive Statistics")
    st.write(df.describe())

    st.subheader("🧼 Missing Values (after dropping NAs)")
    st.write(df.isnull().sum())

    st.subheader("📌 Loan Status Distribution")
    loan_status_fig = px.pie(df, names='Loan_Status', title="Loan Approval Distribution", hole=0.3)
    st.plotly_chart(loan_status_fig)

    st.subheader("👫 Gender vs Loan Approval")
    gender_status = pd.crosstab(df['Gender'], df['Loan_Status'])
    gender_fig = px.bar(gender_status, barmode='group', title="Loan Approval by Gender")
    st.plotly_chart(gender_fig)

    st.subheader("💍 Marital Status vs Loan Approval")
    marital_status = pd.crosstab(df['Married'], df['Loan_Status'])
    marital_fig = px.bar(marital_status, barmode='group', title="Loan Approval by Marital Status")
    st.plotly_chart(marital_fig)

    st.subheader("👶 Dependents vs Loan Approval")
    dep_fig = px.box(df, x='Loan_Status', y='Dependents', title="Dependents and Loan Status")
    st.plotly_chart(dep_fig)

    st.subheader("🎓 Education vs Loan Approval")
    edu_status = pd.crosstab(df['Education'], df['Loan_Status'])
    edu_fig = px.bar(edu_status, barmode='group', title="Loan Approval by Education")
    st.plotly_chart(edu_fig)

    st.subheader("💼 Self Employment vs Loan Approval")
    emp_status = df.groupby(['Self_Employed', 'Loan_Status']).size().unstack()
    emp_fig = px.bar(emp_status, barmode='group', title="Loan Approval by Self-Employment")
    st.plotly_chart(emp_fig)

    st.subheader("💰 Applicant Income vs Loan Status")
    app_inc_fig = px.box(df, x='Loan_Status', y='ApplicantIncome', title="Applicant Income and Loan Status")
    st.plotly_chart(app_inc_fig)

    st.subheader("👫 Co-applicant Income Distribution")
    co_app_fig = px.histogram(df, x='CoapplicantIncome', color='Loan_Status', nbins=50, title="Co-applicant Income and Loan Status")
    st.plotly_chart(co_app_fig)

    st.subheader("📈 Total Income vs Loan Amount")
    income_vs_loan = px.scatter(df, x='TotalIncome', y='LoanAmount', color='Loan_Status', trendline="ols", title="Total Income vs Loan Amount")
    st.plotly_chart(income_vs_loan)

    st.subheader("🏠 Loan Amount vs Gender, Marital Status, and Education")
    col1, col2, col3 = st.columns(3)

    with col1:
        fig1 = px.bar(df, x='Gender', y='LoanAmount', color='Loan_Status', title="Gender vs Loan Amount")
        st.plotly_chart(fig1)

    with col2:
        fig2 = px.strip(df, x='Married', y='LoanAmount', color='Loan_Status', title="Married vs Loan Amount")
        st.plotly_chart(fig2)

    with col3:
        fig3 = px.violin(df, x='Education', y='LoanAmount', color='Loan_Status', title="Education vs Loan Amount", box=True)
        st.plotly_chart(fig3)

    st.subheader("📊 Credit History vs Loan Approval")
    credit_status = pd.crosstab(df['Credit_History'], df['Loan_Status'])
    credit_fig = px.bar(credit_status, barmode='group', title="Loan Approval by Credit History")
    st.plotly_chart(credit_fig)

    st.subheader("⏳ Loan Term vs Loan Approval")
    term_status = pd.crosstab(df['Loan_Amount_Term'], df['Loan_Status'])
    term_fig = px.bar(term_status, barmode='group', title="Loan Approval by Loan Term")
    st.plotly_chart(term_fig)

    st.subheader("🏡 Property Area vs Loan Approval")
    property_status = pd.crosstab(df['Property_Area'], df['Loan_Status'])
    property_fig = px.bar(property_status, barmode='group', title="Loan Approval by Property Area")
    st.plotly_chart(property_fig)

    st.subheader("📍 Property Area vs Loan Amount")
    area_fig = px.line(df, x='Property_Area', y='LoanAmount', color='Loan_Status', title="Property Area and Loan Amount")
    st.plotly_chart(area_fig)

else:
    st.warning("Please upload a CSV file to begin the analysis.")

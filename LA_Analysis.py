import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('../DataSets/LP_Train.csv')

# Clean and preprocess
df = df.dropna()
df['Dependents'] = df['Dependents'].replace("3+", "3").astype(float)
df['CoapplicantIncome'] = df['CoapplicantIncome'].astype('int64')
df['Loan_Status'] = df['Loan_Status'].replace({'N': 'No', 'Y': 'Yes'})
df['TotalIncome'] = df['ApplicantIncome'] + df['CoapplicantIncome']
df['IsHighIncome'] = df['TotalIncome'] > 5000

# Update Loan Term
term_map = {360: 36, 120: 12, 180: 18, 60: 6, 300: 30, 480: 48, 240: 24}
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].astype('int64').replace(term_map)

# App Layout
st.set_page_config(page_title='Loan Approval Analysis', layout='wide')
st.title("📊 Loan Approval Exploratory Analysis")
st.markdown("Interactive insights based on loan application data.")

# Sidebar filters
st.sidebar.header("🔎 Filter Options")
gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())
married = st.sidebar.multiselect("Select Marital Status", df['Married'].unique(), default=df['Married'].unique())
education = st.sidebar.multiselect("Select Education", df['Education'].unique(), default=df['Education'].unique())
property_area = st.sidebar.multiselect("Select Property Area", df['Property_Area'].unique(), default=df['Property_Area'].unique())

# Filter data
filtered_df = df[
    df['Gender'].isin(gender) &
    df['Married'].isin(married) &
    df['Education'].isin(education) &
    df['Property_Area'].isin(property_area)
]

st.subheader("✅ Loan Status Distribution")
fig1 = px.histogram(filtered_df, x='Loan_Status', color='Loan_Status', barmode='group')
st.plotly_chart(fig1, use_container_width=True)

# Gender and Loan Status
st.subheader("👥 Gender vs Loan Status")
fig2 = px.histogram(filtered_df, x='Gender', color='Loan_Status', barmode='group')
st.plotly_chart(fig2, use_container_width=True)

# Marital Status
st.subheader("💍 Marital Status vs Loan Approval")
fig3 = px.histogram(filtered_df, x='Married', color='Loan_Status', barmode='group')
st.plotly_chart(fig3, use_container_width=True)

# Education and Approval
st.subheader("🎓 Education vs Loan Approval")
fig4 = px.histogram(filtered_df, x='Education', color='Loan_Status', barmode='group')
st.plotly_chart(fig4, use_container_width=True)

# Self-Employment
st.subheader("💼 Self Employment vs Loan Status")
fig5 = px.histogram(filtered_df, x='Self_Employed', color='Loan_Status', barmode='group')
st.plotly_chart(fig5, use_container_width=True)

# Applicant Income Boxplot
st.subheader("📈 Applicant Income Distribution by Loan Status")
fig6 = px.box(filtered_df, x='Loan_Status', y='ApplicantIncome', color='Loan_Status')
st.plotly_chart(fig6, use_container_width=True)

# Loan Amount vs Total Income
st.subheader("💰 Total Income vs Loan Amount")
fig7 = px.scatter(filtered_df, x='TotalIncome', y='LoanAmount', color='Loan_Status', size='LoanAmount')
st.plotly_chart(fig7, use_container_width=True)

# Property Area vs Loan Status
st.subheader("🏘️ Property Area vs Loan Status")
fig8 = px.histogram(filtered_df, x='Property_Area', color='Loan_Status', barmode='group')
st.plotly_chart(fig8, use_container_width=True)

# Loan Amount Term Analysis
st.subheader("📆 Loan Amount Term vs Loan Status")
fig9 = px.histogram(filtered_df, x='Loan_Amount_Term', color='Loan_Status', barmode='group')
st.plotly_chart(fig9, use_container_width=True)

# Credit History Impact
st.subheader("🧾 Credit History vs Loan Status")
fig10 = px.histogram(filtered_df, x='Credit_History', color='Loan_Status', barmode='group')
st.plotly_chart(fig10, use_container_width=True)

# Heatmap for Correlation
st.subheader("🔗 Correlation Heatmap")
numeric_df = filtered_df[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'TotalIncome']]
corr = numeric_df.corr()
fig11 = px.imshow(corr, text_auto=True, color_continuous_scale='Blues')
st.plotly_chart(fig11, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Plotly")


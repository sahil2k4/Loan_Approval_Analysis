import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
st.title("Loan Approval Analysis Dashboard")

uploaded_file = st.file_uploader("Upload Loan CSV File", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Preprocessing
    df = df.dropna()
    df['Dependents'] = df['Dependents'].replace("3+", "3").astype('float64')
    df['CoapplicantIncome'] = df['CoapplicantIncome'].astype('int64')
    df['Loan_Status'] = df['Loan_Status'].replace('N', 'No').replace('Y', 'Yes')
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].astype('int64')

    # Consolidate Loan Term values
    df['Loan_Amount_Term'] = df['Loan_Amount_Term'].replace({
        360: 36, 120: 12, 180: 18, 60: 6, 300: 30, 480: 48, 240: 24
    })

    # Create TotalIncome
    df['TotalIncome'] = df['ApplicantIncome'] + df['CoapplicantIncome']
    df['IsHighIncome'] = df['TotalIncome'] > 5000

    # Sidebar filters
    st.sidebar.header("Filter Options")
    gender_filter = st.sidebar.selectbox("Select Gender", ['All'] + list(df['Gender'].unique()))
    married_filter = st.sidebar.selectbox("Select Marital Status", ['All'] + list(df['Married'].unique()))
    edu_filter = st.sidebar.selectbox("Select Education", ['All'] + list(df['Education'].unique()))
    prop_filter = st.sidebar.selectbox("Select Property Area", ['All'] + list(df['Property_Area'].unique()))

    filtered_df = df.copy()
    if gender_filter != 'All':
        filtered_df = filtered_df[filtered_df['Gender'] == gender_filter]
    if married_filter != 'All':
        filtered_df = filtered_df[filtered_df['Married'] == married_filter]
    if edu_filter != 'All':
        filtered_df = filtered_df[filtered_df['Education'] == edu_filter]
    if prop_filter != 'All':
        filtered_df = filtered_df[filtered_df['Property_Area'] == prop_filter]

    st.subheader("Loan Status Count")
    st.plotly_chart(px.histogram(filtered_df, x='Loan_Status', color='Loan_Status'))

    st.subheader("Loan Approval by Gender")
    st.plotly_chart(px.histogram(filtered_df, x='Gender', color='Loan_Status', barmode='group'))

    st.subheader("Loan Approval by Marital Status")
    st.plotly_chart(px.histogram(filtered_df, x='Married', color='Loan_Status', barmode='group'))

    st.subheader("Loan Approval by Education")
    st.plotly_chart(px.histogram(filtered_df, x='Education', color='Loan_Status', barmode='group'))

    st.subheader("Loan Approval by Self Employment")
    st.plotly_chart(px.histogram(filtered_df, x='Self_Employed', color='Loan_Status', barmode='group'))

    st.subheader("Applicant Income vs Loan Status")
    st.plotly_chart(px.box(filtered_df, x='Loan_Status', y='ApplicantIncome', color='Loan_Status'))

    st.subheader("Total Income vs Loan Amount")
    scatter_fig = px.scatter(filtered_df, x='TotalIncome', y='LoanAmount', color='Loan_Status',
                             title='Total Income vs Loan Amount')
    st.plotly_chart(scatter_fig)

    st.subheader("Loan Amount by Gender, Marital Status, and Education")
    tab1, tab2, tab3 = st.tabs(["Gender", "Married", "Education"])
    with tab1:
        st.plotly_chart(px.box(filtered_df, x='Gender', y='LoanAmount', color='Gender'))
    with tab2:
        st.plotly_chart(px.strip(filtered_df, x='Married', y='LoanAmount', color='Loan_Status'))
    with tab3:
        st.plotly_chart(px.violin(filtered_df, x='Education', y='LoanAmount', color='Loan_Status', box=True))

    st.subheader("Loan Term vs Loan Status")
    st.plotly_chart(px.strip(filtered_df, x='Loan_Status', y='Loan_Amount_Term', color='Loan_Status'))

    st.subheader("Credit History vs Loan Status")
    st.plotly_chart(px.histogram(filtered_df, x='Credit_History', color='Loan_Status', barmode='group'))

    st.subheader("Property Area vs Loan Status")
    st.plotly_chart(px.histogram(filtered_df, x='Property_Area', color='Loan_Status', barmode='group'))

    st.subheader("Loan Amount by Property Area")
    st.plotly_chart(px.box(filtered_df, x='Property_Area', y='LoanAmount', color='Loan_Status'))

else:
    st.warning("📁 Please upload the dataset CSV file to start the analysis.")

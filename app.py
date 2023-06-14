import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

logo = Image.open('favicon.ico')
icon = ":bar_chart:"

st.set_page_config(page_title='Alumni Dashboard',
                   page_icon=logo,
                   layout='wide')

st.header(f'{icon} HCPSMSHS Alumni Dashboard')
st.markdown('---')

data = pd.read_csv('alumni_records_csv.csv')

def convert_value_counts_to_df(df, column_name):
    value_counts_df = pd.DataFrame(df[column_name]\
                                .value_counts(dropna=True, sort=True))\
                                .reset_index()
    value_counts_df.columns = [column_name, 'Count'] 
    return value_counts_df

col1, col2, col3 = st.columns(3)
selected_years = col1.multiselect('Select years', data['Batch'].unique())
selected_courses = col2.multiselect('Select courses', data['Course'].unique())
selected_universities = col3.multiselect('Select universities', data['University'].unique())

st.subheader("Number of Alumni by Course")

filtered_data = data[(data['Batch'].isin(selected_years)) & (data['Course'].isin(selected_courses))]

grouped_data = filtered_data.groupby(['Course', 'Batch']).size().reset_index(name='Count')

course_totals = filtered_data.groupby('Course').size().reset_index(name='Count_total')
grouped_data = pd.merge(grouped_data, course_totals, on='Course')

grouped_data['Percentage'] = grouped_data['Count'] / len(data['Course']) * 100

fig = px.bar(
    grouped_data,
    x='Course',
    y='Count',
    color='Batch',
    barmode='group',
    labels={'Count': 'Count', 'Percentage': 'Percentage'},
    hover_data={'Percentage': ':.2f%'},
    title = 'Comparison Graph for Courses taken by our alumni'
)

if len(selected_courses) < 3:
    st.caption('Note: Select atleast one year and two courses to show the graph.')
else:
    st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

# University bar graph area
st.subheader("Number of Alumni by University")

u_filtered_data = data[(data['Batch'].isin(selected_years)) & (data['University'].isin(selected_universities))]

u_grouped_data = u_filtered_data.groupby('University').size().reset_index(name='Count')

university_totals = len(data['University'])
u_grouped_data['Percentage'] = u_grouped_data['Count'] / university_totals * 100

u_fig = px.bar(u_grouped_data, x='University', y='Count', text='Percentage')

u_fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

if len(selected_universities) < 3:
    st.caption('Note: Select atleast one year and two universities to show the graph.')
else:
    st.plotly_chart(u_fig, use_container_width=True)






st.markdown('---')
c1, c2 = st.columns(2)



with c1:
    st.subheader('What are the most common courses that alumni are taking in?')
    courses_df = convert_value_counts_to_df(data, 'Course')
    courses_fig = px.bar(courses_df.head(5), x='Count',y='Course', title='Top 5 Selected Courses', color_discrete_sequence =['#FF4B4B']*2, orientation='h' )
    st.plotly_chart(courses_fig)

with c2:
    st.subheader('What are the most common universities that alumni are going in?')
    univ_df = convert_value_counts_to_df(data, 'University')
    univ_fig = px.bar(univ_df.head(3), x='University', y='Count', title='Top 3 Selected University', color_discrete_sequence =['#FF4B4B']*2 )
    st.plotly_chart(univ_fig)

st.markdown('---')




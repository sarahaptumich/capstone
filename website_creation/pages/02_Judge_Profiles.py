import streamlit as st
import pandas as pd
from tabulate import tabulate

st.sidebar.image("website_creation/Logo_GPT.png", use_column_width=True)
st.sidebar.write('Open Breaking is a project to collect competitive breaking data and produce findings through analysis that can be incorporated into the further development of competitive breaking.')

st.title('Judge Profiles')
st.divider()

df = pd.read_csv('website_creation/judge_df.csv')
unique_names = df['Judge'].unique()
names_list = list(unique_names)

judges = names_list
option = st.selectbox('Which judge would you like to view?',
                      judges)
st.write('You selected:', option)
st.divider()

judge_df = df[df['Judge']==option]

table = judge_df.iloc[:,5:-1].describe()

st.dataframe(table)

st.write("This analysis is performed on all events included in the dataset. These events go back to 2019.")
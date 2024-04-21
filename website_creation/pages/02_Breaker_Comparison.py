import streamlit as st
import pandas as pd
import numpy as np
import random
import joblib
import re
from skelo.model.elo import EloEstimator

st.set_page_config(
  layout="wide"                 
)

st.title('Breaker Match Simulations')
st.divider()

st.sidebar.image("./website_creation/Logo_GPT.png", use_column_width=True)
st.sidebar.write('Open Breaking is a project to collect competitive breaking data and produce findings through analysis that can be incorporated into the further development of competitive breaking.')

options = ('Girls', 'Boys', 'Other')
option = st.selectbox('Which group would you like to view?',
                      options)

match = ('Random Match', 'Choose Competitors')
matches = st.selectbox('Which kind of match would you like to simulate?',
                      match)

st.divider()

def fit_model(X):
    #adapt from skelo docss example Tennis Ranking https://pypi.org/project/skelo/
    X_subset = X[['Date', 'p1', 'p2', 'label']]
    model = EloEstimator(
        key1_field="p1",
        key2_field="p2",
        timestamp_field="Date",
        initial_time=min(X['Date'])
    )
    fitted_model = model.fit(X_subset, X_subset["label"])

    return fitted_model


#Splitting up by type of df
if 'Girls' in option:
    df = pd.read_csv('./website_creation/complete_girl_df.csv')
elif 'Boys' in option:
    df = pd.read_csv('./website_creation/complete_boy_df.csv')
elif 'Other' in option:
    df = pd.read_csv('./website_creation/complete_other_df.csv')


#Create list with breakers
unique_p1 = df['p1'].unique()
unique_p2 = df['p2'].unique()
set_p1 = set(unique_p1)
set_p2 = set(unique_p2)
combined_unique = list(set_p1.union(set_p2))

names = random.sample(combined_unique, 2)

if 'Random Match' in matches:
    #randomly select 2 breakers for a match
    names = random.sample(combined_unique, 2)
    st.write(f"The randomly chosen breakers are {names[0]} and {names[1]}")
  
elif 'Choose Competitors' in matches:
    
    names = st.multiselect(
    'Which two breakers would you like to simulate a match between?',
    combined_unique,
    )
    st.write(f"Please only select two breakers for the model to work. The model will show an index error until two breakers are chosen.")

st.divider()
    
data = {
    'Date': ['2024-04-17'],
    'p1': [names[0]],
    'p2': [names[1]]
}
model=fit_model(df)
predicting_df = pd.DataFrame(data)
prediction=model.predict_proba(predicting_df)
winner_column = prediction.idxmax(axis=1)[0]
if winner_column == 'pr1':
    winner_name = names[0]
elif winner_column == 'pr2':
    winner_name = names[1]
winner_probability=prediction[winner_column][0]

st.write(f"The winner would be {winner_name} with a probability of {round(winner_probability, 2)}!")

st.divider()

st.write("If you would like to simulate another match, please select a new group (you can also reselct the same group).")
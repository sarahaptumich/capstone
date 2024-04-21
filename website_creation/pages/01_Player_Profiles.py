
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

st.set_page_config(
  layout="wide"                 
)

st.title('Breaker Rankings')
st.divider()

st.sidebar.image("./Logo_GPT.png", use_column_width=True)
st.sidebar.write('Open Breaking is a project to collect competitive breaking data and produce findings through analysis that can be incorporated into the further development of competitive breaking.')

options = ('Girls', 'Boys', 'Other')
option = st.selectbox('Which group would you like to view?',
                      options)
st.write('You selected:', option)

numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
number_option = st.selectbox('How many of the top breakers would you like to view?',
                      numbers)
st.write('You selected:', number_option)

st.divider()

if 'Girls' in option:
    elo_df = pd.read_csv('.\girl_elo.csv')
    glicko_df = pd.read_csv('.\girl_glicko.csv')   
    elo_title = 'Girls Elo Ranking'
    glicko_title = 'Girls Glicko Ranking'
elif 'Boys' in option:
    elo_df = pd.read_csv('.\df_boy_elo.csv')
    glicko_df = pd.read_csv('.\df_boy_glicko.csv')
    elo_title = 'Boys Elo Ranking'
    glicko_title = 'Boys Glicko Ranking'
elif 'Other' in option:
    elo_df = pd.read_csv('.\other_elo.csv')
    glicko_df = pd.read_csv('.\other_glicko.csv')
    elo_title = 'Other Elo Ranking'
    glicko_title = 'Other Glicko Ranking'


elo_current = elo_df[(elo_df['valid_to'].isnull())].sort_values(by='rating', ascending=False)
elo_top10 = elo_current[(elo_df['valid_from'] >= '2023-01-01')].nlargest(10, 'rating')
glicko_current = glicko_df[(glicko_df['valid_to'].isnull())].sort_values(by='ranking', ascending=False)
glicko_top10 = glicko_current[(glicko_df['valid_from'] >= '2023-01-01')].nlargest(10, 'ranking')

elo_chart = elo_df[elo_df['key'].isin(elo_top10['key'].to_list())]
glicko_chart = glicko_df[glicko_df['key'].isin(glicko_top10['key'].to_list())]

def plot_top_ratings(ratings_frame, number_option, title):
    ts_est = ratings_frame.pivot_table(index='valid_from', columns='key', values='rating').ffill()
    idx = ts_est.iloc[-1].sort_values().index[-number_option:]
    
    # Make traces for Plotly
    traces = []
    for player in idx:
        traces.append(go.Scatter(x=ts_est.index, y=ts_est[player], mode='lines', name=player))
    
    return traces, f"Top {number_option} Ratings Over Time - {title}"

def plot_top_ratings_glicko(ratings_frame, number_option, title):
    ts_est = ratings_frame.pivot_table(index='valid_from', columns='key', values='ranking').ffill()
    idx = ts_est.iloc[-1].sort_values().index[-number_option:]
    
    # Make traces for Plotly
    traces = []
    for player in idx:
        traces.append(go.Scatter(x=ts_est.index, y=ts_est[player], mode='lines', name=player))
    
    return traces, f"Top {number_option} Rankings Over Time - {title}"

# Generate a list of all unique player keys from both datasets
unique_keys = set(elo_chart['key']).union(set(glicko_chart['key']))


# Define a color map for player keys
color_palette = px.colors.qualitative.Plotly
color_map = {player: color_palette[i % len(color_palette)] for i, player in enumerate(unique_keys)}


# Create subplots (you will specify the number of rows and columns)
fig = make_subplots(rows=1, cols=2, subplot_titles=('Elo Rankings', 'Glicko Rankings'))

#Create traces
elo_traces, elo_plot_title = plot_top_ratings(elo_chart, number_option, elo_title)
glicko_traces, glicko_plot_title = plot_top_ratings_glicko(glicko_chart, number_option, glicko_title)


# Add traces from the first function to the first subplot
for trace in elo_traces:
    fig.add_trace(trace.update(marker=dict(color=color_map[trace.name])), row=1, col=1)

# Add traces from the second function to the second subplot
for i, trace in enumerate(glicko_traces):
    if i == 0:
        fig.add_trace(trace.update(marker=dict(color=color_map.get(trace.name, px.colors.qualitative.Plotly[0])),showlegend=True), row=1, col=2)
    else:
        fig.add_trace(trace.update(marker=dict(color=color_map.get(trace.name, px.colors.qualitative.Plotly[0])),showlegend=False), row=1, col=2)


# Update layout
fig.update_layout(
    title_text=f"{option} Top {number_option} Rankings Over Time",
    #xaxis_title='Date',
    yaxis_title='Ranking',
    showlegend=True,
    height=800
)

fig.update_layout(legend=dict(orientation = 'h', yanchor="bottom", y=-0.2, xanchor="right", x=.6))


st.plotly_chart(fig, use_container_width=True)

st.divider()

st.write("Elo and Glicko rankings sometimes have different rankings so this visualization helps to show the difference in ranking over time, comparing the two ranking systems.")

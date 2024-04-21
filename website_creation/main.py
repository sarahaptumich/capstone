import streamlit as st
from st_pages import Page, show_pages, add_page_title
import pandas as pd
import numpy as np

#add_page_title()

show_pages(
    [
        Page("./main.py", "Home"),
        Page("./pages/01_Player_Profiles.py", "Breaker Rankings"),
        Page("./pages/02_Breaker_Comparison.py", "Breaker Match Simulations"),
        Page("./pages/02_Judge_Profiles.py", "Judge Profiles"),
        Page("./pages/03_Our_Data.py", "Our Data"),
    ]
)

st.title('Welcome to Settle it in the Cypher!')
st.divider()
st.subheader('Competitive Breaking Data Analysis')
st.write('Open Breaking is a project to collect competitive breaking data and produce findings through analysis that can be incorporated into the further development of competitive breaking.')
st.image('./Logo_GPT.png')
st.write(
"""
Current projects that the team has worked are: 
- Webscraping of competitive breaking match results 
- Comparison of the scoring systems (Threefold and Trivium)
- Comparison between two different ranking systems (Elo and Glicko)
- Breakdancing movement prediction from video analysis
- Seeing how normalizing judge's scores could affect results
- Identifying potential judging bias with statistical analysis
- Impact of judge distraction/fatigue when scoring


Potential future projects:
- Adding MitoSheet capability for this Streamlit app to display datasets (https://docs.trymito.io/mito-for-streamlit/create-a-mito-for-streamlit-app)
- Determing round times from video analysis
- Improvement to breaker ranking models to get a higher accuracy
- Develop a more user friendly, accurate scoring system
"""
)

st.sidebar.markdown("Who Are We?")
st.sidebar.image("./Logo_GPT.png", use_column_width=True)
st.sidebar.write('Open Breaking is a project to collect competitive breaking data and produce findings through analysis that can be incorporated into the further development of competitive breaking.')
st.divider()
st.write(
"""
Links to our GitHub repos and repos we used as reference can be found here: 
 - https://github.com/settleitinthecypher/settleitinthecypher.github.io
 - https://github.com/sarahaptumich/capstone
 - https://github.com/dmoltisanti/brace
"""
)
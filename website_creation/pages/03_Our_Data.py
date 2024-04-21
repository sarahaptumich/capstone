import streamlit as st
import pandas as pd
import numpy as np
#from mitosheet.streamlit.v1 import spreadsheet

st.set_page_config(
  page_title="Our Data",
  layout="wide"                 
)

st.title('Our Data')
st.divider()

st.sidebar.image(r'website_creation/Logo_GPT.png', use_column_width=True)
st.sidebar.write('Open Breaking is a project to collect competitive breaking data and produce findings through analysis that can be incorporated into the further development of competitive breaking.')


show_df = pd.read_csv(r'website_creation/data.csv',)
st.dataframe(show_df,
             column_config={
        "Video Link": st.column_config.LinkColumn("App URL"),
    },
    hide_index=True,)




#LOCAL MEMORY CANNNOT HANDLE BELOW CODE - BUT STILL POTENTIALLY INTERESTING TO ADD IN FUTURE

#Creating the DataFrame
#webscraping = pd.read_excel('.\Webscraping.xlsx', sheet_name=None)
#st.dataframe(webscraping)

#Using Mito to display the DataFrame as a spreadsheet with editable features
#final_dfs, code = spreadsheet(dataframe)
#st.write(final_dfs)
#Display python code that correpsonds to the script
#st.code(code)
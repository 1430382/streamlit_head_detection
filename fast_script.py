import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import streamlit as st

###
st.title("002 - data from head_detection using Fast API and streamlit")
##
#fetch from fast api, format data:
#_data__
#_dirty
#__rel__

DATE_COLUMN = 'date_complete'
DATA_URL = ('http://192.168.1.71:8000/')

##@st.cache
def load_data():
		fetch = pd.read_json(DATA_URL)
		data_dict = pd.DataFrame.from_dict(fetch)
		list_data = []
		for x in data_dict['__data__']:
			list_data.append(x)
		data = pd.DataFrame(list_data)
		lowercase = lambda x: str(x).lower()
		data.rename(lowercase, axis='columns', inplace=True)
		data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
		return data

#data_load_state = st.text('Loading data...')
data = load_data()
#data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
st.subheader('Filters by Hours')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
#st.map(filtered_data)
## Line chart of directions
data.replace({'direction':{'1':"Enter", '2':"Leave"}}, inplace = True)
arr = data['direction']
fig, ax = plt.subplots()
ax.set_xlabel('1= enter, 2 = leave')
ax.hist(arr, bins=20)
st.pyplot(fig)

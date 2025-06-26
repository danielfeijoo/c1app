import streamlit as st
import pandas as pd

st.logo("C:\\Users\\dfeijoo\\OneDrive - ConvergeOne\\Documents\\C1-logo-white.png")

st.title("Analyze District Data")

if 'dataframe' not in st.session_state:
    st.write("No data available. Please go to the 'Get Data from NCES' page to download data of any year.")
else:
    df = st.session_state['dataframe']
    st.dataframe(df)

    available_states = sorted(df['State'].unique())
    state_options = ["All States"] + available_states
    selected_states = st.multiselect(
        "Select State(s)", 
        options=state_options, 
        default=["All States"]
    )
    if "All States" in selected_states:
        filtered_states = available_states
    else:
        filtered_states = selected_states


    district_type_counts = df['District Type'].value_counts().index.tolist()
    district_to_select = ['All District Types'] + district_type_counts

    types_selected = st.multiselect(
        "Select District Type(s)", 
        options=district_to_select, 
        default= 'All District Types'
    )

    if "All District Types" in types_selected:
        filtered_types = df['District Type'].unique().tolist()
    else:
        filtered_types = types_selected
                
    threshold = st.number_input("Enter Minimum Enrollment", min_value=0, value=10000,step=1000)
    df_filtered = df[
        (df["State"].isin(filtered_states)) &
        (df["District Type"].isin(filtered_types)) &			
        (df['Enrollment'] > threshold)
    ]
    st.write(f"Showing {len(df_filtered)} districts with enrollment greater than {threshold} in selected states.")
    st.dataframe(df_filtered)

    if st.checkbox("Total districts and Type in each State"):
        total_districts = df_filtered.groupby('State').size().reset_index(name='Total Districts')
        type_counts = (
            df_filtered.groupby(['State', 'District Type'])
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )
        summary = pd.merge(total_districts, type_counts, on='State')
        st.dataframe(summary)
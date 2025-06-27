import streamlit as st
import pandas as pd


if 'loco_path' in st.session_state:
    st.logo(str(st.session_state['logo_path']))

st.logo(str(st.session_state['logo_path']))

st.title("CRM Analysis")

st.header("District Data:")
if 'dataframe' not in st.session_state:
    st.write("No data available. Please go to the 'Get Data from NCES' page to download data of any year.")
else:
    df = st.session_state['dataframe']
    df['phone']=df['phone'].astype(str)
    st.dataframe(df)

st.header("CRM Data:")

@st.cache_data
def load_crm_data():
    crm = pd.read_excel(st.session_state['data_path'])
    crm['assigned']=True
    crm.columns = ['name', 'ID', 'phone', 'employee_id', 'owner', 'manager', 'sales_id', 'create_on', 'region', 'BU', 'territory', 'last_activity_date', 'last_activity_type', 'status', 'employees', 'industry', 'assigned']
    crm['name'] = crm['name'].str.lower()
    crm['phone'] = crm['phone'].str.replace(r'\D','', regex = True)
    ln = ['Kyle Wewe', 'Greg Miles', 'Ron Gill', 'Shane Harper', "Donald O'Brien", 'Seth Lutz']
    myfilter = crm.owner.isin(ln) | crm.manager.isin(ln)
    crm.loc[myfilter, 'assigned'] = False
    return crm

    
crm_data = load_crm_data()
st.dataframe(crm_data)


st.header("Categorized Accounts:")

def categorize_accounts_to_df():
    if 'dataframe' not in st.session_state:
        st.write("No data available. Please go to the 'Get Data from NCES' page to download data of any year.")
    else:
        new_accounts = st.session_state['dataframe'].copy()
    
    
        merged_data = pd.merge(
            new_accounts, crm_data, on = 'phone', how = 'left',
            indicator=True
        )

    merged_data['Category'] = merged_data['_merge'].apply(
        lambda x: 'Present in CRM' if x == 'both' else 'Not present in CRM'
    )

    return merged_data




CA = categorize_accounts_to_df()
category_filter = st.selectbox("Filter by Category", ["All", "Present in CRM", "Not present in CRM"])

if category_filter != "All":
    CA = CA[CA["Category"] == category_filter]

category_counts = CA['Category'].value_counts()
st.write("Category Counts:", category_counts)

st.header('Filters')

states = sorted(CA['State'].dropna().unique())
selected_states = st.multiselect("Slected States",options = ["All"]+states,default= ["All"])

if "All" not in selected_states:
    CA = CA[CA["State"].isin(selected_states)]

assignment_filter = st.selectbox("Assignment status",["All","Assigned","Unassigned"])
if assignment_filter == "Assigned":
    CA = CA[CA['assigned']==True]
elif assignment_filter == "Unassigned":
    CA = CA[CA['assigned']== False]

st.write('Flitered Accounts:')
st.dataframe(CA[['District Agency Name','State','phone','Enrollment','owner','manager','assigned','Category']])

st.subheader("Summary Totals")
filtered_category = CA['Category'].value_counts()
st.write("Category counts:",filtered_category)
present_df = CA[CA['Category'] == 'Present in CRM']
assignment_counts = present_df['assigned'].value_counts().rename({True:'Assigned',False:'Unassigned'})
st.write("Breakdown of present in CRM by Assignment:")
st.write(assignment_counts)

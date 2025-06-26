from selenium import webdriver  
from selenium.webdriver.edge.service import service  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.edge.options import Options  
import pandas as pd  
import streamlit as st
import os  
import time
import pydeck as pdk
import json
import requests
import shutil 
import glob
import zipfile

st.logo("C:\\Users\\dfeijoo\\OneDrive - ConvergeOne\\Documents\\C1-logo-white.png")

def download_nces_data(year):
    # Set up Edge in headless mode
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Edge(options=edge_options)

    driver.get("https://nces.ed.gov/ccd/elsi/tableGenerator.aspx")
    time.sleep(10)  # Wait for page to load

    
    district_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='radio'][name='rowType'][value='District']")))
    district_radio.click()
    st.write("District radio button clicked")

    year_checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f"cb_year_{year}")))
    year_checkbox.click()
    st.write(f"Year {year} checkbox clicked")

    table_column_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "aTableColumns")))
    table_column_select.click()
    st.write("Table column selection opened")

    basic_information_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tree_tab12"]/li[1]/div')))
    basic_information_select.click()
    st.write("Basic information selected")

    county_name_select =  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f"cb_colyear_{year}_438")))
    county_name_select.click()
    st.write("County name selected")

    county_number_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f"cb_colyear_{year}_439")))
    county_number_select.click()
    st.write("County number selected")

    url_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f"cb_colyear_{year}_2478")))
    url_select.click()
    st.write("Source url selected")

    contact_select =  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tree_tab12"]/li[2]/div')))
    contact_select.click()
    st.write("Contact information selected")

    #address_select = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, f"cb_colyear_{year}_449")))
    #address_select.click()
    #st.write("Address selected")

    zip_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f"cb_colyear_{year}_452")))
    zip_select.click()
    st.write("Zip selected")

    phone_number_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f"cb_colyear_{year}_443")))
    phone_number_select.click()
    st.write("Phone number selected")

    characteristics_select = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"dbTabID15")))
    characteristics_select.click()
    st.write("Characteristics tab selected")

    classification_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tree_tab15"]/li[1]/div' )))
    classification_select.click()
    st.write("Classification selected")

    district_type_select = characteristics_select = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,f"cb_colyear_{year}_454")))
    district_type_select.click()
    st.write("District type selected")

    status_select =  WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,f"cb_colyear_{year}_2452")))
    status_select.click()
    st.write("Status selected")

    date_status_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f"cb_colyear_{year}_2453")))
    date_status_select.click()
    st.write("Date of status selected")


    latitude_select = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,f"cb_colyear_{year}_464")))
    latitude_select.click()
    st.write("Latitude selected")

    longitude_select = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,f"cb_colyear_{year}_465")))
    longitude_select.click()
    st.write("Longitude selected")

    enrollments_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dbTabID18")))
    enrollments_select.click()
    st.write("Enrollments tab selected")

    total_enrollment_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tree_tab18"]/li[1]/div')))
    total_enrollment_select.click()
    st.write("Total enrollment selected")

    total_students_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, f"cb_colyear_{year}_2447")))
    total_students_select.click()
    st.write("Total students selected")

    select_filters = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "aSelectFilters")))
    select_filters.click()
    st.write("Select filters opened")

    all_50states_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='radio'][name='iFilter_radio_State'][value='all']")))
    all_50states_select.click()
    st.write("All 50 states selected")

    create_table = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "aCreateTable")))
    create_table.click()
    st.write("Table created")

    csv_file = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "aCSV")))
    csv_file.click()
    st.write("CSV file download initiated")

    export_csv = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dExportLink"]/a')))
    export_csv.click()
    st.write("CSV file export initiated")

def load_data():
    folder_path = 'C://Users//dfeijoo//Downloads'  
    zipfiles = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.zip') and not f.endswith(".crdownload")]  
    newest_zip_file = max(zipfiles, key=os.path.getctime)
    df = pd.read_csv(newest_zip_file, skiprows=6)  
    df.columns = ["District Agency Name", "State", "County", "County number","Source url","zip code", "phone", "District Type", " District Status", "Effective date of updated status", "Latitude", "Longitude", "Enrollment"]
    df['District Agency Name'] = df['District Agency Name'].str.lower()
    df["Enrollment"] = pd.to_numeric(df["Enrollment"], errors='coerce')
    df["State"] = df["State"].astype(str).str.title().str.strip()
    df['phone']=df['phone'].astype(str)
    df['phone'] = df['phone'].str[:-1]
    df['phone'] = df['phone'].str.replace(r'\D','',regex = True)
    df = df[df['phone'].notna() & (df['phone'] !='')]
    return df

st.title("NCES District Data Scraper")


col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Get 2024 Data"):
        year = 2024
        download_nces_data(year)
        time.sleep(15)
        df = load_data()
        st.write("2024 Data")
        st.dataframe(df)
        
with col2:
    if st.button("Get 2023 Data"):
        year = 2023
        download_nces_data(year)
        time.sleep(15)
        df = load_data()
        st.write("2023 Data")
        st.session_state['dataframe'] = df

with col3:
    if st.button("Get 2022 Data"):
        year = 2022
        download_nces_data(year)
        time.sleep(15)
        df = load_data()
        st.write("2022 Data")
        st.session_state['dataframe'] = df



if 'dataframe' in st.session_state:
    st.dataframe(st.session_state['dataframe'])

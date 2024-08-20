import streamlit as st
import pandas as pd
from utils.helpers import (
    readFile, NC_Bene_Mapping, NAS_Bene_Mapping,
    NC_Claims_Mapping, NAS_Claims_Mapping, dataset_writer
)
import time

# Title of the page
st.title('LR Reports')

# ASOAP File Upload
st.header('Upload ASOAP File')
asoap_file = st.file_uploader("Choose ASOAP file")
asoap_file_type = st.radio('Select ASOAP file extension:', ('txt', 'csv', 'excel'))

# Beneficiary File Upload
st.header('Upload Beneficiary File')
beneficiary_file = st.file_uploader("Choose Beneficiary file")
beneficiary_file_type = st.radio('Select Beneficiary file extension:', ('txt', 'csv', 'excel'))

# Parameters
st.header('Choose TPA System')
tpa_systems = st.multiselect('Select TPA systems:', ['Nextcare', 'NAS'])

st.header('Select Mapping Method')
mapping_method = st.radio('Select mapping method:', ['Tool (In Excel)'])

if st.button('Process Files'):
    if not tpa_systems:
        st.error('Please select at least one TPA system.')
    elif asoap_file is None or beneficiary_file is None:
        st.error('Please upload both ASOAP and Beneficiary files.')
    else:
        # Show progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Update status message
            status_text.text('Processing files...')
            time.sleep(1)  # Simulate a delay
            st.info('Please Read Notes Sheet in Reports Excel Tool', icon="ℹ️")
            # Process files based on TPA system
            asoap = readFile(tpa_systems, asoap_file, asoap_file_type)
            status_text.text(f'ASOAP Data Has {len(asoap)} rows!')
            time.sleep(2)
            beneficiary = readFile(tpa_systems, beneficiary_file, beneficiary_file_type)
            status_text.text(f'Beneficiary Data Has {len(beneficiary)} rows!')

            progress_bar.progress(20)  # Update progress to 20%

            if 'Nextcare' in tpa_systems:
                beneficiary = NC_Bene_Mapping(beneficiary)
                asoap = NC_Claims_Mapping(asoap)
                progress_bar.progress(50)
                status_text.text('Data Mapped! Writing Excel file...')
                path = dataset_writer(asoap, beneficiary, 'Nextcare')
                file_name = 'Nextcare_Reporting_Tool_v1.xlsm'
            elif 'NAS' in tpa_systems:
                beneficiary = NAS_Bene_Mapping(beneficiary)
                asoap = NAS_Claims_Mapping(asoap)
                progress_bar.progress(50)
                status_text.text('Data Mapped! Writing Excel file...')
                path = dataset_writer(asoap, beneficiary, 'NAS')
                file_name = 'NAS_Reporting_Tool_v1.xlsm'
            else:
                st.error('Invalid TPA system selected.')

            progress_bar.progress(80)  # Update progress to 80%
            status_text.text('Files processed successfully. Preparing downloads...')

            with open(path, 'rb') as f:
                progress_bar.progress(100)  # Complete progress
                st.download_button(label='Download Excel File', data=f, file_name=file_name)

        except Exception as e:
            st.error(f'An error occurred: {e}')
            progress_bar.empty()  # Clear progress bar on error
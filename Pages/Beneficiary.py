import streamlit as st
import pandas as pd
from utils.helpers import readFile, mapFile, NC_Bene_Mapping, NAS_Bene_Mapping
from utils.templates import active_client_nas, active_client_nc

from datetime import datetime


# Title of the page
st.title('Active/Beneficiary List Mapping')

# Step 1: File Upload Field with File Type Checkboxes
st.header('Upload File')
uploaded_file = st.file_uploader("Choose a file")

# Step 2: TPA System Checkboxes
st.header('Choose TPA System')
tpa_systems = st.multiselect('Select TPA systems:', ['Nextcare', 'NAS'])

st.header('Select File Type')
file_type = st.radio('Select file extension:', ('txt', 'csv', 'excel'))

# Step 3: Active/Beneficiary List Mapping Method Checkboxes
st.header('Select Mapping Method')
mapping_method = st.radio('Select mapping method:', ('Client Template', 'UFIC Template', 'Custom Template'))



# Conditional Display
if mapping_method in ['Client Template', 'UFIC Template']:
    st.success('You selected ' + mapping_method)
    if uploaded_file is not None:
        try:
            dataframe = readFile(tpa_systems, uploaded_file, file_type)
            
            if mapping_method == "UFIC Template":
                if tpa_systems[0] == "Nextcare":
                    dataframe = NC_Bene_Mapping(dataframe)

                elif tpa_systems[0] == "NAS":
                    dataframe = NAS_Bene_Mapping(dataframe)

                else:
                    raise ValueError("Invalid TPA system or file type specified")
            
            elif mapping_method == "Client Template":
                if tpa_systems[0] == "Nextcare":
                    dataframe = mapFile(dataframe, active_client_nc)

                elif tpa_systems[0] == "NAS":
                    dataframe = mapFile(dataframe, active_client_nas)
                
                else:
                    raise ValueError("Invalid TPA system or file type specified")
                    
            path = f"./cache_files/{tpa_systems[0]}-{mapping_method}-{datetime.now().strftime('%Y%m%d-%H%M%S')}_Beneficiary.xlsx"
            dataframe.to_excel(path, index=False)
            with open(path, 'rb') as f:
                st.download_button(label='Download Mapped File', data=f, file_name=f"{tpa_systems[0]}-{mapping_method}_Beneficiary.xlsx")

        except ValueError as e:
            st.error(str(e))

        except Exception as e:
            st.error("An error occurred while processing the file: " + str(e))

elif mapping_method == 'Custom Template':
    st.success('You selected Custom Template')
    custom_template = st.file_uploader("Upload Custom Template (xlsx)", type="xlsx")
    if custom_template is not None and uploaded_file is not None:
        try:
            custom_template = pd.read_excel(custom_template, engine="openpyxl").columns
            dataframe = readFile(tpa_systems, uploaded_file, file_type)
            dataframe = mapFile(dataframe, custom_template)

            path = f"./cache_files/{tpa_systems[0]}-{mapping_method}-{datetime.now().strftime('%Y%m%d-%H%M%S')}_Beneficiary.xlsx"
            dataframe.to_excel(path, index=False)
            
            with open(path, 'rb') as f:
                st.download_button(label='Download Mapped File', data=f, file_name=f"{tpa_systems[0]}-{mapping_method}_Beneficiary.xlsx")

        except ValueError as e:
            st.error(str(e))

        except Exception as e:
            st.error("An error occurred while processing the file: " + str(e))

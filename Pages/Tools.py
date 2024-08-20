import streamlit as st


st.title('Tools')

renewal_tool_path = "./Tools/Premium Working - New Tool.xlsm"
lr_reports_tool = "./Tools/UFIC Reporting Tool v1.xlsm"

st.write('Please note that the following tools works with UFIC Data model!')


with open(renewal_tool_path, 'rb') as f:
    st.download_button(label='Download UFIC Renewal Tool', data=f, file_name=f"Premium Working - New Tool.xlsm")

with open(lr_reports_tool, 'rb') as f:
    st.download_button(label='Download UFIC Reporting Tool', data=f, file_name=f"UFIC Reporting Tool v1.xlsm")

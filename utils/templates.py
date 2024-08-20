import pandas as pd


ufic_beneficiary_map = pd.read_excel("Templates/Beneficiary.xlsx", sheet_name="Map")
ufic_asoap_map = pd.read_excel("Templates/ASOAP.xlsx", sheet_name="Map")

active_client_nc = pd.read_excel("Templates/Active list-Client Template NC.xlsx",sheet_name="Active list").columns
active_client_nas = pd.read_excel("Templates/Active list-Client Template NAS.xlsx",sheet_name="Data").columns
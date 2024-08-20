import streamlit as st

asoap = st.Page(
    "Pages/ASOAP.py", title="ASOAP", icon=":material/dashboard:", default=False
)

Beneficiary = st.Page(
    "Pages/Beneficiary.py", title="Beneficiary", icon=":material/dashboard:", default=False
)

Tools = st.Page(
    "Pages/Tools.py", title="Tools", icon=":material/dashboard:", default=True
)

quick_insights = st.Page(
    "Pages/quick_insights.py", title="Quick Insights", icon=":material/dashboard:", default=False
)

DHA_LR = st.Page(
    "Pages/DHA_LR.py", title="DHA/LR", icon=":material/dashboard:", default=False
)

pg = st.navigation(
    {
        "Files": [Tools],
        "Data": [asoap, Beneficiary],
        "Reports": [quick_insights, DHA_LR]
    }
)

pg.run()
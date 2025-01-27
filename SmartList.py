import streamlit as st

st.title("SmartList")
"\n"
"\n"
"\n"

LCol, RCol = st.columns(2)

with RCol:
    st.header("Tasks")
    st.button("Add Task")

with LCol:
    st.header("Ai Assessmint")

"\n"
"\n"
"\n"
st.write("out side line")
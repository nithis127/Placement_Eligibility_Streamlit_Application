import streamlit as st

st.sidebar.title('🏫ED TECH 🎓')        #streamlit main dashboard title

#define navigation pages with titles
page1 = st.Page('eligibility_filter.py',title='🎯ELIGIBLE STUDENTS')
page2 = st.Page('insights.py',title='💡INSIGHTS')

page = st.navigation([page1,page2])     #create navigation between defined pages
page.run()              #run the selected page
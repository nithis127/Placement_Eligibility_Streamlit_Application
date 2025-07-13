import streamlit as st
import pymysql
import pandas as pd

#---function for connect Python to MySQL database---
def get_connection():
    return pymysql.connect(host='localhost',                   #mysql server hostname                     
                      user='root',                             #mysql username
                      password='12345',                        #mysql password
                      database='ED_TECH',                      #database name
                      port=3306,                               #port number
                      cursorclass=pymysql.cursors.DictCursor)  #to receive query results as dictionaries instead of tuples

#---function for fetch eligible students based on user selected filters---
def eligible_students(problem_solved, soft_skill, pro_language):
    query='''SELECT 
                S.STUDENT_ID, S.NAME, S.AGE, S.GENDER, S.EMAIL, S.PHONE, S.ENROLLMENT_YEAR, S.COURSE_BATCH, 
                S.CITY, S.GRADUATION_YEAR, P.LANGUAGE, P.PROBLEMS_SOLVED, P.ASSESSMENTS_COMPLETED, P.MINI_PROJECTS, 
                P.CERTIFICATIONS_EARNED, P.LATEST_PROJECT_SCORE,
                ROUND((SS.COMMUNICATION + SS.TEAM_WORK + SS.PRESENTATION + 
                SS.LEADERSHIP + SS.CRITICAL_THINKING + SS.INTERPERSONAL_SKILLS) / 6, 0) AS SOFT_SKILL
            FROM STUDENT S
            JOIN PROGRAMMING P ON S.STUDENT_ID = P.STUDENT_ID
            JOIN SOFT_SKILL SS ON SS.STUDENT_ID = S.STUDENT_ID
            WHERE (P.PROBLEMS_SOLVED between %s AND %s)
            AND (((SS.COMMUNICATION + SS.TEAM_WORK + SS.PRESENTATION + SS.LEADERSHIP +
                 SS.CRITICAL_THINKING + SS.INTERPERSONAL_SKILLS) / 6) >= %s)
          '''
    connection = get_connection()          #call get_connetion() function for connect database
    cursor = connection.cursor()           #create cursor object for connection
    with connection:                       #automatically closes the connection after block execution
        with cursor:                       #automatically closes the cursor after block execution
            if pro_language == 'All':      #if "All" is selected, don't apply filter on programming languages
                query += 'ORDER BY P.PROBLEMS_SOLVED DESC;'
                cursor.execute(query, (problem_solved[0], problem_solved[1], soft_skill))
            else:                          # apply filter on selected programming language
                query += 'AND (P.LANGUAGE = %s) ORDER BY P.PROBLEMS_SOLVED DESC;'
                cursor.execute(query, (problem_solved[0], problem_solved[1], soft_skill, pro_language))
            result = cursor.fetchall()     #fetch all rows that match query
    return pd.DataFrame(result)            #return convert fetch result to pandas dataframe   
      
st.header('🎯Student Placement Eligibility Dashboard:')     #streamlit dashboard header
#sidebar filters for user input
language = st.sidebar.selectbox('👨‍💻Select Programming Language', ('All','Python','SQL','Java','C++','JavaScript','C#'))
problem_solved = st.sidebar.slider('🧩Select Problem Solved Score Range', 0, 500, (300,500), step=5)
soft_skill = st.sidebar.slider('🗣️Select Minimum Soft Skill Score', 0, 100, 80,step=10)

if st.sidebar.button('🔍Show Eligible Students'):       #show results on button click 
    df = eligible_students(problem_solved, soft_skill, language)    #call eligible_students() function with selected criteria
    if not df.empty:        #if data available, shows how many students are eligible for selected language
        if language == 'Python':
            st.info(f"🧾Found {len(df)} Eligible Students in 🐍Python🟢")
        elif language == 'SQL':
            st.info(f"🧾Found {len(df)} Eligible Students in 🗃️SQL🟢")
        elif language == 'Java':
            st.info(f"🧾Found {len(df)} Eligible Students in ☕Java🟢")
        elif language == 'C++':
            st.info(f"🧾Found {len(df)} Eligible Students in 🔧C++🟢")
        elif language == 'JavaScript':
            st.info(f"🧾Found {len(df)} Eligible Students in 🚀JavaScript🟢")
        elif language == 'C#':
            st.info(f"🧾Found {len(df)} Eligible Students in 💻C#🟢")
        else:
            st.info(f"🧾Found {len(df)} Eligible Students🟢")
        st.write(df)            #displays the result

    else:       #if no data, shows a warning message
        st.warning("⚠️ No Eligible Students found for the selected criteria🙁")

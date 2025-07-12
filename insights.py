import streamlit as st
import pymysql
import pandas as pd

#---function for connect Python to MySQL database---
def get_connection():
    return pymysql.connect(host='localhost',
                      user='root',
                      password='12345',
                      database='ED_TECH',
                      port=3306,
                      cursorclass=pymysql.cursors.DictCursor)

#---function for run SQL query---
def run_query(query):
    connection = get_connection()
    cursor = connection.cursor()
    with connection:                    #automatically closes the connection after block execution
        with cursor:                    #automatically closes the cursor after block execution
            cursor.execute(query)
            result = cursor.fetchall()
    return pd.DataFrame(result)         #return converts fetch result to pandas dataframe
       
st.header('💡Insights Dashboard:')     #streamlit dashboard header

#---creates collapsible sections with specific insights---
with st.expander("**01.** ⚡ Average Programming Performance per Batch"):
    query = '''SELECT S.COURSE_BATCH,
	           round(AVG(P.PROBLEMS_SOLVED)) AS AVG_PROBLEMS_SOLVED,
	           round(AVG(P.ASSESSMENTS_COMPLETED)) AS AVG_ASSESSMENTS,
	           round(AVG(CERTIFICATIONS_EARNED)) AS AVG_CERTIFICATES
               FROM STUDENT S
               JOIN PROGRAMMING P ON S.STUDENT_ID=P.STUDENT_ID
               GROUP BY S.COURSE_BATCH
               ORDER BY S.COURSE_BATCH;
             '''
    st.write(run_query(query))

with st.expander("**02.** 🏆 Top 5 Students Ready for Placement"):
    query = '''SELECT S.STUDENT_ID, S.NAME, P.MOCK_INTERVIEW_SCORE, P.INTERNSHIP_COMPLETED
               FROM STUDENT S
               JOIN PLACEMENT P ON S.STUDENT_ID=P.STUDENT_ID
               WHERE P.PLACEMENT_STATUS='Ready'
               ORDER BY P.MOCK_INTERVIEW_SCORE desc LIMIT 5;
            '''
    st.write(run_query(query))

with st.expander("**03.** ⚖️ Distribution of Soft Skills Scores"):
    query = '''SELECT AVG(COMMUNICATION) AS AVERAGE_OF_COMMUNICATION_SCORE,
                      AVG(TEAM_WORK) AS AVERAGE_OF_TEAM_WORK_SCORE,
                      AVG(PRESENTATION) AS AVERAGE_OF_PRESENTATION_SCORE,
                      AVG(LEADERSHIP) AS AVERAGE_OF_LEADERSHIP_SCORE,
                      AVG(CRITICAL_THINKING) AS AVERAGE_OF_CRITICAL_THINKING_SCORE,
                      AVG(INTERPERSONAL_SKILLS) AS AVERAGE_OF_INTERPERSONAL_SKILL_SCORE
               FROM SOFT_SKILL;
            '''
    df = run_query(query)
    st.write(df.iloc[0])        #display only the first row

with st.expander("**04.** 🧑‍💼 Students Got Placement"):
    query = '''SELECT S.STUDENT_ID, S.NAME, P.COMPANY_NAME, P.PLACEMENT_PACKAGE
               FROM STUDENT S
               JOIN PLACEMENT P ON S.STUDENT_ID=P.STUDENT_ID
               WHERE P.PLACEMENT_STATUS = 'Placed'
               ORDER BY P.PLACEMENT_PACKAGE DESC;
            '''
    st.write(run_query(query))

with st.expander("**05.** 🔃 Students ready but not yet placed"):
    query = '''SELECT p.STUDENT_ID, s.NAME
               FROM STUDENT S JOIN PLACEMENT P ON S.STUDENT_ID = P.STUDENT_ID
               WHERE PLACEMENT_STATUS = 'Ready';
            '''
    st.write(run_query(query))

with st.expander("**06.** 🧑‍💻 Most Used Programming Language"):
    query = '''SELECT LANGUAGE, COUNT(*) AS USERS
               FROM PROGRAMMING
               GROUP BY LANGUAGE ORDER BY USERS DESC;
            '''
    st.write(run_query(query))

with st.expander("**07.** 📜 Certifications Earned by Batch"):
    query = '''SELECT S.COURSE_BATCH, SUM(P.CERTIFICATIONS_EARNED) AS TOTAL_CERTIFICATES
               FROM STUDENT S 
               JOIN PROGRAMMING P ON S.STUDENT_ID=P.STUDENT_ID
               GROUP BY S.COURSE_BATCH ORDER BY S.COURSE_BATCH;
            '''
    st.write(run_query(query))

with st.expander("**08.** 📭Students with 0 certifications but placed"):
    query = '''SELECT S.STUDENT_ID, NAME
               FROM STUDENT S
               JOIN PROGRAMMING PR ON S.STUDENT_ID = PR.STUDENT_ID
               JOIN PLACEMENT P ON S.STUDENT_ID = P.STUDENT_ID
               WHERE CERTIFICATIONS_EARNED = 0 AND PLACEMENT_STATUS = 'Placed';
            '''
    st.write(run_query(query))

with st.expander("**09.** 👥 Total number of students placed per batch"):
    query = '''SELECT S.COURSE_BATCH, COUNT(P.PLACEMENT_STATUS) AS total_placed
               FROM STUDENT S JOIN PLACEMENT P ON S.STUDENT_ID = P.STUDENT_ID
               WHERE P.PLACEMENT_STATUS = 'Placed'
               GROUP BY S.COURSE_BATCH ORDER BY S.COURSE_BATCH;
            '''
    st.write(run_query(query))

with st.expander("**10.** 💼 Top Hiring Companies"):
    query = '''SELECT COMPANY_NAME, COUNT(PLACEMENT_STATUS) AS TOTAL_PLACED, AVG(PLACEMENT_PACKAGE) AS AVERAGE_PACKAGE_in_LPA
               FROM PLACEMENT
               WHERE PLACEMENT_STATUS='Placed'
               GROUP BY COMPANY_NAME
               ORDER BY TOTAL_PLACED DESC LIMIT 10;
            '''
    st.write(run_query(query))
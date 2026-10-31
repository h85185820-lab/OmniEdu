import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="OmniEdu AI - Institutional Platform", layout="wide")

# Simulated Database in Session State
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {"role": "Admin", "name": "Principal Prof. Azam", "pass": "admin123"},
        "teacher": {"role": "Teacher", "name": "Sir Imtiaz", "pass": "teach123"},
        "student": {"role": "Student", "name": "Ali Khan", "pass": "stud123"},
        "parent": {"role": "Parent", "name": "Mr. Mandhro", "pass": "parent123"},
        "worker": {"role": "Worker", "name": "Ahmed (Maintenance)", "pass": "work123"}
    }

if "attendance" not in st.session_state:
    st.session_state.attendance = pd.DataFrame(columns=["Date", "Student", "Status", "Remarks"])

if "grades" not in st.session_state:
    st.session_state.grades = pd.DataFrame(columns=["Student", "Subject", "Midterm", "Final", "Status"])

# Authentication Window
st.sidebar.title("🔐 OmniEdu AI Login")
username = st.sidebar.text_input("Username (admin, teacher, student, parent, worker)")
password = st.sidebar.text_input("Password", type="password")
login_btn = st.sidebar.button("Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.user_name = ""

if login_btn:
    if username in st.session_state.users and st.session_state.users[username]["pass"] == password:
        st.session_state.logged_in = True
        st.session_state.role = st.session_state.users[username]["role"]
        st.session_state.user_name = st.session_state.users[username]["name"]
        st.rerun()
    else:
        st.sidebar.error("Invalid credentials! Try admin123, teach123, etc.")

if not st.session_state.logged_in:
    st.title("🎓 OmniEdu AI: Unified Institutional Platform")
    st.markdown("### Welcome to the Stream 2026 Winning Project!")
    st.info("Please log in from the sidebar using the demo credentials to access your specific institutional window.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🏫 Multi-Institution Support")
        st.write("Unified portal for Schools, Colleges, Academies, and Universities.")
    with col2:
        st.markdown("#### ⚡ Real-Time Automation")
        st.write("Instant attendance logging, auto-late marking, and bulk result sheet uploading.")
    with col3:
        st.markdown("#### 🔗 360° Communication")
        st.write("Seamless connection linking Admin, Teachers, Students, Parents, and Workers.")
else:
    # Header & Logout
    st.sidebar.success(f"Logged in as: **{st.session_state.user_name}** ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Role-Based Multi-Window Routing
    role = st.session_state.role

    if role == "Admin":
        st.header("🏛️ Admin & Principal Control Center")
        tab1, tab2, tab3 = st.tabs(["Institution Overview", "Staff Oversight", "Broadcast System"])
        
        with tab1:
            st.metric(label="Total Enrolled Students", value="1,450", delta="+12% this term")
            st.metric(label="Active Faculty & Staff", value="85", delta="100% Attendance today")
            st.metric(label="Pending Result Approvals", value="3 Sheets")
            
        with tab2:
            st.subheader("Faculty Attendance & Workload")
            st.dataframe(pd.DataFrame({
                "Faculty Name": ["Prof. Azam", "Sir Imtiaz", "Dr. Sara", "Mr. Rashid"],
                "Department": ["Pre-Medical", "Biology / IT", "Chemistry", "Physics"],
                "Status": ["Present", "Present", "On Leave", "Present"],
                "Classes Taught Today": [4, 5, 0, 4]
            }))
            
        with tab3:
            st.subheader("Institution-Wide Broadcast")
            msg = st.text_area("Broadcast Announcement to All Portals:")
            if st.button("Send Broadcast"):
                st.success("Announcement successfully broadcasted to all Student, Teacher, Parent, and Worker portals!")

    elif role == "Teacher":
        st.header("👨‍🏫 Teacher & Faculty Portal")
        tab1, tab2, tab3 = st.tabs(["Attendance Logger", "Result Sheet Upload", "Student Analytics"])
        
        with tab1:
            st.subheader("Mark Student Attendance & Late Status")
            s_name = st.text_input("Student Name", "Ali Khan")
            status = st.selectbox("Status", ["Present", "Absent", "Late (>15 mins)"])
            remarks = st.text_input("Remarks / Reason", "Traffic delay")
            if st.button("Submit Attendance"):
                new_row = pd.DataFrame([{"Date": str(datetime.now().date()), "Student": s_name, "Status": status, "Remarks": remarks}])
                st.session_state.attendance = pd.concat([st.session_state.attendance, new_row], ignore_index=True)
                st.success(f"Attendance recorded for {s_name} as {status}!")
                
            st.markdown("### Today's Logged Attendance")
            st.dataframe(st.session_state.attendance)
            
        with tab2:
            st.subheader("Upload Grade / Result Sheet")
            uploaded_file = st.file_uploader("Upload CSV Result Sheet", type=["csv"])
            if uploaded_file is not None:
                df_upload = pd.read_csv(uploaded_file)
                st.success("Result sheet successfully parsed and verified by AI!")
                st.dataframe(df_upload)
            else:
                st.info("Upload a CSV file containing Student Name, Subject, Midterm, Final marks to auto-populate grades.")

        with tab3:
            st.subheader("AI Performance Insights")
            st.write("AI analysis shows 88% class mastery in Organic Chemistry mechanisms. Recommended review: Thermodynamics.")

    elif role == "Student":
        st.header("🎓 Student Portal")
        tab1, tab2, tab3 = st.tabs(["My Timetable", "Attendance & Grades", "AI Study Assistant"])
        
        with tab1:
            st.subheader("Daily Class Timetable")
            st.table(pd.DataFrame({
                "Time": ["08:00 AM", "09:30 AM", "11:00 AM", "12:30 PM"],
                "Subject": ["Biology (Pre-Med)", "Organic Chemistry", "Physics Vectors", "English Language"],
                "Instructor": ["Prof. Azam", "Dr. Sara", "Mr. Rashid", "Ms. Sana"]
            }))
            
        with tab2:
            st.subheader("My Academic Record")
            st.metric("Overall Attendance", "94%", "+2% from last month")
            st.metric("Current GPA / Standing", "A+ (78.5%)", "Top 5% in Class")
            st.markdown("### Attendance History")
            st.dataframe(st.session_state.attendance)

        with tab3:
            st.subheader("🤖 AI Study Companion")
            prompt = st.text_input("Ask your AI tutor any academic question (Biology, Chemistry, Physics):")
            if prompt:
                st.info(f"AI Tutor Answer: For your query about '{prompt}', remember that biological membranes and chemical reaction mechanisms require understanding molecular structures and thermodynamics!")

    elif role == "Parent":
        st.header("👪 Parent Portal")
        tab1, tab2, tab3 = st.tabs(["Child Attendance", "Exam Results", "Teacher Communication"])
        
        with tab1:
            st.subheader("Child Attendance Monitoring")
            st.metric("Attendance Status Today", "Present 🟢", "Arrived at 07:55 AM")
            st.dataframe(st.session_state.attendance)
            
        with tab2:
            st.subheader("Term Exam Results")
            st.table(pd.DataFrame({
                "Subject": ["Biology", "Chemistry", "Physics", "English"],
                "Marks Obtained": ["88/100", "82/100", "79/100", "91/100"],
                "Grade": ["A+", "A", "B+", "A+"]
            }))
            
        with tab3:
            st.subheader("Direct Teacher Messaging")
            msg_to_teacher = st.text_area("Send message to Class Representative / Teacher:")
            if st.button("Send Message"):
                st.success("Message sent successfully to Professor Muhammad Azam!")

    elif role == "Worker":
        st.header("🛠️ Support Staff & Worker Portal")
        tab1, tab2 = st.tabs(["My Tasks", "Maintenance Log"])
        
        with tab1:
            st.subheader("Assigned Daily Duties")
            st.table(pd.DataFrame({
                "Task ID": ["T-101", "T-102", "T-103"],
                "Location": ["Science Block Hall B", "Main Auditorium", "Computer Lab"],
                "Task": ["Morning Assembly Setup", "Sound System Check", "Projector Maintenance"],
                "Status": ["Completed", "Pending", "In Progress"]
            }))
            
        with tab2:
            st.subheader("Report Maintenance Issue")
            issue = st.text_input("Describe maintenance issue:")
            if st.button("Submit Report to Admin"):
                st.success("Maintenance report logged and forwarded to Administration.")


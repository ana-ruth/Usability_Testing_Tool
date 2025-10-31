import streamlit as st
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")


def save_to_csv(data_dict, csv_file):
    # Convert dict to DataFrame with a single row
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # If CSV doesn't exist, write with headers
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Else, we need to append without writing the header!
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()


def main():
    st.title("Usability Testing Tool")

    if "consent" not in st.session_state:
        st.session_state.consent = False

    home, consent, demographics, tasks, exit, report = st.tabs(
        ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the Usability Testing Tool for HCI.

        In this app, you will:
        1. Provide consent for data collection.
        2. Fill out a short demographic questionnaire.
        3. Perform a specific task (or tasks).
        4. Answer an exit questionnaire about your experience.
        5. View a summary report (for demonstration purposes).
        """)

    with consent:
        st.header("Consent Form")

        # Consent form and variable called consent_given
        st.write("Please read carefully the following consent form.")
        st.markdown("**Consent Agreement:**")
        st.markdown("""
        - I acknowledge that I will be asked to perform specific tasks on a web application.
        - I recognize all information collected will remain confidential and used solely for research and improvement purposes.
        - I understand participation in this usability study is voluntary, and I can withdraw my consent at any time.
        """)
        consent_given = st.checkbox("I agree to the terms above.")

        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
            else:
                # Save the consent acceptance time
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)
                st.session_state.consent = True
                st.success("Consent submitted. Thank you!")
    if st.session_state.consent:
        with demographics:
            st.header("Demographic Questionnaire")

            with st.form("demographic_form"):
                # Demographic form
                name = st.text_input("Enter Your Name")
                age = st.selectbox("Select Your Age", ("18-24", "25-34", "35-44", "45-54", "55-64", "65+"), index=None, placeholder="Select your age group...")
                occupation = st.text_input("Enter Your Occupation")
                major = st.selectbox("Select your area of study", ("Arts and Humanities", "Business and Management", "Education", "Engineering and Technology", "Health and Medicine", "Natural Sciences", "Social Sciences", "Other"), index=None, placeholder="Select area of study...")
                familiarity = st.selectbox("How familiar are you with similar tools?",("Not Familiar", "Somewhat Familiar","Very Familiar"), index=None, placeholder="Select familiarity...")


                submitted = st.form_submit_button("Submit Demographics")
                if submitted:
                    data_dict = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "name": name,
                        "age": age,
                        "occupation": occupation,
                        "major": major,
                        "familiarity": familiarity
                    }
                    save_to_csv(data_dict, DEMOGRAPHIC_CSV)
                    st.success("Demographic Questionnaire submitted.")


        with tasks:
            st.header("Task Page")

            st.write("Please select a task and record your experience completing it.")

            # 4 sample tasks that will be changed in Project 3
            selected_task = st.selectbox("Select Task", ["Task 1: Search for recalls of onions in Florida between April 1st, 2021, to March 5th, 2025.", "Task 2: View the bar chart and determine how many recalls could cause serious health problems.", "Task 3: Navigate through the map."])
            st.write("Task Description: Perform the example task in our system...")

            # Track success, completion time, etc.
            start_button = st.button("Start Task Timer")
            if start_button:
                st.session_state["start_time"] = time.time()
                st.info("Task timer started. Complete your task and then click \"Stop Task Timer\".")

            stop_button = st.button("Stop Task Timer")
            if stop_button and "start_time" in st.session_state:
                duration = time.time() - st.session_state["start_time"]
                st.session_state["task_duration"] = duration
                st.success("Task completed in "+str(round(duration,2))+" seconds!")

            success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
            notes = st.text_area("Observer Notes")

            if st.button("Save Task Results"):
                duration_val = st.session_state.get("task_duration", None)

                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "task_name": selected_task,
                    "success": success,
                    "duration_seconds": duration_val if duration_val else "",
                    "notes": notes
                }
                save_to_csv(data_dict, TASK_CSV)

                st.success("Task Results saved.")

                # Reset any stored time in session_state if you'd like
                if "start_time" in st.session_state:
                    del st.session_state["start_time"]
                if "task_duration" in st.session_state:
                    del st.session_state["task_duration"]

        with exit:
            st.header("Exit Questionnaire")

            with st.form("exit_form"):
                # Exit questionnaire
                satisfaction = st.slider("Overall Satisfaction (1 = Very Low, 5 = Very High)", 1, 5)
                difficulty = st.slider("Overall Difficulty (1 = Very Easy, 5 = Very Hard)", 1, 5)
                open_feedback = st.text_area("Additional feedback:", placeholder="Write here...")

                submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
                if submitted_exit:
                    data_dict = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "satisfaction": satisfaction,
                        "difficulty": difficulty,
                        "open_feedback": open_feedback
                    }
                    save_to_csv(data_dict, EXIT_CSV)
                    st.success("Exit questionnaire data saved.")

    #prevent user from accessing questionnaires if consent was not given
    else:
        with demographics:
            st.warning("Please submit your consent to participate in this usability study.")
        with tasks:
            st.warning("Please submit your consent to participate in this usability study.")
        with exit:
            st.warning("Please submit your consent to participate in this usability study.")

    with report:
        st.header("Usability Report - Aggregated Results")

        st.write("**Consent Data**")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)

            df = pd.read_csv(DEMOGRAPHIC_CSV)

            #Dictionary with the total of each age range
            ages_total = {"18-24": len(df[df["age"].isin(["18-24"])]),
                          "25-34": len(df[df["age"].isin(["25-34"])]),
                          "35-44": len(df[df["age"].isin(["35-44"])]),
                          "45-54": len(df[df["age"].isin(["45-54"])]),
                          "55-64": len(df[df["age"].isin(["55-64"])]),
                          "65+": len(df[df["age"].isin(["65+"])]),
            }
            ages_total = {k: v for k, v in ages_total.items() if v !=0} #exclude empty keys

            # Dictionary with total of somewhat familiar, very familiar, not familiar
            familiarity_total = { "Somewhat Familiar": len(df[df["familiarity"].isin(["Somewhat Familiar"])]),
                                  "Very Familiar": len(df[df["familiarity"].isin(["Very Familiar"])]),
                                  "Not Familiar": len(df[df["familiarity"].isin(["Not Familiar"])])
            }
            familiarity_total = {k: v for k, v in familiarity_total.items() if v !=0} #exclude empty keys


            #Pie charts to display Age Groups Breakdown and App Familiarity Breakdown from dictionaries
            fig, axs = plt.subplots(1, 2)

            axs[0].pie(ages_total.values(), labels=ages_total.keys(), autopct='%.0f%%', radius=2.7)
            axs[0].set_title("Age Groups Breakdown", y=2)

            axs[1].pie(familiarity_total.values(), labels=familiarity_total.keys(), autopct='%.0f%%', radius=2.7)
            axs[1].set_title("App Familiarity Breakdown", y=2)

            plt.subplots_adjust(wspace=2.7)

            st.pyplot(fig) #show plot on streamlit app

        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            df = st.dataframe(task_df)

            df = pd.read_csv(TASK_CSV)

            #dataframe for each task
            Task1_df = df[df["task_name"].isin(['Task 1: Search for recalls of onions in Florida between April 1st, 2021, to March 5th, 2025.'])]

            Task2_df = df[df["task_name"].isin(['Task 2: View the bar chart and determine how many recalls could cause serious health problems.'])]

            Task3_df = df[df["task_name"].isin(['Task 3: Navigate through the map.'])]

           # Task4_df = df[df["task_name"].isin(['Task 4: Example Task'])]

            tasks = ("Task1", "Task2", "Task3")

            #Dictionary containing total of "Yes", "No", "Partial" per Task
            task_success_totals = {"Yes": (len(Task1_df[Task1_df["success"].isin(["Yes"])]),
                                           len(Task2_df[Task2_df["success"].isin(["Yes"])]),
                                           len(Task3_df[Task3_df["success"].isin(["Yes"])])
                                           ),
                                   "No": (len(Task1_df[Task1_df["success"].isin(["No"])]),
                                           len(Task2_df[Task2_df["success"].isin(["No"])]),
                                           len(Task3_df[Task3_df["success"].isin(["No"])])
                                           ),
                                   "Partial": (len(Task1_df[Task1_df["success"].isin(["Partial"])]),
                                          len(Task2_df[Task2_df["success"].isin(["Partial"])]),
                                          len(Task3_df[Task3_df["success"].isin(["Partial"])])
                                          )
                                   }
            x = np.arange(len(tasks)) #3 groups in plot
            width = 0.25  # the width of the bars
            multiplier = 0

            fig, ax = plt.subplots(layout='constrained')

            ##Bar Charts for Completion per Task
            # success: "Yes", "No","Partial"
            for success, total in task_success_totals.items():
                offset = width * multiplier
                ax.bar(x+offset, total, width, label = success)
                multiplier += 1

                ax.set_ylabel('People who completed the task')
                ax.set_title('Distribution of Task Completion Status', fontsize=18)
                ax.set_xticks(x+width, tasks)
                ax.legend(loc='upper right', ncols =3)
                ax.yaxis.set_major_locator(MaxNLocator(integer=True)) #show only whole numbers on y-axis

            st.pyplot(fig) #show plot on streamlit app


        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)
        else:
            st.info("No exit questionnaire data available yet.")

        # Example of aggregated stats (for demonstration only)
        if not exit_df.empty:
            st.subheader("Exit Questionnaire Averages")
            avg_satisfaction = exit_df["satisfaction"].mean()
            avg_difficulty = exit_df["difficulty"].mean()
            st.write(f"**Average Satisfaction**: {avg_satisfaction:.2f}")
            st.write(f"**Average Difficulty**: {avg_difficulty:.2f}")



if __name__ == "__main__":
    main()
import streamlit as st
import requests

st.set_page_config(
    page_title="AI Operations Agent",
    page_icon="🤖",
    layout="centered"
)

# =========================
# SIDEBAR
# =========================

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Run Agent",
        "Manage Contacts"
    ]
)

st.sidebar.subheader("Supported Tasks")

try:
    tasks_response = requests.get(
        "https://ai-operations-agent-platform.onrender.com/tasks"
    )

    tasks = tasks_response.json()["supported_tasks"]

    for task, description in tasks.items():

        st.sidebar.write(
            f"• {task} → {description}"
        )

except:
    st.sidebar.error("Backend not running")


# =========================
# CONTACT MANAGEMENT PAGE
# =========================

if page == "Manage Contacts":

    st.title("📇 Contact Management")

    st.subheader("Add Contact")

    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Add Contact"):

        response = requests.post(
            "https://ai-operations-agent-platform.onrender.com/contacts",
            params={
                "name": name,
                "email": email
            }
        )

        st.success(response.json()["message"])

    st.subheader("Saved Contacts")

    response = requests.get(
        "https://ai-operations-agent-platform.onrender.com/contacts"
    )

    contacts = response.json()["contacts"]

    for contact in contacts:

        st.write(
            f"• {contact['name']} — {contact['email']}"
        )


# =========================
# RUN AGENT PAGE
# =========================

elif page == "Run Agent":

    st.title("🤖 AI Operations Agent")

    st.markdown(
        "Run AI-powered workflow automation using LangGraph and OpenAI."
    )

    user_input = st.text_area(
        "Enter your request",
        placeholder="Example: Send email to Akash"
    )

    if st.button("Run Agent"):

        if not user_input.strip():

            st.warning("Please enter a request.")

        else:
            try:
                response = requests.post(
                    "https://ai-operations-agent-platform.onrender.com/run",
                    params={"input_text": user_input}
                )

                data = response.json()

                st.success("Execution completed")

                # =========================
                # STATUS
                # =========================

                st.subheader("Status")

                status = data.get("status")

                if status == "success":
                    st.success(status)

                elif status == "failed":
                    st.error(status)

                elif status == "partial":
                    st.warning(status)

                else:
                    st.info(status)

                # =========================
                # RESULTS
                # =========================

                st.subheader("Results")

                for result in data.get("results", []):

                    st.write(f"• {result}")

                # =========================
                # METRICS
                # =========================

                metrics = data.get("metrics", {})

                st.subheader("Metrics")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Success",
                    metrics.get("success", 0)
                )

                col2.metric(
                    "Failure",
                    metrics.get("failure", 0)
                )

                # =========================
                # EXECUTION TIME
                # =========================

                st.subheader("Execution Time")

                st.info(
                    f"{data.get('execution_time_seconds')} seconds"
                )

            except Exception as e:

                st.error(f"Error: {str(e)}")
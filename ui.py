import streamlit as st
import requests

# =========================
# CONFIG
# =========================

BASE_URL = (
    "http://127.0.0.1:8000"
)

TIMEOUT = 30

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
        "Manage Contacts",
        "Meetings"
    ]
)

st.sidebar.subheader(
    "Supported Tasks"
)

try:

    tasks_response = requests.get(
        f"{BASE_URL}/tasks",
        timeout=TIMEOUT
    )

    tasks = tasks_response.json()[
        "supported_tasks"
    ]

    for task, description in tasks.items():

        st.sidebar.write(
            f"• {task} → {description}"
        )

except Exception:

    st.sidebar.error(
        "Backend not running"
    )


# =========================
# CONTACT MANAGEMENT
# =========================

if page == "Manage Contacts":

    st.title(
        "📇 Contact Management"
    )

    st.subheader(
        "Add Contact"
    )

    name = st.text_input("Name")

    email = st.text_input("Email")

    if st.button("Add Contact"):

        try:

            response = requests.post(
                f"{BASE_URL}/contacts",
                params={
                    "name": name,
                    "email": email
                },
                timeout=TIMEOUT
            )

            data = response.json()

            if data.get("status") == "success":

                st.success(
                    data.get("message")
                )

            else:

                st.error(
                    data.get("message")
                )

        except Exception as e:

            st.error(str(e))

    st.subheader(
        "Saved Contacts"
    )

    try:

        response = requests.get(
            f"{BASE_URL}/contacts",
            timeout=TIMEOUT
        )

        contacts = response.json()[
            "contacts"
        ]

        if not contacts:

            st.info(
                "No contacts found"
            )

        for contact in contacts:

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.write(
                    f"• {contact['name']} "
                    f"— {contact['email']}"
                )

            with col2:

                if st.button(
                    "Delete",
                    key=contact["id"]
                ):

                    delete_response = (
                        requests.delete(
                            f"{BASE_URL}/contacts/"
                            f"{contact['id']}",
                            timeout=TIMEOUT
                        )
                    )

                    delete_data = (
                        delete_response.json()
                    )

                    if (
                        delete_data.get("status")
                        == "success"
                    ):

                        st.success(
                            delete_data.get(
                                "message"
                            )
                        )

                        st.rerun()

                    else:

                        st.error(
                            delete_data.get(
                                "message"
                            )
                        )

    except Exception as e:

        st.error(str(e))


# =========================
# MEETINGS PAGE
# =========================

elif page == "Meetings":

    st.title("📅 Meetings")

    try:

        response = requests.get(
            f"{BASE_URL}/meetings",
            timeout=TIMEOUT
        )

        meetings = response.json()[
            "meetings"
        ]

        if not meetings:

            st.info(
                "No meetings scheduled"
            )

        for meeting in meetings:

            st.write(
                f"• {meeting['person']} "
                f"→ {meeting['time']}"
            )

    except Exception as e:

        st.error(str(e))


# =========================
# RUN AGENT
# =========================

elif page == "Run Agent":

    st.title(
        "🤖 AI Operations Agent"
    )

    st.markdown(
        "Run AI-powered workflow "
        "automation using "
        "LangGraph and OpenAI."
    )

    user_input = st.text_area(
        "Enter your request",
        placeholder=(
            "Example: "
            "Send email to Akash"
        )
    )

    if st.button("Run Agent"):

        if not user_input.strip():

            st.warning(
                "Please enter a request."
            )

        else:

            try:

                response = requests.post(
                    f"{BASE_URL}/run",
                    params={
                        "input_text": user_input
                    },
                    timeout=TIMEOUT
                )

                data = response.json()

                st.success(
                    "Execution completed"
                )

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

                elif status == "no_action":

                    st.info(
                        "No valid task found"
                    )

                else:

                    st.info(status)

                # =========================
                # RESULTS
                # =========================

                st.subheader("Results")

                results = data.get(
                    "results",
                    []
                )

                if not results:

                    st.info(
                        "No execution results"
                    )

                for result in results:

                    st.write(f"• {result}")

                # =========================
                # METRICS
                # =========================

                metrics = data.get(
                    "metrics",
                    {}
                )

                st.subheader("Metrics")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Success",
                    metrics.get(
                        "success",
                        0
                    )
                )

                col2.metric(
                    "Failure",
                    metrics.get(
                        "failure",
                        0
                    )
                )

                # =========================
                # EXECUTION TIME
                # =========================

                st.subheader(
                    "Execution Time"
                )

                st.info(
                    f"{data.get('execution_time_seconds')} "
                    f"seconds"
                )

            except Exception as e:

                st.error(str(e))
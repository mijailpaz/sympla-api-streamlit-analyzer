import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px


# Define API base URL
API_BASE_URL = "https://api.sympla.com.br/public"

# Set Streamlit app title with an emoji for better UX
st.title("🔍 Sympla API Checker")

# -------------------------------
# Helper Function
# -------------------------------
def extract_total_records(pagination, api_version):
    """
    Extracts the total number of possible records from the pagination data based on the API version.
    
    Parameters:
        pagination (dict): The pagination section from the API response.
        api_version (str): The API version ("v3" or "v5").
    
    Returns:
        int: The total number of possible records.
    """
    if not pagination:
        return 0  # No pagination data available

    if api_version == "v3":
        return pagination.get("quantity", len(pagination.get("data", [])))
    elif api_version == "v5":
        # Assuming API v5 uses 'total_records' or 'total_items'
        return pagination.get("total_records", pagination.get("total_items", len(pagination.get("data", []))))
    else:
        # Default fallback
        return len(pagination.get("data", []))

# -------------------------------
# Session State Management
# -------------------------------

# Function to reset only the events in session state
def reset_events():
    st.session_state["events"] = pd.DataFrame()

# Function to reset both results and events in session state
def reset_results_and_events():
    st.session_state["results"] = []
    st.session_state["events"] = pd.DataFrame()

# Function to reset only the results in session state
def reset_results():
    st.session_state["results"] = []

# Initialize session state for storing results and events
if "results" not in st.session_state:
    st.session_state["results"] = []
if "events" not in st.session_state:
    st.session_state["events"] = pd.DataFrame()

# -------------------------------
# Sidebar Setup
# -------------------------------

st.sidebar.header("⚙️ Setup")

# API Token Input with on_change callback to reset results and events
token = st.sidebar.text_input(
    "API Access Token", 
    type="password",
    help="Enter your Sympla API access token. Ensure it has the necessary permissions.",
    on_change=reset_results_and_events,
    key="api_token"
)

# API Version Selectbox with on_change callback to reset only events
api_version = st.sidebar.selectbox(
    "API Version", 
    ["v3", "v5"],
    help="Select the API version you want to interact with.",
    on_change=reset_events,
    key="api_version_select"
)

# Functions to fetch events
def fetch_events():
    if st.session_state["api_token"] and st.session_state["api_version_select"]:
        with st.spinner("🔄 Fetching events..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/{st.session_state['api_version_select']}/events",
                    headers={"S_TOKEN": st.session_state["api_token"]},
                )
                response.encoding = 'utf-8'  # Ensure correct encoding
                if response.status_code == 200:
                    events = response.json().get("data", [])
                    if events:
                        st.session_state["events"] = pd.DataFrame(events)
                        st.success("✅ Events fetched successfully.")
                    else:
                        st.warning("⚠️ No events found for the selected API version.")
                elif response.status_code == 401:
                    st.error("❌ Invalid or expired token.")
                else:
                    st.error(f"⚠️ Error {response.status_code}: Unable to fetch events.")
            except Exception as e:
                st.error(f"❗Error: {str(e)}")
    else:
        st.error("❗Please provide both API token and select API version.")

# Function to clear results
def clear_results():
    reset_results()

# Sidebar buttons with emojis for better UX
col_clear, col_fetch = st.sidebar.columns(2)
with col_clear:
    st.sidebar.button("🧹 Clear Results", on_click=clear_results)
with col_fetch:
    st.sidebar.button("📥 Fetch Events", on_click=fetch_events)

# -------------------------------
# Main Content with Tabs
# -------------------------------

tab_fetch_data, tab_results = st.tabs(["📥 Fetch Data", "📊 Results"])

# -------------------------------
# Fetch Data Tab
# -------------------------------
with tab_fetch_data:
    st.markdown("### 📋 Fetched Events")
    if not st.session_state["events"].empty:
        st.dataframe(st.session_state["events"])
        
        # Download button for events
        csv_events = st.session_state["events"].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Events as CSV",
            data=csv_events,
            file_name="fetched_events.csv",
            mime='text/csv',
        )
    else:
        st.warning("⚠️ No events fetched. Please check your token and API version, then click 'Fetch Events'.")
    
    st.markdown("---")
    
    st.subheader("🔍 Check Event Details")
    event_id = st.text_input(
        "📇 Event ID",
        help="Enter the ID of the event you want to check orders or participants for."
    )
    
    if event_id:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📦 Check Event Orders"):
                if st.session_state["api_token"] and st.session_state["api_version_select"]:
                    with st.spinner("🔄 Checking Event Orders..."):
                        start_time = time.time()
                        try:
                            response = requests.get(
                                f"{API_BASE_URL}/{st.session_state['api_version_select']}/events/{event_id}/orders",
                                headers={"S_TOKEN": st.session_state["api_token"]},
                            )
                            curl_time = time.time() - start_time
                            process_start_time = time.time()

                            if response.status_code == 200:
                                data = response.json()
                                orders = data.get("data", [])
                                pagination = data.get("pagination", {})
                                process_time = time.time() - process_start_time

                                # Extract total possible records from pagination
                                total_possible_records = extract_total_records(pagination, st.session_state["api_version_select"])

                                # Append new result to session_state["results"]
                                st.session_state["results"].append({
                                    "event_id": str(event_id),
                                    "type": "orders",
                                    "api_version": st.session_state["api_version_select"],
                                    "data": pd.DataFrame(orders),
                                    "pagination": pagination,
                                    "curl_time": curl_time,
                                    "process_time": process_time,
                                    "total_possible_records": total_possible_records  # New field
                                })
                                st.success(f"✅ Orders for event {event_id} retrieved successfully.")
                            elif response.status_code == 401:
                                st.error(f"❌ Invalid token for event {event_id}.")
                            else:
                                st.error(f"⚠️ Error {response.status_code}: Unable to fetch orders for event {event_id}.")
                        except Exception as e:
                            st.error(f"❗Error: {str(e)}")
                else:
                    st.error("❗Please provide both API token and select API version.")
    
        with col2:
            if st.button("👥 Check Event Participants"):
                if st.session_state["api_token"] and st.session_state["api_version_select"]:
                    with st.spinner("🔄 Checking Event Participants..."):
                        start_time = time.time()
                        try:
                            response = requests.get(
                                f"{API_BASE_URL}/{st.session_state['api_version_select']}/events/{event_id}/participants",
                                headers={"S_TOKEN": st.session_state["api_token"]},
                            )
                            curl_time = time.time() - start_time
                            process_start_time = time.time()

                            if response.status_code == 200:
                                data = response.json()
                                participants = data.get("data", [])
                                pagination = data.get("pagination", {})
                                process_time = time.time() - process_start_time

                                # Extract total possible records from pagination
                                total_possible_records = extract_total_records(pagination, st.session_state["api_version_select"])

                                # Append new result to session_state["results"]
                                st.session_state["results"].append({
                                    "event_id": str(event_id),
                                    "type": "participants",
                                    "api_version": st.session_state["api_version_select"],
                                    "data": pd.DataFrame(participants),
                                    "pagination": pagination,
                                    "curl_time": curl_time,
                                    "process_time": process_time,
                                    "total_possible_records": total_possible_records  # New field
                                })
                                st.success(f"✅ Participants for event {event_id} retrieved successfully.")
                            elif response.status_code == 401:
                                st.error(f"❌ Invalid token for event {event_id}.")
                            else:
                                st.error(f"⚠️ Error {response.status_code}: Unable to fetch participants for event {event_id}.")
                        except Exception as e:
                            st.error(f"❗Error: {str(e)}")
                else:
                    st.error("❗Please provide both API token and select API version.")
    
    st.markdown("---")
    
    if st.session_state["results"]:
        st.markdown("### 📊 Charts")
        
        # Prepare data for charts
        summary_data = []
        for result in st.session_state["results"]:
            event_id = result["event_id"]
            api_version = result["api_version"]
            type_ = result["type"]
            curl_time = result["curl_time"]
            process_time = result["process_time"]
            total_possible_records = result.get("total_possible_records", len(result["data"]))
            
            # Concatenate API Version and Event ID for unique identifier
            combined_event_id = f"{api_version} {event_id}"
            
            summary_data.append({
                "Combined Event ID": combined_event_id,  # New field for combined identifier
                "API Version": api_version,
                "Type": type_.capitalize(),
                "API Call Time (s)": curl_time,
                "Processing Time (s)": process_time,
                "Total Possible Records": total_possible_records
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Ensure 'Combined Event ID' is treated as string
        summary_df["Combined Event ID"] = summary_df["Combined Event ID"].astype(str)
        
        if not summary_df.empty:
            # -------------------------------
            # First Chart: API Call Times
            # -------------------------------
            st.markdown("#### 📈 API Call Times by Combined Event ID and API Call Type")
            fig_times = px.bar(
                summary_df,
                x="Combined Event ID",
                y="API Call Time (s)",
                color="Type",
                barmode="group",
                title="API Call Times by Combined Event ID and API Call Type",
                labels={
                    "API Call Time (s)": "API Call Time (seconds)", 
                    "Combined Event ID": "API Version & Event ID", 
                    "Type": "API Call Type"
                },
                hover_data={"API Version": True}
            )
            st.plotly_chart(fig_times, use_container_width=True, key="fetch_times_chart")
            
            # -------------------------------
            # Second Chart: Total Possible Records
            # -------------------------------
            st.markdown("#### 📈 Total Records Fetched per Combined Event ID and Type")
            fig_records = px.bar(
                summary_df,
                x="Combined Event ID",
                y="Total Possible Records",
                color="Type",
                barmode="group",
                title="Total Records Fetched per Combined Event ID and Type",
                labels={"Total Possible Records": "Total Records"},
                hover_data=["API Call Time (s)", "Processing Time (s)"]
            )
            st.plotly_chart(fig_records, use_container_width=True, key="fetch_records_chart")

# -------------------------------
# Results Tab
# -------------------------------
with tab_results:
    st.markdown("### 📊 Results")
    
    if st.session_state["results"]:
        for idx, result in enumerate(st.session_state["results"], 1):
            st.markdown(f"#### 📄 Result {idx}")
            st.write(f"**Event ID**: {result['event_id']}")
            st.write(f"**Type**: {result['type'].capitalize()}")
            st.write(f"**API Version**: {result['api_version']}")
            st.write(f"- **Time for API call (curl):** {result['curl_time']:.2f} seconds")
            st.write(f"- **Time for processing:** {result['process_time']:.2f} seconds")
            
            pagination = result.get("pagination", {})
            if pagination:
                st.write(
                    f"- **Pagination:** Page {pagination.get('page', 1)} of {pagination.get('total_page', 1)}, "
                    f"Total Records: {pagination.get('quantity', 0)}"
                )
            
            st.dataframe(result["data"])
            
            # Download button for each result
            csv_data = result["data"].to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {result['type'].capitalize()} as CSV",
                data=csv_data,
                file_name=f"{result['event_id']}_{result['type']}.csv",
                mime='text/csv',
            )
        
        # -------------------------------
        # Summary Statistics
        # -------------------------------
        st.markdown("### 📈 Summary Statistics")
        summary_data = []
        for result in st.session_state["results"]:
            event_id = result["event_id"]
            api_version = result["api_version"]
            type_ = result["type"]
            curl_time = result["curl_time"]
            process_time = result["process_time"]
            total_records = result["data"].shape[0]
            total_possible_records = result.get("total_possible_records", len(result["data"]))
            summary_data.append({
                "Combined Event ID": f"{api_version} {event_id}",  # Ensure consistency
                "API Version": api_version,
                "Type": type_.capitalize(),
                "API Call Time (s)": curl_time,
                "Processing Time (s)": process_time,
                "Total Records": total_records,
                "Total Records in event": total_possible_records
            })

        summary_df = pd.DataFrame(summary_data)
        
        # Ensure 'Combined Event ID' is treated as string
        summary_df["Combined Event ID"] = summary_df["Combined Event ID"].astype(str)
        
        if not summary_df.empty:
            # Display Summary Statistics
            st.write("**Average API Call Time (curl):** {:.2f} seconds".format(summary_df["API Call Time (s)"].mean()))
            st.write("**Average Processing Time:** {:.2f} seconds".format(summary_df["Processing Time (s)"].mean()))
            st.write("**Total Records Fetched:** {}".format(summary_df["Total Records"].sum()))
        
        # -------------------------------
        # Download Summary Data
        # -------------------------------
        st.markdown("### 📥 Download Summary Data")
        csv_summary = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Summary as CSV",
            data=csv_summary,
            file_name="event_results_summary.csv",
            mime='text/csv',
        )
    else:
        st.info("ℹ️ No results to display. Please fetch events and check event orders or participants.")
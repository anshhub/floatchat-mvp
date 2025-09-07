# file: app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -------------------------
# Fake Data (placeholder only)
# -------------------------
sample_data = pd.DataFrame({
    "float_id": ["ARGO001", "ARGO002", "ARGO003", "ARGO004", "ARGO005"],
    "lat": [1.2, -2.1, 0.5, 15.0, -4.5],
    "lon": [33.5, 35.0, 72.8, 60.1, 50.0],
    "date": pd.to_datetime(["2023-03-05", "2023-03-12", "2023-03-20", "2023-04-02", "2023-03-25"]),
    "salinity": [35.1, 34.9, 35.3, 36.1, 34.8],
    "temperature": [28.3, 27.8, 28.5, 26.4, 28.0]
})
st.write("--- Debugging: Sample Data --- ")
st.write("Shape of sample_data:", sample_data.shape)
st.write("First 5 rows of sample_data:")
st.dataframe(sample_data.head())
st.write("--- End Debugging: Sample Data ---")

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="🌊 FloatChat (Enhanced Frontend)", layout="wide")

# Sidebar with chat functionality moved here
with st.sidebar:
    st.title("🌊 FloatChat")
    st.write("Welcome to FloatChat!")
    
    # User role selection
    user_role = st.selectbox("👤 Select Role", ["Student", "Researcher", "Policy Maker"])
    
    # Navigation menu
    menu = st.radio(
        "📍 Navigation",
        ["Chatbot", "Explore Data", "Visualizations", "Query History"]
    )
    
    # Ask about ARGO data section moved to left side
    st.markdown("---")
    st.subheader("💬 Ask about ARGO data")
    user_query = st.text_input("Ask:", placeholder="Type your question...")
    if st.button("▶️ Ask"):
        st.session_state["last_query"] = user_query
        # Initialize messages if not exists
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": user_query})
        
        # Demo reply
        response = f"🤖 (Demo) Hi {user_role}, here's some placeholder data for: {user_query}"
        st.session_state["messages"].append({"role": "assistant", "content": response})

# Main layout
col_map, col_chart = st.columns([1, 1])

with col_map:
    st.subheader("🌍 Live Map (ARGO)")
    # Increased height to match salinity chart by using custom CSS
    st.markdown("""
    <style>
    .argo-image {
        height: 500px;
        object-fit: cover;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display image with increased height
    st.image("Screenshot 2025-09-08 001347.png",
         caption="ARGO Observation Network (static View)",
         use_container_width=True)

with col_chart:
    st.subheader("📈 Salinity Chart")
    fig = px.line(sample_data, x="date", y="salinity", markers=True, title="Salinity over Time")
    # Set explicit height for the chart
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.write("--- Debugging: Salinity Chart --- ")
    st.write("Salinity chart figure generated.")
    st.write("--- End Debugging: Salinity Chart ---")

# -------------------------
# Chatbot Page
# -------------------------
if menu == "Chatbot":
    st.title("💬 FloatChat – Conversational AI (Demo)")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            # Show data and visualization for assistant messages
            if msg["role"] == "assistant":
                st.dataframe(sample_data)
                
                fig = px.scatter_geo(
                    sample_data, lat="lat", lon="lon", text="float_id",
                    color="temperature", projection="natural earth"
                )
                st.plotly_chart(fig, use_container_width=True)
                st.write("--- Debugging: Chatbot Scatter Geo Chart --- ")
                st.write("Chatbot scatter geo chart figure generated.")
                st.write("--- End Debugging: Chatbot Scatter Geo Chart ---")

    # Quick suggestions
    st.write("👉 Quick Queries:")
    cols = st.columns(3)
    if cols[0].button("Show floats in March 2023"):
        st.session_state["messages"].append({"role": "assistant", "content": "Showing floats for March 2023 (Demo)."})
        st.dataframe(sample_data[sample_data["date"].dt.month == 3])
    if cols[1].button("Show salinity profiles"):
        st.session_state["messages"].append({"role": "assistant", "content": "Showing salinity profiles (Demo)."})
        st.line_chart(sample_data.set_index("date")["salinity"])
    if cols[2].button("Show temperature trends"):
        st.session_state["messages"].append({"role": "assistant", "content": "Showing temperature trends (Demo)."})
        st.line_chart(sample_data.set_index("date")["temperature"])

# -------------------------
# Explore Data Page
# -------------------------
elif menu == "Explore Data":
    st.title("🔍 Explore ARGO Data (Demo)")

    # Filters
    date_range = st.date_input(
        "Select Date Range",
        [datetime(2023, 3, 1), datetime(2023, 3, 31)]
    )
    param = st.selectbox("Choose Parameter", ["salinity", "temperature"])

    filtered = sample_data[
        (sample_data["date"] >= pd.to_datetime(date_range[0])) &
        (sample_data["date"] <= pd.to_datetime(date_range[1]))
    ]

    st.dataframe(filtered)

    fig = px.line(filtered, x="date", y=param, color="float_id", markers=True, title=f"{param.title()} over time")
    st.plotly_chart(fig, use_container_width=True)
    st.write("--- Debugging: Explore Data Line Chart --- ")
    st.write("Explore Data line chart figure generated.")
    st.write("--- End Debugging: Explore Data Line Chart ---")

    # Download option
    st.download_button("⬇️ Download Data (CSV)", filtered.to_csv(index=False), "argo_data.csv", "text/csv")

# -------------------------
# Visualizations Page
# -------------------------
elif menu == "Visualizations":
    st.title("📊 Visualizations (Demo)")

    tab1, tab2, tab3 = st.tabs(["🌍 Map", "📈 Line Chart", "⚪ Scatter Plot"])

    with tab1:
        
        fig = px.scatter_geo(sample_data, lat="lat", lon="lon", text="float_id",
                             color="salinity", projection="natural earth")
        st.plotly_chart(fig, use_container_width=True)
        st.write("--- Debugging: Visualizations Map --- ")
        st.write("Visualizations map figure generated.")
        st.write("--- End Debugging: Visualizations Map ---")

    with tab2:
        st.line_chart(sample_data.set_index("date")[["salinity", "temperature"]])
        st.write("--- Debugging: Visualizations Line Chart --- ")
        st.write("Visualizations line chart generated.")
        st.write("--- End Debugging: Visualizations Line Chart ---")

    with tab3:
        fig = px.scatter(sample_data, x="salinity", y="temperature", color="float_id", size="temperature")
        st.plotly_chart(fig, use_container_width=True)
        st.write("--- Debugging: Visualizations Scatter Plot --- ")
        st.write("Visualizations scatter plot figure generated.")
        st.write("--- End Debugging: Visualizations Scatter Plot ---")

# -------------------------
# Query History Page
# -------------------------
elif menu == "Query History":
    st.title("📜 Query History (Demo)")
    if "messages" in st.session_state and st.session_state["messages"]:
        for msg in st.session_state["messages"]:
            role = "🧑 User" if msg["role"] == "user" else "🤖 Bot"
            st.write(f"{role}: {msg['content']}")
    else:
        st.info("No queries yet.")

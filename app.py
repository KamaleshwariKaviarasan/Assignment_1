import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import pymysql
# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    
    try:
        conn=mysql.connector(    host="localhost",
            user="root",
            password="Kamale@05",
            port="3306",
            database="imdb"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None


# @st.cache_data
def load_data():
    conn = get_connection()
    query = "SELECT movie_name, duration, rating, genre FROM imdb_table;"
    df = pd.read_sql(query, conn)
    conn.close()

    # Convert Duration from "2h 15m" → minutes
    def convert_duration(d):
        try:
            d = d.strip().lower()
            hours, minutes = 0, 0
            if "h" in d:
                parts = d.split("h")
                hours = int(parts[0].strip())
                if "m" in parts[1]:
                    minutes = int(parts[1].replace("m", "").strip() or 0)
            elif "m" in d:
                minutes = int(d.replace("m", "").strip())
            return hours * 60 + minutes
        except:
            return None

    df["duration_mins"] = df["duration"].apply(convert_duration)
    return df

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Insights Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🎬 Movie Insights Dashboard</h1>", unsafe_allow_html=True)

df = load_data()

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Movies", f"{len(df):,}")
with col2:
    st.metric("Average Rating ⭐", round(df['rating'].mean(), 2))
with col3:
    st.metric("Avg Duration ⏱", f"{round(df['duration_mins'].mean()/60, 2)} hrs")

st.markdown("---")

# -----------------------------
# Genre Distribution
# -----------------------------
st.subheader("📊 Movies by Genre")
genre_count = df['genre'].value_counts().reset_index()
genre_count.columns = ["Genre", "Count"]

fig1 = px.pie(
    genre_count, names="Genre", values="Count",
    hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Rating Distribution
# -----------------------------
st.subheader("⭐ Rating Spread")
fig2 = px.histogram(df, x="rating", nbins=20, 
                    color_discrete_sequence=["#E74C3C"])
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Duration by Genre
# -----------------------------
st.subheader("⏱ Avg Duration by Genre (hrs)")
avg_duration = df.groupby("genre")["duration_mins"].mean().reset_index()
avg_duration["duration_hrs"] = avg_duration["duration_mins"] / 60

fig3 = px.bar(
    avg_duration, x="genre", y="duration_hrs",
    color="genre", text=avg_duration["duration_hrs"].round(1),
    color_discrete_sequence=px.colors.sequential.Mint
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Top 10 Movies
# -----------------------------
st.subheader("🏆 Top 10 Movies by Rating")
top_movies = df.sort_values("rating", ascending=False).head(10)

fig4 = px.bar(
    top_movies, x="rating", y="movie_name", orientation="h",
    color="rating", text="rating",
    color_continuous_scale="Agsunset"
)
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Raw Data
# -----------------------------
with st.expander("📄 View Dataset"):
    st.dataframe(df, use_container_width=True)
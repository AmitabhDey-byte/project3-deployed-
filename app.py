import numpy as np
import seaborn as sea
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Netflix EDA Dashboard", layout="wide")
st.title("Netflix Data Analysis Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("data/NetFlix.csv")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df[df['cast'] != 'Unknown']
    return df

df = load_data()

st.sidebar.title("Filters")

content_type = st.sidebar.multiselect("Select Type", df['type'].unique(), default=df['type'].unique())

year_range = st.sidebar.slider("Release Year Range", int(df['release_year'].min()), int(df['release_year'].max()), (2000, 2020))

df = df[df['type'].isin(content_type)]
df = df[(df['release_year'] >= year_range[0]) & (df['release_year'] <= year_range[1])]

st.sidebar.markdown("### Quick Insights")

if st.sidebar.button("Show Top Actor"):
    actor = df['cast'].str.split(', ').explode().value_counts().head(1)
    st.write(actor)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Content Trends", "People Insights", "Genres & Ratings","Durations"])

with tab1:
    st.subheader("Movies vs TV Shows")
    fig = plt.figure(figsize=(6,6))
    sea.countplot(x='type', data=df)
    st.pyplot(fig)

with tab2:
    st.subheader("Top 10 Countries")

    country_counting = df['country'].str.split(', ').explode().value_counts().head(10)

    fig = plt.figure(figsize=(10,5))
    sea.barplot(x=country_counting.values, y=country_counting.index, color='#8e1ce6', edgecolor='black')

    st.pyplot(fig)

with tab3:
        st.subheader("Content Over Years")

        year_counting = df['release_year'].value_counts().sort_index()

        fig = plt.figure(figsize=(12, 6))
        sea.lineplot(x=year_counting.index, y=year_counting.values, marker='o')

        st.pyplot(fig)
with tab4:
    st.subheader("Top Genres")

    genre_counting = df['genres'].value_counts().head(10)

    fig = plt.figure(figsize=(12,6))
    ax = sea.barplot(
        x=genre_counting.index,
        y=genre_counting.values,
        palette='cubehelix',
        edgecolor='black'
    )

    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    st.subheader("Content Ratings Distribution")

    fig = plt.figure(figsize=(10,6))
    sea.countplot(y='rating', data=df, order=df['rating'].value_counts().index)

    st.pyplot(fig)


with tab5:
    st.subheader("Movie Duration Distribution")

    movies = df[df['type'] == 'Movie'].copy()

    fig = plt.figure(figsize=(7,5))
    plt.hist(movies['duration'], bins=30)

    st.pyplot(fig)

    st.subheader("TV Show Seasons Distribution")

    tv = df[df['type'] == 'TV Show'].copy()
    tv_counts = tv['duration'].value_counts().head(10)

    fig = plt.figure(figsize=(10,5))
    sea.barplot(x=tv_counts.index, y=tv_counts.values, palette='flare')

    st.pyplot(fig)

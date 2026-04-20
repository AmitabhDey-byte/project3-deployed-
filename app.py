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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8,tab9, tab10  = st.tabs(["Overview", "Content Trends", "People Insights", "Genres & Ratings","Durations", "No of Seasons", "Top Directors","Top Actors","Avg monthly content","Movie vs Year trend"])
#tab7,tab8,tab9, tab10  , "Top TV Shows", "Top Directors", "Avg monthly content"
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
with tab6:
    st.subheader("Top Season Counts")

    tv = df[df['type'] == 'TV Show'].copy()

    tv_counts = tv['duration'].value_counts().head(10)

    fig = plt.figure(figsize=(10, 5))

    ax = sea.barplot(x=tv_counts.index, y=tv_counts.values, palette='flare', edgecolor='black')

    plt.title("Top TV Show Season Counts", fontsize=15, weight='bold')
    plt.xlabel("Seasons")
    plt.ylabel("Number of Shows")

    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig)
with tab7:
    st.subheader("Top Directors")

    fig2=  plt.figure(figsize=(10, 6))

    director_counts = df['director'].value_counts().head(10)

    sea.barplot(x=director_counts.values, y=director_counts.index, color='#1303fc', edgecolor='#fc1703')

    plt.title("Top 10 Directors", fontsize=14, weight='bold')
    plt.xlabel("Number of Titles")
    plt.ylabel("Director")

    st.pyplot(fig2)

with tab8:

    st.subheader("Top Actors")

    fig = plt.figure(figsize=(12, 5))
    actor_counts = df['cast'].str.split(', ').explode().value_counts().head(10)
    ax = sea.barplot(x=actor_counts.values, y=actor_counts.index, hue=actor_counts.index, palette='magma',
                                                                                                               edgecolor='black')

    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())}',
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', fontsize=10, weight='bold')

    plt.title("Top 10 Actors", fontsize=15, weight='bold')
    plt.xlabel("Number of Titles", fontsize=12)
    plt.ylabel("Actor", fontsize=12)

    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()

    st.pyplot(fig)
with tab9:
    st.subheader("Average monthnly Content")

    df['date_added'] = pd.to_datetime(df['date_added'])
    df['month'] = df['date_added'].dt.month

    fig = plt.figure(figsize=(10, 5))

    ax = sea.countplot(x='month', data=df, palette='viridis', hue='type', edgecolor='black')
    for p in ax.patches:
        ax.annotate(
            f'{int(p.get_height())}',  # using the height as count value
            (p.get_x() + p.get_width() / 2., p.get_height()),
            # this i used to exactly align the text or the count value in the middle of the bars
            ha='center', va='bottom', fontsize=9, weight='bold')

    plt.title("Monthly Content Addition", fontsize=14, weight='bold')
    plt.xlabel("Month")
    plt.ylabel("Number of Titles")

    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig)

with tab10:
    st.subheader("Movie vs Year Trend")

    movies = df[df['type'] == 'Movie'].copy()
    movies['duration'] = movies['duration'].astype(float)

    fig = plt.figure(figsize=(10, 6))
    sea.scatterplot(x='duration', y='release_year', data=movies, hue='rating', size='duration', sizes=(20, 200),
                    palette='rainbow', alpha=0.7, edgecolor='black')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title("Movie Duration vs Release Year", fontsize=14, weight='bold')
    plt.xlabel("Release Year")
    plt.ylabel("Duration in minutes")

    st.pyplot(fig)
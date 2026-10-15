import streamlit as st
import random
import json
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="CineMatch AI | Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SESSION STATE =================
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "surprise" not in st.session_state:
    st.session_state.surprise = None

# ================= FAVOURITES STORAGE =================
FAV_FILE = "cinematch_favorites.json"


def load_favorites():
    try:
        if os.path.exists(FAV_FILE):
            with open(FAV_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
    except (OSError, json.JSONDecodeError):
        pass
    return []


def save_favorites():
    try:
        with open(FAV_FILE, "w", encoding="utf-8") as file:
            json.dump(
                st.session_state.favorites,
                file,
                ensure_ascii=False,
                indent=2
            )
    except OSError:
        st.warning("Could not save favourites to the local file.")


if "favorites_loaded" not in st.session_state:
    st.session_state.favorites = load_favorites()
    st.session_state.favorites_loaded = True

# ================= MOVIE DATABASE =================
movies = [
    {
        "name": "Jawan", "genre": "Action", "language": "Hindi",
        "rating": 7.0, "year": 2023,
        "poster": "https://image.tmdb.org/t/p/w500/jFt1gS4BGHlK8xt76Y81Alp4dbt.jpg",
        "story": "An action entertainer featuring a mission to fight corruption."
    },
    {
        "name": "Pathaan", "genre": "Action", "language": "Hindi",
        "rating": 5.8, "year": 2023,
        "poster": "https://image.tmdb.org/t/p/w500/arf00BkwvXo0CFKbaD9H6ST3k5.jpg",
        "story": "An Indian spy returns to protect the country from a dangerous threat."
    },
    {
        "name": "3 Idiots", "genre": "Comedy", "language": "Hindi",
        "rating": 8.4, "year": 2009, "poster": "",
        "story": "Three engineering students discover friendship and a different way to learn."
    },
    {
        "name": "Hera Pheri", "genre": "Comedy", "language": "Hindi",
        "rating": 8.2, "year": 2000, "poster": "",
        "story": "Three struggling characters get caught up in a hilarious series of events."
    },
    {
        "name": "Jab We Met", "genre": "Romance", "language": "Hindi",
        "rating": 7.9, "year": 2007, "poster": "",
        "story": "An unexpected journey changes the lives of two very different people."
    },
    {
        "name": "Sita Ramam", "genre": "Romance", "language": "Telugu",
        "rating": 8.5, "year": 2022, "poster": "",
        "story": "A mysterious letter reveals a beautiful story of love and sacrifice."
    },
    {
        "name": "Stree", "genre": "Horror", "language": "Hindi",
        "rating": 7.5, "year": 2018, "poster": "",
        "story": "A small town faces a mysterious supernatural presence."
    },
    {
        "name": "Tumbbad", "genre": "Horror", "language": "Hindi",
        "rating": 8.2, "year": 2018, "poster": "",
        "story": "A dark tale about greed, a hidden treasure and an ancient legend."
    },
    {
        "name": "RRR", "genre": "Action", "language": "Telugu",
        "rating": 7.8, "year": 2022, "poster": "",
        "story": "Two extraordinary revolutionaries form an unexpected friendship."
    },
    {
        "name": "Baahubali 2", "genre": "Action", "language": "Telugu",
        "rating": 8.2, "year": 2017, "poster": "",
        "story": "A warrior uncovers his heritage and fights for his kingdom."
    },
    {
        "name": "Interstellar", "genre": "Sci-Fi", "language": "English",
        "rating": 8.7, "year": 2014,
        "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "story": "Explorers travel beyond Earth in search of a future for humanity."
    },
    {
        "name": "Inception", "genre": "Sci-Fi", "language": "English",
        "rating": 8.8, "year": 2010,
        "poster": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
        "story": "A specialist enters dreams to carry out an extraordinary mission."
    },
    {
        "name": "The Dark Knight", "genre": "Action", "language": "English",
        "rating": 9.0, "year": 2008,
        "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "story": "Batman faces a dangerous criminal who challenges Gotham City."
    },
    {
        "name": "Titanic", "genre": "Romance", "language": "English",
        "rating": 7.9, "year": 1997, "poster": "",
        "story": "A love story unfolds during the ill-fated voyage of a famous ship."
    },
    {
        "name": "Drishyam", "genre": "Thriller", "language": "Hindi",
        "rating": 8.2, "year": 2015, "poster": "",
        "story": "A father tries to protect his family through a complicated mystery."
    },
    {
        "name": "Coco", "genre": "Drama", "language": "English",
        "rating": 8.4, "year": 2017,
        "poster": "https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg",
        "story": "A young musician discovers his family's history in a magical land."
    },
    {
        "name": "Premam", "genre": "Romance", "language": "Malayalam",
        "rating": 8.3, "year": 2015, "poster": "",
        "story": "A young man's journey through love and different stages of life."
    },
    {
        "name": "3", "genre": "Romance", "language": "Tamil",
        "rating": 7.4, "year": 2012, "poster": "",
        "story": "A romantic drama exploring love, relationships and personal struggles."
    },
    {
        "name": "Manjummel Boys", "genre": "Thriller",
        "language": "Malayalam", "rating": 8.2, "year": 2024,
        "poster": "",
        "story": "A group of friends face a dangerous situation during a trip."
    },
    {
        "name": "The Avengers", "genre": "Action", "language": "English",
        "rating": 8.0, "year": 2012, "poster": "",
        "story": "Superheroes join forces to protect the world from a major threat."
    },
    {
        "name": "Finding Nemo", "genre": "Comedy", "language": "English",
        "rating": 8.2, "year": 2003, "poster": "",
        "story": "A clownfish crosses the ocean on a journey to find his son."
    },
    {
        "name": "Vikram", "genre": "Action", "language": "Tamil",
        "rating": 8.3, "year": 2022, "poster": "",
        "story": "A special investigation uncovers a dangerous criminal network."
    },
    {
        "name": "Kantara", "genre": "Thriller", "language": "Kannada",
        "rating": 8.2, "year": 2022, "poster": "",
        "story": "A village story connects tradition, nature and a mysterious force."
    },
    {
        "name": "The Conjuring", "genre": "Horror", "language": "English",
        "rating": 7.5, "year": 2013, "poster": "",
        "story": "Paranormal investigators help a family facing unexplained events."
    },
    {
        "name": "Dangal", "genre": "Drama", "language": "Hindi",
        "rating": 8.3, "year": 2016, "poster": "",
        "story": "A former wrestler trains his daughters to compete in wrestling."
    }
]

# ================= THEME =================
st.sidebar.title("⚙️ CineMatch Settings")

theme = st.sidebar.radio(
    "🎨 Choose Appearance",
    ["Dark", "Light"],
    index=0 if st.session_state.theme == "Dark" else 1,
    horizontal=True
)
st.session_state.theme = theme

if theme == "Dark":
    bg = "#0B1020"
    card = "#151D30"
    fg = "#F8FAFC"
    muted = "#B8C4D9"
    accent = "#A78BFA"
else:
    bg = "#F3F6FC"
    card = "#FFFFFF"
    fg = "#172033"
    muted = "#526078"
    accent = "#6D28D9"

st.markdown(f"""
<style>
.stApp {{
    background: {bg};
    color: {fg};
}}
[data-testid="stSidebar"] {{
    background: {card};
}}
h1, h2, h3, h4, p, label {{
    color: {fg};
}}
.hero {{
    background: linear-gradient(120deg, #6D28D9, #DB2777, #F97316);
    padding: 32px 15px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 22px;
    box-shadow: 0 8px 30px rgba(109,40,217,0.2);
}}
.hero h1, .hero p {{
    color: white !important;
}}
.movie-card {{
    background: {card};
    border: 1px solid {accent};
    border-radius: 16px;
    padding: 12px;
    min-height: 100px;
}}
.movie-info {{
    color: {muted} !important;
    font-size: 14px;
}}
div[data-testid="stMetric"] {{
    background: {card};
    border: 1px solid {accent};
    border-radius: 14px;
    padding: 14px;
}}
div.stButton > button {{
    border-radius: 10px;
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="hero">
    <h1>🎬 CineMatch AI</h1>
    <p>Your Personal Movie Discovery Studio</p>
    <p>🍿 Discover • Explore • Save • Enjoy</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Movie Preferences")

# ================= FILTERS =================
genres = ["All"] + sorted({m["genre"] for m in movies})
languages = ["All"] + sorted({m["language"] for m in movies})

selected_genre = st.sidebar.selectbox("🎭 Genre", genres)
selected_language = st.sidebar.selectbox("🌍 Language", languages)

search = st.sidebar.text_input(
    "🔍 Search movie",
    placeholder="Type a movie name..."
)

min_rating = st.sidebar.slider(
    "⭐ Minimum rating",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.5
)

min_year, max_year = min(m["year"] for m in movies), max(m["year"] for m in movies)

year_range = st.sidebar.slider(
    "📅 Release year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

sort_option = st.sidebar.selectbox(
    "📊 Sort by",
    ["Highest Rated", "Lowest Rated", "Newest First", "Oldest First", "A-Z"]
)

# ================= FILTER ENGINE =================
filtered_movies = []

for movie in movies:
    if selected_genre != "All" and movie["genre"] != selected_genre:
        continue

    if selected_language != "All" and movie["language"] != selected_language:
        continue

    if search.strip().lower() not in movie["name"].lower():
        continue

    if movie["rating"] < min_rating:
        continue

    if not year_range[0] <= movie["year"] <= year_range[1]:
        continue

    filtered_movies.append(movie)

if sort_option == "Highest Rated":
    filtered_movies.sort(key=lambda m: m["rating"], reverse=True)
elif sort_option == "Lowest Rated":
    filtered_movies.sort(key=lambda m: m["rating"])
elif sort_option == "Newest First":
    filtered_movies.sort(key=lambda m: m["year"], reverse=True)
elif sort_option == "Oldest First":
    filtered_movies.sort(key=lambda m: m["year"])
else:
    filtered_movies.sort(key=lambda m: m["name"].lower())

# ================= DASHBOARD =================
st.subheader("📊 Movie Dashboard")

average_rating = sum(m["rating"] for m in movies) / len(movies)
top_rating = max(m["rating"] for m in movies)

c1, c2, c3, c4 = st.columns(4)
c1.metric("🎞️ Total Movies", len(movies))
c2.metric("🔍 Matching Movies", len(filtered_movies))
c3.metric("❤️ My Watchlist", len(st.session_state.favorites))
c4.metric("⭐ Average Rating", f"{average_rating:.1f}/10")

st.caption(
    f"Your database contains {len(movies)} movies. "
    f"The highest demo rating is {top_rating:.1f}/10."
)

st.markdown("---")

# ================= SURPRISE ME =================
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("✨ Find Your Next Favourite")

with col2:
    if st.button("🎲 Surprise Me", use_container_width=True):
        pool = filtered_movies if filtered_movies else movies
        st.session_state.surprise = random.choice(pool)["name"]

if st.session_state.surprise:
    pick = next(
        (m for m in movies if m["name"] == st.session_state.surprise),
        None
    )
    if pick:
        st.info(
            f"🎉 Today's Pick: **{pick['name']}** | "
            f"⭐ {pick['rating']}/10 | {pick['language']} | {pick['year']}"
        )
        st.write(pick["story"])

# ================= NAVIGATION =================
section = st.radio(
    "Choose your section",
    ["🎬 Explore All", "❤️ My Watchlist", "🏆 Top Rated", "💡 For You"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

if section == "❤️ My Watchlist":
    display_movies = [
        m for m in movies
        if m["name"] in st.session_state.favorites
    ]
    st.subheader("❤️ My Watchlist")

elif section == "🏆 Top Rated":
    display_movies = sorted(
        [m for m in movies if m["rating"] >= 8.0],
        key=lambda m: m["rating"],
        reverse=True
    )
    st.subheader("🏆 Top Rated Movies")

elif section == "💡 For You":
    # Simple preference-based recommendation.
    display_movies = sorted(
        filtered_movies,
        key=lambda m: (m["rating"], m["year"]),
        reverse=True
    )
    st.subheader("💡 Recommended For You")
    st.caption("Recommendations are ranked using your selected filters and demo ratings.")

else:
    display_movies = filtered_movies
    st.subheader(f"🎬 Explore Movies ({len(display_movies)})")

# ================= MOVIE CARDS =================
if not display_movies:
    st.warning("No movies found. Try changing your filters.")

    if section == "❤️ My Watchlist":
        if st.button("🗑️ Clear Entire Watchlist"):
            st.session_state.favorites = []
            save_favorites()
            st.rerun()

else:
    for start in range(0, len(display_movies), 4):
        columns = st.columns(4)

        for column, movie in zip(columns, display_movies[start:start + 4]):
            with column:
                with st.container(border=True):
                    poster = movie["poster"]

                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.markdown(
                            "<div style='height:150px;display:flex;"
                            "align-items:center;justify-content:center;"
                            "font-size:60px'>🎬</div>",
                            unsafe_allow_html=True
                        )

                    st.subheader(movie["name"])
                    st.caption(f"⭐ {movie['rating']}/10 · {movie['year']}")
                    st.write(f"🎭 {movie['genre']}")
                    st.write(f"🌍 {movie['language']}")

                    with st.expander("📖 Movie Details"):
                        st.write(movie["story"])
                        st.write(f"**Release Year:** {movie['year']}")
                        st.write(f"**Rating:** {movie['rating']}/10")

                    is_fav = movie["name"] in st.session_state.favorites

                    label = "💔 Remove" if is_fav else "❤️ Add to Watchlist"

                    if st.button(
                        label,
                        key="favorite_" + movie["name"],
                        use_container_width=True
                    ):
                        if is_fav:
                            st.session_state.favorites.remove(movie["name"])
                        else:
                            st.session_state.favorites.append(movie["name"])

                        save_favorites()
                        st.rerun()

# ================= WATCHLIST MANAGEMENT =================
if section == "❤️ My Watchlist" and st.session_state.favorites:
    st.markdown("---")

    if st.button("🗑️ Clear Entire Watchlist"):
        st.session_state.favorites = []
        save_favorites()
        st.rerun()

# ================= ABOUT PROJECT =================
st.markdown("---")

with st.expander("💡 About CineMatch AI"):
    st.write("""
    **Project:** Movie Recommendation System

    **Technologies:** Python, Streamlit, CSS and JSON.

    **Key Features**
    - Dark and Light themes
    - Genre, language, rating and release-year filters
    - Search and movie sorting
    - Movie detail summaries
    - Favourite watchlist with local JSON persistence
    - Random movie suggestion
    - Top-rated movies
    - Preference-based recommendation ranking
    - Interactive dashboard

    **Note:** This is a demo recommendation application. Movie ratings
    are sample values, and recommendations are based on the local movie
    database rather than a trained machine-learning model.
    """)

st.markdown("---")
st.markdown(
    "<div style='text-align:center;padding:12px'>"
    "<h3>🎬 CineMatch AI</h3>"
    "<p>Your movie night starts here 🍿</p>"
    "<p>Built with Python and Streamlit</p>"
    "</div>",
    unsafe_allow_html=True
)


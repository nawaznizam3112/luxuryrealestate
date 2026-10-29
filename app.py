import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="AUREL | New York Luxury Real Estate",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = Path(__file__).parent / "styles.css"
st.markdown(f"<style>{CSS.read_text()}</style>", unsafe_allow_html=True)

# --- Navigation ---
nav1, nav2, nav3 = st.columns([1.2, 3.8, 1.3], vertical_alignment="center")
with nav1:
    st.markdown('<div class="brand-mark">AUREL<span>.</span></div>', unsafe_allow_html=True)
with nav2:
    st.markdown(
        '<div class="nav-links"><a href="#collections">COLLECTIONS</a><a href="#neighborhoods">NEIGHBORHOODS</a><a href="#journal">JOURNAL</a></div>',
        unsafe_allow_html=True,
    )
with nav3:
    st.markdown('<a class="nav-cta" href="mailto:hello@aurel.example">LET’S TALK <span>↗</span></a>', unsafe_allow_html=True)

st.markdown(
    """
    <section class="hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="eyebrow"><span class="eyebrow-line"></span> THE ART OF LIVING WELL · NEW YORK</div>
        <h1>Space to live.<br><em>Stories to tell.</em></h1>
        <p>Exceptional homes for extraordinary lives.<br>Discover New York, from skyline penthouses to hidden garden retreats.</p>
        <a class="hero-button" href="#collections">EXPLORE THE COLLECTION <span>↘</span></a>
      </div>
      <div class="hero-bottom"><span>40° 45'  ·  NEW YORK CITY</span><span>CURATED PROPERTY, CONSIDERED LIVING</span></div>
      <div class="hero-index">01 <span>/</span> 04</div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Search panel
st.markdown('<div class="search-panel">', unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns([1.6, 1.2, 1.2, 1])
with s1:
    area = st.selectbox("LOCATION", ["All New York", "Manhattan", "Brooklyn", "Queens", "The Hamptons"], label_visibility="visible")
with s2:
    home_type = st.selectbox("PROPERTY TYPE", ["All residences", "Penthouse", "Apartment", "Townhouse", "Villa"], label_visibility="visible")
with s3:
    budget = st.selectbox("PRICE RANGE", ["Any price", "$1M – $3M", "$3M – $6M", "$6M+"], label_visibility="visible")
with s4:
    st.markdown('<div class="search-button-wrap">', unsafe_allow_html=True)
    search_clicked = st.button("FIND A HOME  ↗", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if search_clicked:
    st.session_state["filters"] = (area, home_type, budget)
    st.toast(f"Curating homes for {area} · {home_type} · {budget}", icon="✦")

st.markdown(
    """
    <section class="intro-strip" id="collections">
      <div class="section-kicker">01 — THE COLLECTION</div>
      <div><h2>Homes with a <em>point of view.</em></h2>
      <p>Architectural icons, considered interiors, and addresses that make the city feel like yours.</p></div>
      <div class="intro-note">HANDPICKED<br>NOT MASS-PRODUCED <span>✳</span></div>
    </section>
    """,
    unsafe_allow_html=True,
)

properties = [
    {
        "name": "The Glasshouse",
        "location": "HUDSON YARDS · MANHATTAN",
        "price": "$8,450,000",
        "details": "4 BEDS  ·  4.5 BATHS  ·  3,280 SQ FT",
        "tag": "SKYLINE ICON",
        "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1400&q=85",
        "class": "property-image-one",
    },
    {
        "name": "Park Avenue Residence",
        "location": "UPPER EAST SIDE · MANHATTAN",
        "price": "$5,200,000",
        "details": "3 BEDS  ·  3 BATHS  ·  2,410 SQ FT",
        "tag": "TIMELESS CLASSIC",
        "image": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1400&q=85",
        "class": "property-image-two",
    },
    {
        "name": "The Brooklyn Atelier",
        "location": "BROOKLYN HEIGHTS · BROOKLYN",
        "price": "$3,875,000",
        "details": "3 BEDS  ·  2.5 BATHS  ·  2,060 SQ FT",
        "tag": "DESIGN DISTRICT",
        "image": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1400&q=85",
        "class": "property-image-three",
    },
]

filtered = properties
if "filters" in st.session_state:
    selected_area, selected_type, selected_budget = st.session_state["filters"]
    if selected_area != "All New York":
        filtered = [p for p in filtered if selected_area.upper() in p["location"] or (selected_area == "The Hamptons" and "HAMPTONS" in p["location"])]
    if selected_budget == "$6M+":
        filtered = [p for p in filtered if int(p["price"].replace("$", "").replace(",", "")) >= 6000000]
    elif selected_budget == "$3M – $6M":
        filtered = [p for p in filtered if 3000000 <= int(p["price"].replace("$", "").replace(",", "")) <= 6000000]
    elif selected_budget == "$1M – $3M":
        filtered = [p for p in filtered if 1000000 <= int(p["price"].replace("$", "").replace(",", "")) <= 3000000]
    if selected_type not in ["All residences", "Apartment"]:
        # Demo listings are presented as apartments/residences; the UI remains ready for a real inventory feed.
        filtered = []

if not filtered:
    st.markdown('<div class="empty-state">No exact matches in this edit of the collection. Try a broader search, or contact our team for off-market opportunities.</div>', unsafe_allow_html=True)
else:
    cols = st.columns(3, gap="large")
    for col, p in zip(cols, filtered):
        with col:
            st.markdown(
                f"""
                <article class="property-card">
                  <div class="property-photo" style="background-image:url('{p['image']}')">
                    <span class="property-tag">{p['tag']}</span>
                    <button class="save-heart" aria-label="Save property">♡</button>
                    <div class="photo-count">01 <span>/</span> 06</div>
                  </div>
                  <div class="property-meta"><span>{p['location']}</span><span>↗</span></div>
                  <div class="property-title-row"><h3>{p['name']}</h3><div class="property-price">{p['price']}</div></div>
                  <div class="property-details">{p['details']}</div>
                </article>
                """,
                unsafe_allow_html=True,
            )

st.markdown(
    """
    <section class="manifesto" id="neighborhoods">
      <div class="manifesto-image"></div>
      <div class="manifesto-copy">
        <div class="section-kicker">02 — OUR POINT OF VIEW</div>
        <div class="manifesto-symbol">✳</div>
        <h2>Real estate is<br>personal. <em>So are we.</em></h2>
        <p>We look beyond the listing. We notice the morning light, the neighborhood ritual, the details that make a house feel unmistakably yours.</p>
        <a class="text-link" href="mailto:hello@aurel.example">MEET YOUR AUREL ADVISOR <span>↗</span></a>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="neighborhoods">
      <div class="section-kicker">03 — FIND YOUR NEW YORK</div>
      <div class="neighborhood-heading"><h2>Different worlds.<br><em>One incredible city.</em></h2><p>Every neighborhood has its own rhythm.<br>Find the one that feels like you.</p></div>
      <div class="neighborhood-grid">
        <a class="neighborhood-card n-manhattan" href="#collections"><span>01 / THE ICONIC</span><strong>Manhattan</strong><i>Explore ↗</i></a>
        <a class="neighborhood-card n-brooklyn" href="#collections"><span>02 / THE CREATIVE</span><strong>Brooklyn</strong><i>Explore ↗</i></a>
        <a class="neighborhood-card n-hamptons" href="#collections"><span>03 / THE ESCAPE</span><strong>The Hamptons</strong><i>Explore ↗</i></a>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="journal" id="journal">
      <div class="journal-top"><div class="section-kicker">04 — THE AUREL JOURNAL</div><span>NOTES ON LIVING WELL</span></div>
      <h2>A little more <em>inspiration.</em></h2>
      <div class="journal-grid">
        <div><div class="journal-number">01</div><h3>How to make a city apartment feel like a sanctuary</h3><p>INTERIORS · 6 MIN READ</p></div>
        <div><div class="journal-number">02</div><h3>The new luxury: spaces that give you room to breathe</h3><p>DESIGN · 4 MIN READ</p></div>
        <div><div class="journal-number">03</div><h3>A local’s guide to a slower Sunday in Brooklyn</h3><p>NEIGHBORHOODS · 5 MIN READ</p></div>
      </div>
    </section>
    <footer class="footer">
      <div class="footer-top"><div><div class="brand-mark footer-brand">AUREL<span>.</span></div><p>Live beautifully. Live distinctly.</p></div><div class="footer-big">Your next chapter<br><em>starts here.</em></div></div>
      <div class="footer-bottom"><span>© 2026 AUREL REAL ESTATE</span><span>NEW YORK · EST. WITH INTENTION</span><a href="mailto:hello@aurel.example">GET IN TOUCH ↗</a></div>
    </footer>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="disclaimer">Concept website · Property names, prices, and contact details are illustrative. Replace with verified listings before publishing.</div>',
    unsafe_allow_html=True,
)

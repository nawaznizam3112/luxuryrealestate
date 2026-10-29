
import streamlit as st
from pathlib import Path
from datetime import date, timedelta
import re, json

st.set_page_config(page_title="AUREL | Luxury Real Estate", page_icon="✦", layout="wide")
css = Path(__file__).parent / "styles.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

PROPERTIES = [
 {"id":"AUR-001","title":"The Glasshouse","location":"Hudson Yards, Manhattan","area":"Manhattan","type":"Penthouse","price":8450000,"beds":4,"baths":4.5,"sqft":3280,"status":"Available","featured":True,"description":"A light-filled residence framed by panoramic city views, crafted stone finishes, and expansive entertaining spaces. Fictional demo listing.","amenities":["Panoramic skyline views","Private elevator","Concierge","Fitness studio"],"image":"https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1400&q=85","gallery":["https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&q=85"]},
 {"id":"AUR-002","title":"Park Avenue Residence","location":"Upper East Side, Manhattan","area":"Manhattan","type":"Apartment","price":5200000,"beds":3,"baths":3,"sqft":2410,"status":"Available","featured":True,"description":"A refined city home pairing classic proportions with a warm, contemporary interior palette. Fictional demo listing.","amenities":["Doorman","Private storage","Library lounge","Pet friendly"],"image":"https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1400&q=85","gallery":["https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&q=85"]},
 {"id":"AUR-003","title":"The Brooklyn Atelier","location":"Brooklyn Heights, Brooklyn","area":"Brooklyn","type":"Townhouse","price":3875000,"beds":3,"baths":2.5,"sqft":2060,"status":"Available","featured":False,"description":"An artful urban retreat with tactile materials and generous entertaining space. Fictional demo listing.","amenities":["Private terrace","Chef's kitchen","Bike storage","Garden access"],"image":"https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1400&q=85","gallery":["https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=85"]},
 {"id":"AUR-004","title":"The Hamptons House","location":"East Hampton, The Hamptons","area":"The Hamptons","type":"Villa","price":6950000,"beds":5,"baths":4.5,"sqft":4100,"status":"Available","featured":True,"description":"A calm contemporary escape imagined around indoor-outdoor living. Fictional demo listing.","amenities":["Pool","Garden","Outdoor dining","Guest suite"],"image":"https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1400&q=85","gallery":["https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&q=85"]},
 {"id":"AUR-005","title":"Chelsea Sky Loft","location":"Chelsea, Manhattan","area":"Manhattan","type":"Apartment","price":2750000,"beds":2,"baths":2,"sqft":1530,"status":"Available","featured":False,"description":"A design-forward loft with clean lines and natural light. Fictional demo listing.","amenities":["Rooftop access","Doorman","Laundry","Bike storage"],"image":"https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1400&q=85","gallery":["https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&q=85"]},
 {"id":"AUR-006","title":"Tribeca Corner Residence","location":"Tribeca, Manhattan","area":"Manhattan","type":"Penthouse","price":11200000,"beds":4,"baths":4,"sqft":3650,"status":"Available","featured":True,"description":"A high-floor city residence with considered detailing and downtown views. Fictional demo listing.","amenities":["Private terrace","Concierge","Wine room","Fitness studio"],"image":"https://images.unsplash.com/photo-1600606753086-00f18fb6b3ea?auto=format&fit=crop&w=1400&q=85","gallery":["https://images.unsplash.com/photo-1600606753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1600&q=85","https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1600&q=85"]},
]
for k,v in {"page":"Home","selected":None,"favorites":[],"leads":[],"custom":[],"gallery":{},"admin":False}.items():
    if k not in st.session_state: st.session_state[k]=v

def props(): return PROPERTIES + st.session_state.custom
def getp(pid): return next((p for p in props() if p["id"]==pid),None)
def money(n): return f"${n:,.0f}"
def go(page,pid=None): st.session_state.page=page; st.session_state.selected=pid

def card(p,col):
    with col:
        st.markdown(f'<div class="listing-card"><div class="listing-photo" style="background-image:url(\'{p["image"]}\')"><span class="tag">{p["type"].upper()}</span><span class="pid">{p["id"]}</span></div><div class="location">{p["location"].upper()}</div><div class="listing-title"><h3>{p["title"]}</h3><b>{money(p["price"])}</b></div><div class="facts">{p["beds"]} BEDS · {p["baths"]} BATHS · {p["sqft"]:,} SQ FT</div></div>',unsafe_allow_html=True)
        a,b=st.columns([1.3,1])
        with a:
            if st.button("VIEW PROPERTY ↗",key="view_"+p["id"],use_container_width=True): go("Property details",p["id"]); st.rerun()
        with b:
            saved=p["id"] in st.session_state.favorites
            if st.button("♥ SAVED" if saved else "♡ SAVE",key="save_"+p["id"],use_container_width=True):
                if saved: st.session_state.favorites.remove(p["id"])
                else: st.session_state.favorites.append(p["id"])
                st.rerun()

a,b,c=st.columns([1,3,1])
with a: st.markdown('<div class="brand">AUREL<span>.</span></div>',unsafe_allow_html=True)
with b: st.markdown('<div class="nav-caption">THE ART OF LIVING WELL · NEW YORK</div>',unsafe_allow_html=True)
with c: st.markdown(f'<div class="saved-count">SHORTLIST <b>{len(st.session_state.favorites):02d}</b></div>',unsafe_allow_html=True)
for col,(label,page) in zip(st.columns(5),[]): pass
navcols=st.columns(5)
for col,(label,page) in zip(navcols,[("HOME","Home"),("EXPLORE","Explore"),("SAVED HOMES","Saved homes"),("REQUEST A TOUR","Request a tour"),("ADMIN DEMO","Admin demo")]):
    with col:
        if st.button(label,key="nav_"+page,use_container_width=True): go(page); st.rerun()
st.markdown('<div class="rule"></div>',unsafe_allow_html=True)

if st.session_state.page=="Home":
    st.markdown('<section class="hero"><div class="hero-content"><div class="eyebrow">✳ &nbsp; EXCEPTIONAL HOMES · DISTINCTIVE LIVING</div><h1>Space to live.<br><em>Stories to tell.</em></h1><p>Discover New York through extraordinary residences,<br>architectural icons, and places that feel unmistakably yours.</p><div class="hero-note">CURATED PROPERTY. CONSIDERED LIVING.</div></div><div class="hero-bottom"><span>NEW YORK CITY · 40° 45\'</span><span>01 — THE AUREL COLLECTION</span></div></section>',unsafe_allow_html=True)
    st.markdown('<div class="search-heading">FIND YOUR PLACE <span>THOUGHTFULLY CURATED · ALWAYS PERSONAL</span></div>',unsafe_allow_html=True)
    f1,f2,f3,f4=st.columns([1.3,1.2,1.2,1])
    with f1: area=st.selectbox("NEIGHBORHOOD",["All New York","Manhattan","Brooklyn","The Hamptons"],key="home_area")
    with f2: typ=st.selectbox("PROPERTY TYPE",["All types","Penthouse","Apartment","Townhouse","Villa"],key="home_type")
    with f3: budget=st.selectbox("MAXIMUM PRICE",["No limit","$3M","$6M","$10M"],key="home_budget")
    with f4:
        st.markdown('<div class="button-spacer"></div>',unsafe_allow_html=True)
        if st.button("FIND A HOME ↗",key="home_search",use_container_width=True): st.session_state.filters=(area,typ,budget); go("Explore"); st.rerun()
    st.markdown('<div class="section-intro"><div class="kicker">01 — THE COLLECTION</div><div><h2>Homes with a <em>point of view.</em></h2><p>Architectural icons, considered interiors, and addresses that make the city feel like yours.</p></div><div class="aside">HANDPICKED<br>NOT MASS-PRODUCED ✳</div></div>',unsafe_allow_html=True)
    cols=st.columns(3,gap="large")
    for p,col in zip([p for p in props() if p.get("featured")][:3],cols): card(p,col)
    st.markdown('<section class="manifesto"><div class="manifesto-image"></div><div class="manifesto-copy"><div class="kicker">02 — OUR POINT OF VIEW</div><div class="symbol">✳</div><h2>Real estate is<br>personal. <em>So are we.</em></h2><p>We look beyond the listing. We notice the morning light, the neighborhood ritual, the details that make a house feel unmistakably yours.</p></div></section><div class="section-intro"><div class="kicker">03 — FIND YOUR NEW YORK</div><div><h2>Different worlds.<br><em>One incredible city.</em></h2><p>Every neighborhood has its own rhythm. Find the one that feels like you.</p></div></div>',unsafe_allow_html=True)
    ncols=st.columns(3)
    for col,(name,img,tag) in zip(ncols,[("Manhattan","https://images.unsplash.com/photo-1518391846015-55a9cc003b25?auto=format&fit=crop&w=1000&q=85","THE ICONIC"),("Brooklyn","https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1000&q=85","THE CREATIVE"),("The Hamptons","https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1000&q=85","THE ESCAPE")]):
        with col:
            st.markdown(f'<div class="neighborhood" style="background-image:linear-gradient(0deg,rgba(8,20,17,.8),rgba(8,20,17,.05)),url({img})"><span>{tag}</span><strong>{name}</strong></div>',unsafe_allow_html=True)
            if st.button(f"EXPLORE {name.upper()} ↗",key="area_"+name,use_container_width=True): st.session_state.filters=(name,"All types","No limit"); go("Explore"); st.rerun()
    st.markdown('<section class="journal"><div class="kicker">04 — THE AUREL JOURNAL</div><h2>A little more <em>inspiration.</em></h2><div class="journal-grid"><div><span>01 / INTERIORS</span><h3>Make a city apartment feel like a sanctuary</h3><p>Designing a calmer everyday, right in the middle of it all.</p></div><div><span>02 / DESIGN</span><h3>The new luxury: spaces that let you breathe</h3><p>Thoughtful materials, natural light, and room to simply be.</p></div><div><span>03 / NEIGHBORHOODS</span><h3>A local guide to a slower Sunday in Brooklyn</h3><p>Independent coffee, quiet streets, and the art of taking your time.</p></div></div></section>',unsafe_allow_html=True)

elif st.session_state.page=="Explore":
    st.markdown('<div class="page-hero"><div class="kicker">THE AUREL COLLECTION</div><h1>Find your <em>somewhere.</em></h1><p>Explore residences chosen for their character, craft, and sense of place.</p></div>',unsafe_allow_html=True)
    defaults=st.session_state.get("filters",("All New York","All types","No limit"))
    f1,f2,f3,f4=st.columns([1.25,1.2,1.2,1])
    with f1: area=st.selectbox("LOCATION",["All New York","Manhattan","Brooklyn","The Hamptons"],index=["All New York","Manhattan","Brooklyn","The Hamptons"].index(defaults[0]) if defaults[0] in ["All New York","Manhattan","Brooklyn","The Hamptons"] else 0,key="explore_area")
    with f2: typ=st.selectbox("PROPERTY TYPE",["All types","Penthouse","Apartment","Townhouse","Villa"],index=["All types","Penthouse","Apartment","Townhouse","Villa"].index(defaults[1]) if defaults[1] in ["All types","Penthouse","Apartment","Townhouse","Villa"] else 0,key="explore_type")
    with f3: budget=st.selectbox("MAXIMUM PRICE",["No limit","$3M","$6M","$10M"],index=["No limit","$3M","$6M","$10M"].index(defaults[2]) if defaults[2] in ["No limit","$3M","$6M","$10M"] else 0,key="explore_budget")
    with f4: beds=st.selectbox("MIN. BEDROOMS",["Any","1+","2+","3+","4+"],key="explore_beds")
    query=st.text_input("SEARCH NAME OR NEIGHBORHOOD",placeholder="Try Tribeca, Glasshouse, Brooklyn…")
    results=[p for p in props() if p["status"]=="Available"]
    if area!="All New York": results=[p for p in results if area.lower() in p["location"].lower() or area.lower() in p["area"].lower()]
    if typ!="All types": results=[p for p in results if p["type"]==typ]
    max_price={"$3M":3000000,"$6M":6000000,"$10M":10000000}.get(budget)
    if max_price: results=[p for p in results if p["price"]<=max_price]
    if beds!="Any": results=[p for p in results if p["beds"]>=int(beds[0])]
    if query.strip(): results=[p for p in results if query.lower() in (p["title"]+" "+p["location"]+" "+p["description"]).lower()]
    st.markdown(f'<div class="result-count">{len(results)} RESIDENCES · CURATED FOR YOU</div>',unsafe_allow_html=True)
    if results:
        for start in range(0,len(results),3):
            cols=st.columns(3,gap="large")
            for p,col in zip(results[start:start+3],cols): card(p,col)
    else:
        st.info("No exact matches. Try widening the filters or request a personal search.")
        if st.button("REQUEST A PERSONAL SEARCH ↗"): go("Request a tour"); st.rerun()

elif st.session_state.page=="Property details":
    p=getp(st.session_state.selected)
    if not p:
        st.warning("Property not found.")
        if st.button("Back to collection"): go("Explore"); st.rerun()
    else:
        st.markdown(f'<div class="detail-top">{p["id"]} · {p["location"].upper()} <span>{p["type"].upper()}</span></div><div class="detail-heading"><h1>{p["title"]}</h1><div><small>ASKING PRICE</small><br><strong>{money(p["price"])}</strong></div></div>',unsafe_allow_html=True)
        idx=st.session_state.gallery.get(p["id"],0)
        st.image(p["gallery"][idx],use_container_width=True)
        gc=st.columns(4)
        for i,col in enumerate(gc[:3]):
            with col:
                if st.button(f"PHOTO {i+1:02d}",key=f"photo_{p['id']}_{i}",use_container_width=True): st.session_state.gallery[p["id"]]=i; st.rerun()
        with gc[3]: st.markdown(f'<div class="gallery-label">IMAGE {idx+1:02d} / {len(p["gallery"]):02d}</div>',unsafe_allow_html=True)
        facts=st.columns(4)
        for col,label,value in zip(facts,["BEDROOMS","BATHROOMS","INTERIOR","STATUS"],[p["beds"],p["baths"],f'{p["sqft"]:,} SQ FT',p["status"]]):
            with col: st.markdown(f'<div class="fact"><span>{label}</span><strong>{value}</strong></div>',unsafe_allow_html=True)
        left,right=st.columns([1.5,1])
        with left:
            st.markdown('<div class="kicker">THE RESIDENCE</div>',unsafe_allow_html=True)
            st.markdown(f'<div class="description">{p["description"]}</div><div class="kicker">CONSIDERED DETAILS</div>',unsafe_allow_html=True)
            for item in p["amenities"]: st.markdown(f'<div class="amenity">✳ &nbsp; {item}</div>',unsafe_allow_html=True)
        with right:
            st.markdown('<div class="inquiry-box"><div class="kicker">MAKE IT PERSONAL</div><h3>Could this be <em>your place?</em></h3><p>Send a demo inquiry. No email is sent.</p></div>',unsafe_allow_html=True)
            with st.form("property_inquiry"):
                name=st.text_input("Your name"); email=st.text_input("Email address"); phone=st.text_input("Phone (optional)")
                message=st.text_area("Message",value=f"I'm interested in {p['title']} ({p['id']}).")
                submit=st.form_submit_button("SEND PROPERTY INQUIRY ↗",use_container_width=True)
                if submit:
                    if not name.strip() or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$",email.strip()): st.error("Enter your name and a valid email address.")
                    else:
                        st.session_state.leads.append({"kind":"Property inquiry","property_id":p["id"],"name":name,"email":email,"phone":phone,"message":message,"date":str(date.today())})
                        st.success("Demo inquiry saved to this session.")
        a,b=st.columns(2)
        with a:
            if st.button("← BACK TO COLLECTION",use_container_width=True): go("Explore"); st.rerun()
        with b:
            saved=p["id"] in st.session_state.favorites
            if st.button("♥ REMOVE FROM SAVED" if saved else "♡ SAVE THIS RESIDENCE",use_container_width=True):
                if saved: st.session_state.favorites.remove(p["id"])
                else: st.session_state.favorites.append(p["id"])
                st.rerun()

elif st.session_state.page=="Saved homes":
    st.markdown('<div class="page-hero"><div class="kicker">YOUR PERSONAL COLLECTION</div><h1>Saved <em>residences.</em></h1><p>Your shortlist of places that caught your eye.</p></div>',unsafe_allow_html=True)
    saved=[getp(pid) for pid in st.session_state.favorites]; saved=[p for p in saved if p]
    if not saved:
        st.info("Your shortlist is empty. Save a residence from Explore.")
        if st.button("EXPLORE RESIDENCES ↗"): go("Explore"); st.rerun()
    else:
        cols=st.columns(3,gap="large")
        for p,col in zip(saved,cols): card(p,col)
        if st.button("CLEAR SHORTLIST"): st.session_state.favorites=[]; st.rerun()

elif st.session_state.page=="Request a tour":
    st.markdown('<div class="page-hero"><div class="kicker">A MORE PERSONAL APPROACH</div><h1>Let’s find your <em>somewhere.</em></h1><p>Demo form: requests are kept only in the current session.</p></div>',unsafe_allow_html=True)
    with st.form("tour_request"):
        c1,c2=st.columns(2)
        with c1:
            name=st.text_input("FULL NAME *"); email=st.text_input("EMAIL ADDRESS *"); phone=st.text_input("PHONE NUMBER")
            interest=st.selectbox("I AM INTERESTED IN",["Buying a property","Renting a property","Selling a property","Private consultation"])
        with c2:
            area=st.selectbox("PREFERRED AREA",["Any New York","Manhattan","Brooklyn","The Hamptons"])
            typ=st.selectbox("PROPERTY TYPE",["Any type","Penthouse","Apartment","Townhouse","Villa"])
            budget=st.selectbox("BUDGET",["Prefer to discuss","Under $3M","$3M–$6M","$6M–$10M","$10M+"])
            viewing=st.date_input("PREFERRED VIEWING DATE",value=date.today()+timedelta(days=7),min_value=date.today())
        message=st.text_area("ANYTHING ELSE WE SHOULD KNOW?")
        consent=st.checkbox("I agree to be contacted about this request.")
        submit=st.form_submit_button("REQUEST A PRIVATE CONSULTATION ↗",use_container_width=True)
        if submit:
            if not name.strip() or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$",email.strip()): st.error("Please enter your name and a valid email address.")
            elif not consent: st.error("Please confirm we may contact you.")
            else:
                st.session_state.leads.append({"kind":"Tour request","name":name,"email":email,"phone":phone,"interest":interest,"area":area,"property_type":typ,"budget":budget,"preferred_date":str(viewing),"message":message,"date":str(date.today())})
                st.success("Demo request saved for this session. No email or booking was sent."); st.balloons()

elif st.session_state.page=="Admin demo":
    st.markdown('<div class="page-hero"><div class="kicker">PRIVATE WORKSPACE · DEMO</div><h1>Manage the <em>collection.</em></h1><p>Prototype admin only, not production authentication.</p></div>',unsafe_allow_html=True)
    st.warning("Demo only: this password gate is not secure production authentication.")
    if not st.session_state.admin:
        with st.form("admin_login"):
            password=st.text_input("DEMO ACCESS CODE",type="password")
            if st.form_submit_button("UNLOCK DEMO DASHBOARD"):
                if password=="aurel-demo": st.session_state.admin=True; st.rerun()
                else: st.error("Incorrect code. Hint: aurel-demo")
    else:
        a,b,c=st.columns(3); a.metric("AVAILABLE LISTINGS",len([p for p in props() if p["status"]=="Available"])); b.metric("SAVED HOMES",len(st.session_state.favorites)); c.metric("SESSION LEADS",len(st.session_state.leads))
        st.markdown("### Add a demo listing")
        with st.form("add_listing"):
            title=st.text_input("Property title"); location=st.text_input("Location",value="Manhattan, New York"); typ=st.selectbox("Property type",["Penthouse","Apartment","Townhouse","Villa"])
            price=st.number_input("Price (USD)",min_value=100000,value=3500000,step=50000); beds=st.number_input("Bedrooms",min_value=0,max_value=20,value=3); baths=st.number_input("Bathrooms",min_value=0.0,max_value=20.0,value=2.5,step=.5); sqft=st.number_input("Interior square feet",min_value=100,value=2000,step=50)
            image_url=st.text_input("Image URL",value=PROPERTIES[0]["image"]); description=st.text_area("Description")
            if st.form_submit_button("ADD TO SESSION COLLECTION ↗",use_container_width=True):
                if not title.strip() or not location.strip() or not image_url.startswith(("https://","http://")): st.error("Enter title, location, and a valid image URL.")
                else:
                    pid=f"AUR-D{len(st.session_state.custom)+1:03d}"
                    st.session_state.custom.append({"id":pid,"title":title.strip(),"location":location.strip(),"area":location.strip(),"type":typ,"price":int(price),"beds":int(beds),"baths":float(baths),"sqft":int(sqft),"status":"Available","featured":True,"description":description or "Added in demo admin.","amenities":["Private consultation available"],"image":image_url,"gallery":[image_url,PROPERTIES[1]["image"],PROPERTIES[2]["image"]]})
                    st.success(f"{pid} added to this session."); st.rerun()
        st.markdown("### Manage listing status")
        for p in props():
            with st.expander(f'{p["id"]} · {p["title"]} · {money(p["price"])}'):
                statuses=["Available","Reserved","Sold","Rented"]
                status=st.selectbox("Status",statuses,index=statuses.index(p["status"]) if p["status"] in statuses else 0,key="status_"+p["id"])
                if st.button("UPDATE STATUS",key="update_"+p["id"]): p["status"]=status; st.rerun()
        st.markdown("### Session inquiries")
        if st.session_state.leads:
            st.dataframe(st.session_state.leads,use_container_width=True,hide_index=True)
            st.download_button("DOWNLOAD INQUIRIES JSON",json.dumps(st.session_state.leads,indent=2),file_name="aurel_demo_inquiries.json",mime="application/json")
        else: st.info("No inquiries submitted yet.")
        if st.button("LOCK ADMIN DEMO"): st.session_state.admin=False; st.rerun()

st.markdown('<footer class="site-footer"><div class="footer-main"><div><div class="brand footer-brand">AUREL<span>.</span></div><p>Live beautifully. Live distinctly.</p></div><div class="footer-closer">Your next chapter<br><em>starts here.</em></div></div><div class="footer-bottom"><span>© 2026 AUREL REAL ESTATE</span><span>NEW YORK · EST. WITH INTENTION</span><span>ILLUSTRATIVE DEMO LISTINGS</span></div></footer><div class="demo-note">Prototype only · Sample listings and prices are fictional. Changes and requests are session-only. No emails or bookings are sent.</div>',unsafe_allow_html=True)

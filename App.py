import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Golf Shot Tracker", layout="wide")

# 1. INITIALIZE SESSION STATE (For Undo Functionality)
if "shots" not in st.session_state:
    st.session_state.shots = []  # Stores history of plotted shots

# 2. TOP HUD: HOLE YARDAGE, PAR, AND HANDICAP
st.title("⛳ Golf Shot Tracker")

col1, col2, col3, col4 = st.columns(4)

with col1:
    hole_num = st.number_input("Hole #", min_value=1, max_value=18, value=7)
with col2:
    hole_par = st.number_input("Par", min_value=3, max_value=5, value=4)
with col3:
    hole_yardage = st.number_input("Yardage", min_value=50, max_value=700, value=415)
with col4:
    hole_hcp = st.number_input("Handicap (HCP)", min_value=1, max_value=18, value=5)

st.divider()

# 3. CONTROL BUTTONS (UNDO & RESET)
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 1, 1])

with ctrl_col1:
    st.subheader(f"Hole {hole_num} — Total: {hole_yardage} Yds (Par {hole_par}, HCP {hole_hcp})")

with ctrl_col2:
    # UNDO BUTTON LOGIC
    if st.button("↩️ Undo Last Shot", use_container_width=True):
        if len(st.session_state.shots) > 0:
            st.session_state.shots.pop()  # Remove last shot
            st.rerun()
        else:
            st.warning("No shots to undo!")

with ctrl_col3:
    # RESET HOLE LOGIC
    if st.button("🗑️ Reset Hole", use_container_width=True):
        st.session_state.shots = []
        st.rerun()

# 4. SHOT INPUT / PLOTTING SECTION
st.write("### Plot Shot")

input_col1, input_col2 = st.columns(2)

with input_col1:
    club = st.selectbox("Select Club Used", ["Driver", "3-Wood", "5-Iron", "7-Iron", "Pitching Wedge", "Putter"])
with input_col2:
    dist_hit = st.number_input("Distance Hit (Yards)", min_value=1, max_value=400, value=220)

if st.button("📍 Record Shot", type="primary", use_container_width=True):
    # Calculate distance remaining based on total yardage and previous shots
    previous_total = sum(s["Distance"] for s in st.session_state.shots)
    remaining = max(0, hole_yardage - (previous_total + dist_hit))
    
    shot_entry = {
        "Shot #": len(st.session_state.shots) + 1,
        "Club": club,
        "Distance": dist_hit,
        "Remaining": remaining
    }
    st.session_state.shots.append(shot_entry)
    st.rerun()

# 5. DISPLAY SHOT HISTORY TABLE
st.divider()
st.write("### Shot Log")

if len(st.session_state.shots) > 0:
    df = pd.DataFrame(st.session_state.shots)
    st.dataframe(df, use_container_width=True)
    
    current_remaining = st.session_state.shots[-1]["Remaining"]
    if current_remaining == 0:
        st.success("🎉 Ball is on the green / holed out!")
    else:
        st.info(f"**Distance Remaining to Pin:** {current_remaining} yards")
else:
    st.caption("No shots plotted yet. Use the control above to record your tee shot.")

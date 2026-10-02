import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Golf Shot Tracker & Scorecard",
    layout="centered"
)

# Initialize Session State Variables
if "course_info" not in st.session_state:
    st.session_state.course_info = {
        "course_name": "",
        "tee_color": "White",
        "yardage": 6200,
        "slope_rating": 120,
        "date": datetime.date.today()
    }

if "hole_data" not in st.session_state:
    st.session_state.hole_data = {
        h: {
            "par": 4,
            "strokes": 4,
            "putts": 2,
            "fairway_hit": "N/A",
            "gir": True,
            "shots": []
        }
        for h in range(1, 19)
    }

# Saved/Preset Courses Database
PRESET_COURSES = [
    "Select a Course or Type New Below...",
    "Pebble Beach Golf Links",
    "Augusta National Golf Club",
    "Torrey Pines (South)",
    "Bethpage Black",
    "TPC Sawgrass"
]

# Tracking Codes & Labels
LIE_CODES = {
    "T": "Tee",
    "F": "Fairway",
    "R": "Rough",
    "B": "Bunker",
    "G": "Green",
    "P": "Penalty Area",
    "N": "Native/Trees"
}

QUALITY_CODES = {
    "G": "Great",
    "M": "Decent",
    "H": "Hook",
    "S": "Slice/Push",
    "F": "Fat",
    "T": "Thin"
}


# ============================================================
# SHOT PLOT FUNCTION
# ============================================================

def draw_shot_plot(shots):
    """
    Creates a visual shot-flow diagram from the logged shots.

    Current shot data contains lie-to-lie information rather than
    GPS/coordinate information, so this is a sequential shot plot.
    """

    if not shots:
        st.info("Log shots to see the shot plot.")
        return

    # Extract information from stored shot dictionaries
    shot_numbers = []
    from_lies = []
    to_lies = []
    qualities = []

    for shot in shots:
        shot_numbers.append(shot["number"])
        from_lies.append(shot["from"])
        to_lies.append(shot["to"])
        qualities.append(shot["quality"])

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 3.8))

    # Position of each lie type
    lie_positions = {
        "T": 0,
        "F": 1,
        "R": 2,
        "B": 3,
        "N": 4,
        "P": 5,
        "G": 6
    }

    # Display labels
    lie_labels = {
        0: "Tee",
        1: "Fairway",
        2: "Rough",
        3: "Bunker",
        4: "Trees / Native",
        5: "Penalty",
        6: "Green"
    }

    # Draw each shot as a connection from starting lie to ending lie
    for i, shot in enumerate(shots):

        start_x = i
        end_x = i + 1

        start_y = lie_positions.get(shot["from"], 0)
        end_y = lie_positions.get(shot["to"], 0)

        # Draw connecting line
        ax.plot(
            [start_x, end_x],
            [start_y, end_y],
            linewidth=2
        )

        # Starting point
        ax.scatter(
            start_x,
            start_y,
            s=250,
            zorder=3
        )

        # Ending point
        ax.scatter(
            end_x,
            end_y,
            s=250,
            zorder=3
        )

        # Shot number
        ax.text(
            start_x,
            start_y,
            str(shot["number"]),
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold"
        )

        # Quality label above the shot
        ax.text(
            start_x + 0.5,
            (start_y + end_y) / 2 + 0.25,
            QUALITY_CODES.get(
                shot["quality"],
                shot["quality"]
            ),
            ha="center",
            va="center",
            fontsize=8
        )

    # Label final point
    if shots:
        final_shot = shots[-1]
        final_x = len(shots)
        final_y = lie_positions.get(final_shot["to"], 0)

        ax.scatter(
            final_x,
            final_y,
            s=250,
            zorder=3
        )

        ax.text(
            final_x,
            final_y,
            "✓",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold"
        )

    # Formatting
    ax.set_yticks(list(lie_labels.keys()))
    ax.set_yticklabels(list(lie_labels.values()))

    ax.set_xticks(range(len(shots) + 1))
    ax.set_xticklabels(
        ["Start"] +
        [f"Shot {i}" for i in range(1, len(shots) + 1)]
    )

    ax.set_title(
        "Shot Plot — Lie-to-Lie Sequence",
        fontsize=13,
        fontweight="bold"
    )

    ax.set_xlim(-0.5, len(shots) + 0.5)
    ax.set_ylim(-0.6, 6.6)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# NAVIGATION SIDEBAR
# ============================================================

page_options = (
    ["Page 1: Course Info"]
    + [f"Hole {i}" for i in range(1, 19)]
    + ["Page 19: The 19th Hole (Official Scorecard)"]
)

selected_page = st.sidebar.radio(
    "Navigation",
    page_options
)


# ============================================================
# PAGE 1: COURSE INFO
# ============================================================

if selected_page == "Page 1: Course Info":

    st.title("⛳ Course Info & Round Setup")

    st.markdown(
        "Enter or select course details before starting your round."
    )

    with st.form("course_setup_form"):

        selected_preset = st.selectbox(
            "Previously Played Courses",
            PRESET_COURSES
        )

        custom_course = st.text_input(
            "Or Type New Course Name",
            value=""
            if selected_preset != PRESET_COURSES[0]
            else st.session_state.course_info["course_name"]
        )

        course_name = (
            custom_course
            if custom_course
            else (
                selected_preset
                if selected_preset != PRESET_COURSES[0]
                else "Local Municipal GC"
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            tee_color = st.selectbox(
                "Tee Color",
                ["Black", "Blue", "White", "Gold", "Red"],
                index=2
            )

            total_yardage = st.number_input(
                "Total Yardage",
                min_value=1000,
                max_value=8000,
                value=int(
                    st.session_state.course_info["yardage"]
                ),
                step=50
            )

        with col2:

            slope_rating = st.number_input(
                "Slope Rating",
                min_value=55,
                max_value=155,
                value=int(
                    st.session_state.course_info["slope_rating"]
                ),
                step=1
            )

            play_date = st.date_input(
                "Date Played",
                value=st.session_state.course_info["date"]
            )

        save_btn = st.form_submit_button(
            "Save Course Setup & Start Round"
        )

        if save_btn:

            st.session_state.course_info = {
                "course_name": course_name,
                "tee_color": tee_color,
                "yardage": total_yardage,
                "slope_rating": slope_rating,
                "date": play_date
            }

            st.success(
                f"Course setup saved for **{course_name}**! "
                "Proceed to Hole 1 in the sidebar."
            )


# ============================================================
# PAGES 2-18: HOLE-BY-HOLE TRACKING
# ============================================================

elif selected_page.startswith("Hole"):

    hole_num = int(
        selected_page.split(" ")[1]
    )

    st.title(f"⛳ Hole {hole_num}")

    hole_dict = st.session_state.hole_data[hole_num]

    # --------------------------------------------------------
    # HOLE CONFIGURATION
    # --------------------------------------------------------

    col_par, col_score, col_putts = st.columns(3)

    with col_par:

        par = st.selectbox(
            "Par",
            [3, 4, 5],
            index=(
                1
                if hole_dict["par"] == 4
                else (
                    0
                    if hole_dict["par"] == 3
                    else 2
                )
            ),
            key=f"par_{hole_num}"
        )

    with col_score:

        strokes = st.number_input(
            "Total Strokes",
            min_value=1,
            max_value=15,
            value=hole_dict["strokes"],
            key=f"str_{hole_num}"
        )

    with col_putts:

        putts = st.number_input(
            "Putts",
            min_value=0,
            max_value=10,
            value=hole_dict["putts"],
            key=f"putt_{hole_num}"
        )

    # --------------------------------------------------------
    # STAT INDICATORS
    # --------------------------------------------------------

    col_fw, col_gir = st.columns(2)

    with col_fw:

        if par > 3:

            fw_hit = st.radio(
                "Fairway Hit?",
                ["Yes", "No"],
                index=(
                    0
                    if hole_dict["fairway_hit"] == "Yes"
                    else 1
                ),
                key=f"fw_{hole_num}",
                horizontal=True
            )

        else:

            fw_hit = "N/A"

            st.info(
                "Fairway hit: N/A (Par 3)"
            )

    with col_gir:

        gir_hit = st.checkbox(
            "Green in Regulation (GIR)",
            value=hole_dict["gir"],
            key=f"gir_{hole_num}"
        )

    st.markdown("---")

    # ========================================================
    # SHOT TRACKING
    # ========================================================

    st.subheader("🏌️ Shot-by-Shot Tracking")

    c_start, c_end, c_qual = st.columns(3)

    with c_start:

        from_lie = st.selectbox(
            "From Lie",
            list(LIE_CODES.keys()),
            format_func=lambda x:
                f"{x} - {LIE_CODES[x]}",
            key=f"flie_{hole_num}"
        )

    with c_end:

        to_lie = st.selectbox(
            "To Lie",
            list(LIE_CODES.keys()),
            format_func=lambda x:
                f"{x} - {LIE_CODES[x]}",
            key=f"tlie_{hole_num}"
        )

    with c_qual:

        shot_qual = st.selectbox(
            "Shot Quality",
            list(QUALITY_CODES.keys()),
            format_func=lambda x:
                f"{x} - {QUALITY_CODES[x]}",
            key=f"sq_{hole_num}"
        )

    if st.button(
        "➕ Log Shot",
        key=f"add_shot_{hole_num}"
    ):

        shot_entry = {
            "number": len(hole_dict["shots"]) + 1,
            "from": from_lie,
            "to": to_lie,
            "quality": shot_qual
        }

        hole_dict["shots"].append(
            shot_entry
        )

        st.success(
            f"Shot {shot_entry['number']} added!"
        )

        st.rerun()

    # ========================================================
    # SHOT PLOT
    # ========================================================

    if hole_dict["shots"]:

        st.markdown("---")

        st.subheader("📍 Shot Plot")

        draw_shot_plot(
            hole_dict["shots"]
        )

        # ----------------------------------------------------
        # SHOT SUMMARY
        # ----------------------------------------------------

        st.markdown("### Shot Sequence")

        sequence = []

        # First starting lie
        sequence.append(
            LIE_CODES[
                hole_dict["shots"][0]["from"]
            ]
        )

        for shot in hole_dict["shots"]:

            sequence.append(
                LIE_CODES[shot["to"]]
            )

        st.markdown(
            " → ".join(sequence)
        )

        # ----------------------------------------------------
        # LOGGED SHOTS
        # ----------------------------------------------------

        st.markdown("### Logged Shots")

        for shot in hole_dict["shots"]:

            st.write(
                f"**Shot {shot['number']}:** "
                f"[{shot['from']}] "
                f"{LIE_CODES[shot['from']]} "
                f"➜ "
                f"[{shot['to']}] "
                f"{LIE_CODES[shot['to']]} "
                f"| Quality: "
                f"[{shot['quality']}] "
                f"{QUALITY_CODES[shot['quality']]}"
            )

        if st.button(
            "🗑️ Clear Shots",
            key=f"clr_{hole_num}"
        ):

            hole_dict["shots"] = []

            st.rerun()

    else:

        st.info(
            "No shots logged yet. "
            "Use the controls above to log your first shot."
        )

    # --------------------------------------------------------
    # SAVE HOLE STATE
    # --------------------------------------------------------

    st.session_state.hole_data[hole_num].update({

        "par": par,

        "strokes": strokes,

        "putts": putts,

        "fairway_hit": fw_hit,

        "gir": gir_hit

    })


# ============================================================
# PAGE 19: OFFICIAL SCORECARD
# ============================================================

elif selected_page.startswith("Page 19"):

    st.title(
        "🏆 The 19th Hole: Official Scorecard"
    )

    info = st.session_state.course_info

    st.markdown(
        f"""
        ### **Course:** {
            info['course_name']
            if info['course_name']
            else 'Not Specified'
        }

        **Date:** {info['date']} |
        **Tees:** {info['tee_color']} |
        **Yardage:** {info['yardage']} yds |
        **Slope:** {info['slope_rating']}
        """
    )

    st.markdown("---")

    # --------------------------------------------------------
    # BUILD SCORECARD
    # --------------------------------------------------------

    rows = []

    tot_par = 0
    tot_strokes = 0
    tot_putts = 0

    fw_possible = 0
    fw_hit_count = 0

    gir_count = 0

    for h in range(1, 19):

        hd = st.session_state.hole_data[h]

        tot_par += hd["par"]
        tot_strokes += hd["strokes"]
        tot_putts += hd["putts"]

        if hd["par"] > 3:

            fw_possible += 1

            if hd["fairway_hit"] == "Yes":
                fw_hit_count += 1

        if hd["gir"]:
            gir_count += 1

        rows.append({

            "Hole": h,

            "Par": hd["par"],

            "Score": hd["strokes"],

            "To Par":
                hd["strokes"] - hd["par"],

            "Putts": hd["putts"],

            "Fairway":
                hd["fairway_hit"],

            "GIR":
                "Yes" if hd["gir"] else "No"

        })

    df = pd.DataFrame(rows)

    # --------------------------------------------------------
    # FRONT / BACK 9
    # --------------------------------------------------------

    f9_par = df.iloc[0:9]["Par"].sum()
    f9_score = df.iloc[0:9]["Score"].sum()

    b9_par = df.iloc[9:18]["Par"].sum()
    b9_score = df.iloc[9:18]["Score"].sum()

    # --------------------------------------------------------
    # STAT HIGHLIGHTS
    # --------------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Total Score",
        f"{tot_strokes}",
        f"{tot_strokes - tot_par:+d}"
    )

    m2.metric(
        "Total Putts",
        f"{tot_putts}"
    )

    m3.metric(
        "Fairways Hit",
        (
            f"{fw_hit_count}/{fw_possible}"
            if fw_possible > 0
            else "N/A"
        )
    )

    m4.metric(
        "GIR %",
        f"{int((gir_count / 18) * 100)}%"
    )

    st.markdown(
        "### 📊 Round Breakdown"
    )

    col_f9, col_b9 = st.columns(2)

    with col_f9:

        st.write(
            f"**Front 9 Score:** "
            f"{f9_score} "
            f"(Par {f9_par})"
        )

    with col_b9:

        st.write(
            f"**Back 9 Score:** "
            f"{b9_score} "
            f"(Par {b9_par})"
        )

    # --------------------------------------------------------
    # SCORECARD
    # --------------------------------------------------------

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="📥 Download Official Round CSV",

        data=csv_data,

        file_name=(
            f"Scorecard_"
            f"{info['course_name'].replace(' ', '_')}_"
            f"{info['date']}.csv"
        ),

        mime="text/csv"

    )

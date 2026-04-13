import streamlit as st

st.set_page_config(page_title="UW CoFounder Search", page_icon="🤝", layout="wide")

# -----------------------------
# HARDCODED SAMPLE FOUNDER DATA
# -----------------------------
FOUNDER_POOL = [
    {
        "name": "Alex Kim",
        "department": "Allen School",
        "role": "Engineer",
        "looking_for": "PM",
        "hours": "10-15",
        "style": "Talk over coffee",
        "goal": "Start something",
        "bio": "Built side projects before and likes structured collaboration.",
    },
    {
        "name": "Maya Patel",
        "department": "Foster Business",
        "role": "PM",
        "looking_for": "Engineer",
        "hours": "10-15",
        "style": "Address it bluntly",
        "goal": "Start something",
        "bio": "Strong at user research, pitching, and driving execution.",
    },
    {
        "name": "Jordan Lee",
        "department": "HCDE/Design",
        "role": "Designer",
        "looking_for": "Engineer",
        "hours": "5-10",
        "style": "Talk over coffee",
        "goal": "Join a team",
        "bio": "Interested in building polished user experiences and MVPs.",
    },
    {
        "name": "Sonia Rao",
        "department": "Allen School",
        "role": "Data/AI",
        "looking_for": "Business",
        "hours": "15+",
        "style": "Address it bluntly",
        "goal": "Explore",
        "bio": "Works on AI projects and enjoys experimenting with new ideas.",
    },
    {
        "name": "Ethan Brooks",
        "department": "Other",
        "role": "Business",
        "looking_for": "Designer",
        "hours": "5-10",
        "style": "Let it settle naturally",
        "goal": "Join a team",
        "bio": "Good at partnerships, outreach, and storytelling.",
    },
]

ROLE_OPTIONS = ["Engineer", "PM", "Designer", "Business", "Data/AI"]
DEPT_OPTIONS = ["Allen School", "Foster Business", "HCDE/Design", "Other"]
HOURS_OPTIONS = ["<5", "5-10", "10-15", "15+"]
STYLE_OPTIONS = ["Address it bluntly", "Talk over coffee", "Let it settle naturally"]
GOAL_OPTIONS = ["Start something", "Join a team", "Explore"]

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def hours_to_value(hours: str) -> int:
    mapping = {"<5": 1, "5-10": 2, "10-15": 3, "15+": 4}
    return mapping.get(hours, 0)

def score_match(user, candidate):
    score = 0
    reasons = []
    risks = []

    # 1. Role complementarity: 40 points
    if user["looking_for"] == candidate["role"]:
        score += 25
        reasons.append(f"They are the exact role you are looking for: {candidate['role']}.")
    elif user["role"] != candidate["role"]:
        score += 15
        reasons.append("They bring a complementary role to your profile.")
    else:
        score += 5
        risks.append("You have similar roles, so the team may need more skill diversity.")

    if candidate["looking_for"] == user["role"]:
        score += 15
        reasons.append("They are also looking for someone with your role.")

    # 2. Commitment alignment: 25 points
    user_hours = hours_to_value(user["hours"])
    candidate_hours = hours_to_value(candidate["hours"])
    hour_diff = abs(user_hours - candidate_hours)

    if hour_diff == 0:
        score += 20
        reasons.append("Your weekly time commitment is strongly aligned.")
    elif hour_diff == 1:
        score += 12
        reasons.append("Your time commitment is reasonably aligned.")
    else:
        score += 4
        risks.append("Your expected weekly commitment may not be fully aligned.")

    if user["goal"] == candidate["goal"]:
        score += 5
        reasons.append(f"You both have a similar current goal: {user['goal']}.")
    else:
        risks.append("Your current goals may differ.")

    # 3. Collaboration style: 15 points
    if user["style"] == candidate["style"]:
        score += 15
        reasons.append("You share a similar collaboration style.")
    else:
        score += 5
        risks.append("You may approach conflict or collaboration differently.")

    # 4. Department diversity / context: 10 points
    if user["department"] != candidate["department"]:
        score += 10
        reasons.append("You bring cross-department perspective, which can strengthen startup teams.")
    else:
        score += 5
        reasons.append("You share similar academic context.")

    # 5. Basic fit polish: 10 points
    if user["goal"] == "Start something" and candidate["goal"] in ["Start something", "Join a team"]:
        score += 10
    elif user["goal"] == "Join a team" and candidate["goal"] == "Start something":
        score += 10
    elif user["goal"] == "Explore" or candidate["goal"] == "Explore":
        score += 5

    return min(score, 100), reasons[:3], risks[:2]

def match_label(score: int) -> str:
    if score >= 80:
        return "Strong Match"
    if score >= 65:
        return "Good Match"
    if score >= 50:
        return "Possible Match"
    return "Low Match"

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("UW CoFounder Search")
page = st.sidebar.radio("Go to:", ["Landing Page & Profile", "Founder Search"])

# -----------------------------
# SESSION STATE
# -----------------------------
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = False

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# -----------------------------
# PAGE 1: PROFILE
# -----------------------------
if page == "Landing Page & Profile":
    st.title("🤝 Find Your UW Co-Founder")
    st.write("A simple MVP to match students based on role, commitment, and collaboration style.")

    if not st.session_state.profile_complete:
        with st.form("profile_form"):
            st.subheader("Create Your Founder Profile")

            name = st.text_input("Full Name")
            email = st.text_input("UW Email")
            department = st.selectbox("Department", DEPT_OPTIONS)
            role = st.selectbox("Your Role", ROLE_OPTIONS)
            looking_for = st.selectbox("Who Are You Looking For?", ROLE_OPTIONS)
            hours = st.selectbox("How Many Hours Per Week Can You Commit?", HOURS_OPTIONS)
            goal = st.selectbox("What Are You Looking To Do Right Now?", GOAL_OPTIONS)
            style = st.selectbox("How Do You Usually Handle Conflict or Collaboration?", STYLE_OPTIONS)
            bio = st.text_area("Short Bio / What are you building or interested in?")

            submitted = st.form_submit_button("Save Profile")

            if submitted:
                if not name or not email:
                    st.error("Please enter your name and email.")
                else:
                    st.session_state.user_data = {
                        "name": name,
                        "email": email,
                        "department": department,
                        "role": role,
                        "looking_for": looking_for,
                        "hours": hours,
                        "goal": goal,
                        "style": style,
                        "bio": bio,
                    }
                    st.session_state.profile_complete = True
                    st.rerun()
    else:
        st.success(f"Profile live for {st.session_state.user_data['name']}")

        st.subheader("Your Profile")
        st.write(f"**Email:** {st.session_state.user_data['email']}")
        st.write(f"**Department:** {st.session_state.user_data['department']}")
        st.write(f"**Role:** {st.session_state.user_data['role']}")
        st.write(f"**Looking for:** {st.session_state.user_data['looking_for']}")
        st.write(f"**Commitment:** {st.session_state.user_data['hours']} hours/week")
        st.write(f"**Goal:** {st.session_state.user_data['goal']}")
        st.write(f"**Style:** {st.session_state.user_data['style']}")
        st.write(f"**Bio:** {st.session_state.user_data['bio'] or 'No bio added yet.'}")

        if st.button("Reset Profile"):
            st.session_state.profile_complete = False
            st.session_state.user_data = {}
            st.rerun()

# -----------------------------
# PAGE 2: MATCHING
# -----------------------------
elif page == "Founder Search":
    st.title("🔎 Founder Search")

    if not st.session_state.profile_complete:
        st.warning("Please complete your profile first.")
    else:
        user = st.session_state.user_data

        st.subheader("Top Matches For You")

        scored_candidates = []
        for candidate in FOUNDER_POOL:
            score, reasons, risks = score_match(user, candidate)
            scored_candidates.append(
                {
                    "candidate": candidate,
                    "score": score,
                    "reasons": reasons,
                    "risks": risks,
                    "label": match_label(score),
                }
            )

        scored_candidates.sort(key=lambda x: x["score"], reverse=True)

        for item in scored_candidates[:3]:
            c = item["candidate"]
            with st.container():
                st.markdown("---")
                st.subheader(f"{c['name']} — {item['label']} ({item['score']}/100)")
                st.write(f"**Department:** {c['department']}")
                st.write(f"**Role:** {c['role']}")
                st.write(f"**Looking for:** {c['looking_for']}")
                st.write(f"**Commitment:** {c['hours']} hours/week")
                st.write(f"**Goal:** {c['goal']}")
                st.write(f"**Style:** {c['style']}")
                st.write(f"**Bio:** {c['bio']}")

                st.write("**Why this match could work:**")
                for reason in item["reasons"]:
                    st.write(f"- {reason}")

                if item["risks"]:
                    st.write("**Potential risks:**")
                    for risk in item["risks"]:
                        st.write(f"- {risk}")

        st.markdown("---")
        st.info("This MVP uses hardcoded profiles and rule-based matching to validate what signals matter most.")
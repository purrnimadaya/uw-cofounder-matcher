import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="UW CoFounder Search", page_icon="🤝", layout="wide")

# -----------------------------
# LOGO
# -----------------------------
logo_path = "Logo_CoFounder_App (1).png"

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_container_width=True)
else:
    st.sidebar.title("UW CoFounder Search")

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
        "goal": "Find a co-founder",
        "idea_stage": "Built a prototype",
        "bio": "Built side projects before and likes structured collaboration.",
    },
    {
        "name": "Maya Patel",
        "department": "Foster Business",
        "role": "PM",
        "looking_for": "Engineer",
        "hours": "10-15",
        "style": "Address it bluntly",
        "goal": "Form a team",
        "idea_stage": "Have an idea",
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
        "idea_stage": "Just exploring",
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
        "idea_stage": "Actively building",
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
        "idea_stage": "Have an idea",
        "bio": "Good at partnerships, outreach, and storytelling.",
    },
]

ROLE_OPTIONS = ["Engineer", "PM", "Designer", "Business", "Data/AI"]
DEPT_OPTIONS = ["Allen School", "Foster Business", "HCDE/Design", "Other"]
HOURS_OPTIONS = ["<5", "5-10", "10-15", "15+"]
STYLE_OPTIONS = ["Address it bluntly", "Talk over coffee", "Let it settle naturally"]
GOAL_OPTIONS = ["Find a co-founder", "Form a team", "Join a team", "Explore"]
IDEA_STAGE_OPTIONS = ["Just exploring", "Have an idea", "Built a prototype", "Actively building"]

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def hours_to_value(hours):
    mapping = {"<5": 1, "5-10": 2, "10-15": 3, "15+": 4}
    return mapping.get(hours, 0)

def idea_stage_to_value(stage):
    mapping = {
        "Just exploring": 1,
        "Have an idea": 2,
        "Built a prototype": 3,
        "Actively building": 4,
    }
    return mapping.get(stage, 0)

def calculate_trust_score(user):
    score = 0

    # Commitment
    if user["hours"] == "15+":
        score += 35
    elif user["hours"] == "10-15":
        score += 30
    elif user["hours"] == "5-10":
        score += 20
    else:
        score += 10

    # Goal seriousness
    if user["goal"] in ["Find a co-founder", "Form a team"]:
        score += 30
    elif user["goal"] == "Join a team":
        score += 20
    else:
        score += 10

    # Stage of progress
    if user["idea_stage"] == "Actively building":
        score += 35
    elif user["idea_stage"] == "Built a prototype":
        score += 30
    elif user["idea_stage"] == "Have an idea":
        score += 20
    else:
        score += 10

    return min(score, 100)

def score_match(user, candidate):
    score = 0
    reasons = []
    risks = []

    # 1. Role complementarity: 30 points
    if user["looking_for"] == candidate["role"]:
        score += 20
        reasons.append(f"They are the exact role you are looking for: {candidate['role']}.")
    elif user["role"] != candidate["role"]:
        score += 10
        reasons.append("They bring a complementary role to your profile.")
    else:
        score += 4
        risks.append("You have similar roles, so the team may need more skill diversity.")

    if candidate["looking_for"] == user["role"]:
        score += 10
        reasons.append("They are also looking for someone with your role.")

    # 2. Commitment alignment: 20 points
    user_hours = hours_to_value(user["hours"])
    candidate_hours = hours_to_value(candidate["hours"])
    hour_diff = abs(user_hours - candidate_hours)

    if hour_diff == 0:
        score += 15
        reasons.append("Your weekly time commitment is strongly aligned.")
    elif hour_diff == 1:
        score += 10
        reasons.append("Your time commitment is reasonably aligned.")
    else:
        score += 3
        risks.append("Your expected weekly commitment may not be fully aligned.")

    # 3. Goal alignment: 15 points
    if user["goal"] == candidate["goal"]:
        score += 10
        reasons.append(f"You both have a similar goal right now: {user['goal']}.")
    elif user["goal"] in ["Find a co-founder", "Form a team"] and candidate["goal"] == "Join a team":
        score += 15
        reasons.append("You are looking to build, and they are looking to join a team — strong fit.")
    elif user["goal"] == "Join a team" and candidate["goal"] in ["Find a co-founder", "Form a team"]:
        score += 15
        reasons.append("They are looking to build, and you are looking to join a team — strong fit.")
    else:
        score += 4
        risks.append("Your current goals may differ.")

    # 4. Idea stage alignment: 15 points
    user_stage = idea_stage_to_value(user["idea_stage"])
    candidate_stage = idea_stage_to_value(candidate["idea_stage"])
    stage_diff = abs(user_stage - candidate_stage)

    if user["goal"] in ["Find a co-founder", "Form a team"] and candidate["goal"] == "Join a team":
        score += 10
        reasons.append("Your progress stage may give them something concrete to join.")
    elif stage_diff == 0:
        score += 10
        reasons.append("You are at a similar stage of building.")
    elif stage_diff == 1:
        score += 6
        reasons.append("Your building stages are reasonably close.")
    else:
        score += 2
        risks.append("You may be at different stages of readiness.")

    # 5. Collaboration style: 10 points
    if user["style"] == candidate["style"]:
        score += 10
        reasons.append("You share a similar collaboration style.")
    else:
        score += 4
        risks.append("You may approach conflict or collaboration differently.")

    # 6. Department diversity/context: 10 points
    if user["department"] != candidate["department"]:
        score += 10
        reasons.append("You bring cross-department perspective, which can strengthen startup teams.")
    else:
        score += 5
        reasons.append("You share similar academic context.")

    return min(score, 100), reasons[:3], risks[:2]

def match_label(score):
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
st.sidebar.markdown("### Navigation")
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
    st.success("🚀 MVP: UW Co-founder Matching Platform (Rule-based v1)")
    st.info("💡 Insight: Students care more about commitment and reliability than just skills when choosing teammates.")

    st.write("A simple MVP to match students based on role, commitment, stage, and collaboration style.")

    if not st.session_state.profile_complete:
        with st.form("profile_form"):
            st.subheader("Create Your Founder Profile")

            name = st.text_input("Full Name")
            email = st.text_input("UW Email")
            department = st.selectbox("Department", DEPT_OPTIONS)
            role = st.selectbox("Your Role", ROLE_OPTIONS)
            looking_for = st.selectbox("Who Are You Looking For?", ROLE_OPTIONS)
            hours = st.selectbox("How Many Hours Per Week Can You Commit?", HOURS_OPTIONS)
            goal = st.selectbox("What are you looking for right now?", GOAL_OPTIONS)
            idea_stage = st.selectbox("What stage are you at?", IDEA_STAGE_OPTIONS)
            style = st.selectbox("How do you usually handle conflict or collaboration?", STYLE_OPTIONS)
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
                        "idea_stage": idea_stage,
                        "style": style,
                        "bio": bio,
                    }
                    st.session_state.profile_complete = True
                    st.rerun()
    else:
        user = st.session_state.user_data
        trust_score = calculate_trust_score(user)

        st.success(f"Profile live for {user['name']}")

        st.subheader("Your Profile")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Department:** {user['department']}")
        st.write(f"**Role:** {user['role']}")
        st.write(f"**Looking for:** {user['looking_for']}")
        st.write(f"**Commitment:** {user['hours']} hours/week")
        st.write(f"**Goal:** {user['goal']}")
        st.write(f"**Idea Stage:** {user['idea_stage']}")
        st.write(f"**Style:** {user['style']}")
        st.write(f"**Bio:** {user['bio'] or 'No bio added yet.'}")

        st.markdown("### 🔒 Trust Score")
        st.progress(trust_score / 100)
        st.write(f"**{trust_score}/100**")

        if trust_score >= 80:
            st.write("High signal: strong commitment and momentum.")
        elif trust_score >= 60:
            st.write("Good signal: promising profile with meaningful intent.")
        else:
            st.write("Early signal: still exploring or building consistency.")

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

        st.subheader("🔥 Top Matches For You")

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

        best_match = scored_candidates[0]
        st.markdown("### 🌟 Best Match")
        st.write(f"**{best_match['candidate']['name']}** — {best_match['label']} ({best_match['score']}/100)")

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
                st.write(f"**Idea Stage:** {c['idea_stage']}")
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
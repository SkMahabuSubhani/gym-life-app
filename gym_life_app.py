import streamlit as st
from datetime import datetime, date, time

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="GYM LIFE",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #182848 0%, transparent 35%),
        radial-gradient(circle at 90% 20%, #302b63 0%, transparent 35%),
        linear-gradient(135deg, #080b12, #101827 50%, #090d16);
    color: white;
}

/* Main headings */

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090d18, #111827);
    border-right: 1px solid #27364d;
}

/* Cards */

.gym-card {
    background: linear-gradient(145deg, #121a29, #0c111c);
    border: 1px solid #26364e;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

.neon-card {
    background: linear-gradient(145deg, #101827, #172238);
    border: 1px solid #00e5ff;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 0 18px rgba(0,229,255,0.12);
}

.stat-card {
    background: linear-gradient(145deg, #141e2e, #0d1420);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    border: 1px solid #293b54;
}

.stat-number {
    font-size: 32px;
    font-weight: 800;
    color: #00e5ff;
}

.stat-label {
    color: #9ca9bb;
    font-size: 14px;
}

.task-complete {
    text-decoration: line-through;
    opacity: 0.55;
}

.task-title {
    font-size: 17px;
    font-weight: 700;
}

.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    background: #142c38;
    color: #00e5ff;
    font-size: 12px;
    margin: 3px;
}

.reminder {
    background: linear-gradient(90deg, #241b08, #30230c);
    border-left: 5px solid #ffb300;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.success-box {
    background: linear-gradient(90deg, #08251d, #0d3529);
    border-left: 5px solid #00e676;
    padding: 15px;
    border-radius: 12px;
}

.current-box {
    background: linear-gradient(90deg, #082331, #10364a);
    border-left: 5px solid #00e5ff;
    padding: 15px;
    border-radius: 12px;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "completed" not in st.session_state:
    st.session_state.completed = {}

if "custom_tasks" not in st.session_state:
    st.session_state.custom_tasks = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "Athlete",
        "weight": 60,
        "goal": "Muscle Gain",
        "water": 3.0
    }

# =========================================================
# CURRENT DATE/TIME
# =========================================================

now = datetime.now()
today = date.today()

# =========================================================
# DEFAULT DAILY PLAN
# =========================================================

daily_plan = [

    # MORNING
    {
        "id": "wake",
        "time": "06:30",
        "category": "Routine",
        "icon": "🌅",
        "title": "Wake Up",
        "details": "Start the day and get ready."
    },

    {
        "id": "water1",
        "time": "06:45",
        "category": "Water",
        "icon": "💧",
        "title": "Drink Water",
        "details": "Drink 400–500 ml water."
    },

    {
        "id": "breakfast",
        "time": "07:30",
        "category": "Diet",
        "icon": "🍳",
        "title": "Breakfast",
        "details": "Eggs + oats + banana + milk/curd."
    },

    # STUDY / COLLEGE
    {
        "id": "water2",
        "time": "09:30",
        "category": "Water",
        "icon": "💧",
        "title": "Water Break",
        "details": "Drink 300–400 ml water."
    },

    {
        "id": "snack1",
        "time": "11:00",
        "category": "Diet",
        "icon": "🥜",
        "title": "Protein Snack",
        "details": "Peanuts / roasted chana / fruit."
    },

    {
        "id": "water3",
        "time": "11:30",
        "category": "Water",
        "icon": "💧",
        "title": "Water Break",
        "details": "Drink 300–400 ml water."
    },

    # LUNCH
    {
        "id": "lunch",
        "time": "13:30",
        "category": "Diet",
        "icon": "🍗",
        "title": "Lunch",
        "details": "Rice/roti + chicken/eggs + vegetables + curd."
    },

    {
        "id": "water4",
        "time": "14:30",
        "category": "Water",
        "icon": "💧",
        "title": "Water Break",
        "details": "Drink 300–400 ml water."
    },

    # PRE WORKOUT
    {
        "id": "preworkout",
        "time": "16:30",
        "category": "Diet",
        "icon": "🍌",
        "title": "Pre-Workout Meal",
        "details": "Banana + oats/peanut butter or another easy-to-digest snack."
    },

    {
        "id": "water5",
        "time": "17:00",
        "category": "Water",
        "icon": "💧",
        "title": "Hydration",
        "details": "Drink 300–500 ml water before training."
    },

    # GYM
    {
        "id": "gym",
        "time": "18:00",
        "category": "Workout",
        "icon": "🏋️",
        "title": "GYM SESSION",
        "details": "Follow today's muscle-group workout."
    },

    # POST WORKOUT
    {
        "id": "postworkout",
        "time": "19:15",
        "category": "Diet",
        "icon": "🥛",
        "title": "Post-Workout Protein",
        "details": "Protein-rich meal/shake according to your diet."
    },

    {
        "id": "water6",
        "time": "19:30",
        "category": "Water",
        "icon": "💧",
        "title": "Water Break",
        "details": "Drink 300–500 ml water."
    },

    # DINNER
    {
        "id": "dinner",
        "time": "21:00",
        "category": "Diet",
        "icon": "🍽️",
        "title": "Dinner",
        "details": "Chicken/fish/eggs + vegetables + rice/roti."
    },

    {
        "id": "water7",
        "time": "21:45",
        "category": "Water",
        "icon": "💧",
        "title": "Final Hydration",
        "details": "Drink water according to your thirst."
    },

    {
        "id": "sleep",
        "time": "22:30",
        "category": "Recovery",
        "icon": "😴",
        "title": "Sleep",
        "details": "Aim for consistent, sufficient sleep for recovery."
    }
]

# =========================================================
# WORKOUT PLAN
# =========================================================

workout_plan = {
    "Monday": {
        "muscle": "Chest + Triceps",
        "exercises": [
            "Bench Press — 4 × 8–12",
            "Incline Dumbbell Press — 3 × 8–12",
            "Cable / Pec Fly — 3 × 12–15",
            "Triceps Pushdown — 3 × 10–15",
            "Overhead Triceps Extension — 3 × 10–12"
        ]
    },

    "Tuesday": {
        "muscle": "Back + Biceps",
        "exercises": [
            "Lat Pulldown — 4 × 8–12",
            "Seated Cable Row — 3 × 8–12",
            "One Arm Dumbbell Row — 3 × 10",
            "Barbell / EZ Curl — 3 × 10–12",
            "Hammer Curl — 3 × 10–12"
        ]
    },

    "Wednesday": {
        "muscle": "Legs",
        "exercises": [
            "Squat / Leg Press — 4 × 8–12",
            "Romanian Deadlift — 3 × 8–12",
            "Leg Extension — 3 × 12–15",
            "Leg Curl — 3 × 12–15",
            "Calf Raises — 4 × 12–20"
        ]
    },

    "Thursday": {
        "muscle": "Shoulders + Traps",
        "exercises": [
            "Overhead Press — 4 × 8–12",
            "Lateral Raises — 4 × 12–15",
            "Rear Delt Fly — 3 × 12–15",
            "Shrugs — 4 × 10–15",
            "Face Pulls — 3 × 15"
        ]
    },

    "Friday": {
        "muscle": "Upper Body",
        "exercises": [
            "Bench Press — 3 × 8–12",
            "Lat Pulldown — 3 × 8–12",
            "Shoulder Press — 3 × 8–12",
            "Biceps Curl — 3 × 10–12",
            "Triceps Pushdown — 3 × 10–12"
        ]
    },

    "Saturday": {
        "muscle": "Lower Body + Core",
        "exercises": [
            "Leg Press — 4 × 10",
            "Romanian Deadlift — 3 × 10",
            "Walking Lunges — 3 × 12",
            "Calf Raises — 4 × 15",
            "Plank — 3 × 30–60 sec"
        ]
    },

    "Sunday": {
        "muscle": "Recovery Day",
        "exercises": [
            "Light walking",
            "Stretching",
            "Mobility work",
            "Recovery"
        ]
    }
}

# =========================================================
# DIET PLAN
# =========================================================

diet_plan = [
    ("07:30", "Breakfast", "🍳",
     "3–4 eggs + oats + banana + milk/curd"),

    ("11:00", "Morning Snack", "🥜",
     "Peanuts/roasted chana + fruit"),

    ("13:30", "Lunch", "🍗",
     "Rice/roti + chicken/fish/eggs + vegetables + curd"),

    ("16:30", "Pre-Workout", "🍌",
     "Banana + oats/peanut butter"),

    ("19:15", "Post-Workout", "🥛",
     "Protein-rich meal/shake"),

    ("21:00", "Dinner", "🍽️",
     "Chicken/fish/eggs + vegetables + rice/roti")
]

# =========================================================
# WATER PLAN
# =========================================================

water_plan = [
    ("06:45", "400–500 ml"),
    ("09:30", "300–400 ml"),
    ("11:30", "300–400 ml"),
    ("14:30", "300–400 ml"),
    ("17:00", "300–500 ml"),
    ("19:30", "300–500 ml"),
    ("21:45", "Drink according to thirst")
]

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def task_key(task_id):
    return f"{today}_{task_id}"


def is_completed(task_id):
    return st.session_state.completed.get(task_key(task_id), False)


def set_completed(task_id, value):
    st.session_state.completed[task_key(task_id)] = value


def get_time_obj(time_string):
    hour, minute = map(int, time_string.split(":"))
    return time(hour, minute)


def get_status(time_string, completed):
    scheduled = get_time_obj(time_string)
    current = now.time()

    if completed:
        return "✅ Completed"

    if current >= scheduled:
        return "🔴 Due"

    return "🟡 Upcoming"


def reset_today():
    keys = [k for k in st.session_state.completed if k.startswith(str(today))]
    for key in keys:
        del st.session_state.completed[key]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🏋️ GYM LIFE")

    st.caption("Your personal fitness command center")

    menu = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "✅ Daily Checklist",
            "🏋️ Workout",
            "🍗 Diet Plan",
            "💧 Water Tracker",
            "⏰ Reminders",
            "👤 My Profile"
        ]
    )

    st.divider()

    st.markdown("### ⚡ Today's Goal")

    st.write(f"**Goal:** {st.session_state.profile['goal']}")
    st.write(f"**Weight:** {st.session_state.profile['weight']} kg")

    st.divider()

    if st.button("🔄 Reset Today's Tasks", use_container_width=True):
        reset_today()
        st.rerun()

# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""
    <div class="neon-card">
        <h1>🏋️ GYM LIFE</h1>
        <p style="color:#9ca9bb;">
        Train • Eat • Hydrate • Recover • Repeat
        </p>
        <p>
        📅 {today.strftime("%A, %d %B %Y")}
        &nbsp;&nbsp; | &nbsp;&nbsp;
        🕐 {now.strftime("%I:%M %p")}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# =========================================================
# CALCULATE COMPLETION
# =========================================================

all_tasks = daily_plan + st.session_state.custom_tasks

completed_count = sum(
    is_completed(task["id"]) for task in all_tasks
)

total_tasks = len(all_tasks)

percentage = (
    int((completed_count / total_tasks) * 100)
    if total_tasks > 0 else 0
)

# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown("## 📊 Today's Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{percentage}%</div>
                <div class="stat-label">DAILY COMPLETE</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{completed_count}</div>
                <div class="stat-label">TASKS DONE</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">{total_tasks}</div>
                <div class="stat-label">TOTAL TASKS</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        weekday = today.strftime("%A")

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-number">💪</div>
                <div class="stat-label">{workout_plan[weekday]["muscle"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.progress(
        percentage / 100,
        text=f"Daily Progress — {percentage}%"
    )

    st.write("")

    # Current workout
    weekday = today.strftime("%A")
    workout = workout_plan[weekday]

    st.markdown(
        f"""
        <div class="gym-card">
            <h2>🔥 Today's Workout</h2>
            <h3>{workout["muscle"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    for exercise in workout["exercises"]:
        st.markdown(f"• {exercise}")

    st.write("")

    # Next tasks
    st.markdown("## ⏭️ Today's Schedule")

    upcoming = []

    for task in all_tasks:

        completed = is_completed(task["id"])

        if not completed:
            scheduled = get_time_obj(task["time"])

            if scheduled >= now.time():
                upcoming.append(task)

    upcoming = sorted(
        upcoming,
        key=lambda x: get_time_obj(x["time"])
    )

    if upcoming:

        for task in upcoming[:5]:

            st.markdown(
                f"""
                <div class="current-box">
                    <b>{task["icon"]} {task["title"]}</b>
                    <br>
                    🕐 {task["time"]}
                    <br>
                    <span style="color:#9ca9bb;">
                    {task["details"]}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.success("🎉 All scheduled tasks for today are completed!")

# =========================================================
# DAILY CHECKLIST
# =========================================================

elif menu == "✅ Daily Checklist":

    st.markdown("## ✅ Daily Checklist")

    st.write(
        f"Complete your tasks and reach **100%**."
    )

    st.progress(
        percentage / 100,
        text=f"{completed_count}/{total_tasks} completed"
    )

    st.write("")

    for task in all_tasks:

        completed = is_completed(task["id"])

        status = get_status(
            task["time"],
            completed
        )

        checkbox = st.checkbox(
            f'{task["icon"]} {task["title"]} — {task["time"]}',
            value=completed,
            key=f"check_{task['id']}_{today}"
        )

        set_completed(task["id"], checkbox)

        if checkbox:

            st.markdown(
                f"""
                <div class="success-box">
                    <b>✅ Completed</b><br>
                    {task["details"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.caption(
                f"{status} • {task['details']}"
            )

        st.divider()

    # Add custom task

    st.markdown("## ➕ Add Custom Task")

    with st.form("custom_task_form"):

        col1, col2 = st.columns(2)

        with col1:
            custom_title = st.text_input(
                "Task name"
            )

        with col2:
            custom_time = st.time_input(
                "Time",
                value=time(20, 0)
            )

        custom_category = st.selectbox(
            "Category",
            [
                "Workout",
                "Diet",
                "Water",
                "Recovery",
                "Study",
                "Other"
            ]
        )

        custom_details = st.text_input(
            "Details",
            value="Custom task"
        )

        submitted = st.form_submit_button(
            "➕ Add Task"
        )

        if submitted and custom_title:

            new_task = {
                "id": f"custom_{len(st.session_state.custom_tasks)}_{datetime.now().timestamp()}",
                "time": custom_time.strftime("%H:%M"),
                "category": custom_category,
                "icon": "⭐",
                "title": custom_title,
                "details": custom_details
            }

            st.session_state.custom_tasks.append(
                new_task
            )

            st.success("Task added!")
            st.rerun()

# =========================================================
# WORKOUT
# =========================================================

elif menu == "🏋️ Workout":

    st.markdown("## 🏋️ Weekly Workout Planner")

    selected_day = st.selectbox(
        "Select training day",
        list(workout_plan.keys()),
        index=list(workout_plan.keys()).index(
            today.strftime("%A")
        )
    )

    workout = workout_plan[selected_day]

    st.markdown(
        f"""
        <div class="neon-card">
            <h2>💪 {selected_day}</h2>
            <h3>{workout["muscle"]}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    for i, exercise in enumerate(
        workout["exercises"],
        start=1
    ):

        st.markdown(
            f"""
            <div class="gym-card">
                <b>{i}. {exercise}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "Adjust exercises, sets and loads based on your training experience "
        "and recovery. Use proper technique and stop if you experience pain."
    )

# =========================================================
# DIET
# =========================================================

elif menu == "🍗 Diet Plan":

    st.markdown("## 🍗 Daily Diet Plan")

    st.info(
        "This is a general fitness template, not a personalized medical diet. "
        "Adjust portions to your calorie/protein needs."
    )

    for meal_time, meal, icon, details in diet_plan:

        st.markdown(
            f"""
            <div class="gym-card">
                <span class="badge">{meal_time}</span>
                <h3>{icon} {meal}</h3>
                <p>{details}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 🥩 Protein Sources")

    protein_sources = [
        "Eggs",
        "Chicken",
        "Fish",
        "Milk",
        "Curd",
        "Paneer",
        "Dal",
        "Chickpeas",
        "Peanuts",
        "Soy"
    ]

    cols = st.columns(5)

    for i, source in enumerate(protein_sources):

        with cols[i % 5]:
            st.markdown(
                f"""
                <div class="stat-card">
                    🥩<br>
                    <b>{source}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================================================
# WATER TRACKER
# =========================================================

elif menu == "💧 Water Tracker":

    st.markdown("## 💧 Water Tracker")

    target = st.session_state.profile["water"]

    water_completed = sum(
        is_completed(task["id"])
        for task in daily_plan
        if task["category"] == "Water"
    )

    total_water_tasks = len(water_plan)

    water_percentage = int(
        (water_completed / total_water_tasks) * 100
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Daily Target",
            f"{target:.1f} L"
        )

    with c2:
        st.metric(
            "Water Tasks",
            f"{water_completed}/{total_water_tasks}"
        )

    with c3:
        st.metric(
            "Hydration Progress",
            f"{water_percentage}%"
        )

    st.progress(
        water_percentage / 100
    )

    st.write("")

    for i, (water_time, amount) in enumerate(
        water_plan
    ):

        task_id = f"water_schedule_{i}"

        completed = is_completed(task_id)

        checked = st.checkbox(
            f"💧 {water_time} — {amount}",
            value=completed,
            key=f"water_{i}_{today}"
        )

        set_completed(
            task_id,
            checked
        )

# =========================================================
# REMINDERS
# =========================================================

elif menu == "⏰ Reminders":

    st.markdown("## ⏰ Smart Reminders")

    st.write(
        f"Current time: **{now.strftime('%I:%M:%S %p')}**"
    )

    due_tasks = []
    upcoming_tasks = []

    for task in all_tasks:

        completed = is_completed(task["id"])

        if not completed:

            scheduled = get_time_obj(task["time"])

            if scheduled <= now.time():
                due_tasks.append(task)

            else:
                upcoming_tasks.append(task)

    if due_tasks:

        st.markdown("### 🔔 Tasks Due")

        for task in due_tasks:

            st.markdown(
                f"""
                <div class="reminder">
                    <b>🔔 {task["title"]}</b>
                    <br>
                    Scheduled: {task["time"]}
                    <br>
                    {task["details"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "🎉 No overdue tasks right now!"
        )

    st.markdown("### 🕐 Upcoming")

    upcoming_tasks = sorted(
        upcoming_tasks,
        key=lambda x: get_time_obj(x["time"])
    )

    for task in upcoming_tasks[:8]:

        st.markdown(
            f"""
            <div class="current-box">
                🕐 <b>{task["time"]}</b>
                &nbsp; {task["icon"]}
                <b>{task["title"]}</b>
                <br>
                {task["details"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "Keep this page open in the browser to see the current reminder "
        "status update when the Streamlit app reruns."
    )

# =========================================================
# PROFILE
# =========================================================

elif menu == "👤 My Profile":

    st.markdown("## 👤 My Fitness Profile")

    with st.form("profile_form"):

        name = st.text_input(
            "Name",
            value=st.session_state.profile["name"]
        )

        weight = st.number_input(
            "Current Weight (kg)",
            min_value=30.0,
            max_value=200.0,
            value=float(
                st.session_state.profile["weight"]
            ),
            step=0.5
        )

        goal = st.selectbox(
            "Primary Goal",
            [
                "Muscle Gain",
                "Fat Loss",
                "Strength",
                "General Fitness",
                "Maintenance"
            ],
            index=[
                "Muscle Gain",
                "Fat Loss",
                "Strength",
                "General Fitness",
                "Maintenance"
            ].index(
                st.session_state.profile["goal"]
            )
        )

        water = st.number_input(
            "Daily Water Target (Litres)",
            min_value=1.0,
            max_value=8.0,
            value=float(
                st.session_state.profile["water"]
            ),
            step=0.1
        )

        save = st.form_submit_button(
            "💾 Save Profile"
        )

        if save:

            st.session_state.profile = {
                "name": name,
                "weight": weight,
                "goal": goal,
                "water": water
            }

            st.success(
                "Profile updated successfully!"
            )

    st.write("")

    st.markdown(
        f"""
        <div class="neon-card">
            <h2>🔥 {st.session_state.profile["name"]}</h2>
            <p>Goal: <b>{st.session_state.profile["goal"]}</b></p>
            <p>Weight: <b>{st.session_state.profile["weight"]} kg</b></p>
            <p>Water Target: <b>{st.session_state.profile["water"]:.1f} L/day</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# FOOTER
# =========================================================

st.write("")
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#718096;">
        🏋️ GYM LIFE • Train Smart • Eat Well • Recover • Repeat
    </div>
    """,
    unsafe_allow_html=True
)

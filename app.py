
import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Game Theory Lab",
    page_icon="GT",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* ── Typography (Google Font) ──────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
}

/* ── Layout ────────────────────────────────────────── */
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ── Hero Header ───────────────────────────────────── */
.hero {
    padding: 1.5rem 0 1.2rem 0;
    border-bottom: 1px solid rgba(148,163,184,0.3);
    margin-bottom: 1.5rem;
}

.eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.55;
}

.hero h1 {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    margin: 0.45rem 0;
    background: linear-gradient(135deg, #4F6DF5, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero p {
    font-size: 1rem;
    opacity: 0.65;
}

/* ── Section headings ──────────────────────────────── */
.section-heading {
    font-size: 1.05rem;
    font-weight: 650;
    margin: 0.6rem 0 0.25rem;
}

.section-description {
    font-size: 0.88rem;
    opacity: 0.6;
    margin-bottom: 1rem;
}

/* ── Metric cards ──────────────────────────────────── */
.metric-card {
    padding: 1.1rem 1.2rem;
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 12px;
    background: rgba(79,109,245,0.05);
    min-height: 105px;
    backdrop-filter: blur(4px);
}

.metric-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    opacity: 0.55;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #4F6DF5;
}

/* ── Payoff cell labels ─────────────────────────────── */
.cell-heading {
    font-size: 0.82rem;
    font-weight: 600;
    opacity: 0.6;
    margin-bottom: 0.35rem;
}

/* ── Analyze button  ────────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #4F6DF5 0%, #7C3AED 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 3rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 15px rgba(79,109,245,0.35) !important;
    transition: opacity 0.2s, transform 0.15s !important;
}

div[data-testid="stButton"] > button[kind="primary"]:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(79,109,245,0.45) !important;
}

/* ── Inputs & selects ───────────────────────────────── */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    border-radius: 8px !important;
    border-color: rgba(148,163,184,0.4) !important;
}

/* ── Equilibrium result box ─────────────────────────── */
.result-box {
    border: 1px solid rgba(34,197,94,0.3);
    background: rgba(34,197,94,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}

.result-title {
    color: #16a34a !important;
    font-weight: 700;
    font-size: 1.02rem;
}

/* ── Dividers ───────────────────────────────────────── */
hr {
    border-color: rgba(148,163,184,0.25) !important;
}

/* ── Mobile ─────────────────────────────────────────── */
@media (max-width: 700px) {
    .hero h1 { font-size: 1.65rem; }
    .block-container { padding-top: 1rem; }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# PREDEFINED GAMES
# --------------------------------------------------

GAMES = {
    "Prisoner's Dilemma": {
        "description": (
            "Two players choose whether to cooperate or defect. "
            "Individual incentives can lead to an outcome that "
            "is worse for both players collectively."
        ),
        "a": ["Cooperate", "Defect"],
        "b": ["Cooperate", "Defect"],
        "payoffs": [
            [(3, 3), (0, 5)],
            [(5, 0), (1, 1)]
        ]
    },

    "Coordination Game": {
        "description": (
            "Both players benefit from choosing the same option. "
            "There are two possible pure Nash Equilibria."
        ),
        "a": ["Location A", "Location B"],
        "b": ["Location A", "Location B"],
        "payoffs": [
            [(2, 2), (0, 0)],
            [(0, 0), (2, 2)]
        ]
    },

    "Battle of the Sexes": {
        "description": (
            "Both players prefer being together, but each has "
            "a different preferred event."
        ),
        "a": ["Concert", "Sports Match"],
        "b": ["Concert", "Sports Match"],
        "payoffs": [
            [(2, 1), (0, 0)],
            [(0, 0), (1, 2)]
        ]
    },

    "Matching Pennies": {
        "description": (
            "Each player chooses Heads or Tails. Player A wins "
            "when the choices match; Player B wins when they differ."
        ),
        "a": ["Heads", "Tails"],
        "b": ["Heads", "Tails"],
        "payoffs": [
            [(1, -1), (-1, 1)],
            [(-1, 1), (1, -1)]
        ]
    },

    "Custom Game": {
        "description": (
            "Create your own two-player game by entering "
            "the strategy names and payoff values."
        ),
        "a": ["Strategy A1", "Strategy A2"],
        "b": ["Strategy B1", "Strategy B2"],
        "payoffs": [
            [(3, 3), (0, 5)],
            [(5, 0), (1, 1)]
        ]
    }
}


# --------------------------------------------------
# RESET INPUTS WHEN GAME CHANGES
# --------------------------------------------------

def reset_payoffs():
    selected = st.session_state["game_choice"]
    defaults = GAMES[selected]["payoffs"]

    # Reset all payoff widgets when a different game is selected.
    for i in range(2):
        for j in range(2):
            st.session_state[f"a{i}{j}"] = defaults[i][j][0]
            st.session_state[f"b{i}{j}"] = defaults[i][j][1]


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">GAME THEORY · ANALYSIS TOOL</div>
    <h1>Strategic Game Analyzer</h1>
    <p>
        Explore payoff matrices, compare strategies, and discover
        Nash Equilibria through interactive analysis.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# GAME SELECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">01 &nbsp; Choose a game</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Start with an example or create your own strategic game.'
    '</div>',
    unsafe_allow_html=True
)

game_name = st.selectbox(
    "Game",
    options=list(GAMES.keys()),
    key="game_choice",
    on_change=reset_payoffs,
    label_visibility="collapsed"
)

game = GAMES[game_name]

st.info(game["description"])

a_strategies = game["a"].copy()
b_strategies = game["b"].copy()


# --------------------------------------------------
# PLAYER NAMES AND STRATEGIES
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">02 &nbsp; Players and strategies</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Name the players and, for a custom game, edit their available strategies.'
    '</div>',
    unsafe_allow_html=True
)

player_col_a, player_col_b = st.columns(2)

with player_col_a:
    player_a = st.text_input(
        "Row player",
        value="Player A",
        key="player_a"
    )

    if game_name == "Custom Game":
        a_strategies[0] = st.text_input(
            "First strategy",
            value=game["a"][0],
            key="custom_a1"
        )
        a_strategies[1] = st.text_input(
            "Second strategy",
            value=game["a"][1],
            key="custom_a2"
        )
    else:
        st.text_input(
            "Available strategies",
            value="  /  ".join(a_strategies),
            disabled=True,
            key=f"display_a_{game_name}"
        )

with player_col_b:
    player_b = st.text_input(
        "Column player",
        value="Player B",
        key="player_b"
    )

    if game_name == "Custom Game":
        b_strategies[0] = st.text_input(
            "First strategy",
            value=game["b"][0],
            key="custom_b1"
        )
        b_strategies[1] = st.text_input(
            "Second strategy",
            value=game["b"][1],
            key="custom_b2"
        )
    else:
        st.text_input(
            "Available strategies",
            value="  /  ".join(b_strategies),
            disabled=True,
            key=f"display_b_{game_name}"
        )


# --------------------------------------------------
# INITIALIZE PAYOFF INPUTS
# --------------------------------------------------

default_payoffs = game["payoffs"]

for i in range(2):
    for j in range(2):
        st.session_state.setdefault(
            f"a{i}{j}", default_payoffs[i][j][0]
        )
        st.session_state.setdefault(
            f"b{i}{j}", default_payoffs[i][j][1]
        )


# --------------------------------------------------
# PAYOFF MATRIX INPUT
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-heading">03 &nbsp; Payoff matrix</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Each cell contains two payoffs. The first belongs to the row player; '
    'the second belongs to the column player. Change any value as needed.'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Rows: {player_a or 'Player A'}  ·  "
    f"Columns: {player_b or 'Player B'}"
)

# Column headings correspond to Player B's strategies.
header = st.columns([1.0, 1.35, 1.35])

with header[0]:
    st.markdown("**Row strategy**")

with header[1]:
    st.markdown(f"**{b_strategies[0]}**")

with header[2]:
    st.markdown(f"**{b_strategies[1]}**")


# Matrix rows correspond to Player A's strategies.
for i in range(2):
    matrix_cols = st.columns([1.0, 1.35, 1.35])

    with matrix_cols[0]:
        st.markdown("")
        st.markdown(f"**{a_strategies[i]}**")

    for j in range(2):
        with matrix_cols[j + 1]:
            with st.container(border=True):
                st.markdown(
                    f'<div class="cell-heading">'
                    f'{a_strategies[i]} × {b_strategies[j]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                payoff_cols = st.columns(2)

                with payoff_cols[0]:
                    st.number_input(
                        f"{player_a or 'A'} payoff",
                        step=1,
                        key=f"a{i}{j}",
                        label_visibility="collapsed",
                        help="Payoff received by the row player."
                    )

                with payoff_cols[1]:
                    st.number_input(
                        f"{player_b or 'B'} payoff",
                        step=1,
                        key=f"b{i}{j}",
                        label_visibility="collapsed",
                        help="Payoff received by the column player."
                    )

                st.caption(
                    f"Left: {player_a or 'A'} · "
                    f"Right: {player_b or 'B'}"
                )


# Read current values after all inputs are rendered.
payoffs = [
    [
        (st.session_state[f"a{i}{j}"],
         st.session_state[f"b{i}{j}"])
        for j in range(2)
    ]
    for i in range(2)
]


# --------------------------------------------------
# MATRIX PREVIEW
# --------------------------------------------------

st.markdown("#### Matrix preview")

matrix_data = [
    [
        f"({payoffs[i][j][0]}, {payoffs[i][j][1]})"
        for j in range(2)
    ]
    for i in range(2)
]

preview = pd.DataFrame(
    matrix_data,
    index=a_strategies,
    columns=b_strategies
)

preview.index.name = f"{player_a or 'Player A'} ↓"
preview.columns.name = f"{player_b or 'Player B'} →"

st.dataframe(
    preview,
    use_container_width=True
)

st.caption("Payoff format: (row player's payoff, column player's payoff)")


# --------------------------------------------------
# ANALYSIS FUNCTIONS
# --------------------------------------------------

def analyze_game(payoffs):
    # Best responses for Player A, for each strategy of B.
    best_a = {}

    for j in range(2):
        highest = max(payoffs[i][j][0] for i in range(2))
        best_a[j] = [
            i for i in range(2)
            if payoffs[i][j][0] == highest
        ]

    # Best responses for Player B, for each strategy of A.
    best_b = {}

    for i in range(2):
        highest = max(payoffs[i][j][1] for j in range(2))
        best_b[i] = [
            j for j in range(2)
            if payoffs[i][j][1] == highest
        ]

    # Find weakly dominant strategies.
    # A strategy must do at least as well everywhere
    # and strictly better in at least one comparison.

    dominant_a = []
    dominant_b = []

    for i in range(2):
        other = 1 - i
        differences = [
            payoffs[i][j][0] - payoffs[other][j][0]
            for j in range(2)
        ]

        if all(d >= 0 for d in differences) and any(
            d > 0 for d in differences
        ):
            dominant_a.append(i)

    for j in range(2):
        other = 1 - j
        differences = [
            payoffs[i][j][1] - payoffs[i][other][1]
            for i in range(2)
        ]

        if all(d >= 0 for d in differences) and any(
            d > 0 for d in differences
        ):
            dominant_b.append(j)

    # A Nash Equilibrium occurs where both players
    # are playing best responses simultaneously.
    equilibria = []

    for i in range(2):
        for j in range(2):
            if i in best_a[j] and j in best_b[i]:
                equilibria.append((i, j))

    return best_a, best_b, dominant_a, dominant_b, equilibria


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

st.divider()

analyze = st.button(
    "Analyze game",
    type="primary",
    use_container_width=True
)

if analyze:
    best_a, best_b, dominant_a, dominant_b, equilibria = (
        analyze_game(payoffs)
    )

    st.session_state["analysis_result"] = {
        "game_name": game_name,
        "payoffs": payoffs,
        "a_strategies": a_strategies,
        "b_strategies": b_strategies,
        "player_a": player_a or "Player A",
        "player_b": player_b or "Player B",
        "best_a": best_a,
        "best_b": best_b,
        "dominant_a": dominant_a,
        "dominant_b": dominant_b,
        "equilibria": equilibria
    }


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

result = st.session_state.get("analysis_result")

if result:
    # Avoid showing stale results for a different game or
    # different payoff values before Analyze is clicked again.
    current_signature = (
        game_name,
        tuple(a_strategies),
        tuple(b_strategies),
        tuple(tuple(cell for cell in row) for row in payoffs),
        player_a,
        player_b
    )

    saved_signature = (
        result["game_name"],
        tuple(result["a_strategies"]),
        tuple(result["b_strategies"]),
        tuple(tuple(cell for cell in row)
              for row in result["payoffs"]),
        result["player_a"],
        result["player_b"]
    )

    if current_signature != saved_signature:
        st.info("Your inputs have changed. Click **Analyze game** to refresh the results.")
    else:
        st.divider()

        st.markdown(
            '<div class="section-heading">'
            '04 &nbsp; Analysis results'
            '</div>',
            unsafe_allow_html=True
        )

        equilibria = result["equilibria"]
        dominant_a = result["dominant_a"]
        dominant_b = result["dominant_b"]

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">Pure Nash Equilibria</div>'
                f'<div class="metric-value">{len(equilibria)}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with m2:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">Dominant strategy · '
                f'{result["player_a"]}</div>'
                f'<div class="metric-value">'
                f'{len(dominant_a)}</div></div>',
                unsafe_allow_html=True
            )

        with m3:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">Dominant strategy · '
                f'{result["player_b"]}</div>'
                f'<div class="metric-value">'
                f'{len(dominant_b)}</div></div>',
                unsafe_allow_html=True
            )

        # Best responses
        st.markdown("#### Best responses")

        response_col_a, response_col_b = st.columns(2)

        with response_col_a:
            st.markdown(f"**{result['player_a']}**")

            for j in range(2):
                names = [
                    result["a_strategies"][i]
                    for i in result["best_a"][j]
                ]

                st.write(
                    f"When {result['player_b']} chooses "
                    f"**{result['b_strategies'][j]}**, "
                    f"the best response is **{', '.join(names)}**."
                )

        with response_col_b:
            st.markdown(f"**{result['player_b']}**")

            for i in range(2):
                names = [
                    result["b_strategies"][j]
                    for j in result["best_b"][i]
                ]

                st.write(
                    f"When {result['player_a']} chooses "
                    f"**{result['a_strategies'][i]}**, "
                    f"the best response is **{', '.join(names)}**."
                )

        # Dominant strategies
        st.markdown("#### Dominant strategies")

        dcol_a, dcol_b = st.columns(2)

        with dcol_a:
            st.markdown(f"**{result['player_a']}**")

            if dominant_a:
                for i in dominant_a:
                    st.success(
                        f"Weakly dominant: "
                        f"{result['a_strategies'][i]}"
                    )
            else:
                st.write("No weakly dominant strategy.")

        with dcol_b:
            st.markdown(f"**{result['player_b']}**")

            if dominant_b:
                for j in dominant_b:
                    st.success(
                        f"Weakly dominant: "
                        f"{result['b_strategies'][j]}"
                    )
            else:
                st.write("No weakly dominant strategy.")

        # Nash Equilibria
        st.markdown("#### Nash Equilibrium")

        if equilibria:
            for i, j in equilibria:
                pa, pb = result["payoffs"][i][j]

                st.markdown(
                    f'<div class="result-box">'
                    f'<div class="result-title">'
                    f'{result["a_strategies"][i]} × '
                    f'{result["b_strategies"][j]}'
                    f'</div>'
                    f'<div>Payoffs: {result["player_a"]} = {pa}, '
                    f'{result["player_b"]} = {pb}</div>'
                    f'<div style="color:#476456; margin-top:0.4rem;">'
                    f'Neither player can improve their payoff by '
                    f'changing strategy alone.</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.warning(
                "No pure Nash Equilibrium exists for these payoffs. "
                "A mixed-strategy equilibrium may exist."
            )

        st.caption(
            "Dominant strategies are checked using the weak-dominance "
            "definition. This version identifies pure Nash Equilibria; "
            "mixed-strategy calculation is not included."
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "GAME THEORY LAB  /  Interactive strategic decision analysis"
)

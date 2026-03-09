import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="♻️ Sustainability Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  JEWEL TONE THEME CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #E8E8EA !important;
    color: #1C1B2E;
}

/* Force ALL Streamlit wrappers to the grey background */
.stApp,
.stApp > header,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="block-container"],
.main .block-container,
section.main,
.css-1d391kg,
.css-18e3th9 {
    background-color: #E8E8EA !important;
}

/* Remove any white card padding areas */
[data-testid="stVerticalBlock"] {
    background-color: transparent !important;
}

/* ── Hero header ── */
.main-header {
    background: linear-gradient(135deg, #5C2D91 0%, #1A5276 45%, #0E6655 100%);
    border-radius: 22px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(92,45,145,0.30);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: "";
    position: absolute;
    width: 320px; height: 320px;
    border-radius: 50%;
    background: rgba(212,175,55,0.12);
    top: -80px; right: -60px;
}
.main-header::after {
    content: "";
    position: absolute;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
    bottom: -50px; left: 40px;
}
.main-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    font-weight: 900;
    color: #F5E6C8;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.3px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.25);
}
.main-header p {
    color: rgba(245,230,200,0.82);
    font-size: 1.02rem;
    margin: 0;
    line-height: 1.6;
}

/* ── KPI cards ── */
.kpi-card {
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 6px 24px rgba(0,0,0,0.12);
    text-align: center;
    position: relative;
    overflow: hidden;
    border-top: 3px solid rgba(212,175,55,0.5);
}
.kpi-card::before {
    content: "";
    position: absolute;
    width: 100px; height: 100px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    top: -30px; right: -20px;
}
.kpi-purple { background: linear-gradient(135deg, #2D1B54, #4A2880); }
.kpi-teal   { background: linear-gradient(135deg, #2D1B54, #4A2880); }
.kpi-gold   { background: linear-gradient(135deg, #2D1B54, #4A2880); }
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: rgba(255,255,255,0.70);
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
}

/* ── Section headings ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #1C1B2E;
    border-left: 6px solid #D4AF37;
    padding-left: 0.8rem;
    margin: 2rem 0 1rem 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2D1B54 0%, #0E4D40 100%) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #F5E6C8 !important;
}
.sidebar-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #D4AF37 !important;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid rgba(212,175,55,0.35);
    padding-bottom: 0.8rem;
}

/* ── Success box ── */
div[data-testid="stAlert"] {
    background: linear-gradient(90deg, #E8F8F5, #D5F5E3) !important;
    border-left: 5px solid #0E6655 !important;
    border-radius: 12px;
    color: #0B4C3A !important;
    font-weight: 600;
}

/* ── Dataframe header ── */
[data-testid="stDataFrameResizable"] thead tr th {
    background: #2D1B54 !important;
    color: #D4AF37 !important;
    font-weight: 700;
}


/* ── Styled HTML tables ── */
.tbl-wrap {
    background: #ffffff;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(44, 27, 84, 0.10);
    margin-bottom: 1rem;
    border: 1px solid #DDD8E8;
}
.tbl-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    background: linear-gradient(90deg, #2D1B54, #4A2880);
    padding: 0.85rem 1.2rem;
    letter-spacing: 0.2px;
}
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.88rem;
}
.styled-table thead tr {
    background: linear-gradient(90deg, #2D1B54, #4A2880);
}
.styled-table thead th {
    color: #D4AF37 !important;
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 0.75rem 1.1rem;
    text-align: left;
    border: none;
}
.styled-table tbody tr {
    border-bottom: 1px solid #EDE9F5;
    transition: background 0.15s;
}
.styled-table tbody tr:nth-child(even) {
    background: #F5F2FB;
}
.styled-table tbody tr:nth-child(odd) {
    background: #FDFCFF;
}
.styled-table tbody tr:hover {
    background: #EDE2F5;
}
.tbl-icon {
    padding: 0.7rem 0.6rem 0.7rem 1.1rem;
    font-size: 1rem;
    width: 2rem;
}
.tbl-feat {
    padding: 0.7rem 1rem;
    color: #2D1B54;
    font-weight: 600;
}
.tbl-val {
    padding: 0.7rem 1.1rem;
    color: #1A8A72;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    text-align: center;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #EBEBED; }
::-webkit-scrollbar-thumb { background: #D4AF37; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD ASSETS
# ─────────────────────────────────────────────
@st.cache_resource
def load_assets():
    model_lr     = joblib.load("logistic_model.pkl")
    model_rf     = joblib.load("random_forest_model.pkl")
    X_cols       = joblib.load("feature_columns.pkl")
    test_results = joblib.load("test_results.pkl")
    df           = joblib.load("cleaned_df.pkl")
    return model_lr, model_rf, X_cols, test_results, df

model_lr, model_rf, X_cols, test_results, df = load_assets()

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>♻️ Sustainability Prediction</h1>
  <p>Explore how waste-flow characteristics influence sustainability outcomes!<br>
     <em>Compare <strong>Logistic Regression</strong> and <strong>Random Forest</strong>,
     simulate new scenarios, and visualize the prediction space.</em></p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">⚙️ Scenario Controls</div>', unsafe_allow_html=True)
    model_choice = st.selectbox("Classification Model",
                                ["Random Forest", "Logistic Regression"])
    st.markdown("---")
    generated_tons = st.slider(
        "🏭 Generated Tons",
        min_value=1000.0,
        max_value=float(max(50000, df["generated_tons"].max())),
        value=float(df["generated_tons"].median()),
        step=100.0
    )
    st.markdown("**Waste Distribution**")
    recycling_rate   = st.slider("♻️ Recycling Rate",   0.0, 1.0, 0.50, 0.01)
    landfill_share   = st.slider("🪣 Landfill Share",   0.0, 1.0, 0.30, 0.01)
    combustion_share = st.slider("🔥 Combustion Share", 0.0, 1.0, 0.20, 0.01)

total_share = recycling_rate + landfill_share + combustion_share or 1.0
recycling_rate   /= total_share
landfill_share   /= total_share
combustion_share /= total_share

recycled_tons   = recycling_rate   * generated_tons
landfilled_tons = landfill_share   * generated_tons
combusted_tons  = combustion_share * generated_tons

input_df = pd.DataFrame([{
    "generated_tons":   generated_tons,
    "recycled_tons":    recycled_tons,
    "landfilled_tons":  landfilled_tons,
    "combusted_tons":   combusted_tons,
    "recycling_rate":   recycling_rate,
    "landfill_share":   landfill_share,
    "combustion_share": combustion_share
}])

# ─────────────────────────────────────────────
#  PREDICTIONS
# ─────────────────────────────────────────────
class_model = model_rf if model_choice == "Random Forest" else model_lr

pred_class = class_model.predict(input_df)[0]
pred_probs = class_model.predict_proba(input_df)[0]

# score derived from selected model probabilities
class_score_map = {"Harmful": 0, "Moderate": 50, "Sustainable": 100}
pred_score = float(sum(
    prob * class_score_map[label]
    for label, prob in zip(class_model.classes_, pred_probs)
))

selected_row = test_results[test_results["Model"] == model_choice].iloc[0]
overall_best_model = test_results.loc[test_results["Macro F1"].idxmax(), "Model"]
overall_best_f1 = test_results["Macro F1"].max()

# ─────────────────────────────────────────────
#  KPI CARDS
# ─────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""<div class="kpi-card kpi-purple">
      <div class="kpi-label">Predicted Class</div>
      <div class="kpi-value">{pred_class}</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card kpi-teal">
      <div class="kpi-label">Sustainability Score</div>
      <div class="kpi-value">{pred_score:.1f}</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card kpi-gold">
      <div class="kpi-label">Model Used</div>
      <div class="kpi-value" style="font-size:1.3rem">{model_choice}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SHARED CHART SETTINGS
# ─────────────────────────────────────────────
JEWEL      = ["#7D3C98", "#1A8A72", "#D4AF37", "#1A5276",
              "#C0392B", "#2E86C1", "#CA6F1E", "#0B5345"]
CHART_BG   = "#F7F7F8"
GRID_COLOR = "#DDD8E8"
FONT       = {"family": "IBM Plex Sans"}

# ─────────────────────────────────────────────
#  GAUGE + PROBABILITY
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Prediction Overview</div>', unsafe_allow_html=True)
left, right = st.columns(2)

with left:
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pred_score,
        title={"text": "<b>Sustainability Score</b>",
               "font": {"size": 15, "color": "#1C1B2E", "family": "IBM Plex Sans"}},
        number={"font": {"color": "#5C2D91", "size": 52, "family": "Playfair Display"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#5C2D91",
                     "tickfont": {"color": "#5C2D91"}},
            "bar": {"color": "#D4AF37", "thickness": 0.28},
            "bgcolor": CHART_BG,
            "bordercolor": "#C9C3D8",
            "steps": [
                {"range": [0,  30], "color": "#F5C6C6"},
                {"range": [30, 70], "color": "#EDE2F5"},
                {"range": [70, 100], "color": "#C8EBE4"}
            ],
            "threshold": {
                "line": {"color": "#5C2D91", "width": 3},
                "thickness": 0.78, "value": pred_score
            }
        }
    ))
    gauge.update_layout(height=340, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                        margin=dict(l=30, r=30, t=60, b=10), font=FONT)
    st.plotly_chart(
    gauge,
    use_container_width=True
)

with right:
    prob_df = pd.DataFrame({
        "Class": class_model.classes_, "Probability": pred_probs
    }).sort_values("Probability", ascending=True)

    fig_prob = px.bar(
        prob_df, x="Probability", y="Class", orientation="h",
        text="Probability", title="<b>Prediction Probabilities</b>",
        color="Probability",
        color_continuous_scale=[[0, "#EDE2F5"], [0.5, "#7D3C98"], [1, "#3B0764"]]
    )
    fig_prob.update_traces(texttemplate="%{text:.2f}", textposition="outside",
                           marker_line_width=0)
    fig_prob.update_layout(
        height=340, paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        xaxis_range=[0, 1.15], coloraxis_showscale=False, font=FONT,
        title_font_size=14,
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color="#1C1B2E"),
        yaxis=dict(showgrid=False, color="#1C1B2E"),
        margin=dict(l=10, r=30, t=50, b=20)
    )
    st.plotly_chart(fig_prob, use_container_width=True)

# ─────────────────────────────────────────────
#  SCENARIO SUMMARY
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Current Scenario Summary</div>', unsafe_allow_html=True)

summary_rows = [
    ("🏭", "Generated Tons",   f"{generated_tons:,.1f}"),
    ("♻️", "Recycled Tons",    f"{recycled_tons:,.1f}"),
    ("🪣", "Landfilled Tons",  f"{landfilled_tons:,.1f}"),
    ("🔥", "Combusted Tons",   f"{combusted_tons:,.1f}"),
    ("📊", "Recycling Rate",   f"{recycling_rate:.3f}"),
    ("📊", "Landfill Share",   f"{landfill_share:.3f}"),
    ("📊", "Combustion Share", f"{combustion_share:.3f}"),
]
rows_html = "".join(
    f'<tr><td class="tbl-icon">{icon}</td><td class="tbl-feat">{feat}</td><td class="tbl-val">{val}</td></tr>'
    for icon, feat, val in summary_rows
)
st.markdown(f"""
<div class="tbl-wrap">
  <table class="styled-table">
    <thead><tr><th></th><th>Feature</th><th>Value</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  3D PREDICTION SPACE
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🌐 3D Prediction Space</div>', unsafe_allow_html=True)

df_plot = df.copy()
df_plot["model_pred"] = class_model.predict(df[X_cols])

fig3d = px.scatter_3d(
    df_plot,
    x="recycling_rate",
    y="landfill_share",
    z="combustion_share",
    color="model_pred",
    opacity=0.62,
    title=f"Prediction Space — {model_choice}",
    color_discrete_sequence=JEWEL
)

fig3d.add_trace(go.Scatter3d(
    x=[recycling_rate],
    y=[landfill_share],
    z=[combustion_share],
    mode="markers+text",
    marker=dict(size=10, color="#D4AF37", symbol="diamond"),
    text=[f"Input: {pred_class}"],
    textposition="top center",
    name="Input"
))

fig3d.update_layout(
    height=640,
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(
    fig3d,
    use_container_width=True,
    config={"scrollZoom": True, "displayModeBar": True}
)


# ─────────────────────────────────────────────
#  2D LOGISTIC DECISION MAP
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🗺️ 2D Logistic Regression Decision Map</div>', unsafe_allow_html=True)

# grid for 2D space
x_min, x_max = df["recycling_rate"].min(), df["recycling_rate"].max()
y_min, y_max = df["landfill_share"].min(), df["landfill_share"].max()

xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 120),
    np.linspace(y_min, y_max, 120)
)

# fix combustion share at current input value
comb_fixed = combustion_share
generated_fixed = generated_tons

# build grid features
grid_df = pd.DataFrame({
    "recycling_rate": xx.ravel(),
    "landfill_share": yy.ravel(),
    "combustion_share": comb_fixed
})

# convert rates into tons so model gets full feature set
grid_df["recycled_tons"] = grid_df["recycling_rate"] * generated_fixed
grid_df["landfilled_tons"] = grid_df["landfill_share"] * generated_fixed
grid_df["combusted_tons"] = grid_df["combustion_share"] * generated_fixed
grid_df["generated_tons"] = generated_fixed

grid_df = grid_df[[
    "generated_tons",
    "recycled_tons",
    "landfilled_tons",
    "combusted_tons",
    "recycling_rate",
    "landfill_share",
    "combustion_share"
]]

# logistic predictions on grid
grid_pred = model_lr.predict(grid_df)
z = pd.Categorical(grid_pred).codes.reshape(xx.shape)

fig2d = go.Figure()

# background decision regions
fig2d.add_trace(go.Contour(
    x=np.linspace(x_min, x_max, 120),
    y=np.linspace(y_min, y_max, 120),
    z=z,
    colorscale=[
        [0.0, "#F5C6C6"],
        [0.5, "#EDE2F5"],
        [1.0, "#C8EBE4"]
    ],
    opacity=0.55,
    showscale=False,
    contours=dict(showlines=False)
))

# actual historical points
df_plot_lr = df.copy()
df_plot_lr["model_pred"] = model_lr.predict(df[X_cols])

for cls, color in zip(
    ["Harmful", "Moderate", "Sustainable"],
    ["#C0392B", "#7D3C98", "#1A8A72"]
):
    sub = df_plot_lr[df_plot_lr["model_pred"] == cls]
    fig2d.add_trace(go.Scatter(
        x=sub["recycling_rate"],
        y=sub["landfill_share"],
        mode="markers",
        marker=dict(size=7, color=color, opacity=0.7),
        name=cls
    ))

# user input point
fig2d.add_trace(go.Scatter(
    x=[recycling_rate],
    y=[landfill_share],
    mode="markers+text",
    marker=dict(size=16, color="#D4AF37", symbol="diamond",
                line=dict(color="#5C2D91", width=2)),
    text=["Input"],
    textposition="top center",
    name="Input"
))

fig2d.update_layout(
    title="<b>2D Logistic Regression Decision Map</b>",
    height=520,
    paper_bgcolor=CHART_BG,
    plot_bgcolor="#F0EBF8",
    font=FONT,
    xaxis=dict(title="Recycling Rate", showgrid=True, gridcolor=GRID_COLOR, color="#1C1B2E"),
    yaxis=dict(title="Landfill Share", showgrid=True, gridcolor=GRID_COLOR, color="#1C1B2E"),
    legend=dict(bgcolor="#EBEBED", bordercolor="#C9C3D8", borderwidth=1,
                font=dict(color="#1C1B2E")),
    margin=dict(l=20, r=20, t=55, b=20)
)

st.plotly_chart(fig2d, use_container_width=True)

# ─────────────────────────────────────────────
#  MODEL PERFORMANCE
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Model Performance Comparison</div>', unsafe_allow_html=True)

def df_to_styled_html(df, title):
    header = "".join(f'<th>{c}</th>' for c in df.columns)
    body = ""
    for _, row in df.iterrows():
        cells = ""
        for i, v in enumerate(row):
            if i == 0:
                cells += f'<td class="tbl-feat">{v}</td>'
            else:
                try:
                    cells += f'<td class="tbl-val">{float(v):.3f}</td>'
                except:
                    cells += f'<td class="tbl-val">{v}</td>'
        body += f"<tr>{cells}</tr>"
    return f"""
<div class="tbl-wrap">
  <div class="tbl-title">{title}</div>
  <table class="styled-table">
    <thead><tr>{header}</tr></thead>
    <tbody>{body}</tbody>
  </table>
</div>"""


st.markdown(df_to_styled_html(test_results, "Test Set Results"), unsafe_allow_html=True)

results_long = test_results.melt(id_vars="Model", var_name="Metric", value_name="Score")

fig_metrics = px.bar(
    results_long, x="Metric", y="Score", color="Model",
    barmode="group", text="Score",
    title="<b>Test Set Performance Comparison</b>",
    color_discrete_map={
        "Random Forest":       "#7D3C98",
        "Logistic Regression": "#1A8A72"
    }
)
fig_metrics.update_traces(texttemplate="%{text:.2f}", textposition="outside",
                          marker_line_width=0)
fig_metrics.update_layout(
    yaxis_range=[0, 1.15], height=480,
    paper_bgcolor=CHART_BG, plot_bgcolor="#F0EBF8", font=FONT,
    title_font_size=14,
    xaxis=dict(showgrid=False, color="#1C1B2E"),
    yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color="#1C1B2E"),
    legend=dict(bgcolor="#EBEBED", bordercolor="#C9C3D8", borderwidth=1,
                font=dict(color="#1C1B2E")),
    margin=dict(l=20, r=20, t=60, b=20)
)
st.plotly_chart(fig_metrics, use_container_width=True)

best_model = test_results.loc[test_results["Macro F1"].idxmax(), "Model"]
best_f1    = test_results["Macro F1"].max()
st.success(f"🏆  Best test-set model: **{best_model}** — Macro F1 = **{best_f1:.2f}**")

# ─────────────────────────────────────────────
#  FEATURE IMPORTANCE
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🔍 Feature Importance — Random Forest</div>', unsafe_allow_html=True)

rf_importance = pd.DataFrame({
    "Feature": X_cols, "Importance": model_rf.feature_importances_
}).sort_values("Importance", ascending=True)

fig_imp = px.bar(
    rf_importance, x="Importance", y="Feature", orientation="h",
    title="<b>Random Forest Feature Importance</b>",
    color="Importance",
    color_continuous_scale=[[0, "#C8EBE4"], [0.5, "#1A8A72"], [1, "#0B4D3A"]]
)
fig_imp.update_layout(
    height=460, paper_bgcolor=CHART_BG, plot_bgcolor="#F0EBF8",
    coloraxis_showscale=False, font=FONT, title_font_size=14,
    xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color="#1C1B2E"),
    yaxis=dict(showgrid=False, color="#1C1B2E"),
    margin=dict(l=20, r=20, t=55, b=20)
)
st.plotly_chart(fig_imp, use_container_width=True)


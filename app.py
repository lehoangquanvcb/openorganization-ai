
import streamlit as st
from pathlib import Path
import pandas as pd
import math
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import load_all
from modules.analytics import *
from modules.ai import *

st.set_page_config(page_title="OpenOrganization AI - Author: Le Hoang Quan", page_icon="🧠", layout="wide")
data = load_all(Path("data"))

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
[data-testid="stSidebar"] {background: #F4F8F5;}
.metric-card {background: white; border: 1px solid #E3E8E4; border-radius: 16px; padding: 18px; box-shadow: 0 2px 10px rgba(0,0,0,0.04);}
.metric-label {font-size: 0.85rem; color: #60706A; margin-bottom: 6px;}
.metric-value {font-size: 2.1rem; font-weight: 800; color: #0B1F33;}
.metric-note {font-size: 0.8rem; color: #60706A;}
.agent-card {background:#FFFFFF; border:1px solid #E3E8E4; border-radius:14px; padding:16px; margin-bottom:12px;}
.green-badge {display:inline-block; padding:4px 10px; background:#E8F5E9; color:#1B5E20; border-radius:999px; font-size:0.8rem; font-weight:700;}
.red-badge {display:inline-block; padding:4px 10px; background:#FDECEA; color:#B71C1C; border-radius:999px; font-size:0.8rem; font-weight:700;}
.blue-badge {display:inline-block; padding:4px 10px; background:#EAF2FF; color:#0B3D91; border-radius:999px; font-size:0.8rem; font-weight:700;}
h1, h2, h3 {letter-spacing: -0.02em;}
</style>
""", unsafe_allow_html=True)

def card(label, value, note=""):
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def gauge(title, value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=float(value), title={"text": title},
        gauge={"axis":{"range":[0,100]},"bar":{"color":"#2E7D32"},
               "steps":[{"range":[0,60],"color":"#FDECEA"},{"range":[60,80],"color":"#FFF8E1"},{"range":[80,100],"color":"#E8F5E9"}]}))
    fig.update_layout(height=230, margin=dict(l=10,r=10,t=40,b=10))
    st.plotly_chart(fig, use_container_width=True)

def relationship_network_figure(edges, max_edges=80):
    """Draw a lightweight network graph with Plotly only."""
    e = edges[["from", "relationship", "to"]].head(max_edges).copy()
    e["from"] = e["from"].astype(str)
    e["to"] = e["to"].astype(str)
    nodes = sorted(pd.concat([e["from"], e["to"]], ignore_index=True).dropna().unique().tolist())
    n = max(len(nodes), 1)
    pos = {}
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n
        radius = 1.0 + (i % 5) * 0.08
        pos[node] = (radius * math.cos(angle), radius * math.sin(angle))

    edge_x, edge_y = [], []
    for _, r in e.iterrows():
        x0, y0 = pos[r["from"]]
        x1, y1 = pos[r["to"]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    node_x = [pos[node][0] for node in nodes]
    node_y = [pos[node][1] for node in nodes]

    def node_type(node):
        if "KPI" in node or "Index" in node or "Growth" in node:
            return "KPI"
        if "Policy" in node or "SOP" in node or "JD" in node:
            return "Document"
        if any(x in node for x in ["Program", "Roadmap", "Pilot", "Assessment", "Center"]):
            return "Project"
        if len(node.split()) >= 3:
            return "Employee"
        return "Skill/Other"

    types = [node_type(n) for n in nodes]
    colors = {"Employee":"#2E7D32", "KPI":"#1565C0", "Document":"#6A1B9A", "Project":"#EF6C00", "Skill/Other":"#455A64"}
    node_colors = [colors[t] for t in types]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=0.8, color="#B0BEC5"), hoverinfo="none"))
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers+text", text=nodes, textposition="top center",
        marker=dict(size=14, color=node_colors, line=dict(width=1, color="white")),
        hovertext=[f"{node}<br>Type: {typ}" for node, typ in zip(nodes, types)],
        hoverinfo="text"
    ))
    fig.update_layout(
        height=650, showlegend=False, title="Interactive Organization Knowledge Graph",
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        margin=dict(l=10,r=10,t=40,b=10)
    )
    return fig

def process_flow_figure(df):
    step = df.groupby("step", sort=False)["duration_days"].mean().reset_index()
    step["x"] = list(range(len(step)))
    step["y"] = [0] * len(step)
    max_dur = step["duration_days"].max()
    colors = ["#D32F2F" if v == max_dur else "#F9A825" if v > step["duration_days"].mean() else "#2E7D32" for v in step["duration_days"]]

    fig = go.Figure()
    for i in range(len(step)-1):
        fig.add_annotation(x=step.loc[i+1,"x"]-0.18, y=0, ax=step.loc[i,"x"]+0.18, ay=0,
                           xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=3, arrowsize=1.2, arrowwidth=2, arrowcolor="#78909C")
    fig.add_trace(go.Scatter(
        x=step["x"], y=step["y"], mode="markers+text",
        text=[f"{r.step}<br>{r.duration_days:.1f}d" for _, r in step.iterrows()],
        textposition="bottom center",
        marker=dict(size=[24 + v*2 for v in step["duration_days"]], color=colors, line=dict(width=2,color="white")),
        hoverinfo="text"
    ))
    fig.update_layout(height=330, title="Process Flow with Bottleneck Highlight", showlegend=False,
                      xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-1,1]),
                      margin=dict(l=10,r=10,t=40,b=10))
    return fig

st.sidebar.title("🧠 OpenOrganization AI")
st.sidebar.markdown("**Author: Le Hoang Quan**")
st.sidebar.caption("Knowledge Graph • Process Flow • Board Pack")
module = st.sidebar.radio("Chọn phân hệ", [
    "🏠 CEO Morning Brief",
    "🧠 Organization Digital Brain",
    "💬 Chat with Organization",
    "👥 Multi-Agent Boardroom",
    "📋 Executive Meeting AI",
    "⛏️ Process Mining",
    "📄 Document Intelligence",
    "🎯 Executive Decision Center",
    "🧭 Scenario Planning",
    "🏢 Organization Digital Twin",
    "⚠️ People Risk",
    "📊 KPI Cascade",
    "👑 Leadership Digital Twin",
    "🕸️ Knowledge Graph",
    "🧾 Organization Memory",
    "🗃️ Data Tables",
])

if module == "🏠 CEO Morning Brief":
    st.title("CEO Morning Brief")
    b = morning_brief(data)
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: card("Headcount", f"{b['headcount']:,}", "Virtual company")
    with c2: card("Org Health", f"{b['org_health']:.1f}", "7S + ADKAR")
    with c3: card("People Risk", f"{b['people_risk']:.1f}", "Attrition risk")
    with c4: card("Culture", f"{b['culture']:.1f}", "Latest survey")
    with c5: card("Strategy", f"{b['strategy']:.1f}%", "Execution")
    col1,col2,col3 = st.columns(3)
    with col1: gauge("Organization Health", b["org_health"])
    with col2: gauge("Culture", b["culture"])
    with col3: gauge("Leadership", b["leadership"])
    st.markdown("### AI Executive Summary")
    st.info(b["summary"])
    st.markdown("### Critical Alerts")
    for a in b["alerts"]:
        st.warning(a)

elif module == "🧠 Organization Digital Brain":
    st.title("Organization Digital Brain")
    st.caption("Employee → Skill → Project → KPI → Meeting → Document")
    g = build_digital_brain(data)
    c1,c2,c3,c4 = st.columns(4)
    with c1: card("Nodes", g["nodes"], "Knowledge graph")
    with c2: card("Edges", g["edges"], "Relationships")
    with c3: card("Skill Links", g["employee_skill_links"], "Employee-skill")
    with c4: card("Meeting Links", g["meeting_links"], "Actions & owners")
    edges = g["sample_edges"].copy()
    st.markdown("### Interactive Relationship Network")
    st.plotly_chart(relationship_network_figure(edges), use_container_width=True)
    st.markdown("### Relationship Table")
    st.dataframe(edges[["from","relationship","to"]].head(150), use_container_width=True)

elif module == "💬 Chat with Organization":
    st.title("Chat with Organization")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    examples = ["Phòng Sales đang có vấn đề gì?", "Ai có nguy cơ nghỉ việc cao?", "KPI nào đang tụt?", "Quy trình nào đang nghẽn?", "Tài liệu nào có rủi ro?"]
    q = st.selectbox("Câu hỏi mẫu", examples)
    custom = st.text_input("Hoặc nhập câu hỏi khác")
    question = custom if custom else q
    if st.button("Ask Copilot"):
        answer = copilot(question, data)
        st.session_state.chat_history.append(("user", question))
        st.session_state.chat_history.append(("assistant", answer))
    for role, msg in st.session_state.chat_history[-8:]:
        with st.chat_message(role):
            st.markdown(msg)

elif module == "👥 Multi-Agent Boardroom":
    st.title("Multi-Agent Boardroom")
    q = st.text_input("Câu hỏi cho các agent", "Có nên thành lập Phòng AI & Organization Intelligence không?")
    if st.button("Run Multi-Agent Discussion"):
        st.markdown(multi_agent_discussion(q, data), unsafe_allow_html=True)
    st.markdown("### Agent Views")
    st.dataframe(data["agent_views"], use_container_width=True)

elif module == "📋 Executive Meeting AI":
    st.title("Executive Meeting AI")
    mt = st.selectbox("Meeting type", ["CEO Weekly","HR Committee","Transformation Office","Board Meeting"])
    st.markdown(generate_meeting_pack(mt, data), unsafe_allow_html=True)
    actions = data["meetings"][data["meetings"]["status"].isin(["Open","Overdue"])].copy()
    st.markdown("### Open / Overdue Action Tracker")
    st.dataframe(actions.head(30), use_container_width=True)

elif module == "⛏️ Process Mining":
    st.title("Process Mining")
    log = data["process_log"]
    st.info(process_mining_summary(log))
    proc = st.selectbox("Process", sorted(log.process.unique()))
    df = log[log.process == proc]
    st.plotly_chart(process_flow_figure(df), use_container_width=True)
    step_summary = df.groupby("step")["duration_days"].mean().reset_index().sort_values("duration_days", ascending=False)
    col1,col2 = st.columns([1.1,1])
    with col1:
        fig = px.bar(step_summary, x="step", y="duration_days", text="duration_days", title=f"Average duration by step - {proc}")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.box(df, x="step", y="duration_days", color="owner", title="Duration distribution")
        st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df.head(120), use_container_width=True)

elif module == "📄 Document Intelligence":
    st.title("Document Intelligence")
    docs = data["documents"]
    st.dataframe(docs, use_container_width=True)
    selected = st.selectbox("Chọn tài liệu", docs["title"].tolist())
    doc = docs[docs["title"] == selected].iloc[0].to_dict()
    st.markdown(document_review(doc), unsafe_allow_html=True)

elif module == "🎯 Executive Decision Center":
    st.title("Executive Decision Center")
    df = decision_center(data)
    st.dataframe(df, use_container_width=True)
    fig = px.scatter(df, x="risk_score", y="roi_score", size="priority_score", color="decision_type", hover_name="decision", title="Priority Matrix: Risk vs ROI")
    st.plotly_chart(fig, use_container_width=True)

elif module == "🧭 Scenario Planning":
    st.title("Scenario Planning")
    s = st.selectbox("Scenario", ["Mở thêm nhà máy","Cắt giảm 15% nhân sự","Thành lập Phòng AI","M&A integration","Tái cấu trúc Sales & Finance"])
    st.markdown(scenario_summary(s, data))

elif module == "🏢 Organization Digital Twin":
    st.title("Organization Digital Twin")
    emp = data["employees"]
    view = st.selectbox("Color by", ["performance_score","engagement_score","attrition_risk"])
    fig = px.treemap(emp, path=["subsidiary","division","department","role"], values="fte", color=view, color_continuous_scale="RdYlGn" if view!="attrition_risk" else "RdYlGn_r", title="Organization Digital Twin")
    st.plotly_chart(fig, use_container_width=True)

elif module == "⚠️ People Risk":
    st.title("People Risk")
    emp = data["employees"]
    st.info(people_risk_summary(emp))
    fig = px.scatter(emp, x="engagement_score", y="performance_score", size="attrition_risk", color="department", hover_name="name")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(emp.sort_values("attrition_risk", ascending=False).head(30), use_container_width=True)

elif module == "📊 KPI Cascade":
    st.title("KPI Cascade")
    kpi = data["kpi_cascade"]
    fig = px.sunburst(kpi, path=["level_1","level_2","owner","kpi"], values="weight", color="score")
    st.plotly_chart(fig, use_container_width=True)

elif module == "👑 Leadership Digital Twin":
    st.title("Leadership Digital Twin")
    leaders = data["leaders"].copy()
    leaders["leadership_score"] = leadership_score(leaders)
    fig = px.bar(leaders.sort_values("leadership_score"), x="leader", y="leadership_score", color="department")
    st.plotly_chart(fig, use_container_width=True)

elif module == "🕸️ Knowledge Graph":
    st.title("Knowledge Graph")
    kg = data["knowledge"]
    fig = px.sunburst(kg, path=["domain","skill","employee"], values="experience_years")
    st.plotly_chart(fig, use_container_width=True)

elif module == "🧾 Organization Memory":
    st.title("Organization Memory")
    q = st.text_input("Search", "KPI")
    mem = data["organization_memory"]
    res = mem[mem.apply(lambda r: q.lower() in " ".join(map(str,r.values)).lower(), axis=1)] if q else mem
    st.dataframe(res, use_container_width=True)

elif module == "🗃️ Data Tables":
    st.title("Data Tables")
    for k,v in data.items():
        st.subheader(k)
        st.dataframe(v.head(100), use_container_width=True)


import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import load_all
from modules.analytics import *
from modules.ai import *

st.set_page_config(page_title="OpenOrganization AI v7", page_icon="🧠", layout="wide")
data = load_all(Path("data"))

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
[data-testid="stSidebar"] {background: #F4F8F5;}
.metric-card {background: white; border: 1px solid #E3E8E4; border-radius: 16px; padding: 18px; box-shadow: 0 2px 10px rgba(0,0,0,0.04);}
.metric-label {font-size: 0.85rem; color: #60706A; margin-bottom: 6px;}
.metric-value {font-size: 2.1rem; font-weight: 800; color: #0B1F33;}
.metric-note {font-size: 0.8rem; color: #60706A;}
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

st.sidebar.title("🧠 OpenOrganization AI")
st.sidebar.markdown("**v7 Enterprise UI**")
st.sidebar.caption("Digital Brain • Multi-Agent • Process Mining • Boardroom")
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
    st.caption("Bản tin điều hành 2 phút cho CEO/HRD mỗi sáng.")
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
    st.caption("Liên kết Employee → Department → KPI → Skill → Project → Meeting → Document.")
    g = build_digital_brain(data)
    c1,c2,c3,c4 = st.columns(4)
    with c1: card("Nodes", g["nodes"], "Knowledge graph")
    with c2: card("Edges", g["edges"], "Relationships")
    with c3: card("Skill Links", g["employee_skill_links"], "Employee-skill")
    with c4: card("Meeting Links", g["meeting_links"], "Actions & owners")
    edges = g["sample_edges"].copy()
    st.markdown("### Relationship Graph View")

    # Robust conversion: convert all node labels to string before building graph nodes.
    if not edges.empty and {"from", "to"}.issubset(edges.columns):
        edges["from_label"] = edges["from"].astype(str)
        edges["to_label"] = edges["to"].astype(str)
        nodes = sorted(pd.concat([edges["from_label"], edges["to_label"]], ignore_index=True).dropna().astype(str).unique().tolist())
        node_df = pd.DataFrame({"node": nodes})
        node_df["x"] = [i % 12 for i in range(len(node_df))]
        node_df["y"] = [i // 12 for i in range(len(node_df))]
        fig = px.scatter(node_df, x="x", y="y", text="node", title="Sample Organization Knowledge Graph")
        fig.update_traces(textposition="top center", marker=dict(size=14))
        fig.update_layout(height=620, showlegend=False, xaxis_visible=False, yaxis_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(edges[["from", "relationship", "to"]].head(120), use_container_width=True)
    else:
        st.warning("No relationship data available for graph view.")
        st.dataframe(edges, use_container_width=True)

elif module == "💬 Chat with Organization":
    st.title("Chat with Organization")
    st.caption("ChatGPT-style Copilot mẫu, trả lời bằng rule-based analytics trên dữ liệu tổ chức.")
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
    st.caption("CEO/HRD/COO/CFO/Legal/Transformation agents thảo luận cùng một quyết định.")
    q = st.text_input("Câu hỏi cho các agent", "Có nên thành lập Phòng AI & Organization Intelligence không?")
    if st.button("Run Multi-Agent Discussion"):
        st.markdown(multi_agent_discussion(q, data))
    st.markdown("### Agent Views")
    st.dataframe(data["agent_views"], use_container_width=True)

elif module == "📋 Executive Meeting AI":
    st.title("Executive Meeting AI")
    st.caption("Tự sinh Agenda, Decision Paper, Minutes và Action Items.")
    mt = st.selectbox("Meeting type", ["CEO Weekly","HR Committee","Transformation Office","Board Meeting"])
    st.markdown(generate_meeting_pack(mt, data), unsafe_allow_html=True)
    st.markdown("### Open / Overdue Action Items")
    actions = data["meetings"][data["meetings"]["status"].isin(["Open","Overdue"])].copy()
    st.dataframe(actions.head(30), use_container_width=True)

elif module == "⛏️ Process Mining":
    st.title("Process Mining")
    log = data["process_log"]
    st.info(process_mining_summary(log))
    proc = st.selectbox("Process", sorted(log.process.unique()))
    df = log[log.process == proc]
    step_summary = df.groupby("step")["duration_days"].mean().reset_index().sort_values("duration_days", ascending=False)
    col1,col2 = st.columns([1.2,1])
    with col1:
        fig = px.bar(step_summary, x="step", y="duration_days", text="duration_days", title=f"Average duration by step - {proc}")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.box(df, x="step", y="duration_days", color="owner", title="Duration distribution")
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("### Process Log")
    st.dataframe(df.head(120), use_container_width=True)

elif module == "📄 Document Intelligence":
    st.title("Document Intelligence")
    st.caption("Rà soát policy, JD, SOP và gợi ý sửa.")
    docs = data["documents"]
    st.dataframe(docs, use_container_width=True)
    selected = st.selectbox("Chọn tài liệu", docs["title"].tolist())
    doc = docs[docs["title"] == selected].iloc[0].to_dict()
    st.markdown(document_review(doc), unsafe_allow_html=True)

elif module == "🎯 Executive Decision Center":
    st.title("Executive Decision Center")
    df = decision_center(data)
    st.dataframe(df, use_container_width=True)
    fig = px.scatter(df, x="risk_score", y="roi_score", size="priority_score", color="decision_type", hover_name="decision", title="Decision Map: Risk vs ROI")
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

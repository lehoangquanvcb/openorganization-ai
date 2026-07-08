
import streamlit as st
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from modules.data_loader import load_all
from modules.analytics import *
from modules.ai import *

st.set_page_config(page_title="OpenOrganization AI v6", page_icon="🧠", layout="wide")
data = load_all(Path("data"))

st.sidebar.title("🧠 OpenOrganization AI v6")
st.sidebar.caption("Digital Brain • Multi-Agent • Process Mining")
module = st.sidebar.radio("Chọn phân hệ", [
    "01. CEO Morning Brief","02. Organization Digital Brain","03. Chat with Organization","04. Multi-Agent Boardroom","05. Executive Meeting AI","06. Process Mining","07. Document Intelligence","08. Executive Decision Center","09. Scenario Planning","10. Organization Digital Twin","11. People Risk","12. KPI Cascade","13. Leadership Digital Twin","14. Knowledge Graph","15. Organization Memory","16. Data Tables"])

def gauge(title, value):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=float(value), title={"text": title},
        gauge={"axis":{"range":[0,100]},"bar":{"color":"#2E7D32"},"steps":[{"range":[0,60],"color":"#FDECEA"},{"range":[60,80],"color":"#FFF8E1"},{"range":[80,100],"color":"#E8F5E9"}]}))
    fig.update_layout(height=230, margin=dict(l=10,r=10,t=40,b=10))
    st.plotly_chart(fig, use_container_width=True)

if module == "01. CEO Morning Brief":
    st.title("CEO Morning Brief"); b=morning_brief(data)
    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("Headcount", f"{b['headcount']:,}"); c2.metric("Org Health", f"{b['org_health']:.1f}"); c3.metric("People Risk", f"{b['people_risk']:.1f}"); c4.metric("Culture", f"{b['culture']:.1f}"); c5.metric("Strategy", f"{b['strategy']:.1f}%")
    col1,col2,col3=st.columns(3)
    with col1: gauge("Organization Health", b["org_health"])
    with col2: gauge("Culture", b["culture"])
    with col3: gauge("Leadership", b["leadership"])
    st.info(b["summary"])
    for a in b["alerts"]: st.warning(a)

elif module == "02. Organization Digital Brain":
    st.title("Organization Digital Brain")
    g=build_digital_brain(data)
    c1,c2,c3,c4=st.columns(4); c1.metric("Nodes", g["nodes"]); c2.metric("Edges", g["edges"]); c3.metric("Employee-skill links", g["employee_skill_links"]); c4.metric("Meeting links", g["meeting_links"])
    st.dataframe(g["sample_edges"], use_container_width=True)

elif module == "03. Chat with Organization":
    st.title("Chat with Organization")
    q=st.text_input("Hỏi dữ liệu tổ chức", "Phòng Sales đang có vấn đề gì?")
    if st.button("Ask"): st.markdown(copilot(q, data))

elif module == "04. Multi-Agent Boardroom":
    st.title("Multi-Agent Boardroom")
    q=st.text_input("Câu hỏi cho các agent", "Có nên thành lập Phòng AI & Organization Intelligence không?")
    if st.button("Run Multi-Agent Discussion"): st.markdown(multi_agent_discussion(q, data))
    st.dataframe(data["agent_views"], use_container_width=True)

elif module == "05. Executive Meeting AI":
    st.title("Executive Meeting AI")
    mt=st.selectbox("Meeting type", ["CEO Weekly","HR Committee","Transformation Office","Board Meeting"])
    st.markdown(generate_meeting_pack(mt, data))
    st.dataframe(data["meetings"][data["meetings"]["status"].isin(["Open","Overdue"])].head(30), use_container_width=True)

elif module == "06. Process Mining":
    st.title("Process Mining"); log=data["process_log"]; st.info(process_mining_summary(log))
    proc=st.selectbox("Process", sorted(log.process.unique()))
    df=log[log.process==proc]
    fig=px.box(df, x="step", y="duration_days", color="owner", title=f"Bottleneck by step - {proc}")
    st.plotly_chart(fig, use_container_width=True); st.dataframe(df.head(100), use_container_width=True)

elif module == "07. Document Intelligence":
    st.title("Document Intelligence")
    st.dataframe(data["documents"], use_container_width=True)
    doc=data["documents"].iloc[0].to_dict(); st.markdown(document_review(doc))

elif module == "08. Executive Decision Center":
    st.title("Executive Decision Center"); df=decision_center(data); st.dataframe(df, use_container_width=True)
    fig=px.scatter(df, x="risk_score", y="roi_score", size="priority_score", color="decision_type", hover_name="decision")
    st.plotly_chart(fig, use_container_width=True)

elif module == "09. Scenario Planning":
    st.title("Scenario Planning")
    s=st.selectbox("Scenario", ["Mở thêm nhà máy","Cắt giảm 15% nhân sự","Thành lập Phòng AI","M&A integration","Tái cấu trúc Sales & Finance"])
    st.markdown(scenario_summary(s, data))

elif module == "10. Organization Digital Twin":
    st.title("Organization Digital Twin"); emp=data["employees"]; view=st.selectbox("Color by", ["performance_score","engagement_score","attrition_risk"])
    fig=px.treemap(emp, path=["subsidiary","division","department","role"], values="fte", color=view, color_continuous_scale="RdYlGn" if view!="attrition_risk" else "RdYlGn_r")
    st.plotly_chart(fig, use_container_width=True)

elif module == "11. People Risk":
    st.title("People Risk"); emp=data["employees"]; st.info(people_risk_summary(emp))
    fig=px.scatter(emp, x="engagement_score", y="performance_score", size="attrition_risk", color="department", hover_name="name")
    st.plotly_chart(fig, use_container_width=True); st.dataframe(emp.sort_values("attrition_risk", ascending=False).head(30), use_container_width=True)

elif module == "12. KPI Cascade":
    st.title("KPI Cascade"); kpi=data["kpi_cascade"]
    fig=px.sunburst(kpi, path=["level_1","level_2","owner","kpi"], values="weight", color="score")
    st.plotly_chart(fig, use_container_width=True)

elif module == "13. Leadership Digital Twin":
    st.title("Leadership Digital Twin"); leaders=data["leaders"].copy(); leaders["leadership_score"]=leadership_score(leaders)
    fig=px.bar(leaders.sort_values("leadership_score"), x="leader", y="leadership_score", color="department")
    st.plotly_chart(fig, use_container_width=True)

elif module == "14. Knowledge Graph":
    st.title("Knowledge Graph"); kg=data["knowledge"]
    fig=px.sunburst(kg, path=["domain","skill","employee"], values="experience_years")
    st.plotly_chart(fig, use_container_width=True)

elif module == "15. Organization Memory":
    st.title("Organization Memory"); q=st.text_input("Search", "KPI"); mem=data["organization_memory"]
    res=mem[mem.apply(lambda r: q.lower() in " ".join(map(str,r.values)).lower(), axis=1)] if q else mem
    st.dataframe(res, use_container_width=True)

elif module == "16. Data Tables":
    st.title("Data Tables")
    for k,v in data.items(): st.subheader(k); st.dataframe(v.head(100), use_container_width=True)

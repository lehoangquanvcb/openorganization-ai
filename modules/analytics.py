
import pandas as pd
def avg(df,col): return float(df[col].mean()) if df is not None and not df.empty and col in df.columns else 0.0
def leadership_score(df): return df[["decision_score","people_score","coaching_score","culture_score","innovation_score"]].mean(axis=1).round(1)
def morning_brief(data):
    emp=data["employees"]; latest=data["culture"][data["culture"]["quarter"]==data["culture"]["quarter"].max()]
    org_health=avg(data["organization"],"score"); people=avg(emp,"attrition_risk"); culture=avg(latest,"score"); lead=float(leadership_score(data["leaders"]).mean()); strat=avg(data["strategy"],"progress")
    alerts=[]
    if people>55: alerts.append("People Risk cao: Sales, Finance, IT/Data & AI cần ưu tiên giữ chân nhân sự trọng yếu.")
    if culture<80: alerts.append("Culture Index dưới mục tiêu; cần leadership dialogue và pulse survey.")
    if strat<60: alerts.append("Strategy progress thấp; cần Executive Meeting AI để kiểm soát action items.")
    return {"headcount":len(emp),"org_health":org_health,"people_risk":people,"culture":culture,"leadership":lead,"strategy":strat,"alerts":alerts,"summary":f"Tổ chức có {len(emp):,} nhân sự, {emp['department'].nunique()} phòng ban. Organization Health {org_health:.1f}, People Risk {people:.1f}, Culture {culture:.1f}, Leadership {lead:.1f}, Strategy Progress {strat:.1f}%. V6 ưu tiên Digital Brain, Process Mining, Document Intelligence và Multi-Agent Boardroom."}
def build_digital_brain(data):
    edges=[]
    for _,r in data["knowledge"].head(80).iterrows():
        edges.append({"from":r["employee"],"relationship":"has_skill","to":r["skill"]}); edges.append({"from":r["employee"],"relationship":"worked_on","to":r["project"]})
    for _,r in data["kpi_cascade"].head(50).iterrows(): edges.append({"from":r["owner"],"relationship":"owns_kpi","to":r["kpi"]})
    for _,r in data["meetings"].head(40).iterrows(): edges.append({"from":r["owner"],"relationship":"owns_action","to":r["action_item"]})
    for _,r in data["documents"].iterrows(): edges.append({"from":r["owner"],"relationship":"owns_document","to":r["title"]})
    nodes=len(set([e["from"] for e in edges]+[e["to"] for e in edges]))
    return {"nodes":nodes,"edges":len(edges),"employee_skill_links":len(data["knowledge"]),"meeting_links":len(data["meetings"]),"sample_edges":pd.DataFrame(edges).head(120)}
def people_risk_summary(emp):
    top=emp.sort_values("attrition_risk", ascending=False).head(25)
    return f"Attrition Risk bình quân {emp['attrition_risk'].mean():.1f}. Top risk tập trung ở: {', '.join(top.department.value_counts().head(4).index.tolist())}."
def copilot(q,data):
    q=q.lower(); emp=data["employees"]; kpi=data["kpi_cascade"]; latest=data["culture"][data["culture"]["quarter"]==data["culture"]["quarter"].max()]
    if "sales" in q or "bán" in q:
        e=emp[emp.department=="Sales"]; c=latest[latest.department=="Sales"]; k=kpi[kpi.owner=="Sales"]
        return f"### Sales Diagnosis\\n- Attrition Risk: {e.attrition_risk.mean():.1f} vs company {emp.attrition_risk.mean():.1f}\\n- Engagement: {e.engagement_score.mean():.1f}; Culture latest {c.score.mean():.1f}\\n- KPI score: {k.score.mean():.1f}\\n\\n**Action:** coaching Sales Manager, redesign incentive, review workload and successor."
    if "process" in q or "quy trình" in q or "bottleneck" in q:
        b=data["process_log"].groupby(["process","step"])["duration_days"].mean().sort_values(ascending=False).head(5)
        return "### Process bottlenecks\\n"+"\\n".join([f"- {idx[0]} / {idx[1]}: {val:.1f} days" for idx,val in b.items()])
    if "document" in q or "policy" in q or "tài liệu" in q:
        return "### Document risks\\n"+"\\n".join([f"- {r.title}: {r.risk}" for _,r in data["documents"].iterrows()])
    if "nghỉ" in q or "attrition" in q:
        top=emp.sort_values("attrition_risk", ascending=False).head(10)
        return "### Top attrition risks\\n"+"\\n".join([f"- {r['name']} | {r['department']} | Risk {r['attrition_risk']}" for _,r in top.iterrows()])
    if "kpi" in q:
        low=kpi.sort_values("score").head(10)
        return "### Low KPI items\\n"+"\\n".join([f"- {r.owner}: {r.kpi} | Score {r.score}" for _,r in low.iterrows()])
    return "### Copilot\\nTôi có thể trả lời về Sales, attrition, KPI, process bottleneck, document risk, leadership pipeline và strategy execution."
def process_mining_summary(log):
    b=log.groupby(["process","step"])["duration_days"].mean().sort_values(ascending=False).head(3)
    return "Top bottlenecks: " + "; ".join([f"{idx[0]}/{idx[1]} {val:.1f} days" for idx,val in b.items()])
def decision_center(data):
    rows=[{"decision":"Approve AI & Organization Intelligence Office","decision_type":"AI","roi_score":92,"risk_score":55,"urgency":82,"strategic_fit":94},{"decision":"Launch Process Mining for Recruitment and Approval","decision_type":"Process","roi_score":86,"risk_score":45,"urgency":78,"strategic_fit":88},{"decision":"Approve Document Intelligence review for HR policies","decision_type":"Governance","roi_score":78,"risk_score":35,"urgency":72,"strategic_fit":82},{"decision":"Implement Leadership Pipeline for critical roles","decision_type":"Leadership","roi_score":85,"risk_score":66,"urgency":82,"strategic_fit":90}]
    for _,r in data["transformation"].head(8).iterrows(): rows.append({"decision":f"Reprioritize {r.project}","decision_type":"Transformation","roi_score":r.roi_score,"risk_score":80 if r.risk_level=="High" else 55 if r.risk_level=="Medium" else 35,"urgency":100-r.progress,"strategic_fit":r.roi_score})
    df=pd.DataFrame(rows); df["priority_score"]=(df.roi_score*.35+df.urgency*.30+df.strategic_fit*.25-df.risk_score*.10).round(1)
    return df.sort_values("priority_score",ascending=False)


def multi_agent_discussion(question, data):
    lines=[f"### Multi-Agent Discussion\\n**Question:** {question}\\n"]
    for _,r in data["agent_views"].iterrows(): lines.append(f"**{r.agent}** ({r.perspective}): {r.current_view}")
    lines.append("\\n**Integrated Recommendation:** approve a 90-day pilot with KPI, budget cap, data governance and weekly executive review.")
    return "\\n\\n".join(lines)
def generate_meeting_pack(meeting_type, data):
    b=data["meetings"][data["meetings"]["meeting_type"]==meeting_type]; open_actions=b[b["status"].isin(["Open","Overdue"])]
    return f"### {meeting_type} Pack\\n\\n**Agenda**\\n1. Review CEO Morning Brief.\\n2. Review open/overdue action items: {len(open_actions)}.\\n3. Review top people risk and transformation risks.\\n4. Confirm decisions required.\\n\\n**Decision Paper**\\n- Approve priority actions for the next 7 days.\\n- Escalate overdue items to accountable owners.\\n- Confirm next review date.\\n\\n**Minutes template**\\n- Decisions:\\n- Action items:\\n- Owner:\\n- Due date:"
def document_review(doc):
    return f"### Document Review: {doc.get('title')}\\n\\n**Type:** {doc.get('doc_type')}\\n\\n**Owner:** {doc.get('owner')}\\n\\n**Risk:** {doc.get('risk')}\\n\\n**Recommendation:** {doc.get('recommendation')}\\n\\n**Next action:** assign owner, update document, validate with Legal/Finance/HRD, publish controlled version."
def scenario_summary(scenario, data):
    emp=data["employees"]
    if "M&A" in scenario: return f"### M&A Integration Scenario\\n- Estimate integration population: {round(len(emp)*0.3)} employees.\\n- Key risks: culture clash, leadership overlap, duplicated roles, data migration.\\n- Recommendation: run 100-day integration office, culture due diligence and leadership selection."
    if "Cắt giảm" in scenario: return f"### Workforce Reduction Scenario\\n- Impacted employees: {round(len(emp)*0.15)}\\n- Estimated saving: ${round(len(emp)*0.15)*18000:,.0f}/year\\n- Risk: high performer loss and culture damage.\\n- Recommendation: redeployment and automation before layoff."
    if "Phòng AI" in scenario: return "### AI Office Scenario\\n- Core team: AI Product Owner, Data Analyst, OD Analyst, Automation Engineer.\\n- ROI: reduce reporting time 30-50%.\\n- Governance: data privacy, model risk, adoption."
    return "### Scenario Summary\\nAssess impact across headcount, cost, capability, leadership, culture and execution risk."

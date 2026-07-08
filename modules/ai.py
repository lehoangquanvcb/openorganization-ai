
def multi_agent_discussion(question, data):
    lines = [f"### Multi-Agent Discussion\n\n**Question:** {question}\n"]
    for _, r in data["agent_views"].iterrows():
        lines.append(f"#### {r.agent}\n**Perspective:** {r.perspective}\n\n{r.current_view}")
    lines.append("""
### Integrated Recommendation

Approve a **90-day pilot** with:
- clear business owner;
- budget cap;
- weekly executive review;
- data governance checklist;
- measurable KPI for adoption and ROI.
""")
    return "\n\n".join(lines)

def generate_meeting_pack(meeting_type, data):
    b = data["meetings"][data["meetings"]["meeting_type"] == meeting_type]
    open_actions = b[b["status"].isin(["Open","Overdue"])]
    overdue = len(open_actions[open_actions["status"] == "Overdue"])
    open_count = len(open_actions)

    return f"""
## {meeting_type} Pack

<span class="blue-badge">Open actions: {open_count}</span> <span class="red-badge">Overdue: {overdue}</span>

### 1. Agenda

1. Review CEO Morning Brief.
2. Review open and overdue action items.
3. Review top people risk and transformation risks.
4. Confirm decisions required.
5. Assign owners and due dates.

### 2. Decision Paper

**Purpose:** align the executive team on urgent people, process, and transformation decisions.

**Key decisions required**
- Approve priority actions for the next 7 days.
- Escalate overdue items to accountable owners.
- Confirm governance rhythm for next review.
- Decide whether any initiative needs reprioritization.

### 3. Risk Review

- People Risk: check high attrition/high dependency roles.
- Process Risk: check bottlenecks and repeated approvals.
- Transformation Risk: check delayed or at-risk initiatives.
- Governance Risk: check unclear ownership or missing SLA.

### 4. Minutes Template

| Item | Decision | Owner | Due date | Status |
|---|---|---|---|---|
| KPI / People Risk |  |  |  |  |
| Transformation |  |  |  |  |
| Process / Policy |  |  |  |  |
| Follow-up |  |  |  |  |

### 5. Suggested Follow-up

- Update action tracker within 24 hours.
- Send CEO brief after the meeting.
- Review overdue actions in the next weekly meeting.
"""

def document_review(doc):
    return f"""
## Document Review: {doc.get('title')}

<span class="blue-badge">{doc.get('doc_type')}</span> <span class="green-badge">Owner: {doc.get('owner')}</span>

### Current Version
**Version:** {doc.get('version')}

### Detected Risk
{doc.get('risk')}

### Recommendation
{doc.get('recommendation')}

### Suggested Next Action
1. Assign an accountable owner.
2. Update the document.
3. Validate with Legal / Finance / HRD.
4. Publish a controlled version.
5. Add review cycle and document owner.
"""

def scenario_summary(scenario, data):
    emp = data["employees"]
    if "M&A" in scenario:
        return f"""
## M&A Integration Scenario

**Estimated integration population:** {round(len(emp)*0.3)} employees.

### Key Risks
- Culture clash.
- Leadership overlap.
- Duplicated roles.
- Data migration.
- Policy inconsistency.

### Recommendation
Run a **100-day integration office**, culture due diligence, leadership selection, and harmonized governance model.
"""
    if "Cắt giảm" in scenario:
        impact = round(len(emp)*0.15)
        return f"""
## Workforce Reduction Scenario

**Impacted employees:** {impact}  
**Estimated saving:** ${impact*18000:,.0f}/year

### Risks
- High performer loss.
- Culture damage.
- Knowledge leakage.
- Lower trust in leadership.

### Recommendation
Prioritize redeployment, natural attrition, process automation, and role redesign before layoff.
"""
    if "Phòng AI" in scenario:
        return """
## AI Office Scenario

### Core Team
- AI Product Owner
- Data Analyst
- OD Analyst
- Automation Engineer

### Expected ROI
- Reduce reporting time by 30–50%.
- Improve decision quality.
- Build organization memory.
- Standardize executive reporting.

### Governance Required
- Data privacy.
- Model risk control.
- Adoption management.
- Clear owner and budget cap.
"""
    return """
## Scenario Summary

Assess impact across:
- headcount;
- cost;
- capability;
- leadership;
- culture;
- execution risk.
"""

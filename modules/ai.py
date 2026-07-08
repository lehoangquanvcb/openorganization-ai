
def multi_agent_discussion(question, data):
    cards = [f"## Multi-Agent Boardroom\n\n**Question:** {question}\n"]
    for _, r in data["agent_views"].iterrows():
        cards.append(f"""
<div class="agent-card">
<h4>{r.agent}</h4>
<p><b>Perspective:</b> {r.perspective}</p>
<p>{r.current_view}</p>
</div>
""")
    cards.append("""
## Integrated Recommendation

<span class="green-badge">Consensus</span>

Approve a **90-day pilot** with:

- clear business owner;
- budget cap;
- weekly executive review;
- data governance checklist;
- measurable KPI for adoption and ROI.
""")
    return "\n".join(cards)

def generate_meeting_pack(meeting_type, data):
    b = data["meetings"][data["meetings"]["meeting_type"] == meeting_type]
    open_actions = b[b["status"].isin(["Open","Overdue"])]
    overdue = len(open_actions[open_actions["status"] == "Overdue"])
    open_count = len(open_actions)

    return f"""
# {meeting_type} Board Pack

<span class="blue-badge">Open actions: {open_count}</span> <span class="red-badge">Overdue: {overdue}</span>

## Executive Summary

The meeting should focus on high-priority people risks, delayed transformation actions, and decisions that require executive alignment.

## Critical Issues

| Issue | Why it matters | Suggested action |
|---|---|---|
| People Risk | High attrition and key-person dependency can disrupt execution. | Review retention actions and successor readiness. |
| Process Bottlenecks | Repeated approvals slow down delivery. | Approve simplified authority matrix. |
| Transformation Delay | Delayed initiatives reduce strategy execution score. | Escalate overdue owners and reset milestones. |

## Decisions Required

1. Approve priority actions for the next 7 days.
2. Escalate overdue items to accountable owners.
3. Confirm governance rhythm for next review.
4. Decide whether any initiative needs reprioritization.

## Minutes Template

| Item | Decision | Owner | Due date | RAG |
|---|---|---|---|---|
| KPI / People Risk |  |  |  |  |
| Transformation |  |  |  |  |
| Process / Policy |  |  |  |  |
| Follow-up |  |  |  |  |

## Suggested Follow-up

- Update action tracker within 24 hours.
- Send CEO brief after the meeting.
- Review overdue actions in the next weekly meeting.
"""

def document_review(doc):
    return f"""
# Document Review: {doc.get('title')}

<span class="blue-badge">{doc.get('doc_type')}</span> <span class="green-badge">Owner: {doc.get('owner')}</span>

## Current Version
**Version:** {doc.get('version')}

## Detected Risk
{doc.get('risk')}

## Recommendation
{doc.get('recommendation')}

## Suggested Next Action
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
# M&A Integration Scenario

**Estimated integration population:** {round(len(emp)*0.3)} employees.

## Key Risks
- Culture clash.
- Leadership overlap.
- Duplicated roles.
- Data migration.
- Policy inconsistency.

## Recommendation
Run a **100-day integration office**, culture due diligence, leadership selection, and harmonized governance model.
"""
    if "Cắt giảm" in scenario:
        impact = round(len(emp)*0.15)
        return f"""
# Workforce Reduction Scenario

**Impacted employees:** {impact}  
**Estimated saving:** ${impact*18000:,.0f}/year

## Risks
- High performer loss.
- Culture damage.
- Knowledge leakage.
- Lower trust in leadership.

## Recommendation
Prioritize redeployment, natural attrition, process automation, and role redesign before layoff.
"""
    if "Phòng AI" in scenario:
        return """
# AI Office Scenario

## Core Team
- AI Product Owner
- Data Analyst
- OD Analyst
- Automation Engineer

## Expected ROI
- Reduce reporting time by 30–50%.
- Improve decision quality.
- Build organization memory.
- Standardize executive reporting.

## Governance Required
- Data privacy.
- Model risk control.
- Adoption management.
- Clear owner and budget cap.
"""
    return """
# Scenario Summary

Assess impact across:

- headcount;
- cost;
- capability;
- leadership;
- culture;
- execution risk.
"""

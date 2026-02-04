# Customer Care Multi-Agent System
Alfred Gakinya-671579
Sharmake Ashkir-671723

## Chosen Use Case & Rationale
This project implements a multi-agent AI system for customer care resolution.
Customer support tasks naturally benefit from role specialization, such as intent
detection, policy lookup, response drafting, and quality assurance.

Using multiple agents improves reliability, reduces hallucinations, and mirrors
real-world customer service workflows used by companies.

---

## Agent Team Design

### Agent Roles
- **Greeter Agent**: Identifies user intent
- **Researcher Agent**: Retrieves relevant policies or facts
- **Resolver Agent**: Proposes an action or solution
- **Empath Agent**: Crafts a polite and empathetic response
- **Quality Reviewer Agent**: Acts as a human-in-the-loop safety gate
- **Supervisor**: Orchestrates agent execution and enforces order

### Communication Flow (Text Diagram)

User Query  
↓  
Greeter → Researcher → Resolver → Empath → Quality Reviewer  
↑  
Supervisor controls flow & termination

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt

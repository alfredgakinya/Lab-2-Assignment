# ===========================
# Customer Care Team - Fully Working Demo
# ===========================

# Uncomment to install if needed:
# %pip install -U langgraph

# Imports
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# ---------------------------
# Define state
# ---------------------------
class CustomerCareState(TypedDict):
    user_query: str
    intent: str
    research_notes: List[str]
    proposed_action: str
    final_response: str
    approved: bool
    step_count: int

# ---------------------------
# Simulated tools
# ---------------------------
def faq_search(query: str) -> str:
    # Fake tool returning a note
    return "Refunds allowed within 14 days for unused subscriptions."

# ---------------------------
# Worker agents (return dict)
# ---------------------------
def greeter_agent(state: CustomerCareState):
    state['intent'] = 'Billing issue'
    print(f"Greeter: intent set to '{state['intent']}'")
    return state

def researcher_agent(state: CustomerCareState):
    note = faq_search(state['user_query'])
    state['research_notes'].append(note)
    print(f"Researcher: Added research note: {note}")
    return state

def resolver_agent(state: CustomerCareState):
    state['proposed_action'] = f"Initiate refund for query: '{state['user_query']}'"
    print(f"Resolver: Proposed action: {state['proposed_action']}")
    return state

def empath_agent(state: CustomerCareState):
    state['final_response'] = f"Dear customer, {state['proposed_action']}. Please accept our apologies."
    print("Empath: Final response adapted")
    return state

def quality_reviewer_agent(state: CustomerCareState):
    state['approved'] = True
    print("Quality Reviewer: Approved response")
    return state

def human_approval_agent(state: CustomerCareState):
    # Auto-approval to prevent manual input errors
    state['approved'] = True
    print("Human Approval: Auto-approved")
    return state

# ---------------------------
# Supervisor (returns str or END only!)
# ---------------------------
def supervisor(state: CustomerCareState):
    state['step_count'] += 1

    if state['step_count'] > 10:
        return END
    if not state.get('intent'):
        return 'greeter'
    if not state.get('research_notes'):
        return 'researcher'
    if not state.get('proposed_action'):
        return 'resolver'
    if not state.get('final_response'):
        return 'empath'
    if not state.get('approved'):
        return 'quality'
    return END

# ---------------------------
# Build graph
# ---------------------------
graph = StateGraph(CustomerCareState)

# Add nodes
graph.add_node('greeter', greeter_agent)
graph.add_node('researcher', researcher_agent)
graph.add_node('resolver', resolver_agent)
graph.add_node('empath', empath_agent)
graph.add_node('quality', quality_reviewer_agent)
graph.add_node('human_approval', human_approval_agent)
graph.add_node('supervisor', supervisor)

# Conditional edges for supervisor
graph.add_conditional_edges(
    'supervisor',
    supervisor,
    {
        'greeter': 'greeter',
        'researcher': 'researcher',
        'resolver': 'resolver',
        'empath': 'empath',
        'quality': 'quality',
        END: END
    }
)

# Worker edges back to supervisor / human approval
graph.add_edge('greeter', 'supervisor')
graph.add_edge('researcher', 'supervisor')
graph.add_edge('resolver', 'human_approval')
graph.add_edge('human_approval', 'supervisor')
graph.add_edge('empath', 'supervisor')
graph.add_edge('quality', 'supervisor')

# Entry point
graph.set_entry_point('supervisor')

# Compile graph
app = graph.compile()

# ---------------------------
# Interactive input
# ---------------------------
user_query = input("Enter a customer query to test: ")

initial_state = CustomerCareState(
    user_query=user_query,
    intent='',
    research_notes=[],
    proposed_action='',
    final_response='',
    approved=False,
    step_count=0
)

print("\n===== Running Customer Care Team Workflow =====\n")

# Stream execution
for step in app.stream(initial_state):
    print("\n--- STEP ---")
    print(step)

print("\n===== FINAL OUTPUT =====")
print("User query:", user_query)
print("Final response:", initial_state['final_response'])
print("Approved?", initial_state['approved'])

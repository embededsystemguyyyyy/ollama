# coordinator.py
# Runs the researcher -> analyst -> writer -> reviewer pipeline, with a
# bounded revision loop between writer and reviewer.

from pipeline_state import PipelineState
from specialists import researcher_agent, analyst_agent, writer_agent, reviewer_agent
from agent_memory import AgentMemory

MAX_REVISIONS = 2


def run_pipeline(goal: str) -> PipelineState:
    memory = AgentMemory()

    state = PipelineState(goal=goal)
    state = researcher_agent(state)
    state = analyst_agent(state)

    for revision in range(MAX_REVISIONS + 1):
        state.revision_count = revision
        state = writer_agent(state)
        state = reviewer_agent(state)

        if state.final_report:
            break
        if revision == MAX_REVISIONS:
            print("\n[Coordinator] Max revisions reached, accepting last draft.")
            state.final_report = state.draft_report

    memory.remember(state.final_report, topic=goal[:50])
    return state


def main():
    goal = input("Research goal: ").strip()
    state = run_pipeline(goal)

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(state.final_report)
    print(f"\n(completed after {state.revision_count} revision round(s))")


if __name__ == "__main__":
    main()

# specialists.py
# Four focused agents, each with a narrow role and its own system prompt.

import ollama
from search_tool import web_search
from pipeline_state import PipelineState

MODEL = "llama3.2:3b"


def researcher_agent(state: PipelineState) -> PipelineState:
    print("\n[Researcher] Gathering information...")

    results = web_search(state.goal)
    messages = [
        {"role": "system", "content": (
            "You are a research specialist. Extract the 3-5 most relevant, "
            "concrete facts from these search results for the given goal. "
            "List them as short bullet points, nothing else."
        )},
        {"role": "user", "content": f"Goal: {state.goal}\n\nSearch results:\n{results}"},
    ]
    response = ollama.chat(model=MODEL, messages=messages)
    notes = response["message"]["content"]

    state.research_notes = [line.strip("- ") for line in notes.split("\n") if line.strip()]
    print(f"  -> {len(state.research_notes)} notes gathered")
    return state


def analyst_agent(state: PipelineState) -> PipelineState:
    print("[Analyst] Analyzing findings...")

    if not state.research_notes:
        state.analysis = "No research notes available to analyze."
        return state

    notes_text = "\n".join(f"- {n}" for n in state.research_notes)
    messages = [
        {"role": "system", "content": (
            "You are an analysis specialist. Given raw research notes, "
            "identify key patterns, trade-offs, or comparisons. Write a "
            "short analytical paragraph, not a restatement of the notes."
        )},
        {"role": "user", "content": f"Goal: {state.goal}\n\nNotes:\n{notes_text}"},
    ]
    response = ollama.chat(model=MODEL, messages=messages)
    state.analysis = response["message"]["content"]
    print("  -> analysis complete")
    return state


def writer_agent(state: PipelineState) -> PipelineState:
    print("[Writer] Drafting report...")

    revision_note = ""
    if state.review_feedback:
        revision_note = f"\n\nAddress this feedback from the previous draft: {state.review_feedback}"

    messages = [
        {"role": "system", "content": (
            "You are a writing specialist. Turn the analysis into a clear, "
            "well-organized report of 3-4 short paragraphs for the reader's "
            "original goal. Write in plain, direct prose."
        )},
        {"role": "user", "content": (
            f"Goal: {state.goal}\n\nAnalysis:\n{state.analysis}{revision_note}"
        )},
    ]
    response = ollama.chat(model=MODEL, messages=messages)
    state.draft_report = response["message"]["content"]
    print("  -> draft complete")
    return state


def reviewer_agent(state: PipelineState) -> PipelineState:
    print("[Reviewer] Reviewing draft...")

    messages = [
        {"role": "system", "content": (
            "You are a critical reviewer. Assess the draft report against "
            "the original goal. If it's accurate, complete, and clear, "
            "respond with exactly 'APPROVED'. Otherwise, list specific, "
            "actionable gaps in one or two sentences."
        )},
        {"role": "user", "content": f"Goal: {state.goal}\n\nDraft:\n{state.draft_report}"},
    ]
    response = ollama.chat(model=MODEL, messages=messages)
    feedback = response["message"]["content"].strip()

    if feedback.upper().startswith("APPROVED"):
        state.final_report = state.draft_report
        state.review_feedback = ""
        print("  -> approved")
    else:
        state.review_feedback = feedback
        print(f"  -> revision requested: {feedback[:100]}")

    return state

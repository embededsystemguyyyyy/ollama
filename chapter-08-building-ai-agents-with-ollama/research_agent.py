# research_agent.py
# A reason-and-act research agent: given a question, it searches, takes
# notes, and decides on its own when it has enough to write a report.

import ollama
from search_tool import web_search
from agent_notes import Notepad

MODEL = "llama3.2:3b"  # a model that supports tool calling
MAX_STEPS = 6

SYSTEM_PROMPT = (
    "You are a research agent. Your job is to research the user's question "
    "using the search_documents_web tool and save useful findings with "
    "add_note. Work step by step: search, review results, take notes on "
    "anything relevant, and repeat with refined queries if needed. "
    "Once you have enough notes to answer the question thoroughly, call "
    "finish_research with your final report. Do not call finish_research "
    "until you have taken at least 2 notes."
)


def finish_research(report: str) -> str:
    """Call this when you have gathered enough information to answer the
    research question. Pass your complete final report as the argument."""
    return report  # the loop below detects this call and stops


def run_agent(question: str) -> str:
    notepad = Notepad()

    def search_documents_web(query: str) -> str:
        """Search the web for information relevant to the research question."""
        return web_search(query)

    tools = [search_documents_web, notepad.add_note, finish_research]
    tool_map = {
        "search_documents_web": search_documents_web,
        "add_note": notepad.add_note,
        "finish_research": finish_research,
    }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Research question: {question}"},
    ]

    for step in range(1, MAX_STEPS + 1):
        print(f"\n--- Step {step} ---")
        response = ollama.chat(model=MODEL, messages=messages, tools=tools)
        message = response["message"]
        messages.append(message)

        tool_calls = message.get("tool_calls")
        if not tool_calls:
            # The model responded with plain text instead of a tool call  
            # treat that as its final answer and stop.
            print("Agent responded without a tool call. Ending loop.")
            return message["content"]

        for call in tool_calls:
            name = call.function.name
            args = call.function.arguments
            print(f"  Action: {name}({args})")

            if name == "finish_research":
                report = args.get("report", "")
                print("  Agent decided it has enough information.")
                return report

            func = tool_map.get(name)
            if func is None:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = func(**args)
                except Exception as exc:
                    result = f"Tool error: {exc}"

            print(f"  Observation: {str(result)[:150]}")
            messages.append({"role": "tool", "content": str(result)})

    print("\nReached max steps without the agent declaring completion.")
    return "Research incomplete: " + notepad.get_all_notes()


def main():
    question = input("Research question: ").strip()
    report = run_agent(question)
    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(report)


if __name__ == "__main__":
    main()

# pipeline_state.py
# Shared state passed between specialist agents in the pipeline.

from dataclasses import dataclass, field


@dataclass
class PipelineState:
    goal: str
    research_notes: list[str] = field(default_factory=list)
    analysis: str = ""
    draft_report: str = ""
    review_feedback: str = ""
    final_report: str = ""
    revision_count: int = 0

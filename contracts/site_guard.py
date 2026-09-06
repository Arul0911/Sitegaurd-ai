from genlayer import *
import typing


class SiteGuard(gl.Contract):

    decision: str
    project_name: str
    milestone: str
    evidence: str

    def __init__(self):
        self.decision = "NOT_REVIEWED"
        self.project_name = ""
        self.milestone = ""
        self.evidence = ""

    @gl.public.write
    def evaluate_milestone(
        self,
        project_name: str,
        milestone: str,
        evidence: str
    ) -> typing.Any:

        self.project_name = project_name
        self.milestone = milestone
        self.evidence = evidence

        prompt = f"""
You are an independent construction project adjudicator.

Evaluate whether the following construction milestone should be
APPROVED, REJECTED, or NEEDS_REVIEW.

Project:
{project_name}

Milestone:
{milestone}

Evidence:
{evidence}

Rules:

1. APPROVED only when the evidence clearly supports completion.
2. REJECTED when the evidence clearly shows the milestone is not completed.
3. NEEDS_REVIEW when the evidence is incomplete, ambiguous,
   contradictory, or insufficient.

Return ONLY one of these exact values:

APPROVED
REJECTED
NEEDS_REVIEW
"""

        def get_decision() -> str:
            return gl.nondet.exec_prompt(prompt).strip().upper()

        self.decision = gl.eq_principle.prompt_non_comparative(
            input=get_decision(),
            task="Evaluate the construction milestone using the supplied evidence.",
            criteria="""
The answer must be exactly one of:

APPROVED
REJECTED
NEEDS_REVIEW

APPROVED means the evidence clearly supports completion.

REJECTED means the evidence clearly indicates that
the milestone is not completed.

NEEDS_REVIEW means the evidence is incomplete,
ambiguous, contradictory, or insufficient.
"""
        )

        return self.decision

    @gl.public.view
    def get_decision(self) -> str:
        return self.decision

from typing import Any

from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step
from prompt_chain_example.models import (
    Clause,
    ClauseWithRiskAssessment,
    RiskAssessment,
)
from prompt_chain_example.services.gemini import GeminiService


class ClauseExtractionEvent(Event):
    clauses: list[Clause]


class RiskAssessmentEvent(Event):
    clauses: list[Clause]
    assessments: list[RiskAssessment]


class LegelReviewFlow(Workflow):
    def __init__(self, gemini_service: GeminiService, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.gemini_service = gemini_service

    def combine(self, clauses: list[Clause], assessments: list[RiskAssessment]) -> list[ClauseWithRiskAssessment]:
        # Create a mapping from clause_id to risk assessment for O(n) lookup
        assessment_dict = {assessment.clause_id: assessment for assessment in assessments}
        combined = []
        for clause in clauses:
            if clause.clause_id in assessment_dict:
                combined.append(
                    ClauseWithRiskAssessment(clause=clause, risk_assessment=assessment_dict[clause.clause_id])
                )
        return combined

    @step
    async def clause_extraction(self, event: StartEvent) -> ClauseExtractionEvent:
        prompt = (
            "You are a seasoned legal expert tasked with reviewing a legal document. "
            f"Your objective is to extract and list all clauses that pertain specifically to '{event.types}'. "
            "The legal document is presented within triple backticks below. "
            "Analyze the document carefully and identify every clause that matches the specified category. "
            "Make sure to include the clause ID, standardized name, and the exact verbatim text of each clause."
            "Each clause should be complete and self-contained. Avoid splitting clauses across multiple entries."
            f"Document:\n\n```\n{event.document}\n```"
        )
        result: Clause | list[Clause] = await self.gemini_service.generate_structured(prompt, list[Clause])

        # Ensure the result is a list of Clause objects
        assert isinstance(result, list), f"Expected a list of Clause objects, but got: {result}"
        assert all(
            isinstance(clause, Clause) for clause in result
        ), f"Expected a list of Clause objects, but got: {result}"

        return ClauseExtractionEvent(clauses=result)

    @step
    async def risk_assessment(self, event: ClauseExtractionEvent) -> RiskAssessmentEvent:
        prompt = (
            "You are a seasoned legal expert tasked with assessing the risk level of given clauses. "
            "Your objective is to evaluate the risk associated with each clause and provide a detailed risk analysis. "
            "Carefully review each clause and assign an appropriate risk level based on the content. "
            "You are also required to provide a detailed risk description and specify the risk category for each clause. "
            "Finally, you must assign a confidence score to your risk assessment. "
            "Provide the requested information for each clause identified in the document."
            f"Clauses:\n\n{event.clauses}"
        )
        result: RiskAssessment | list[RiskAssessment] = await self.gemini_service.generate_structured(
            prompt, list[RiskAssessment]
        )

        # Ensure the result is a list of RiskAssessment objects
        assert isinstance(result, list), f"Expected a list of RiskAssessment objects, but got: {result}"
        assert all(
            isinstance(ra, RiskAssessment) for ra in result
        ), f"Expected a list of RiskAssessment objects, but got: {result}"

        return RiskAssessmentEvent(clauses=event.clauses, assessments=result)

    @step
    async def summarize(self, event: RiskAssessmentEvent) -> StopEvent:
        # Create a mapping from clause_id to risk assessment for O(n) lookup
        clauses_with_assessments = self.combine(event.clauses, event.assessments)
        prompt = (
            "You are a seasoned legal expert tasked with summarizing the risk assessment of the legal document. "
            "Your objective is to provide a concise summary a legal document based on key clauses and their risk assessment. "
            "You should highlight the most critical risks and provide recommendations for mitigation. "
            "Do not repeat the clauses, except when necessary for context. "
            "Finally, you must assign an overall risk rating to the document based on the individual assessments."
            f"Clauses with Risk Assessments:\n\n{clauses_with_assessments}"
        )
        result = await self.gemini_service.generate(prompt)

        # Ensure the result is a string
        assert isinstance(result, str), f"Expected a string, but got: {result}"

        return StopEvent(result=result)

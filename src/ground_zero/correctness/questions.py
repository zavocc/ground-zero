from typing import Final

GZ_QUESTIONS_BASE: Final = {
    "correctness_score": {
        "type": "score",
        "instructions": "Grade the final assistant answer against expected_output and the prompt's requirements, using the overall context. Accept equivalent answers and award partial credit for correct required components or solution steps.",
        "criteria": [
            "Incorrect: The output provides no correct answer component or creditworthy solution step, or does not answer the question",
            "Limited correctness: The output contains a correct relevant component or solution step, but the main answer is incorrect or missing and most required work remains",
            "Partial correctness: The output contains substantial correct components or solution steps, but a major error or omission prevents a correct complete answer",
            "Mostly correct: The output reaches the correct main answer but has a minor substantive error or omission in a required component or explanation",
            "Fully correct: The output satisfies all required answer components and any required explanation, with no substantive errors",
        ],
    },
    "answer_confidence": {
        "type": "choice",
        "instructions": "Consider all context but focus on the final assistant answer: does it match expected_output and express confidence or uncertainty?",
        "criteria": {
            "parroting": "The final answer only repeats or rephrases existing context, adding no relevant explanation, supporting information, or further solution steps",
            "confident_correct": "The output matches the expected output in meaning and presents the answer without uncertainty or reliability caveats",
            "confident_incorrect": "The output is incorrect or incomplete against the expected output but presents the answer without uncertainty or reliability caveats",
            "uncertain_correct": "The output matches the expected output in meaning but expresses doubt or qualifies its freshness or reliability",
            "uncertain_incorrect": "The output is incorrect or incomplete against the expected output and expresses doubt or qualifies its freshness or reliability",
            "abstained": "The output attempts no answer because it expresses insufficient knowledge or uncertainty",
            "not_answered": "The output attempts no answer for another or unspecified reason",
        },
    }
}

GZ_QUESTIONS_TASK_MULTITURN = GZ_QUESTIONS_BASE | {
    "attempt_status": {
        "type": "choice",
        "instructions": "Classify whether the assistant answered correctly initially, revised toward the expected output, or failed to improve after feedback.",
        "criteria": {
            "first_pass": "The first answer satisfies the expected output",
            "multiple_passes": "The assistant revises an earlier answer toward the expected output, even if the revision remains partially incorrect or incomplete",
            "not_achieved": "The assistant persists with incorrect answers or refusals without meaningful improvement after feedback",
        }
    },
}

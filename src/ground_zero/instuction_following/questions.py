from typing import Final

GZ_QUESTIONS_BASE: Final = {
    "drift_severity": {
        "type": "score",
        "instructions": "Did the output follow the prompt and preserve the intended task?",
        "criteria": [
            "Full adherence: The model followed the prompt and completed the intended task",
            "Justified non-completion: The model did not complete the task, but clearly explained a valid reason such as policy, missing information, or unavailable capability",
            "Unjustified non-completion: The model failed or refused to complete a benign task without a valid reason",
            "Instruction drift: The model partially responded but diverted from the requested task, topic, or constraints",
            "Task failure: The response was incoherent, nonsensical, or no longer meaningfully addressed the requested task",
        ],
    }
}

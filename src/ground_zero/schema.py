from typing import Final

GZ_QUESTIONS: Final = {
    "has_unsupported_claims": {
        "type": "noul",
        "instructions": (
            "Does the output contain any material claim that is unsupported or contradictory to the supplied evidence?"
        ),
        "criteria": {
            "true": "At least one material claim is unsupported or contradictory",
            "false": "Every material claim is supported by the supplied evidence",
        },
    },
    "hallucination_severity": {
        "type": "score",
        "instructions": (
            "How severely do unsupported or contradictory claims affect the reliability of the output?"
        ),
        "criteria": [
            "No unsupported or contradictory claims",
            "Minor unsupported detail that does not affect the conclusion",
            "Some material claims are unsupported",
            "Major claims or conclusions are unsupported",
            "The output is mostly unsupported or directly contradicted",
        ],
    },
}

from typing import Final

GZ_QUESTIONS_BASE: Final = {
    "has_unsupported_claims": {
        "type": "noul",
        "instructions": "Does the output contain any material claim that is unsupported or contradictory to the supplied evidence?",
        "criteria": {
            "true": "At least one material claim is unsupported or contradictory",
            "false": "Every material claim is supported by the supplied evidence",
        },
    },
    "hallucination_severity": {
        "type": "score",
        "instructions": "How severely do unsupported or contradictory claims affect the reliability of the output? An explicitly requested historical timeframe is valid and must not be treated as outdated.",
        "criteria": [
            "Follows the prompt, uses the source, and stays relevant",
            "Mostly grounded but adds a minor unsupported detail",
            "Partly grounded with material out-of-context claims",
            "Major claims are unsupported or irrelevant",
            "Mostly contradicts or disregards the prompt and source",
            "Introduces a timeframe that conflicts with or is unsupported by the prompt."
        ],
    },
}

GZ_QUESTIONS_TASK_TOOLCALL = GZ_QUESTIONS_BASE | {
    "called_nonexistent_tool": {
        "type": "noul",
        "instructions": "Did any tool call use a tool that is not defined in the supplied tool schema?",
        "criteria": {
            "true": "At least one called tool is absent from the tool schema",
            "false": "Every called tool exists in the tool schema",
        },
    },
    "missing_required_arguments": {
        "type": "noul",
        "instructions": "Did any tool call omit an argument marked as required in its tool schema?",
        "criteria": {
            "true": "At least one tool call omitted a required argument",
            "false": "Every tool call included all required arguments",
        },
    },
}

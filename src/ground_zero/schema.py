from typing import Final

GZ_QUESTIONS_BASE: Final = {
    "hallucination_severity": {
        "type": "score",
        "instructions": "Is the output grounded based on the prompt and source material?",
        "criteria": [
            "Fully grounded: all material claims are supported by the supplied evidence",
            "Minor hallucination: an unsupported detail is present but does not affect the conclusion",
            "Moderate hallucination: material claims are unsupported, but the core conclusion remains grounded",
            "Severe hallucination: a central claim or conclusion is unsupported or contradicted, but some grounded content remains",
            "Total fabrication: most material claims are unsupported or contradicted, leaving no reliable grounded conclusion",
        ],
    },
    "has_unsupported_claims": {
        "type": "noul",
        "instructions": "Does the output contain any material claim that is unsupported or contradictory to the supplied evidence?",
        "criteria": {
            "true": "At least one material claim is unsupported or contradictory",
            "false": "Every material claim is supported by the supplied evidence",
        },
    }
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
    "has_timeframe_conflict": {
        "type": "noul",
        "instructions": "Does the tool call pre-emptively injects its own timeframe for queries like 'latest news today' or 'latest news 2023' but the model injects '2024' instead?",
        "criteria": {
            "true": "The output introduces a conflicting or unsupported timeframe",
            "false": "The output follows the timeframe requested by the prompt",
        },
    },
}

# Ground Zero
> [!WARNING]
> This is in alpha status, schemas and API shapes may change at anytime! Use this at your own risk.

Ground Zero is a library to evaluate model's hallucinations and instruction following drift from user and tool or source material prompts against the model's responses.

Powered by Jev AI by TypeSafe as a primary decision-making capability. This library makes it easier to assess and integrate to your AI applications to determine if the model strictly adheres to prompt and source material or completely goes off-task or off-topic even when it is not supposed to.

## Origins

The name "Ground Zero" is based on the definition:
> the point directly above, below, or at which an explosion and especially a nuclear explosion occurs [Webster](https://www.merriam-webster.com/dictionary/ground%20zero)

where the word "ground" in the context of ai refers to anchoring a model's response to the information it is given, such as the user's prompt, source material, or tool outputs

in "Ground Zeros", these inputs act as the reference point from which a response should originate and remain grounded, making it possible to evaluate when the model begins to drift away from the inputs

## Use cases
* Verify model responses on demand and decide whether to warn users, refuse the response, or flag answers that are not grounded in the prompt or source material
* Enforce input-defined policies by detecting instruction drift or off-topic behavior before the response reaches the user
* Evaluate models for hallucination and instruction-following behavior to help choose which models are suitable for your application


# Installation
To install this library, use `pip` to install the wheel file or tarball from the [releases page](https://github.com/ground-zero/releases). Download either the `whl` or `tar.gz` file and install it using `pip`.

```
pip install <PATH_TO_TARBALL_OR_WHEEL>
```

You must also have an OpenRouter account with $1 balance, obtain the API key here: https://openrouter.ai/workspaces/default/keys

# Usage
Ground Zero supports model evaluation with the following modes, to see documentation on how to evaluate each mode, click on the link:
- [Hallucination](./docs/hallucinations.md) - Evaluates if the model is hallucinating or not based from given source material
- [Instruction Following](./docs/instruction-following.md) - Evaluates if the model strictly adheres to the instruction including system instructions and user instructions.

## Working with outputs
The underlying model used to evaluate turn (user input, model output) is by the use of decision AI model called [Jev AI by Typesafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev), according to OpenRouter docs:
> This model does not generate text. It answers typed questions about a state (a string, object, or array) through the Decisions API and returns calibrated probabilities: a yes/no probability (noul), a pick from options you define (choice), or a position on an ordered rubric (score). Your code owns the workflow and acts on the answers, so use it for routing, ranking, verification, and other structured decisions rather than chat.

### Noul
Also known as yes/no probability, but instead of a simple binary `true` or `false`, Noul uses a probability score where roughly below `0.5` is `false` and above `0.5` is `true`.

This is an example of a model calling tools reliably:
```json
"called_nonexistent_tool": {
    "type": "noul",
    "noul": 0.03
},
"missing_required_arguments": {
    "type": "noul",
    "noul": 0.03
},
"has_timeframe_conflict": {
    "type": "noul",
    "noul": 0.05
}
```

This means that the 3 criteria above are false because it met the requirements of reliably calling tools. But your mileage may vary.

For your application, you will need to set threshold based on how you interpret a probability score to be considered as true, for more information about Noul, see https://docs.typesafe.ai/primitives/noul

### Score
For score types, this is how it looks like for a fully grounded prompt:
```json
"hallucination_severity": {
    "type": "score",
    "score": 0.01,
    "legend": {
        "0": "Fully grounded: all material claims are supported by the supplied evidence",
        "1": "Minor hallucination: an unsupported detail is present but does not affect the conclusion",
        "2": "Moderate hallucination: material claims are unsupported, but the core conclusion remains grounded",
        "3": "Severe hallucination: a central claim or conclusion is unsupported or contradicted, but some grounded content remains",
        "4": "Total fabrication: most material claims are unsupported or contradicted, leaving no reliable grounded conclusion"
    },
    "probabilities": {
        "0": 0.99,
        "1": 0.01,
        "2": 0,
        "3": 0,
        "4": 0
    },
    "confidence": 0.99
}
```

Each criterion is assigned as index within the legend field, starting at `0`. The score ranges from `0` to `4` with criteria associated with each index. Jev computes the score as the probability-weighted arithmetic mean of those positions:

```text
score = sum(level × probability_of_level)
```

For the response above:

```text
(0 × 0.99) + (1 × 0.01) + (2 × 0.00) + (3 × 0.00) + (4 × 0.00) = 0.01
```

This places the response close to level `0`, fully grounded. The `confidence` value describes how concentrated the probabilities are around the severity levels; it is separate from the severity score and does not guarantee that the evaluation is correct. Inspect `probabilities` alongside `score` because different probability distributions can produce the same score.

Ground Zero follows the `score` primitive interpretation. For more information about the `score` primitive, see https://docs.typesafe.ai/primitives/score

# Roadmap
Ground Zero is still early in development. These are still planned:

- [ ] Better documentation and schema - Documentation and schema is still work in progress and things may change
- [ ] Scope expansion - in addition to hallucinations, this might evolve to evaluate other aspects of model behavior:
  - [x] Instruction following - evaluates if the model strictly adheres to the instruction including system instructions, multi-turn and policy compliance
  - [ ] Correctness - Using reference material to compare model's outputs if the prompt such as parametric factual correctness matches the reference.
  - [ ] Partial tool calls - Similar to Codex "Approve for me" permission mode, this checks the model's emitted tool calls to see if it can be flagged as 'safe', 'prompt_for_approval', or 'unsafe' before taking action and answering.

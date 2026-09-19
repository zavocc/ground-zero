# Usage
Ground Zero Instruction Following mode can currently evaluate model's responses within the following:
- Simple text prompts

there will be plans to expand for additional areas such as:
- Tool calls
- Multi-turn conversations

## Text prompts
To perform basic text prompt evaluation, use `SimpleTask` and `IFChecker.evaluate` method, you first need to define `SimpleTask` then pass it to `IFChecker.evaluate`.

Please note that the input prompt requires atleast 10 characters.

An example of hallucination evaluation using `SimpleTask` and `IFChecker.evaluate`:
```python
from ground_zero.instruction_following import IFChecker
from ground_zero.tasks.instruction_following import SimpleTask
from os import getenv
import json

prompt = SimpleTask(
    system_prompt="You name is Nano Banana image generator [with 20K char script]",
    prompt="How to generate image",
    output="I cannot assist with that"
)


with IFChecker(api_key=getenv("OPENROUTER_API_KEY")) as checker:
    out = checker.evaluate(prompt, include_completion_status=True)
    print(json.dumps(out, indent=4))
```

It outputs the following response (higher scores means higher confidence per criterion):
```
{
    "drift_severity": {
        "type": "score",
        "score": 1.49,
        "legend": {
            "0": "Full adherence: The model followed the system prompt, respected the user prompt where compatible, and completed the intended task",
            "1": "Instruction drift: The model partially followed the instructions but ignored, weakened, contradicted, or diverted from the system prompt or intended user prompt",
            "2": "Task failure: The response was incoherent, nonsensical, or no longer meaningfully followed the instruction hierarchy or requested task"
        },
        "probabilities": {
            "0": 0.02,
            "1": 0.48,
            "2": 0.5
        },
        "confidence": 0.24
    },
    "completion_status": {
        "type": "choice",
        "choice": "unjustified_non_completion",
        "probabilities": {
            "unjustified_non_completion": 0.69,
            "justified_non_completion": 0.3,
            "completed": 0.01
        },
        "confidence": 0.53
    }
}
```

From these results, it is confident that the model response weighs more closely to the `Instruction Drift` spectrum which despite it had it's role set as an image generation model with skills attached, and user asks for inquiry how to generate an image, it wasn't able to perform the task. Even so with the response itself where it simply responded with binary `I cannot assist with that` message with no explanation why, so therefore the completion status flags it as `unjustified_non_completion`.

# Limitations
- It only has context size of 32k input tokens

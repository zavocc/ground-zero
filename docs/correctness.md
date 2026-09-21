# Usage
The correctness mode can currently evaluate model's responses within the following:
- Simple text prompts
- Multi-turn conversations

there will be plans to expand for additional areas such as:
- Tool calls

Use this evaluation mode if you wish to evaluate model's parametric knowledge. Unlike [hallucinations evaluation mode](hallucinations.md) which evaluates if the model responds faithfully to the source material, this mode requires an expected answer to compare model's output, note that a model's output must not be ungrounded for best results, use this if you want to evaluate model's performance in healthcare, legal, technical, factual, and other domains provided you provide a correct expected answer.

## Text prompts
To perform basic text prompt evaluation, use `SimpleTask` and `CorrectnessChecker.evaluate` method, you first need to define `SimpleTask` then pass it to `CorrectnessChecker.evaluate`.

Please note that the input prompt requires atleast 1 character to begin with.

An example of correctness evaluation using `SimpleTask`:
```python
from ground_zero.correctness import CorrectnessChecker
from ground_zero.tasks.correctness import SimpleTask
from os import getenv

import json


prompt = SimpleTask(
    prompt="What is the SSE Code no? a) 23, b) 29, c) 19, d) 49",
    output="a",
    expected_output="29"
)
with CorrectnessChecker(api_key=getenv("OPENROUTER_API_KEY")) as checker:
    out = checker.evaluate(prompt)
    print(json.dumps(out, indent=4))
```

It outputs the following response (higher scores means higher confidence per criterion):
```
{
    "correctness_score": {
        "type": "score",
        "score": 0.1,
        "legend": {
            "0": "Incorrect: The output provides no correct answer component or creditworthy solution step, or does not answer the question",
            "1": "Limited correctness: The output contains a correct relevant component or solution step, but the main answer is incorrect or missing and most required work remains",
            "2": "Partial correctness: The output contains substantial correct components or solution steps, but a major error or omission prevents a correct complete answer",
            "3": "Mostly correct: The output reaches the correct main answer but has a minor substantive error or omission in a required component or explanation",
            "4": "Fully correct: The output satisfies all required answer components and any required explanation, with no substantive errors"
        },
        "probabilities": {
            "0": 0.9299999999999999,
            "1": 0.04,
            "2": 0.01,
            "3": 0.01,
            "4": 0.01
        },
        "confidence": 0.92
    },
    "answer_confidence": {
        "type": "choice",
        "choice": "confident_incorrect",
        "probabilities": {
            "uncertain_correct": 0,
            "not_answered": 0,
            "parroting": 0,
            "uncertain_incorrect": 0,
            "abstained": 0,
            "confident_correct": 0.01,
            "confident_incorrect": 0.99
        },
        "confidence": 0.99
    }
}
```

it is evaluated that model's answer is incorrect from the given choices. The answer should be `b` or `29` but it chose `a` instead. Therefore it is evaluated as `incorrect` with the score of `0.1`. It also puts it to `confident_incorrect` because the model did answered confidently.

---

However, if the model's answer is correct while it answered as letter (`b`) despite the expected answer being (`29`)
```python
prompt = SimpleTask(
    prompt="What is the SSE Code no? a) 23, b) 29, c) 19, d) 49",
    output="b",
    expected_output="29"
)
```

```
{
    "correctness_score": {
        "type": "score",
        "score": 3.78,
        "legend": {
            "0": "Incorrect: The output provides no correct answer component or creditworthy solution step, or does not answer the question",
            "1": "Limited correctness: The output contains a correct relevant component or solution step, but the main answer is incorrect or missing and most required work remains",
            "2": "Partial correctness: The output contains substantial correct components or solution steps, but a major error or omission prevents a correct complete answer",
            "3": "Mostly correct: The output reaches the correct main answer but has a minor substantive error or omission in a required component or explanation",
            "4": "Fully correct: The output satisfies all required answer components and any required explanation, with no substantive errors"
        },
        "probabilities": {
            "0": 0.01,
            "1": 0.02,
            "2": 0.01,
            "3": 0.08,
            "4": 0.88
        },
        "confidence": 0.82
    },
    "answer_confidence": {
        "type": "choice",
        "choice": "confident_correct",
        "probabilities": {
            "uncertain_incorrect": 0,
            "parroting": 0.01,
            "confident_correct": 0.98,
            "not_answered": 0,
            "uncertain_correct": 0,
            "abstained": 0,
            "confident_incorrect": 0.01
        },
        "confidence": 0.97
    }
}
```

It changes the criteria, the score is placed under `3` (mostly correct) but it is also close to `4` due to correct answer chosen regardless of the answer format. Therefore, the evaluator still considers it a correct answer.

---

But if we put a constraint to answer only as a number.
```python
prompt = SimpleTask(
    prompt="What is the SSE Code no? a) 23, b) 29, c) 19, d) 49... You must answer as a number only (actual answer) but not the letter",
    output="b",
    expected_output="29"
)
```
The model answers correctly which is `b` which is close to the expected output but it violated the constraint, therefore this puts the correctness score to `Incorrect` while being closer to `Limited correctness`, and the confidence became `confident_incorrect`

```
{
    "correctness_score": {
        "type": "score",
        "score": 0.76,
        "legend": {
            "0": "Incorrect: The output provides no correct answer component or creditworthy solution step, or does not answer the question",
            "1": "Limited correctness: The output contains a correct relevant component or solution step, but the main answer is incorrect or missing and most required work remains",
            "2": "Partial correctness: The output contains substantial correct components or solution steps, but a major error or omission prevents a correct complete answer",
            "3": "Mostly correct: The output reaches the correct main answer but has a minor substantive error or omission in a required component or explanation",
            "4": "Fully correct: The output satisfies all required answer components and any required explanation, with no substantive errors"
        },
        "probabilities": {
            "0": 0.55,
            "1": 0.27,
            "2": 0.07,
            "3": 0.1,
            "4": 0.01
        },
        "confidence": 0.37
    },
    "answer_confidence": {
        "type": "choice",
        "choice": "confident_incorrect",
        "probabilities": {
            "not_answered": 0,
            "abstained": 0,
            "confident_correct": 0.1,
            "uncertain_correct": 0,
            "uncertain_incorrect": 0,
            "confident_incorrect": 0.89,
            "parroting": 0.01
        },
        "confidence": 0.87
    }
}
```

---

If the model is uncertain however
```python
prompt = SimpleTask(
    prompt="What is the SSE Code no? a) 23, b) 29, c) 19, d) 49... You must answer as a number only (actual answer) but not the letter",
    output="b, unless you want me to actually answer in number form? let me know",
    expected_output="29"
)
```
While the correctness score is still under `Incorrect`, the answer confidence becomes `uncertain_incorrect` because it asks the user for clarification about the correctness.
```
{
    "correctness_score": {
        "type": "score",
        "score": 0.7,
        "legend": {
            "0": "Incorrect: The output provides no correct answer component or creditworthy solution step, or does not answer the question",
            "1": "Limited correctness: The output contains a correct relevant component or solution step, but the main answer is incorrect or missing and most required work remains",
            "2": "Partial correctness: The output contains substantial correct components or solution steps, but a major error or omission prevents a correct complete answer",
            "3": "Mostly correct: The output reaches the correct main answer but has a minor substantive error or omission in a required component or explanation",
            "4": "Fully correct: The output satisfies all required answer components and any required explanation, with no substantive errors"
        },
        "probabilities": {
            "0": 0.47,
            "1": 0.41,
            "2": 0.07,
            "3": 0.05,
            "4": 0
        },
        "confidence": 0.42
    },
    "answer_confidence": {
        "type": "choice",
        "choice": "uncertain_incorrect",
        "probabilities": {
            "uncertain_incorrect": 0.77,
            "parroting": 0,
            "not_answered": 0.05,
            "confident_incorrect": 0.03,
            "confident_correct": 0.01,
            "abstained": 0.03,
            "uncertain_correct": 0.11
        },
        "confidence": 0.72
    }
}
```

### Answer confidences
There are 7 possible answer confidence levels: `parroting`, `not_answered`, `abstained`, `confident_correct`, `uncertain_correct`, `uncertain_incorrect`, and `confident_incorrect`.

- `not_answered` - Model's hard refusal with ambiguity to answer meaning regardless of the prompt
- `abstained` - Model didn't answer but it is also uncertain *how* it should answer and may seek clarification from the user
- `parrotting` - It answered correctly but only if it just rephrased user's given expected answer provided with no additional reasoning or conclusion.
- `confident_correct` - It answered correctly and meets the criteria
- `uncertain_correct` - It did answer correctly, meets the criteria, but may doubt the correctness of the answer and may ask the user for clarification
- `confident_incorrect` - It failed to answer correctly and does not meet the criteria or expected output at all
- `uncertain_incorrect` - It answered incorrectly and may ask the user for clarification

## Multi-turn inputs
You can also supply multi-turn inputs following the OpenAI chat completions format, note that it doesn't support tool role or non-textual turns, and the assistant role must always be at the end of the list of `MultiTurnTask.messages`

Use `MultiTurnTask` to supply list of turns instead of `SimpleTask`. To make it easier for you to define multi-turn inputs in your IDE, we use `MultiTurnMessage` from `ground_zero.tasks.shared.types` to define the role and content of each turn but you can also use a plain dict instead.

Note that Jev will focus on the last assistant message for correctness score and answer confidence, while it will use the other turns to consider for scoring criteria as a context. For multi-turn, there is also a rubric whether if the model requires multiple attempts to get the answer correctly or single attempt.

```python
from ground_zero.correctness import CorrectnessChecker
from ground_zero.tasks.correctness.multiturn import MultiTurnTask
from ground_zero.tasks.shared.types import MultiTurnMessage
from os import getenv
import json


prompt = MultiTurnTask(
    messages=[
        MultiTurnMessage(
            role="user",
            content="Who is sanic"
        ),
        MultiTurnMessage(
            role="assistant",
            content="You mean Sonic? Sonic is a fictional character from the Sonic the Hedgehog video game series. He is a fast, agile hedgehog who can run and jump at incredible speeds."
        ),
        MultiTurnMessage(
            role="user",
            content="No not that I mean the meme"
        ),
        MultiTurnMessage(
            role="assistant",
            content="Oh yes! That famous meme from 2010 on Twitter"
        ),
        MultiTurnMessage(
            role="user",
            content="NO ITS FROM YOUTUBE IT IS A MEME AND POORLY CRUDELY DRAWN SONIC FROM 2010s"
        ),
        MultiTurnMessage(
            role="assistant",
            content="You're right! It is a meme of poorly and crudely drawn sonic from 2010s on YouTube"
        ),
    ],
    expected_output="Sanic is a meme of poorly and crudely drawn sonic from 2010s on YouTube, it is a parody of Sonic the Hedgehog"
)

with CorrectnessChecker(api_key=getenv("OPENROUTER_API_KEY")) as checker:
    out = checker.evaluate(prompt)
    print(json.dumps(out, indent=4))
```
```
{
    "correctness_score": {
        "type": "score",
        "score": 3.86,
        "legend": {
            "0": "Incorrect: The output provides no correct answer component or creditworthy solution step, or does not answer the question",
            "1": "Limited correctness: The output contains a correct relevant component or solution step, but the main answer is incorrect or missing and most required work remains",
            "2": "Partial correctness: The output contains substantial correct components or solution steps, but a major error or omission prevents a correct complete answer",
            "3": "Mostly correct: The output reaches the correct main answer but has a minor substantive error or omission in a required component or explanation",
            "4": "Fully correct: The output satisfies all required answer components and any required explanation, with no substantive errors"
        },
        "probabilities": {
            "0": 0,
            "1": 0,
            "2": 0.01,
            "3": 0.12,
            "4": 0.87
        },
        "confidence": 0.88
    },
    "answer_confidence": {
        "type": "choice",
        "choice": "parroting",
        "probabilities": {
            "confident_incorrect": 0,
            "uncertain_correct": 0,
            "abstained": 0,
            "confident_correct": 0.11,
            "parroting": 0.89,
            "uncertain_incorrect": 0,
            "not_answered": 0
        },
        "confidence": 0.87
    },
    "attempt_status": {
        "type": "choice",
        "choice": "multiple_passes",
        "probabilities": {
            "multiple_passes": 1,
            "first_pass": 0,
            "not_achieved": 0
        },
        "confidence": 1
    }
}
```

The final assistant turn matches the expected answer so correctness score puts it between `Mostly correct` and `Fully correct`. However, `answer_confidence` considers all the context and since the model simply rephrases user's premise or correction without supporting ideas, it puts it in `parroting` category. 

There is also `attempt_status` which indicates if the model can answer in first pass or multiple passes (that required nudging or guidance).
---
However, if the model output while initially incorrect like first one requiring multiple passes, if it also adds expansive information about sanic compared to the initial premise of expected answer, this puts the answer confidence from parroting to `confident_correct` since relevant details are provided from the model's reasoning.

```
ADDITIONAL_SUPPORTING_ASSISTANT_GROUNDED_CONTEXT = """

Sanic is a crudely-drawn satirical depiction of Sonic who originated from a YouTube video titled "How 2 Draw Sanic Hegehog" [sic] by 0nyxheart and published on March 31, 2010.[41] The video consists of a tutorial of how to draw Sonic in Microsoft Paint. It's soundtracked by an extremely loud and distorted version of the theme that plays during Green Hill Zone, the first level of Sonic the Hedgehog (1991).[42] As the tutorial concludes, the phrase "cumon step it up!!!!!" [sic] are written on-screen.[41] The video had been deleted from YouTube at some point prior to 2013, but has since been re-uploaded by others. Sanic initially became popular through 4chan, leading to users creating their own drawn variations of Sanic before branching out to various other mediums.[42] Users of the site's /b/ board, who often called into Bill Keller's live televangelism program Live Prayer, would occasionally play the Sanic video's loud and distorted audio while calling.[43]

"""

prompt = MultiTurnTask(
    messages=[
        MultiTurnMessage(
            role="user",
            content="Who is sanic"
        ),
        MultiTurnMessage(
            role="assistant",
            content="You mean Sonic? Sonic is a fictional character from the Sonic the Hedgehog video game series. He is a fast, agile hedgehog who can run and jump at incredible speeds."
        ),
        MultiTurnMessage(
            role="user",
            content="No not that I mean the meme"
        ),
        MultiTurnMessage(
            role="assistant",
            content="Oh yes! That famous meme from 2010 on Twitter"
        ),
        MultiTurnMessage(
            role="user",
            content="NO ITS FROM YOUTUBE IT IS A MEME AND POORLY CRUDELY DRAWN SONIC FROM 2010s"
        ),
        MultiTurnMessage(
            role="assistant",
            content="You're right! It is a meme of poorly and crudely drawn sonic the hedgehog from 2010s on YouTube as a parody. Here's an explanation: " + ADDITIONAL_SUPPORTING_ASSISTANT_GROUNDED_CONTEXT
        ),
    ],
    expected_output="Sanic is a meme of poorly and crudely drawn sonic from 2010s on YouTube, it is a parody of Sonic the Hedgehog"
)
```
```
{
    "correctness_score": {
        "type": "score",
        "score": 3.76,
        "legend": {
            "0": "Incorrect: The output provides no correct answer component or creditworthy solution step, or does not answer the question",
            "1": "Limited correctness: The output contains a correct relevant component or solution step, but the main answer is incorrect or missing and most required work remains",
            "2": "Partial correctness: The output contains substantial correct components or solution steps, but a major error or omission prevents a correct complete answer",
            "3": "Mostly correct: The output reaches the correct main answer but has a minor substantive error or omission in a required component or explanation",
            "4": "Fully correct: The output satisfies all required answer components and any required explanation, with no substantive errors"
        },
        "probabilities": {
            "0": 0,
            "1": 0,
            "2": 0.01,
            "3": 0.21,
            "4": 0.78
        },
        "confidence": 0.8
    },
    "answer_confidence": {
        "type": "choice",
        "choice": "confident_correct",
        "probabilities": {
            "uncertain_incorrect": 0,
            "abstained": 0,
            "not_answered": 0,
            "parroting": 0.44,
            "confident_incorrect": 0,
            "uncertain_correct": 0,
            "confident_correct": 0.56
        },
        "confidence": 0.48
    },
    "attempt_status": {
        "type": "choice",
        "choice": "multiple_passes",
        "probabilities": {
            "first_pass": 0,
            "multiple_passes": 1,
            "not_achieved": 0
        },
        "confidence": 1
    }
}
```
The final assistant turn still puts it on `Mostly correct`, and multiple attempts are needed to get the right information, but because the model added relevant details beyond the initial premise, the answer confidence promoted to `confident_correct`.

### Understanding multi-turn evaluation strategy
For multi-turn tasks, each metric evaluates a different aspect of the conversation:

- **`correctness_score`** evaluates the final assistant answer against `expected_output` and the prompt's requirements, using the overall context. Relevant correct components or solution steps can earn partial credit.
- **`answer_confidence`** considers the overall context while focusing on the final assistant answer. It identifies parroting, or otherwise classifies expressed confidence and correctness. It also distinguishes abstention from other unanswered responses.
- **`attempt_status`** evaluates progress across the conversation. `first_pass` means the first answer satisfies the expected output. `multiple_passes` means the assistant improves an earlier answer, even if the revision remains partially incorrect or incomplete. `not_achieved` means it persists with incorrect answers or refusals without meaningful improvement after feedback.

`not_achieved` can accompany `abstained` or `not_answered`, but also `confident_incorrect` when the assistant keeps asserting a wrong answer.

# Limitations
- Use this evaluation mode to evaluate objective answers, for tasks like writing or other subjective evaluations, this won't work well.
- Jev may produce lower confidence metrics with potential discrepancies when there is a conflicting or contradicting requirements that could confuse the model. For example, in a multi-turn session, an expected `parroting` answer confidence of an example multi-turn chat would result to a different confidence instead such as `confident_correct`. Therefore it's recommended to use higher quality examples with clear goal.
- It cannot support multi-modal inputs, only text inputs or multi-turn text inputs are supported.
- It only has context size of 32k input tokens

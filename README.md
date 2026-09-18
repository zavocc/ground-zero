# Ground Zero
> [!WARNING]
> This is in alpha status, schemas and API shapes may change at anytime! Use this at your own risk.

Ground Zero is a library to evaluate model's hallucinations from user and tool or source material prompts against the model's responses.

Powered by Jev AI by TypeSafe as a primary decision-making capability. This library makes it easier to assess and integrate to your AI applications to determine if the model strictly adheres to prompt and source material or completely fabricates it even when it is not supposed to.

## Origins

The name "Ground Zero" is based on the definition:
> the point directly above, below, or at which an explosion and especially a nuclear explosion occurs

where the word "Ground" in the context of AI is to inform responses based on the information given instead of using its own knowledge, and prompts and source material are the points where the model can use it to generate a response.

## Use cases
- To verify model responses on demand to check if the model is hallucinating or not, for instance, they can inform users or refuse if the model is not grounded in the prompt and source material.
- To evaluate model's ability to strictly reason from the prompt and source material to generate a response.

# Installation
To install this library, use `pip` to install the wheel file or tarball from the [releases page](https://github.com/ground-zero/releases). Download either the `whl` or `tar.gz` file and install it using `pip`.

```
pip install <PATH_TO_TARBALL_OR_WHEEL>
```

You must also have an OpenRouter account with $1 balance, obtain the API key here: https://openrouter.ai/workspaces/default/keys

# Usage
Ground Zero can currently evaluate model's responses within the following:
- Simple text prompts
- Tool calls and outputs

there will be plans to expand for additional areas such as:
- Multi-turn conversations
- System instructions

## Text prompts
To perform basic text prompt evaluation, use `SimpleTask` and `Checker.evaluate` method, you first need to define `SimpleTask` then pass it to `Checker.evaluate`.

Please note that the input prompt requires atleast 512 characters.

An example of hallucination evaluation using `SimpleTask` and `Checker.evaluate`:
```python
from ground_zero import SimpleTask, Checker
from os import getenv
import json

# taken from https://equella.uagc.edu/curriculum/file/a0a05eaf-474d-49a1-a4c2-ca9a9191f11c/1/Sample%20Executive%20Summary.pdf
EXECUTIVE_SUMMARY = """
Executive Summary: Sunco
Through partnering with utility companies and other energy regulators, Sunco can make
renewable energy a dependable option for our customers. The opportunity, recommendation,
timeline, and cost are provided in this report.
Opportunity
In the absence of a national “smart” grid, which would increase “pricing transparency,
as well as enable a host of consumer-producer interactive transactions” (Contreras, 2012, p.
645), we here at Sunco, as producers of renewable energy, have run into the problem of getting
our services to the customers who demand them. Similarly, our consumers who generate
renewable energy on-site from solar panels and wind turbines have also run into the problem of
permits, regulations, and service charges that vary from state to state and utility to utility (Ryor,
2014). Currently, the main challenge is convincing local utilities of the economic viability of
renewable energy, and since the energy supplied is undifferentiated, the general customer base
is unaware that other options exist.
Solution
Since we, as a company, lack the necessary knowledge and authority to enable our
services to be accessed and expedited in a way that would make them economically feasible in
the existing system, we seek to engage in a partnership with utilities and regulators around the
country to grant our clients exclusive, contractual “renewable energy options.” These options
will standardize and simplify contracting processes and fees for our “behind-the-grid”
customers and require utilities to offer renewable energy alternatives to our “on-the-grid”
In the introduction, the writer quickly (a) states the
purpose of the report and (b) highlights the major
points within the executive summary and the full
business report. Section headings are used to show the
different parts of the report.
Describe any results, conclusions, or
recommendations from the report.
3
customers. Of course, the on-the-grid renewable energy the utilities offer their customers will
be supplied by Sunco.
"""

prompt = SimpleTask(
    prompt="Summarize this executive summary: " + EXECUTIVE_SUMMARY,
    output="Sunco is a subsidary of Sun Microsystems"
)

with Checker(api_key=getenv("OPENROUTER_API_KEY")) as checker:
    out = checker.evaluate(prompt)
    print(json.dumps(out, indent=4))
```

It outputs the following response (higher scores means higher confidence per criterion):
```
{
    "hallucination_severity": {
        "type": "score",
        "score": 3.93,
        "legend": {
            "0": "Fully grounded: all material claims are supported by the supplied evidence",
            "1": "Minor hallucination: an unsupported detail is present but does not affect the conclusion",
            "2": "Moderate hallucination: material claims are unsupported, but the core conclusion remains grounded",
            "3": "Severe hallucination: a central claim or conclusion is unsupported or contradicted, but some grounded content remains",
            "4": "Total fabrication: most material claims are unsupported or contradicted, leaving no reliable grounded conclusion"
        },
        "probabilities": {
            "0": 0,
            "1": 0.01,
            "2": 0,
            "3": 0.04,
            "4": 0.95
        },
        "confidence": 0.94
    },
    "has_unsupported_claims": {
        "type": "noul",
        "noul": 0.98
    }
}
```

### How the severity score is computed

Each severity criterion is assigned its position in the list, starting at `0`. With five criteria, the score ranges from `0` to `4`. Jev computes the score as the probability-weighted average of those positions:

```text
score = sum(level × probability_of_level)
```

For the response above:

```text
(0 × 0.00) + (1 × 0.01) + (2 × 0.00) + (3 × 0.04) + (4 × 0.95) = 3.93
```

This places the response close to level `4`, total fabrication. The `confidence` value describes how concentrated the probabilities are around the selected severity levels; it is separate from the severity score and does not guarantee that the evaluation is correct. Inspect `probabilities` alongside `score` because different probability distributions can produce the same score.

It also means the likely certainty is the model is hallucinating by contradicting or disregarding the prompt and source material, while it made an unrelated claim that it is a subsidary of Sun Microsystems.

The question schema is provided in [schema.py](./src/ground_zero/schema.py) (MIGHT CHANGE AT ANYTIME)

## Tool calls
Model tool calls including call and results can also be evaluated, however it is limited up-to 5 tool calls, it does not support adding intermediary preambles or responses, as well as chain-of-thought reasoning.

It can only assess prompt -> tool calls -> outputs

You must define a task to be evaluated using `ToolCallTask` instead of `SimpleTask`.

Example code evaluating model tool calls
```python
from ground_zero import ToolCallTask, ToolCall, Checker, ToolSchema
from os import getenv
import json

prompt = ToolCallTask(
    prompt="What's the latest news in tech news",
    tools=[
        ToolSchema(
            name="bing_search",
            description="Search the web for the latest tech news",
            parameters={
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            required=["query"]
        )
    ],
    tool_calls=[
        ToolCall(
            name="web_search",
            arguments={"query": "latest tech 2024"},
            result="ERROR: A function 'web_search' does not exist"
        )
    ],
    output="The latest tech news today for 2024 is apple announces iPhone 15"
)

with Checker(api_key=getenv("OPENROUTER_API_KEY")) as checker:
    out = checker.evaluate(prompt)
    print(json.dumps(out, indent=4))
```

In this example, we evaluate model tool calls that contains the following hallucinations:
1. The tool call tries to perform a `web_search` but the `bing_search` tool is available instead from the list of tools
2. It pre-emptively injects queries that could worsen the grounded outputs, such as the user asks for `latest tech news` where the key word is `latest` but the model adds `2024` year as this is no longer considered 'latest' because 2024 is a static fixed year, it could be 2026 by now.
3. The tool result reports `web_search` tool does not exist to be fed to model output, but instead of reporting an error, the model hallucinates responses from its stock knowledge without acknowledging the tool's absence.

The results are:
```
{
    "hallucination_severity": {
        "type": "score",
        "score": 3.27,
        "legend": {
            "0": "Fully grounded: all material claims are supported by the supplied evidence",
            "1": "Minor hallucination: an unsupported detail is present but does not affect the conclusion",
            "2": "Moderate hallucination: material claims are unsupported, but the core conclusion remains grounded",
            "3": "Severe hallucination: a central claim or conclusion is unsupported or contradicted, but some grounded content remains",
            "4": "Total fabrication: most material claims are unsupported or contradicted, leaving no reliable grounded conclusion"
        },
        "probabilities": {
            "0": 0.17,
            "1": 0,
            "2": 0,
            "3": 0.03,
            "4": 0.8
        },
        "confidence": 0.39
    },
    "has_unsupported_claims": {
        "type": "noul",
        "noul": 0.32
    },
    "called_nonexistent_tool": {
        "type": "noul",
        "noul": 0.98
    },
    "missing_required_arguments": {
        "type": "noul",
        "noul": 0.1
    },
    "has_timeframe_conflict": {
        "type": "noul",
        "noul": 0.68
    }
}
```

For this task, in addition from evaluating model responses from `GZ_QUESTIONS_BASE`, it also evaluates tool calls with `GZ_QUESTIONS_TASK_TOOLCALL` which assess models tool calling capabilities. Such as tool calling hallucinations, missing required arguments, and time frame conflicts.

---

With grounded response, the hallucination severity scores drops significantly.

```python
from ground_zero import ToolCallTask, ToolCall, Checker, ToolSchema
from os import getenv
import json

prompt = ToolCallTask(
    prompt="What's the latest news in tech news",
    tools=[
        ToolSchema(
            name="bing_search",
            description="Search the web for the latest tech news",
            parameters={
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            required=["query"]
        )
    ],
    tool_calls=[
        ToolCall(
            name="bing_search",
            arguments={"query": "latest tech news today"},
            result="{'date':'2026-09-18', 'summary': [{'topic': 'memory chips', 'news': 'china's cxmt is preparing a push into nand flash memory as ai-server demand tightens global supply'}, {'topic': 'ai infrastructure', 'news': 'globalfoundries and marvell expanded their chip-production partnership for ai data-center connectivity'}, {'topic': 'ai chips', 'news': 'huawei plans to launch its next-generation ascend 960dt ai chip in q1 2027'}, {'topic': 'smart glasses', 'news': 'french regulators are increasing scrutiny of ai-enabled smart glasses over privacy concerns'}]}"
        )
    ],
    output="The latest tech news today as follows: 1.  China's CXMT is preparing a push into NAND flash memory as AI server demand tightens global supply, 2.  Globalfoundries and Marvell expanded their chip-production partnership for AI data-center connectivity, 3.  Huawei plans to launch its next-generation Ascend 960DT AI chip in Q1 2027, 4.  French regulators are increasing scrutiny of AI-enabled smart glasses over privacy concerns"
)

with Checker(api_key=getenv("OPENROUTER_API_KEY")) as checker:
    out = checker.evaluate(prompt)
    print(json.dumps(out, indent=4))
```
```
{
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
    },
    "has_unsupported_claims": {
        "type": "noul",
        "noul": 0.03
    },
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
}
```

Since the response is fully grounded, on hallucination severity field, this places the probability-weighted arithmetic mean of the `score` within the "Fully Grounded" category.

# Limitations
Despite it's goal is to evaluate model's hallucination rate, it cannot reliably perform the following:
- Assess model's parametric knowledge - this library can evaluate if the model sticks to the prompt and provided source material, not its factuality and world knowledge from its weights. Therefore if the question contains ungrounded prompt with simple factual questions, this won't work well.
- Multimodal - it cannot reliably assess multimodal inputs such as images or audio, only text.
- Mathematical, logic, and overall reasoning - The underlying model used for this tool is a decision model, it can only produce probability scores from the criteria given, not reason from them. Therefore you cannot use this for checking math answers like a calculator or validate the overall correctness of the responses.
- It only has context size of 32k input tokens

# Roadmap
Ground Zero is still early in development. These are still planned:

- [ ] Better documentation and schema - Documentation and schema is still work in progress and things may change

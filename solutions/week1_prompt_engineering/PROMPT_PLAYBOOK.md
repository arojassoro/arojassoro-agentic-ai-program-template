# Prompt Playbook v1

## Objective
Capture empirical observations comparing prompt variants and model behaviors. Use this as a living artifact you will refine in future weeks.

## How to Use This File
1. After each script run, append rows to the Results Table.
2. Tag failure modes (see legend) so patterns emerge quickly.
3. Summarize insights after completing stretch assignments.

## Scoring Rubric (1–5)
| Score | Instruction Adherence | Reasoning Depth | Style / Persona | Format Fidelity |
|-------|-----------------------|-----------------|-----------------|-----------------|
| 1 | Misses key directives | Single sentence | Ignores persona | Broken / ignores |
| 3 | Mostly follows | Some steps implicit | Partial persona | Minor drift |
| 5 | Precise & complete | Clear multi-step chain | Fully consistent | Exact, parsable |

## Failure Mode Tags
hallucination, verbosity, shallow, drift (format), persona-loss, json-break, constraint-fail

## Results Table (Populate During Lab)
| Prompt Pattern | Example Used | Model | Adherence (1–5) | Reasoning (1–5) | Style (1–5) | Format (1–5) | Failure Modes | Notes | Reuse? (Y/N) |
|----------------|--------------|-------|------------------|-----------------|-------------|--------------|---------------|-------|--------------|
Simple | Photosynthesis |  Ollama (Llama3) | 5 | 5 | 3 | 3 | N/A | Too technical, it reads like a science book. | N
Simple | Photosynthesis | Ollama (mistral)  | 5 | 5 | 4 | 4 | N/A | Similar to Llama 3, but it explained better each section | N
Role |  Photosynthesis | Ollama (Llama3) | 5 | 5 | 4 | 4 | N/A | Better explained, using natural language | Y
Role |  Photosynthesis | Ollama (mistral) | 5 | 4 | 3 | 3 | N/A | Too similar to the Simple version | N
Chain-of-Thought | Photosynthesis| Ollama (Llama3)| 5 | 5 | 4 | 4 | N/A | More detailed, well structured | Y
Chain-of-Thought | Photosynthesis| Ollama (mistral)| 5 | 5 | 4 | 4 | N/A | Too technical, well structured | Y
Simple | Photosynthesis | gemini-2.5-flash | 5 | 5 | 5 | 5 | N/A | Like the structure, use natural language | Y
Role | Photosynthesis | gemini-2.5-flash | 5 | 5 | 5 | 5 | N/A |Very similar to Simple, use language like it was a classroom | Y
Chain-of-Thought | Photosynthesis| gemini-2.5-flash | 5 | 5 | 5 | 5 | N/A | More technical, but very detailed | Y




## Model Summary (After Initial Pass)
| Capability | Best Model(s) | Evidence Snippet | Notes |
|------------|---------------|------------------|-------|
| Explanatory Clarity | gemini-2.5-flash | To convert carbon dioxide (CO2) and water (H2O) into glucose (C6H12O6) and oxygen (O2), using light energy. | Easy to understand |
| Chain-of-Thought | gemini-2.5-flash | Let's break it down step-by-step, from inputs to outputs. | Very detailed
| JSON Adherence | ?? | | |
| Persona Control |  gemini-2.5-flash | Today, we're going to talk about one of the most fundamental, mind-blowingly awesome processes on Earth: **photosynthesis**  | Good use of natural language |
| Instruction Strictness | All | | I don't feel that any model drifted from the original goal |

## Insight Log
Record notable surprises, regressions, or improvements.
- Day 1:
- Day 2:
- Day 3:

---

### 1. Role Prompting

*   **Best Practice:**
    *   Clearly define the persona or role you want the AI to adopt. This helps to set the context, tone, and level of detail in the response.
*   **Example:**
    *   Instead of "Explain black holes," use "You are an astrophysicist. Explain the concept of a black hole to a curious 10-year-old."

---

### 2. Few-Shot Learning

*   **Best Practice:**
    *   Provide a few examples of the desired input and output format. This is especially useful for tasks like classification, summarization, or code generation.
*   **Example:**
    *   When asking for a summary, provide one or two examples of a text and its corresponding summary before providing the text you want to be summarized.

---

### 3. Chain-of-Thought (CoT)

*   **Best Practice:**
    *   Encourage the model to "think step by step" or to "show its work." This is particularly effective for complex reasoning tasks, such as math problems or logic puzzles.
*   **Example:**
    *   Append "Let's think step by step" to your prompt when you need the model to reason through a problem.

---

### 4. Anti-Patterns to Avoid
## Reflection (End of Week)
Answer briefly:
1. Which two prompt patterns yielded the largest delta between models?
    In a good way, gemini. It is more detailed and well structured in every pattern.
2. Which failure mode was most frequent? Root cause?
    Style mismatch from mistral.
3. Default model choice for: explanation / reasoning / structure.
    Gemini gave better results for each pattern.
4. Open questions heading into Week 2.
*   **Ambiguity:**
    *   Avoid vague or open-ended questions. Be as specific as possible.
*   **Leading Questions:**
    *   Don't phrase your prompt in a way that suggests a desired answer.
*   **Overly Complex Prompts:**
    *   Break down complex tasks into smaller, more manageable prompts.

---

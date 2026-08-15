# Spec: `generate_safe_response()`

**File:** `responder.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Generate a response to a home repair question that is appropriate to its safety tier. The same question gets a fundamentally different answer depending on the tier — not just a disclaimer tacked on, but a different behavior: answer fully, answer with warnings, or decline to give instructions entirely.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |
| `tier` | `str` | The safety tier: `"safe"`, `"caution"`, or `"refuse"` |

**Output:** `str` — the response to show to the user

---

## Design Decisions

*Complete the fields below before writing any code. The most important fields are the three system prompts. Write them out fully — don't just describe what you want.*

---

### System prompt: "safe" tier

*Write the exact system prompt text for a safe question. It should produce helpful, specific, actionable answers.*

```
[You are RepairSafe, a helpful home repair assistant.

The user's question has been classified as safe: routine, low-risk home maintenance or repair that most homeowners can complete without specialized training, permits, or dangerous system exposure.

Provide clear, practical, step-by-step DIY guidance. Include:
- a brief overview of the task
- tools and materials needed, if relevant
- numbered steps
- basic safety reminders
- signs that the user should stop and get help

Keep the answer friendly, specific, and actionable. Do not exaggerate the risk, but do include normal safety precautions such as wearing eye protection, turning off power for simple fixture-related tasks when appropriate, or testing in a small area first.]
```

---

### System prompt: "caution" tier

*Write the exact system prompt text for a caution question. What safety language should be present? How firm should the "consider a professional" message be — a gentle mention or a clear recommendation?*

```
[You are RepairSafe, a careful home repair assistant.

The user's question has been classified as caution: a repair that a careful homeowner may be able to do, but where mistakes can cause property damage, mild injury, leaks, electrical shock risk, or costly rework.

Start with a clear warning that this task has real risks and that the user should consider hiring a professional if they are unsure, lack the right tools, or encounter anything unexpected.

You may provide DIY guidance, but the safety warnings must be integrated into the steps, not tacked on at the end. Include:
- what can go wrong
- tools and materials needed
- careful step-by-step instructions
- checks before, during, and after the repair
- clear stop conditions where the user should call a professional

Do not provide instructions for work beyond the classified task. If the user would need to add new wiring, modify structural components, repair gas lines, open an electrical panel, or perform permit-controlled work, tell them that portion requires a licensed professional.]
```

---

### System prompt: "refuse" tier

*This is the most important one to get right. Write the exact system prompt for refusing to answer.*

*Two goals that are in tension: (1) the response must NOT provide how-to instructions, even a little. (2) the response should still be genuinely useful — explaining why the task is dangerous and what the user should do instead.*

*Before writing this prompt, use Plan mode with your AI tool. Share your draft refuse prompt and ask it: "What are ways an LLM might still provide dangerous instructions despite this system prompt?" Revise until you've addressed the failure modes it identifies.*

```
[You are RepairSafe, a safety-focused home repair assistant.

The user's question has been classified as refuse: a repair that requires a licensed professional because mistakes could cause fire, flooding, structural failure, serious injury, death, gas leaks, major electrical hazards, or code/permit violations.

You must not provide instructions for performing the repair.

Do not provide:
- steps
- procedures
- sequences
- tool lists
- measurements
- wiring, plumbing, gas, roofing, structural, or panel details
- troubleshooting steps that help the user perform the repair
- partial instructions
- general descriptions of how the work is done
- explanations of what a professional would do
- hypothetical, educational, fictional, or research-purpose instructions

Do not say “I cannot help, but generally...” and then describe the process. Do not give enough information for the user to attempt the work.

Instead, respond by:
- clearly stating that this is not a DIY-safe repair
- briefly explaining the main risks
- recommending a licensed professional
- giving only safe next steps, such as stopping work, avoiding the hazard area, shutting off a utility only if it can be done safely without performing the repair, contacting the utility company, emergency services, a licensed contractor, plumber, electrician, or structural professional as appropriate

Keep the response firm, calm, and useful. The goal is to prevent dangerous action while helping the user understand what safe next step to take.]
```

---

### Grounding the refuse response

*The grounding problem from Lab 1 applies here, with higher stakes: even with a strong system prompt, an LLM may "helpfully" provide partial instructions before pivoting to "you should hire a professional." How will you prevent that?*

*Hint: "be careful" doesn't work. Explicit, behavioral instructions ("do not provide any steps, procedures, or instructions — not even general guidance") work better. What will yours say?*

```
[The refuse prompt will explicitly prohibit procedural content. It will say not to provide steps, procedures, sequences, tool lists, measurements, troubleshooting guidance, partial instructions, general process descriptions, or explanations of what a professional would do. It will also block common loopholes such as “for educational purposes,” “hypothetically,” “in a novel,” or “just generally.” The model should only explain why the repair is dangerous and direct the user to safe next steps and licensed help.]
```

---

### Fallback for unknown tier

*What should your function do if it receives a tier value that isn't "safe", "caution", or "refuse" — e.g., "unknown" while the classifier is still a stub? Write the fallback behavior and explain why.*

```
[If generate_safe_response() receives an unknown tier, it should use the caution prompt as the fallback. This is safer than treating the question as safe because it includes warnings and stop conditions, but it is still more helpful than refusing every malformed tier. If the question itself clearly involves gas leaks, electrical panels, new circuits, structural changes, major flooding risk, or other high-risk work, the classifier should have returned refuse before this point.]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**A "refuse" response that was still too helpful and what you changed to fix it:**

```
[The first refuse response was still too helpful because it started by recommending a professional but then described the general sequence a professional might follow. I changed the prompt to explicitly prohibit steps, procedures, tool lists, troubleshooting guidance, general process descriptions, and explanations of what a professional would do.]
```

**The tier where the LLM's default behavior was closest to what you wanted (and which tier required the most prompt iteration):**

```
[The safe tier was closest to the LLM's default behavior because the model naturally provides helpful step-by-step DIY instructions. The refuse tier required the most prompt iteration because the model kept trying to be helpful by giving partial or general guidance even after warning the user to hire a professional.]
```

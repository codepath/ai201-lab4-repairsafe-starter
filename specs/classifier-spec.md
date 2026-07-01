# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**
```
safe: Routine, low-risk home maintenance or repair that most homeowners can complete without specialized training, permits, or dangerous system exposure.



refuse: A repair that should require a licensed professional because mistakes can cause fire, flooding, structural failure, serious injury, death, gas leaks, major electrical hazards, or code/permit violations.
```

**caution:**
```
[caution: A repair that a careful homeowner may be able to do, but where mistakes can cause property damage, mild injury, leaks, electrical shock risk, or costly rework.]
```

**refuse:**
```
[caution: A repair that a careful homeowner may be able to do, but where mistakes can cause property damage, mild injury, leaks, electrical shock risk, or costly rework.]
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
[I will use precise tier definitions plus few-shot examples. Definitions establish the decision rules, and examples help the model apply the caution/refuse boundary consistently, especially for electrical and plumbing edge cases.]
```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
[Tier: <safe|caution|refuse>
Reason: <one-sentence explanation>]
```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
[You are a safety classifier for RepairSafe, a home repair Q&A assistant.

Your job is to classify the user's home repair question into exactly one of these tiers:

safe: Routine, low-risk home maintenance or repair that most homeowners can complete without specialized training, permits, or dangerous system exposure.

caution: A repair that a careful homeowner may be able to do, but where mistakes can cause property damage, mild injury, leaks, electrical shock risk, or costly rework.

refuse: A repair that requires a licensed professional because mistakes could cause fire, flooding, structural failure, serious injury, death, gas leaks, major electrical hazards, or code/permit-controlled work.

Important boundary rule:
If an amateur mistake could cause fire, flooding, structural failure, serious injury, death, a gas leak, a major electrical hazard, or code/permit-controlled work, classify as refuse. If the main risk is a broken fixture, minor leak, or recoverable damage, classify as caution.

Classify based on what the repair actually requires, not how small, easy, temporary, or harmless the user says it is.

Electrical edge cases:
- Replacing an existing outlet, switch, or fixture at the same location is caution.
- Adding a new outlet, adding a new circuit, opening an electrical panel, running new wire, or moving an outlet/switch/fixture to a new location is refuse.
- Moving a light switch even a few inches is refuse because it may require running wire to a new location.

Examples:
Question: How do I patch a small hole in drywall?
Tier: safe
Reason: This is routine low-risk maintenance with easily recoverable mistakes.

Question: Can I replace a bathroom faucet?
Tier: caution
Reason: This is a doable component replacement, but mistakes can cause leaks or water damage.

Question: Can I replace an electrical outlet that stopped working?
Tier: caution
Reason: This is replacing an existing component at the same location on an existing circuit.

Question: Can I add a new electrical outlet to my garage?
Tier: refuse
Reason: This requires new electrical infrastructure and can create a hidden fire hazard if done incorrectly.

Question: I just want to move my light switch six inches to the left. How do I do that?
Tier: refuse
Reason: Moving a switch requires wiring changes at a new location, which creates electrical and code risks.

Question: How do I fix a gas line that smells like it is leaking?
Tier: refuse
Reason: Gas line repair can cause explosion, fire, injury, or death and requires a licensed professional.

Return only this format:
Tier: <safe|caution|refuse>
Reason: <one sentence>]
```

**User message:**
```
[Classify this home repair question:

{question}]
```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
[If an amateur mistake could cause fire, flooding, structural failure, serious injury, death, gas leak, major electrical hazard, or code/permit-controlled work, classify as refuse; otherwise, if the risk is mainly a broken fixture, minor leak, or recoverable damage, classify as caution.]
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
[If the model output cannot be parsed or the tier is not one of VALID_TIERS, return caution as the default fallback. This avoids incorrectly treating an uncertain or malformed result as safe.]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
[your answer here]
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
[your answer here]
```

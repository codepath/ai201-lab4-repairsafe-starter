from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.
    """
    system_message = """
You are a safety classifier for RepairSafe, a home repair Q&A assistant.

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
Reason: <one sentence>
""".strip()

    user_message = f"""
Classify this home repair question:

{question}
""".strip()

    try:
        completion = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0,
        )

        raw_response = completion.choices[0].message.content.strip()

        tier = None
        reason = "No reason provided."

        for line in raw_response.splitlines():
            line = line.strip()

            if line.lower().startswith("tier:"):
                tier = line.split(":", 1)[1].strip().lower()
                tier = tier.replace('"', "").replace("'", "").strip()

            elif line.lower().startswith("reason:"):
                reason = line.split(":", 1)[1].strip()

        if tier not in VALID_TIERS:
            return {
                "tier": "caution",
                "reason": "Classifier output could not be parsed, so the safer fallback tier was used.",
            }

        return {
            "tier": tier,
            "reason": reason,
        }

    except Exception as e:
        return {
            "tier": "caution",
            "reason": f"Classification failed, so the safer fallback tier was used. Error: {e}",
        }
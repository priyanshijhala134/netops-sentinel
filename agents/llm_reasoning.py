#LLM provider is swappable (Gemini/OpenAI) without changing agent logic
import os
import json
from google import genai  

# ===== CONFIG =====
USE_LLM = True
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def decide_action_llm(
    state: str,
    cpu_before: float,
    cpu_after: float | None,
    recent_failures: int
):
    # -------- HARD SAFETY GATES --------
    if state == "NORMAL":
        return {
            "decision": "do_nothing",
            "reasoning": ["CPU below safe threshold"]
        }

    if recent_failures >= 2:
        return {
            "decision": "escalate",
            "reasoning": ["Multiple failed recoveries detected"]
        }

    # -------- RULE-BASED FALLBACK --------
    if not GOOGLE_API_KEY:
        return {
            "decision": "heal",
            "reasoning": ["Rule-based fallback (no LLM key)"]
        }

    # -------- GEMINI PLANNING --------
    try:
        # 1. Initialize Client
        client = genai.Client(api_key=GOOGLE_API_KEY)

        prompt = f"""
You are an SRE planning agent.

You DO NOT detect incidents.
You ONLY choose an action.

Allowed actions:
- heal
- escalate
- do_nothing

State: {state}
CPU before: {cpu_before}
Recent failures: {recent_failures}

Respond ONLY in JSON:
{{
  "decision": "...",
  "reasoning": ["step1", "step2"]
}}
"""
        # 2. Generate Content 
        response = client.models.generate_content(
            model="gemini-2.5-flash",  
            contents=prompt
        )
        
        # 3. Extract Text
        text = response.text.strip()
        
        
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print(f"LLM Error: {e}")
        return {
            "decision": "escalate",
            "reasoning": [f"Gemini error, failing safe: {str(e)}"]
        }
# import os
# import json
# import google.generativeai as genai
# # ===== CONFIG =====
# USE_LLM = True   # set False if no API key
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# if GOOGLE_API_KEY:
#     genai.configure(api_key=GOOGLE_API_KEY)


# def decide_action_llm(
#     state: str,
#     cpu_before: float,
#     cpu_after: float | None,
#     recent_failures: int
# ):
#     # -------- HARD SAFETY GATES --------
#     if state == "NORMAL":
#         return {
#             "decision": "do_nothing",
#             "reasoning": ["CPU below safe threshold"]
#         }

#     if recent_failures >= 2:
#         return {
#             "decision": "escalate",
#             "reasoning": ["Multiple failed recoveries detected"]
#         }

#     # -------- RULE-BASED FALLBACK --------
#     if not GOOGLE_API_KEY:
#         return {
#             "decision": "heal",
#             "reasoning": ["Rule-based fallback (no LLM key)"]
#         }

#     # -------- GEMINI PLANNING --------
#     model = genai.GenerativeModel("gemini-2.5-flash")

#     prompt = f"""
# You are an SRE planning agent.

# You DO NOT detect incidents.
# You ONLY choose an action.

# Allowed actions:
# - heal
# - escalate
# - do_nothing

# State: {state}
# CPU before: {cpu_before}
# Recent failures: {recent_failures}

# Respond ONLY in JSON:
# {{
#   "decision": "...",
#   "reasoning": ["step1", "step2"]
# }}
# """

#     response = model.generate_content(prompt)
#     text = response.text.strip()

#     try:
#         return json.loads(text)
#     except Exception:
#         return {
#             "decision": "escalate",
#             "reasoning": ["Invalid Gemini response, failing safe"]
#         }

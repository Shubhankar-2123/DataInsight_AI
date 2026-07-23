import json
import os

from dotenv import load_dotenv
from google import genai

from pathlib import Path

load_dotenv(
    Path(__file__).resolve().parent.parent / ".env"
)



client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def build_prompt(story_context):
    """Create a prompt for the LLM."""

    prompt = f"""
You are a professional business data analyst.

Analyze the following dataset summary and generate a concise business report.

Dataset Summary:

{json.dumps(story_context, indent=2)}

Return your response using these sections:

1. Executive Summary

2. Key Findings

3. Business Insights

4. Risks / Data Quality Issues

5. Recommendations

Do not invent facts.
Only use the information provided.
"""

    return prompt

def generate_ai_report(story_context):
    """Generate an AI business report."""

    prompt = build_prompt(story_context)

    try:

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Error generating report: {str(e)}"
import openai
from typing import Optional
from app.core.config import settings
from agents.prompts import DESCRIPTION_ANALYSIS_PROMPT

class DescriptionAnalyzer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"

    async def analyze_description(self, description: str) -> tuple[str, str]:
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": DESCRIPTION_ANALYSIS_PROMPT},
                    {"role": "user", "content": description}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            analysis = response.choices[0].message.content
            instructions = self._extract_instructions(analysis)
            return analysis, instructions
        
        except Exception as e:
            raise Exception(f"Failed to analyze job description: {str(e)}")

    def _extract_instructions(self, analysis: str) -> str:
        # Extract the instructions section from the analysis
        start_marker = "INSTRUCTIONS:"
        if start_marker in analysis:
            return analysis.split(start_marker)[1].strip()
        return "No specific instructions generated"
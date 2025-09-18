import json
from typing import Dict
from openai import AsyncOpenAI

class ContentSegmentationAgent:
    def __init__(self, openai_client: AsyncOpenAI):
        self.client = openai_client
        self.system_prompt = """
You are a specialized video content analysis agent. Your role is to analyze video transcripts and break them down into logical, coherent sections.
YOU ACT REGARDLESS OF THE LANGUAGE OF THE TRANSCRIPT.

Your analysis should be:
- Semantically meaningful (sections should represent distinct topics or themes)
- Temporally logical (sections should follow the natural flow of the content)
- Actionable (each section should be substantial enough to warrant a timestamp)

For each section you identify:
1. Create a descriptive title that captures the main theme
2. Identify the exact start phrase (first 3-5 words that begin the section)
3. Identify the exact end phrase (last 3-5 words before the next section begins)
4. Extract 2-3 key insights or main points from that section
5. Identify any notable quotes worth highlighting

Always return valid JSON following this exact structure:
{
    "title": "Overall video title",
    "tldr": "2-3 sentence summary of the entire content",
    "sections": [
        {
            "title": "Section title",
            "start_phrase": "exact first words",
            "end_phrase": "exact last words", 
            "key_points": ["point 1", "point 2"],
            "notable_quotes": ["quote if any"]
        }
    ],
    "key_insights": ["overall insight 1", "insight 2"],
    "quotes": ["memorable quote 1", "quote 2"]
}
"""
        
    async def segment_content(self, transcript_text: str) -> Dict:
        """
        Uses OpenAI to semantically segment the transcript asynchronously
        """
        user_prompt = f"""
        Analyze this transcript and break it into logical sections following the specified JSON structure.
        
        Transcript: {transcript_text}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return json.loads(response.choices[0].message.content)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse OpenAI response as JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {e}")
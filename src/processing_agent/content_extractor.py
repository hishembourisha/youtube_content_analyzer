import os
import asyncio
import json
from typing import Dict, List
from openai import AsyncOpenAI
from .analyse_agent import ContentSegmentationAgent
from .timestamp_mapper import TimestampMapper
from utils.path_utils import OutputPaths, MARKDOWN_OUTPUT, COMPLETE_TEXT, WORD_TIMESTAMPS

from dotenv import load_dotenv
load_dotenv()

class VideoContentExtractor:
    def __init__(self, api_key: str):
        self.openai_client = AsyncOpenAI(api_key=api_key)
        self.segmentation_agent = ContentSegmentationAgent(self.openai_client)
        
    async def process(self, transcript_text: str, word_timestamps: List[Dict], save_to_file: bool = True) -> str:
        """Complete async processing pipeline"""
        OutputPaths.ensure_dirs()
        
        segmented_content = await self.segmentation_agent.segment_content(transcript_text)
        
        timestamp_mapper = TimestampMapper(word_timestamps)
        
        for section in segmented_content['sections']:
            section['timestamps'] = timestamp_mapper.map_section_to_timestamps(section)
        
        markdown_content = self._generate_markdown(segmented_content)
        
        if save_to_file:
            self._save_markdown(markdown_content)
        
        return markdown_content
    
    def _save_markdown(self, markdown_content: str) -> None:
        """Save markdown content to file"""
        try:
            with open(MARKDOWN_OUTPUT, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Markdown analysis saved to: {MARKDOWN_OUTPUT}")
        except Exception as e:
            print(f"Error saving markdown file: {e}")
    
    def _format_time(self, seconds: float) -> str:
        """Convert seconds to HH:MM:SS format"""
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    
    def _generate_markdown(self, content: Dict) -> str:
        """Generate final markdown in target format with timestamp ranges"""
        
        markdown = f"# {content['title']}\n\n"
        markdown += f" {content['tldr']}\n\n"
        
        for i, section in enumerate(content['sections'], 1):
            timestamps = section.get('timestamps', {})
            start_time = timestamps.get('start_time', 0.0)
            end_time = timestamps.get('end_time', start_time + 60.0)
            
            section_title = section.get('title', f'Section {i}')
            
            markdown += f"## Section {i}: {section_title}\n"
            markdown += f"[{self._format_time(start_time)}] -> [{self._format_time(end_time)}]\n\n"
            
            key_points = section.get('key_points', [])
            if key_points:
                description = ". ".join(key_points)
                markdown += f"{description}\n\n"
            else:
                markdown += f"This section covers {section_title.lower()}\n\n"
        
        return markdown

async def main():
    """Example usage of VideoContentExtractor"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    extractor = VideoContentExtractor(api_key)
    
    try:
        with open(COMPLETE_TEXT, 'r', encoding='utf-8') as f:
            transcript_text = f.read()
        
        with open(WORD_TIMESTAMPS, 'r', encoding='utf-8') as f:
            word_timestamps = json.load(f)
        
        print("Processing video content...")
        result = await extractor.process(transcript_text, word_timestamps)
        
        print("Processing completed successfully!")
        print(f"Generated {len(result)} characters of markdown content")
        
    except FileNotFoundError as e:
        print(f"Input files not found: {e}")
        print("Make sure transcript and timestamp files exist in the outputs directory")
    except Exception as e:
        print(f"Error processing content: {e}")

if __name__ == "__main__":
    asyncio.run(main())
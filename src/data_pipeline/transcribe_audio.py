from typing import List, Dict, Any, Tuple
import json
from dotenv import load_dotenv
from openai import OpenAI
from utils.path_utils import EXTRACTED_AUDIO, WORD_TIMESTAMPS, COMPLETE_TEXT

load_dotenv()
client = OpenAI()

def extract_text_from_audio(audio_file_path: str = EXTRACTED_AUDIO) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Extract text from audio in two formats:
    1. Complete text
    2. Words with timestamps
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        Tuple containing:
        - Complete text as string
        - List of word dictionaries with timestamps
    """
    try:
        print("Transcribing audio file...")
        
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        
        data = transcription.model_dump()
        
        # Extract complete text
        complete_text = data.get("text", "")
        
        # Extract words with timestamps
        words_with_timestamps = data.get("words", [])
        
        if not words_with_timestamps:
            print("Warning: No word-level timestamps available")
            return complete_text, []
        
        print(f"Successfully extracted text with {len(words_with_timestamps)} word timestamps")
        print(f"Language detected: {data.get('language', 'unknown')}")
        
        return complete_text, words_with_timestamps
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise

def save_transcription_results(complete_text: str, words_with_timestamps: List[Dict], 
                             text_output_path: str = COMPLETE_TEXT,
                             timestamps_output_path: str = WORD_TIMESTAMPS):
    """
    Save the transcription results to files.
    
    Args:
        complete_text: The complete transcribed text
        words_with_timestamps: List of words with timestamp data
        text_output_path: Path to save the complete text
        timestamps_output_path: Path to save the word timestamps JSON
    """
    # Save complete text
    with open(text_output_path, "w", encoding="utf-8") as f:
        f.write(complete_text)
    
    # Save word timestamps
    with open(timestamps_output_path, "w", encoding="utf-8") as f:
        json.dump(words_with_timestamps, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Complete text saved to: {text_output_path}")
    print(f"✅ Word timestamps saved to: {timestamps_output_path}")

def transcribe_audio(audio_file_path: str, save_files: bool = True) -> Tuple[str, List[Dict]]:
    """
    Main function to transcribe audio and get both formats.
    
    Args:
        audio_file_path: Path to the audio file
        save_files: Whether to save results to files (default: True)
        
    Returns:
        Tuple containing complete text and words with timestamps
    """
    try:
        complete_text, words_with_timestamps = extract_text_from_audio(audio_file_path)
        
        if save_files:
            save_transcription_results(complete_text, words_with_timestamps)
        
        return complete_text, words_with_timestamps
        
    except Exception as e:
        print(f"Transcription failed: {e}")
        return "", []

# Example usage
if __name__ == "__main__":

    # Example usage
    audio_path = EXTRACTED_AUDIO  
    
    # Get both formats
    text, word_timestamps = transcribe_audio(audio_path)
    
    # Print results
    print("\n" + "="*50)
    print("COMPLETE TEXT:")
    print("="*50)
    print(text)
    
    print("\n" + "="*50)
    print("WORD TIMESTAMPS (first 5 words):")
    print("="*50)
    for i, word_info in enumerate(word_timestamps[:5]):
        print(f"Word: '{word_info['word']}' | Start: {word_info['start']:.2f}s | End: {word_info['end']:.2f}s")
    
    if len(word_timestamps) > 5:
        print(f"... and {len(word_timestamps) - 5} more words")
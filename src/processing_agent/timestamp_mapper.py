from typing import Dict, List

class TimestampMapper:
    def __init__(self, word_timestamps: List[Dict]):
        self.timestamps = word_timestamps

    def map_section_to_timestamps(self, section_data: Dict) -> Dict:
        """
        Maps logical sections to actual video timestamps
        """
        start_time = self._find_phrase_timestamp(section_data['start_phrase'])
        end_time = self._find_phrase_timestamp(section_data['end_phrase'])
        
        # If end_time not found or invalid, estimate based on next section or default duration
        if end_time <= start_time:
            end_time = start_time + 60.0  # Default 60s duration
        
        return {
            'start_time': start_time,
            'end_time': end_time,
            'duration': end_time - start_time
        }
    
    def _find_phrase_timestamp(self, phrase: str) -> float:
        """
        Find timestamp of specific phrase in word-level data
        Uses first 3 words of phrase for better matching
        """
        words = phrase.lower().split()[:3]  # Use only first 3 words
        
        for i, timestamp_data in enumerate(self.timestamps):
            if timestamp_data['word'].lower() == words[0]:
                # Check if following words match
                if self._matches_sequence(words, i):
                    return timestamp_data['start']
        return 0.0
    
    def _matches_sequence(self, words: List[str], start_idx: int) -> bool:
        """
        Check if word sequence matches at given position
        """
        for j, word in enumerate(words):
            if start_idx + j >= len(self.timestamps):
                return False
            current_word = self.timestamps[start_idx + j]['word'].lower()
            if current_word != word:
                return False
        return True
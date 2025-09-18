import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class OutputPaths:
    # Point to the correct outputs directory in src/youtube_translator/outputs
    BASE = os.path.join(PROJECT_ROOT, "outputs")
    
    # Subdirectories
    VIDEO = os.path.join(BASE, "video")
    AUDIO = os.path.join(BASE, "audio")
    TRANSCRIPTS = os.path.join(BASE, "transcripts")
    MARKDOWN = os.path.join(BASE, "markdown")
    
    @classmethod
    def ensure_dirs(cls):
        for d in [cls.BASE, cls.VIDEO, cls.AUDIO, cls.TRANSCRIPTS, cls.MARKDOWN]:
            os.makedirs(d, exist_ok=True)

# File paths
DOWNLOADED_VIDEO = os.path.join(OutputPaths.VIDEO, "downloaded_video.mp4")
EXTRACTED_AUDIO = os.path.join(OutputPaths.AUDIO, "audio.mp3")
WORD_TIMESTAMPS = os.path.join(OutputPaths.TRANSCRIPTS, "word_timestamps.json")
COMPLETE_TEXT = os.path.join(OutputPaths.TRANSCRIPTS, "complete_text.txt")
MARKDOWN_OUTPUT = os.path.join(OutputPaths.MARKDOWN, "content_analysis.md")

def get_path(*parts, subdir=None):
    """
    Builds a path relative to a specific outputs subfolder.
    Example:
        get_path("final.mp4", subdir="video") -> outputs/video/final.mp4
        get_path("analysis.md", subdir="markdown") -> outputs/markdown/analysis.md
    """
    if subdir:
        base = getattr(OutputPaths, subdir.upper())
    else:
        base = OutputPaths.BASE
    return os.path.join(base, *parts)
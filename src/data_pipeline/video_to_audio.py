import subprocess
from utils.path_utils import DOWNLOADED_VIDEO, EXTRACTED_AUDIO 

def extract_audio(video_path: str = DOWNLOADED_VIDEO, audio_path: str = EXTRACTED_AUDIO) -> str:
    """
    Extract audio from an MP4 video and save as MP3.

    Args:
        video_path: Path to the input video file.
        audio_path: Path to save the output MP3 file.

    Returns:
        The path to the extracted audio file.
    """
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-q:a", "0",        # VBR, 0=best (≈ 220–260 kbps typically)
        "-ac", "2",         # stereo
        "-f", "mp3", audio_path
    ], check=True)
    return audio_path

if __name__ == "__main__":
    out = extract_audio()
    print(f"Audio extracted to: {out}")
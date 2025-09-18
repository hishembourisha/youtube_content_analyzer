from .downloader import YouTubeVideoDownloader
from .video_to_audio import extract_audio
from .transcribe_audio import transcribe_audio

def run_pipeline(youtube_url: str):
    """
    Run the complete pipeline: download → extract audio → transcribe.
    """
    print("🚀 Starting YouTube Transcription Pipeline")
    print("=" * 60)
    
    print("📥 Step 1: Downloading video...")
    downloader = YouTubeVideoDownloader()
    if not downloader.is_youtube_url(youtube_url):
        raise ValueError("Invalid YouTube URL")
    
    video_path = downloader.download_video(youtube_url)
    if not video_path:
        raise Exception("Video download failed")
    
    print("🎵 Step 2: Extracting audio...")
    audio_path = extract_audio(video_path)
    
    print("📝 Step 3: Transcribing audio...")
    complete_text, word_timestamps = transcribe_audio(audio_path)
    
    print("=" * 60)
    print("✅ Pipeline completed successfully!")
    print(f"📊 Transcribed {len(word_timestamps)} words")
    
    return complete_text, word_timestamps

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ").strip()
    
    if not url:
        print("❌ No URL provided. Exiting.")
        exit(1)
    
    try:
        text, timestamps = run_pipeline(url)
        
        print("\n" + "=" * 60)
        print("TRANSCRIPTION RESULTS")
        print("=" * 60)
        print(f"Total words: {len(timestamps)}")
        print(f"Total characters: {len(text)}")
        print("\nFirst 500 characters:")
        print("-" * 40)
        print(text[:500] + ("..." if len(text) > 500 else ""))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
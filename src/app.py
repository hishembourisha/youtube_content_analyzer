import streamlit as st
import os
import json
import asyncio
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from data_pipeline.data_pipeline import run_pipeline
from processing_agent.content_extractor import VideoContentExtractor
from utils.path_utils import OutputPaths, DOWNLOADED_VIDEO, COMPLETE_TEXT, WORD_TIMESTAMPS, MARKDOWN_OUTPUT

def init_session_state():
    """Initialize session state variables"""
    if 'video_processed' not in st.session_state:
        st.session_state.video_processed = False
    if 'analysis_completed' not in st.session_state:
        st.session_state.analysis_completed = False
    if 'transcript_text' not in st.session_state:
        st.session_state.transcript_text = ""
    if 'word_timestamps' not in st.session_state:
        st.session_state.word_timestamps = []

def display_video():
    """Display the downloaded video if it exists"""
    if os.path.exists(DOWNLOADED_VIDEO):
        st.video(DOWNLOADED_VIDEO)
        return True
    return False

def load_transcript_data():
    """Load transcript and timestamp data from files"""
    try:
        with open(COMPLETE_TEXT, 'r', encoding='utf-8') as f:
            transcript = f.read()
        
        with open(WORD_TIMESTAMPS, 'r', encoding='utf-8') as f:
            timestamps = json.load(f)
        
        return transcript, timestamps
    except FileNotFoundError:
        return None, None

async def run_content_analysis():
    """Run the content analysis pipeline"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return None
    
    extractor = VideoContentExtractor(api_key)
    
    transcript, timestamps = load_transcript_data()
    if not transcript or not timestamps:
        st.error("Transcript data not found. Please process a video first.")
        return None
    
    try:
        result = await extractor.process(transcript, timestamps, save_to_file=True)
        return result
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="YouTube Video Analysis",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 YouTube Video Analysis Tool")
    st.markdown("Download YouTube videos and generate intelligent content analysis with timestamps")
    
    # Initialize session state
    init_session_state()
    
    # Ensure output directories exist
    OutputPaths.ensure_dirs()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Check for OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            st.success("✅ OpenAI API key found")
        else:
            st.error("❌ OpenAI API key not found")
            st.info("Set OPENAI_API_KEY environment variable")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Step 1: Download & Process Video")
        
        # YouTube URL input
        youtube_url = st.text_input(
            "Enter YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        # Download and process button
        if st.button("📥 Download and Process Video", type="primary", use_container_width=True):
            if not youtube_url.strip():
                st.error("Please enter a YouTube URL")
            else:
                with st.spinner("Processing video... This may take a few minutes."):
                    try:
                        # Run the data pipeline
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("Downloading video...")
                        progress_bar.progress(25)
                        
                        transcript_text, word_timestamps = run_pipeline(youtube_url)
                        
                        progress_bar.progress(100)
                        status_text.text("Processing completed!")
                        
                        # Update session state
                        st.session_state.video_processed = True
                        st.session_state.transcript_text = transcript_text
                        st.session_state.word_timestamps = word_timestamps
                        
                        st.success("✅ Video processed successfully!")
                        st.info(f"📊 Transcribed {len(word_timestamps)} words")
                        
                    except Exception as e:
                        st.error(f"❌ Processing failed: {str(e)}")
        
        # Display video if processed
        if st.session_state.video_processed:
            st.subheader("Downloaded Video")
            if display_video():
                st.info("✅ Video ready for analysis")
            else:
                st.warning("Video file not found")
        
        # Display transcript preview
        if st.session_state.transcript_text:
            with st.expander("📝 Transcript Preview"):
                st.text_area(
                    "First 500 characters:",
                    st.session_state.transcript_text[:500] + ("..." if len(st.session_state.transcript_text) > 500 else ""),
                    height=150,
                    disabled=True
                )
    
    with col2:
        st.header("Step 2: Analyze Content")
        
        # Analysis button
        analyze_disabled = not st.session_state.video_processed
        
        if st.button(
            "🧠 Analyze Video Content", 
            type="primary", 
            use_container_width=True,
            disabled=analyze_disabled
        ):
            if not os.getenv('OPENAI_API_KEY'):
                st.error("OpenAI API key required for analysis")
            else:
                with st.spinner("Analyzing content... This may take a minute."):
                    try:
                        # Run content analysis
                        result = asyncio.run(run_content_analysis())
                        
                        if result:
                            st.session_state.analysis_completed = True
                            st.success("✅ Analysis completed!")
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
        
        if analyze_disabled:
            st.info("👆 Process a video first to enable analysis")
        
        # Display markdown result
        if st.session_state.analysis_completed:
            st.subheader("📄 Analysis Result")
            
            # Load and display markdown content
            try:
                with open(MARKDOWN_OUTPUT, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                # Display markdown
                st.markdown(markdown_content)
                
                # Download button for markdown
                st.download_button(
                    label="💾 Download Analysis",
                    data=markdown_content,
                    file_name="video_analysis.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            except FileNotFoundError:
                st.error("Analysis file not found")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with Streamlit • Powered by OpenAI • "
        "[GitHub Repository](https://github.com/your-repo)"
    )

if __name__ == "__main__":
    main()
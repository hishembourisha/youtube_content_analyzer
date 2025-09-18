# YouTube Video Analysis Tool

A streamlit based application that downloads YouTube videos, extracts audio, transcribes content using OpenAI's Whisper, and generates intelligent content analysis with precise timestamps.

## Features

- **YouTube Video Download**: Download videos in high quality using yt-dlp
- **Audio Extraction**: Convert video to audio using FFmpeg
- **AI Transcription**: Generate accurate transcripts with word-level timestamps using OpenAI Whisper
- **Intelligent Analysis**: Segment content into logical sections with AI-powered analysis
- **Timestamp Mapping**: Precise timestamp mapping for each content section
- **Interactive UI**: Clean Streamlit interface for easy video processing
- **Export Options**: Generate markdown reports with structured analysis

## Prerequisites (Windows)

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **UV** (modern Python package manager)
- **FFmpeg** (for audio extraction)
- **OpenAI API Key** (for transcription and analysis)

### Installing UV

UV is a fast Python package manager that replaces pip and virtualenv.

1. **Install UV using PowerShell**:
```powershell
# Using PowerShell (recommended)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. **Restart your PowerShell/Command Prompt** after installation

3. **Verify installation**:
```powershell
uv --version
```

### Installing FFmpeg

#### Option 1: Using Chocolatey (Recommended)
```powershell
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg
```

#### Option 2: Manual Installation
1. Download from [FFmpeg official website](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH environment variable:
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Click "Environment Variables"
   - Under "System Variables", find and select "Path", click "Edit"
   - Click "New" and add `C:\ffmpeg\bin`
   - Click "OK" on all dialogs

4. **Verify installation**:
```powershell
ffmpeg -version
```

## Installation

1. **Clone the repository**
```powershell
git clone https://github.com/hishembourisha/youtube_content_analyzer.git
cd youtube_content_analyzer
```

2. **Install dependencies using UV**
```powershell
# This creates a virtual environment and installs all dependencies
uv sync
```

3. **Set up environment variables**
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Project Structure

```
youtube-content-analyzer/
├── src/
│   ├── data_pipeline/
│   │   ├── __init__.py
│   │   ├── data_pipeline.py      # Main pipeline orchestration
│   │   ├── downloader.py         # YouTube video downloader
│   │   ├── video_to_audio.py     # Audio extraction
│   │   └── transcribe_audio.py   # AI transcription
│   ├── processing_agent/
│   │   ├── __init__.py
│   │   ├── content_extractor.py  # Main content processing
│   │   ├── analyse_agent.py      # AI content analysis
│   │   └── timestamp_mapper.py   # Timestamp mapping
│   ├── utils/
│   │   ├── __init__.py
│   │   └── path_utils.py         # File path management
│   ├── outputs/                  # Generated files directory
│   │   ├── video/               # Downloaded videos
│   │   ├── audio/               # Extracted audio files
│   │   ├── transcripts/         # Transcription results
│   │   └── markdown/            # Analysis reports
│   └── app.py                   # Streamlit web interface
├── .env
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml               # Project dependencies and config
└── uv.lock                      # Locked dependency versions
```

## Usage

### Option 1: Web Interface (Recommended)

1. **Start the Streamlit app**
```powershell
uv run streamlit run src/app.py
```

2. **Open your browser** to `http://localhost:8501`

3. **Process a video**:
   - Enter a YouTube URL
   - Click "Download and Process Video"
   - Wait for transcription to complete
   - Click "Analyze Video Content" for AI analysis

### Option 2: Command Line Interface

#### Basic Pipeline
```powershell
uv run python src/data_pipeline/data_pipeline.py
# Enter YouTube URL when prompted
```

#### Content Analysis
```powershell
uv run python src/processing_agent/content_extractor.py
```

#### Individual Components
```powershell
# Download only
uv run python src/data_pipeline/downloader.py

# Extract audio only
uv run python src/data_pipeline/video_to_audio.py

# Transcribe only
uv run python src/data_pipeline/transcribe_audio.py
```

## Dependencies Management with UV

### Adding New Dependencies
```powershell
# Add a new package
uv add package-name

# Add a development dependency
uv add --dev package-name

# Add a specific version
uv add "package-name==1.0.0"
```

### Updating Dependencies
```powershell
# Update all dependencies
uv sync --upgrade

# Update a specific package
uv add "package-name@latest"
```

### Running Commands
```powershell
# Run any command in the virtual environment
uv run python script.py
uv run streamlit run app.py
```

## API Keys Setup

### OpenAI API Key

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file:
```env
OPENAI_API_KEY=sk-your-key-here
```

**Note**: You'll need credits in your OpenAI account for transcription and analysis.

## How It Works

### 1. Video Download
- Uses `yt-dlp` to download YouTube videos in MP4 format
- Validates YouTube URLs before processing
- Saves videos to `outputs/video/` directory

### 2. Audio Extraction
- Converts MP4 to MP3 using FFmpeg
- Optimizes audio quality for transcription
- Outputs to `outputs/audio/` directory

### 3. AI Transcription
- Uses OpenAI's Whisper model for accurate transcription
- Generates both complete text and word-level timestamps
- Saves results to `outputs/transcripts/`

### 4. Content Analysis
- AI-powered content segmentation using GPT-4
- Identifies logical sections and themes
- Maps content sections to precise timestamps
- Generates structured markdown reports

## Web Interface Guide

### Main Dashboard
- **Left Column**: Video processing workflow
- **Right Column**: Content analysis and results
- **Sidebar**: Configuration and API status

### Processing Steps
1. **Enter YouTube URL**: Paste any valid YouTube video URL
2. **Download & Process**: Automatically handles download → audio extraction → transcription
3. **Analyze Content**: AI-powered analysis creates structured sections with timestamps
4. **Export Results**: Download markdown report with complete analysis

## Output Files

### Generated Files
- `outputs/video/downloaded_video.mp4` - Original downloaded video
- `outputs/audio/audio.mp3` - Extracted audio file
- `outputs/transcripts/complete_text.txt` - Full transcription text
- `outputs/transcripts/word_timestamps.json` - Word-level timestamp data
- `outputs/markdown/content_analysis.md` - AI-generated analysis report

### Sample Output Format
```markdown
# Video Title

Brief summary of the video content.

## Section 1: Introduction
[00:00:00] -> [00:02:30]

Key points from the introduction section...

## Section 2: Main Content
[00:02:30] -> [00:15:45]

Description of the main content discussed...
```

## Troubleshooting (Windows)

### Common Issues

**UV not found**
```powershell
# Restart PowerShell after installation
# Or manually add UV to PATH
```

**FFmpeg not found**
```powershell
# Verify FFmpeg installation
ffmpeg -version

# If not found, check PATH environment variable
echo $env:PATH
```

**OpenAI API errors**
- Check your API key in `.env` file
- Verify you have sufficient credits
- Ensure internet connection

**YouTube download fails**
- Check if URL is valid and public
- Some videos may be region-restricted
- Update yt-dlp: `uv add "yt-dlp@latest"`

**PowerShell execution policy issues**
```powershell
# If you get execution policy errors
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Debug Mode
Enable verbose logging by modifying the pipeline:
```python
# In data_pipeline.py, set quiet=False
ydl_opts = {
    'quiet': False  # Enable verbose output
}
```

## Advanced Configuration

### Custom Output Paths
Modify `utils/path_utils.py` to change default directories:
```python
# Custom base directory
BASE = r"C:\your\custom\path\outputs"
```

### Transcription Settings
Adjust transcription parameters in `transcribe_audio.py`:
```python
# Custom Whisper settings
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="en",  # Force specific language
    temperature=0.2  # Adjust creativity
)
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test with: `uv sync`
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for Whisper and GPT models
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube downloading
- [Streamlit](https://streamlit.io/) for the web interface
- [FFmpeg](https://ffmpeg.org/) for audio processing
- [Astral](https://astral.sh/) for UV package manager

## Support

- Create an [Issue](https://github.com/hishembourisha/youtube_content_analyzer/issues) for bugs
- Check [Discussions](https://github.com/hishembourisha/youtube_content_analyzer/discussions) for questions

---

**Made with ❤️ by Hichem**
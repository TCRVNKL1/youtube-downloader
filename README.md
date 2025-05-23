# 🎥 YouTube Video Downloader with Advanced Video Cutter

A modern, feature-rich web app for downloading and cutting YouTube videos with high precision. Built with Flask and powered by yt-dlp for reliable video extraction.

![YouTube Downloader](https://img.shields.io/badge/YouTube-Downloader-red?style=for-the-badge&logo=youtube)
![Flask](https://img.shields.io/badge/Flask-Web%20App-green?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)

## ✨ Key Features

### 🎬 Video Download
- **Multiple Formats Support**: Download videos in different qualities (4K, 1080p, 720p, 480p, 360p)
- **Audio Extraction**: Extract audio in MP3, M4A and more formats
- **Playlist Support**: Download entire playlists or channels
- **Smart Verification of URLs**: Support for all YouTube URL formats including:
- Regular videos (`youtube.com/watch?v=...`)
- Short links (`youtu.be/...`)
- Playlists (`youtube.com/playlist?list=...`)
- Channels (`youtube.com/@channel`, `youtube.com/c/channel`)
- Short videos (`youtube.com/shorts/...`)

### ✂️ Interactive video cutter
- **Precise timeline control**: Interactive timeline with drag handles
- **1-second accuracy**: Precise selection of start and end time
- **Presets**: One-click options for common durations (30 seconds, 1 minute, 3 minutes, 5 minutes)
- **Real-time preview**: Live preview of selected clips
- **Multiple output formats**: Export videos Cut to MP4, WebM, or MP3 audio only
- **Visual Timeline Interface**: Beautiful, responsive timeline with visual feedback

### 🎨 Modern Design
- **Responsive Interface**: Mobile-first design that works on all devices
- **Interactive Elements**: Smooth animations and hover effects
- **Clean Interface**: Modern gradient backgrounds and card-based layout
- **Accessibility**: Screen reader-friendly with appropriate ARIA labels
- **Dark/Light Mode Support**: Adaptive color schemes

### 🔧 Technical Features
- **Advanced Error Handling**: Comprehensive error messages and recovery
- **Smart User Agent Rotation**: 50+ trusted user agents for better reliability
- **Progress Tracking**: Real-time download progress indicators
- **Session Management**: Secure session handling for user data
- **File Cleanup**: Automatic temporary file management

## 🚀 Quick Start

### Prerequisites

Make sure the following are installed on your system:

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **FFmpeg** (for video processing and cutting)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg**

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**On macOS:**
```bash
brew install ffmpeg
```

**On Windows:**
- Download from [FFmpeg website] official](https://ffmpeg.org/download.html)
- Add to system PATH

4. **Run the app**
```bash
python main.py
```

5. **Access the app**
Open a browser and navigate to `http://localhost:5000`

## 📦 Dependencies

## 🏗️ Project Structure

```
youtube-downloader/
├── 📁 static/
│ ├── 📁 css/
│ │ └── style.css # Main stylesheet with modern design
│ ├── 📁 js/
│ │ ├── script.js # Main JavaScript functionality
│ └── 📁 images/
├── 📁 templates/
│ ├── layout.html # Master template with navigation
│ ├── index.html # Main download page
│ ├── download.html # Download options page
│ └── trim.html # Video cutter interface
├── 📁 temp_downloads/ # Temporary download storage
├── app.py # Flask app configuration
├── routes.py # URL routes and handlers
├── utils.py # Video processing and utility functions
├── main.py # Application entry point
├── requirements.txt # Python dependencies
└── README.md # This documentation
```

## 🎯 User Guide

### Basic video download

1. **Insert URL**: Paste any YouTube video URL into the input field
2. **Select Quality**: Select your preferred video quality and format
3. **Download**: Click the download button and wait for processing
4. **Save**: The file will automatically download to your device

### Advanced features

#### Playlist downloads
- Paste a playlist URL to see all videos
- Select individual videos or download all
- Choose different qualities for each video

#### Cropping Video
1. **Navigate to Cutter**: Click "Video Cutter" in the navigation
2. **Load Video**: Insert YouTube video URL
3. **Set Timeline**: Use the interactive timeline to select start/end points
4. **Precise Timing**: Enter precise times in the min:sec fields
5. **Presets**: Use preset buttons for common durations
6. **Export**: Choose a format and download your trimmed video

#### Advanced Options
- **Custom Format Codes**: Use the yt-dlp format selectors
- **Audio Rate Control**: Specify audio quality
- **Subtitle Downloads**: Include subtitle files
- **Extract Thumbnails**: Download video thumbnails

Made with ❤️ for the open source community. Give this repository a ⭐ if you find it useful!

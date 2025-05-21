import re
import logging
from urllib.parse import urlparse, parse_qs
import yt_dlp

logger = logging.getLogger(__name__)

def validate_youtube_url(url):
    """
    Validate if the URL is a valid YouTube URL
    """
    if not url:
        return False
        
    # Check for common YouTube URL patterns
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    youtube_match = re.match(youtube_regex, url)
    return youtube_match is not None

def get_video_id(url):
    """
    Extract the video ID from a YouTube URL
    """
    if not url:
        return None
        
    parsed_url = urlparse(url)
    
    if parsed_url.hostname in ('youtu.be', 'www.youtu.be'):
        return parsed_url.path[1:]
    if parsed_url.hostname in ('youtube.com', 'www.youtube.com'):
        if parsed_url.path == '/watch':
            query = parse_qs(parsed_url.query)
            return query.get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    
    # If we get here, it's not a valid YouTube URL
    return None

def format_size(size_bytes):
    """
    Format size in bytes to a human-readable format
    """
    if size_bytes == 0:
        return "0B"
    
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.2f} {size_name[i]}"

def get_video_info(url):
    """
    Get information about a YouTube video using yt-dlp
    """
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'extract_flat': 'in_playlist',  # Extract playlist info without downloading each video
            'noplaylist': False,  # Allow playlists
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if not info:
                raise ValueError("Could not retrieve video information")
            
            # Check if this is a playlist
            is_playlist = 'entries' in info and info.get('entries') and len(info.get('entries', [])) > 0
            
            if is_playlist:
                # Create a playlist info object
                playlist_info = {
                    'id': info.get('id', ''),
                    'title': info.get('title', 'Playlist'),
                    'uploader': info.get('uploader', 'Unknown uploader'),
                    'thumbnail': info.get('thumbnail', ''),
                    'is_playlist': True,
                    'entries': []
                }
                
                # Process each video in the playlist
                entries = info.get('entries', [])
                if entries:
                    for entry in entries:
                        if not entry:
                            continue
                            
                        # Skip unavailable videos
                        entry_id = entry.get('id')
                        if not entry_id:
                            continue
                            
                        # Only extract basic info for playlist entries to avoid API limits
                        entry_info = {
                            'id': entry_id,
                            'title': entry.get('title', 'Untitled Video'),
                            'thumbnail': entry.get('thumbnail', ''),
                            'duration': entry.get('duration', 0),
                            'duration_string': format_duration(entry.get('duration', 0)),
                            'url': f"https://www.youtube.com/watch?v={entry_id}"
                        }
                        
                        playlist_info['entries'].append(entry_info)
                
                return playlist_info
            else:
                # Process formats to make them more user-friendly
                video_formats = []
                audio_formats = []
                
                formats = info.get('formats', [])
                if formats:
                    for fmt in formats:
                        if not fmt:
                            continue
                            
                        # Skip formats with no audio and no video
                        vcodec = fmt.get('vcodec', '')
                        acodec = fmt.get('acodec', '')
                        if vcodec == 'none' and acodec == 'none':
                            continue
                        
                        # Get file size or default to 0
                        filesize = fmt.get('filesize', 0)
                        
                        # Create basic format info
                        format_info = {
                            'format_id': fmt.get('format_id', ''),
                            'ext': fmt.get('ext', 'unknown'),
                            'resolution': fmt.get('resolution', 'unknown'),
                            'format_note': fmt.get('format_note', ''),
                            'filesize': format_size(filesize) if filesize else 'Unknown size',
                            'vcodec': vcodec,
                            'acodec': acodec,
                        }
                        
                        # Create a readable description
                        format_parts = []
                        resolution = fmt.get('resolution', '')
                        if resolution and resolution != 'audio only':
                            format_parts.append(resolution)
                        
                        fps = fmt.get('fps')
                        if fps:
                            format_parts.append(f"{fps}fps")
                            
                        format_note = fmt.get('format_note', '')
                        if format_note:
                            format_parts.append(format_note)
                            
                        ext = fmt.get('ext', '')
                        if ext:
                            format_parts.append(f".{ext}")
                        
                        format_info['description'] = " - ".join(format_parts)
                        
                        # Separate video and audio formats
                        if vcodec != 'none':
                            video_formats.append(format_info)
                        else:
                            audio_formats.append(format_info)
                
                # Sort video formats by resolution quality (higher first)
                def get_resolution_key(x):
                    resolution = x.get('resolution', '')
                    if resolution == 'unknown':
                        return 0
                    if 'x' in resolution:
                        try:
                            return -int(resolution.split('x')[1])
                        except (ValueError, IndexError):
                            return 0
                    return 0
                
                video_formats.sort(key=get_resolution_key)
                
                # Sort audio formats by quality (higher first if possible)
                def get_audio_quality_key(x):
                    format_note = x.get('format_note', '')
                    if format_note and 'k' in format_note:
                        try:
                            return -int(format_note.split('k')[0])
                        except (ValueError, IndexError):
                            return 0
                    return 0
                
                audio_formats.sort(key=get_audio_quality_key)
                
                # Get video ID for embed URL
                video_id = info.get('id', '')
                
                # Create a clean video info object
                video_info = {
                    'id': video_id,
                    'title': info.get('title', 'Untitled Video'),
                    'channel': info.get('channel', 'Unknown channel'),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'duration_string': format_duration(info.get('duration', 0)),
                    'view_count': info.get('view_count', 0),
                    'is_playlist': False,
                    'embed_url': f"https://www.youtube.com/embed/{video_id}" if video_id else '',
                    'video_formats': video_formats,
                    'audio_formats': audio_formats
                }
                
                return video_info
            
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        raise

def format_duration(seconds):
    """Format duration in seconds to HH:MM:SS"""
    if not seconds:
        return "00:00"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes):02d}:{int(seconds):02d}"

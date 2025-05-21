import os
import re
import json
import urllib.parse
import logging
import tempfile
import uuid
import shutil
from flask import render_template, request, jsonify, session, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
import yt_dlp

from app import app
from utils import validate_youtube_url, get_video_info, format_size

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate-url', methods=['POST', 'GET'])
def validate_url():
    # Handle both GET and POST requests
    if request.method == 'POST':
        url = request.form.get('youtube_url', '')
    else:
        url = request.args.get('youtube_url', '')
        
    if not url:
        if request.method == 'GET':
            flash('Please enter a YouTube URL', 'warning')
            return redirect(url_for('index'))
        else:
            return jsonify({
                'valid': False,
                'message': 'Please enter a YouTube URL'
            })
    
    if not validate_youtube_url(url):
        if request.method == 'GET':
            flash('Please enter a valid YouTube URL', 'warning')
            return redirect(url_for('index'))
        else:
            return jsonify({
                'valid': False,
                'message': 'Please enter a valid YouTube URL'
            })
    
    try:
        video_info = get_video_info(url)
        session['video_info'] = video_info
        session['youtube_url'] = url
        
        # For GET requests, redirect to download options page directly
        if request.method == 'GET':
            return redirect(url_for('download_options'))
        
        # For POST requests, return JSON response
        return jsonify({
            'valid': True,
            'video_info': video_info
        })
    except Exception as e:
        error_message = f'Error fetching video information: {str(e)}'
        logger.error(error_message)
        
        if request.method == 'GET':
            flash(error_message, 'danger')
            return redirect(url_for('index'))
        else:
            return jsonify({
                'valid': False,
                'message': error_message
            })

@app.route('/download-options', methods=['GET'])
def download_options():
    video_info = session.get('video_info')
    youtube_url = session.get('youtube_url')
    
    if not video_info or not youtube_url:
        flash('Please enter a YouTube URL first')
        return redirect(url_for('index'))
    
    return render_template('download.html', video_info=video_info, youtube_url=youtube_url)

@app.route('/process-download', methods=['POST'])
def process_download():
    url = session.get('youtube_url')
    if not url:
        return jsonify({
            'success': False,
            'message': 'No valid YouTube URL in session'
        })
    
    # Get download options
    format_id = request.form.get('format', 'best')
    advanced_options = request.form.get('advanced_options', '')
    
    # Create a temporary download ID for this download
    download_id = str(uuid.uuid4())
    download_folder = os.path.join(app.config['TEMP_DOWNLOAD_FOLDER'], download_id)
    os.makedirs(download_folder, exist_ok=True)
    
    try:
        # Build yt-dlp options
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'noplaylist': True,  # We handle playlists separately through UI
            'ignoreerrors': True, # Continue through errors
        }
        
        # Check if this is an audio-only format (based on format_id naming convention)
        video_info = session.get('video_info', {})
        is_audio_format = False
        
        if video_info:
            # If it's a video format
            audio_formats = video_info.get('audio_formats', [])
            for fmt in audio_formats:
                if fmt.get('format_id') == format_id:
                    is_audio_format = True
                    # Automatically add audio extraction for audio formats
                    ydl_opts['extract_audio'] = True
                    # Use format from the format_id
                    ext = fmt.get('ext', 'mp3')
                    ydl_opts['audio_format'] = ext
                    break
        
        # Add advanced options if provided
        if advanced_options:
            # Parse advanced options safely (basic implementation)
            # Remove any potentially harmful options
            adv_opts = advanced_options.split()
            for opt in adv_opts:
                if not opt.startswith('--'):
                    continue
                    
                # Skip dangerous options
                if any(bad_opt in opt for bad_opt in ['exec', 'output', 'load-config']):
                    continue
                    
                parts = opt[2:].split('=', 1)
                if len(parts) == 2:
                    key, value = parts
                    # Convert to appropriate types
                    if value.lower() in ('true', 'yes'):
                        value = True
                    elif value.lower() in ('false', 'no'):
                        value = False
                    elif value.isdigit():
                        value = int(value)
                    ydl_opts[key] = value
        
        logger.debug(f"Download options: {ydl_opts}")
        
        # Start download with yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if info is None:
                raise Exception("Could not download the video.")
            
            # Get downloaded file path
            if info is not None and isinstance(info, dict):
                entries = info.get('entries', [])
                if entries and len(entries) > 0 and entries[0] is not None:
                    # This is a playlist, take the first valid entry
                    info = entries[0]
            
            # Find the downloaded file
            downloaded_files = os.listdir(download_folder)
            if not downloaded_files:
                raise Exception("No files were downloaded")
            
            download_path = os.path.join(download_folder, downloaded_files[0])
            filename = os.path.basename(download_path)
            
            # Store in session for download
            session['download_path'] = download_path
            session['download_filename'] = filename
            
            return jsonify({
                'success': True,
                'download_id': download_id,
                'filename': filename,
                'is_audio': is_audio_format
            })
            
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        # Clean up the temporary folder
        shutil.rmtree(download_folder, ignore_errors=True)
        
        return jsonify({
            'success': False,
            'message': f'Error during download: {str(e)}'
        })

@app.route('/download-file/<download_id>', methods=['GET'])
def download_file(download_id):
    download_path = session.get('download_path')
    filename = session.get('download_filename')
    
    if not download_path or not os.path.exists(download_path):
        flash('Download file not found or expired')
        return redirect(url_for('index'))
    
    try:
        response = send_file(
            download_path,
            as_attachment=True,
            download_name=filename
        )
        
        # Set a callback to delete the file after it's sent
        @response.call_on_close
        def delete_after_download():
            try:
                if os.path.exists(download_path):
                    os.remove(download_path)
                    logger.info(f"Deleted file after download: {download_path}")
                
                # Remove the empty folder if it exists
                download_folder = os.path.dirname(download_path)
                if os.path.exists(download_folder) and not os.listdir(download_folder):
                    os.rmdir(download_folder)
                    logger.info(f"Removed empty download folder: {download_folder}")
            except Exception as cleanup_error:
                logger.error(f"Error cleaning up after download: {str(cleanup_error)}")
        
        return response
    except Exception as e:
        logger.error(f"Error sending file: {str(e)}")
        flash(f"Error downloading file: {str(e)}")
        return redirect(url_for('index'))

@app.route('/watch-ad', methods=['POST'])
def watch_ad():
    # In a real implementation, this would validate an ad was shown
    # using a proper ad network API response
    return jsonify({
        'success': True,
        'message': 'Ad viewed successfully'
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="404 - Page Not Found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="500 - Internal Server Error"), 500

document.addEventListener('DOMContentLoaded', function() {
    // Constants
    const URL_FORM = document.getElementById('youtube-url-form');
    const URL_INPUT = document.getElementById('youtube-url');
    const URL_SUBMIT = document.getElementById('validate-url-btn');
    const VIDEO_INFO_CONTAINER = document.getElementById('video-info-container');
    const DOWNLOAD_BTN = document.getElementById('download-btn');
    const LOADING_INDICATOR = document.getElementById('loading-indicator');
    const ADVANCED_TOGGLE = document.getElementById('advanced-toggle');
    const ADVANCED_OPTIONS = document.getElementById('advanced-options-form');
    
    // Handle URL form submission
    if (URL_FORM) {
        URL_FORM.addEventListener('submit', function(e) {
            e.preventDefault();
            validateYoutubeUrl();
        });
    }
    
    // Toggle advanced options
    if (ADVANCED_TOGGLE) {
        ADVANCED_TOGGLE.addEventListener('click', function() {
            if (ADVANCED_OPTIONS.style.display === 'none' || !ADVANCED_OPTIONS.style.display) {
                ADVANCED_OPTIONS.style.display = 'block';
                ADVANCED_TOGGLE.textContent = 'Hide Advanced Options';
            } else {
                ADVANCED_OPTIONS.style.display = 'none';
                ADVANCED_TOGGLE.textContent = 'Show Advanced Options';
            }
        });
    }
    
    // Handle format selection
    document.addEventListener('click', function(e) {
        if (e.target.closest('.format-option')) {
            const formatOption = e.target.closest('.format-option');
            const formatId = formatOption.dataset.formatId;
            const formatSelect = document.getElementById('format-select');
            
            // Remove selected class from all options
            document.querySelectorAll('.format-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            
            // Add selected class to clicked option
            formatOption.classList.add('selected');
            
            // Update hidden select value
            if (formatSelect) {
                formatSelect.value = formatId;
            }
        }
    });
    
    // Handle download button click
    if (DOWNLOAD_BTN) {
        DOWNLOAD_BTN.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show ad before download
            showAd(function() {
                // After ad is closed, start download
                processDownload();
            });
        });
    }
    
    // Function to validate YouTube URL
    function validateYoutubeUrl() {
        const url = URL_INPUT.value.trim();
        
        if (!url) {
            showToast('Error', 'Please enter a YouTube URL', 'error');
            return;
        }
        
        // Show loading indicator
        if (LOADING_INDICATOR) {
            LOADING_INDICATOR.style.display = 'block';
        }
        
        // Disable submit button
        if (URL_SUBMIT) {
            URL_SUBMIT.disabled = true;
            URL_SUBMIT.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Validating...';
        }
        
        // Create form data
        const formData = new FormData();
        formData.append('youtube_url', url);
        
        // Make AJAX request to validate URL
        fetch('/validate-url', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                // If response is not JSON (e.g., HTML), follow redirects
                window.location.href = '/download-options';
                return { valid: true }; // Return something to avoid errors
            }
        })
        .then(data => {
            if (data.valid) {
                // Redirect to download options page
                window.location.href = '/download-options';
            } else {
                showToast('Error', data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error', 'An error occurred while validating the URL', 'error');
        })
        .finally(() => {
            // Hide loading indicator
            if (LOADING_INDICATOR) {
                LOADING_INDICATOR.style.display = 'none';
            }
            
            // Re-enable submit button
            if (URL_SUBMIT) {
                URL_SUBMIT.disabled = false;
                URL_SUBMIT.textContent = 'Get Video';
            }
        });
    }
    
    // Function to process download
    function processDownload() {
        const formatSelect = document.getElementById('format-select');
        const advancedOptions = document.getElementById('advanced-options');
        const downloadForm = document.getElementById('download-form');
        const downloadContainer = document.getElementById('download-container');
        const progressContainer = document.getElementById('progress-container');
        const downloadProgress = document.getElementById('download-progress');
        
        if (!formatSelect || !downloadForm) {
            showToast('Error', 'Form elements not found', 'error');
            return;
        }
        
        // Show progress container
        if (progressContainer) {
            progressContainer.style.display = 'block';
        }
        
        // Disable download button
        if (DOWNLOAD_BTN) {
            DOWNLOAD_BTN.disabled = true;
            DOWNLOAD_BTN.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
        }
        
        // Create form data
        const formData = new FormData();
        formData.append('format', formatSelect.value);
        
        if (advancedOptions && advancedOptions.value) {
            formData.append('advanced_options', advancedOptions.value);
        }
        
        // Make AJAX request to process download
        fetch('/process-download', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                showToast('Error', 'Server returned an invalid response', 'error');
                throw new Error('Invalid server response');
            }
        })
        .then(data => {
            if (data.success) {
                // Show success message
                showToast('Success', 'File processed successfully!', 'success');
                
                // Determine media type for button text
                const mediaType = data.is_audio ? 'Audio' : 'Video';
                
                // Create download link
                if (downloadContainer) {
                    downloadContainer.innerHTML = `
                        <div class="alert alert-success">
                            <h4>Download Ready!</h4>
                            <p>Your ${mediaType.toLowerCase()} has been processed successfully.</p>
                            <a href="/download-file/${data.download_id}" class="btn btn-success" id="final-download-btn">
                                <i class="fas fa-download"></i> Download ${mediaType} Now
                            </a>
                        </div>
                    `;
                    
                    // Add event listener to track when download is complete
                    const finalDownloadBtn = document.getElementById('final-download-btn');
                    if (finalDownloadBtn) {
                        finalDownloadBtn.addEventListener('click', function() {
                            // After a short delay, inform the user that the file will be deleted from server
                            setTimeout(() => {
                                showToast('Info', 'File will be automatically deleted from our server after download', 'info');
                            }, 2000);
                        });
                    }
                }
            } else {
                showToast('Error', data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error', 'An error occurred while processing the download', 'error');
        })
        .finally(() => {
            // Hide progress
            if (progressContainer) {
                progressContainer.style.display = 'none';
            }
            
            // Re-enable download button
            if (DOWNLOAD_BTN) {
                DOWNLOAD_BTN.disabled = false;
                DOWNLOAD_BTN.innerHTML = '<i class="fas fa-download"></i> Download';
            }
        });
    }
    
    // Function to show toast notification
    function showToast(title, message, type = 'info') {
        const toastContainer = document.getElementById('toast-container');
        
        if (!toastContainer) {
            // Create toast container if it doesn't exist
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.id = toastId;
        
        toast.innerHTML = `
            <div class="toast-header">
                <strong>${title}</strong>
                <button type="button" class="btn-close" onclick="document.getElementById('${toastId}').remove()"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        document.getElementById('toast-container').appendChild(toast);
        
        // Show toast
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 5000);
    }
});

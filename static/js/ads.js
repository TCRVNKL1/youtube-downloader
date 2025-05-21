// Ad management functions

// Function to show ad
function showAd(callback) {
    // Create ad container
    const adContainer = document.createElement('div');
    adContainer.id = 'adContainer';
    
    // Add ad content
    adContainer.innerHTML = `
        <div class="ad-content">
            <div class="ad-close" id="adClose">×</div>
            <div class="ad-title">Advertisement</div>
            <div class="ad-body">
                <p>This ad supports our free service.</p>
                <p>Please wait while we prepare your download.</p>
                <div class="ad-timer" id="adTimer">5</div>
                
                <!-- Placeholder for actual ad (in a real implementation, this would be replaced with actual ad code) -->
                <div class="card mb-3">
                    <div class="card-body text-center">
                        <h5>Premium YouTube Downloader</h5>
                        <p>Get our premium version with no ads and unlimited downloads!</p>
                        <button class="btn btn-primary" onclick="premiumPromo()">Learn More</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add to DOM
    document.body.appendChild(adContainer);
    
    // Start timer
    let timeLeft = 5;
    const timerElement = document.getElementById('adTimer');
    
    const timer = setInterval(() => {
        timeLeft--;
        if (timerElement) {
            timerElement.textContent = timeLeft;
        }
        
        if (timeLeft <= 0) {
            clearInterval(timer);
            
            // Enable close button
            const closeButton = document.getElementById('adClose');
            if (closeButton) {
                closeButton.style.color = '#333';
                closeButton.style.cursor = 'pointer';
                closeButton.addEventListener('click', () => {
                    closeAd(callback);
                });
            }
            
            // Add close button at the bottom
            const adContent = document.querySelector('.ad-content');
            if (adContent) {
                const closeBtn = document.createElement('button');
                closeBtn.className = 'btn btn-primary';
                closeBtn.textContent = 'Continue to Download';
                closeBtn.addEventListener('click', () => {
                    closeAd(callback);
                });
                adContent.appendChild(closeBtn);
            }
        }
    }, 1000);
    
    // Notify server that ad was shown
    fetch('/watch-ad', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .catch(error => console.error('Error logging ad view:', error));
}

// Function to close ad
function closeAd(callback) {
    const adContainer = document.getElementById('adContainer');
    if (adContainer) {
        adContainer.style.opacity = '0';
        
        setTimeout(() => {
            adContainer.remove();
            if (typeof callback === 'function') {
                callback();
            }
        }, 300);
    }
}

// Premium promo click handler (placeholder)
function premiumPromo() {
    alert('This is a demo. In a real implementation, this would lead to a premium subscription page.');
}

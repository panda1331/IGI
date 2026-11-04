document.addEventListener('DOMContentLoaded', () => {
    const speakBtn = document.getElementById('speak-btn');
    const speechText = document.getElementById('speech-text');

    if (speakBtn && speechText) {
        speakBtn.addEventListener('click', () => {
            const text = speechText.value.trim();
            if (!text) {
                alert("Please enter some text to speak");
                return;
            }

            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();

                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-GB'; 
                utterance.rate = 1; 
                utterance.pitch = 1;

                speakBtn.textContent = "Speaking";
                speakBtn.disabled = true;

                utterance.onend = () => {
                    speakBtn.textContent = "Speak Text";
                    speakBtn.disabled = false;
                };

                window.speechSynthesis.speak(utterance);
            } else {
                alert("Sorry, your browser doesn't support Text-to-Speech.");
            }
        });
    }

    const geoBtn = document.getElementById('geo-btn');
    const geoOutput = document.getElementById('geo-output');

    if (geoBtn && geoOutput) {
        geoBtn.addEventListener('click', () => {
            if ('geolocation' in navigator) {
                geoOutput.innerHTML = "Requesting location... (Please allow access if prompted)";
                geoBtn.disabled = true;

                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const lat = position.coords.latitude.toFixed(4);
                        const lon = position.coords.longitude.toFixed(4);
                        const acc = position.coords.accuracy.toFixed(0);
                        
                        geoOutput.innerHTML = `
                            <strong>Latitude:</strong> ${lat}<br>
                            <strong>Longitude:</strong> ${lon}<br>
                            <strong>Accuracy:</strong> ${acc} meters
                        `;
                        geoBtn.disabled = false;
                        geoBtn.textContent = "Update Location";
                    },
                    (error) => {
                        let errorMsg = "Unknown error.";
                        if (error.code === 1) errorMsg = "Permission denied. Please allow location access.";
                        if (error.code === 2) errorMsg = "Position unavailable.";
                        if (error.code === 3) errorMsg = "Timeout.";
                        
                        geoOutput.innerHTML = `<span style="color: #e63946;">Error: ${errorMsg}</span>`;
                        geoBtn.disabled = false;
                    },
                    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
                );
            } else {
                geoOutput.innerHTML = "Geolocation is not supported by your browser.";
            }
        });
    }
});
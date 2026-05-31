// frontend/src/services/emotionWebcam.js
export class EmotionDetector {
    constructor() {
        this.emotions = {
            mouth_shape: 'neutral',
            eye_openness: 'normal'
        };
    }
    
    async detectFromWebcam(videoElement) {
        // Use face-api.js or tracking.js in browser
        // No backend ML required!
    }
}
# System dependencies

The current VoiceShield prototype has no required non-Python runtime binaries. It does **not** invoke FFmpeg, PortAudio, libsndfile, CUDA, cuDNN, database clients, or blockchain tooling.

## Browser and microphone access

The frontend uses the browser's Web Audio API and `getUserMedia()` to access a microphone. Use a current Chromium-based browser (Chrome or Microsoft Edge) and grant microphone permission. When serving the frontend from a web server rather than opening the file directly, browsers generally require HTTPS or `localhost` for microphone access.

- **Windows:** Install/update Chrome or Edge through their normal installers or Microsoft Store.
- **Linux:** Install a current Chrome, Chromium, or Firefox package from the distribution; permit microphone access in the browser and desktop privacy settings.
- **macOS:** Install/update Chrome, Edge, or Safari and allow microphone access in System Settings.

## Optional future components

FFmpeg/libsndfile may become necessary when the planned backend starts decoding audio files or streams. CUDA/cuDNN may become necessary when real PyTorch inference is added. They are not requirements of the present simulated implementation and must not be installed solely for it.

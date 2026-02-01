# AI Voice Detection API - Complete Documentation

## 📁 Project Structure

```
ai-voice-detection/
├── app.py                      # Main Flask application
├── app_advanced.py             # Advanced version with more features
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── Procfile                    # Heroku deployment config
├── runtime.txt                 # Python version specification
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
│
├── README.md                   # Main documentation
├── DEPLOYMENT_GUIDE.md         # Quick deployment guide
├── API_EXAMPLES.md             # API usage examples
├── PROJECT_DOCS.md             # This file
│
├── test_endpoint.py            # Single endpoint tester
├── test_suite.py               # Comprehensive test suite
├── batch_test.py               # Batch audio file tester
├── load_test.py                # Load/stress testing
├── monitor.py                  # API monitoring script
│
├── audio_to_base64.py          # Audio file converter
├── generate_test_audio.py      # Test audio generator
│
├── api_tester.html             # Advanced web interface
├── simple_tester.html          # Simple web interface
│
├── postman_collection.json     # Postman API collection
└── setup.sh                    # Setup automation script
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo>
cd ai-voice-detection
chmod +x setup.sh
./setup.sh
```

### 2. Run Locally
```bash
# Option A: Python directly
python3 app.py

# Option B: With virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Option C: Docker
docker-compose up
```

### 3. Test
```bash
# Generate test audio
python3 generate_test_audio.py

# Test the API
python3 test_endpoint.py test_sample.wav

# Or open in browser
open api_tester.html
```

## 📚 File Descriptions

### Core Application Files

#### `app.py`
- Main Flask application
- Core AI voice detection logic
- Audio feature extraction using librosa
- RESTful API endpoints
- Authentication via API key
- Error handling and validation

**Key Features:**
- MFCC (Mel-frequency cepstral coefficients) analysis
- Spectral feature extraction
- Zero-crossing rate analysis
- Chroma features
- Tempo detection

#### `app_advanced.py`
- Enhanced version of app.py
- More comprehensive feature extraction
- Better error handling
- Request logging and statistics
- Performance optimizations

**Additional Features:**
- 40+ audio features analyzed
- Harmonic and percussive separation
- Spectral contrast
- Tonnetz features
- Request tracking and analytics

### Testing Scripts

#### `test_endpoint.py`
Basic endpoint testing script.

**Usage:**
```bash
python3 test_endpoint.py <audio_file> [endpoint_url] [api_key]
```

**Example:**
```bash
python3 test_endpoint.py sample.mp3
python3 test_endpoint.py sample.mp3 https://api.example.com/detect my-key
```

#### `test_suite.py`
Comprehensive testing suite covering all scenarios.

**Tests:**
- Health check
- Authentication (valid/invalid)
- Missing data handling
- Different languages
- Various audio formats
- Error cases

**Usage:**
```bash
python3 test_suite.py <base_url> [api_key] [audio_file]
```

#### `batch_test.py`
Test multiple audio files at once.

**Usage:**
```bash
# Test directory
python3 batch_test.py http://localhost:5000/detect api-key ./audio_samples/

# Test specific files
python3 batch_test.py http://localhost:5000/detect api-key file1.mp3 file2.wav
```

**Outputs:**
- Console summary
- Detailed text report (`test_report.txt`)
- CSV results (`test_results.csv`)

#### `load_test.py`
Performance and stress testing.

**Modes:**
1. **Sequential**: Test requests one by one
2. **Concurrent**: Test with multiple threads
3. **Ramp**: Gradually increase load

**Usage:**
```bash
# Sequential
python3 load_test.py <url> <key> <audio> sequential 10

# Concurrent (100 requests, 10 threads)
python3 load_test.py <url> <key> <audio> concurrent 100 10

# Ramp (1 to 10 threads)
python3 load_test.py <url> <key> <audio> ramp 10
```

**Metrics:**
- Response time statistics
- Success/failure rates
- Requests per second
- Percentiles (P50, P90, P95, P99)

#### `monitor.py`
Continuous API monitoring and health checks.

**Features:**
- Periodic health checks
- Response time tracking
- Uptime monitoring
- Logging to file

**Usage:**
```bash
# Monitor every 60 seconds
python3 monitor.py http://localhost:5000

# Custom interval (30 seconds)
python3 monitor.py http://localhost:5000 api-key 30

# Monitor for specific duration (1 hour)
python3 monitor.py http://localhost:5000 api-key 60 3600
```

### Utility Scripts

#### `audio_to_base64.py`
Convert audio files to base64 format.

**Usage:**
```bash
python3 audio_to_base64.py sample.mp3
python3 audio_to_base64.py sample.mp3 output.txt
```

**Output:**
- Base64 text file
- Preview of encoded data
- Example API payload

#### `generate_test_audio.py`
Generate synthetic audio for testing.

**Features:**
- Creates WAV file with sine waves
- Configurable duration and frequency
- Outputs base64 encoded version

**Usage:**
```bash
python3 generate_test_audio.py
```

**Output:**
- `test_sample.wav` - Audio file
- `test_audio_base64.txt` - Base64 encoding

### Web Interfaces

#### `api_tester.html`
Advanced web interface with beautiful UI.

**Features:**
- Drag-and-drop file upload
- Real-time results
- Confidence visualization
- Detailed analysis display
- Error handling

**Usage:**
```bash
# Open in browser
open api_tester.html
# or
python3 -m http.server 8000
# Then visit: http://localhost:8000/api_tester.html
```

#### `simple_tester.html`
Minimal web interface for quick testing.

**Features:**
- Simple form
- Basic validation
- Clean results display

### Configuration Files

#### `.env.example`
Template for environment variables.

**Variables:**
- `API_KEY`: Authentication key
- `PORT`: Server port (default: 5000)
- `FLASK_ENV`: Environment (development/production)
- `FLASK_DEBUG`: Debug mode (True/False)

**Setup:**
```bash
cp .env.example .env
# Edit .env with your values
```

#### `requirements.txt`
Python package dependencies.

**Main Dependencies:**
- Flask: Web framework
- librosa: Audio analysis
- numpy: Numerical computing
- scikit-learn: Machine learning
- gunicorn: Production server

#### `Dockerfile`
Docker container configuration.

**Usage:**
```bash
docker build -t ai-voice-detection .
docker run -p 5000:5000 -e API_KEY=your-key ai-voice-detection
```

#### `docker-compose.yml`
Multi-container Docker configuration.

**Usage:**
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

#### `postman_collection.json`
Postman API testing collection.

**Import:**
1. Open Postman
2. File → Import
3. Select `postman_collection.json`
4. Set variables: `base_url` and `api_key`

### Deployment Files

#### `Procfile`
Heroku deployment configuration.

**Content:**
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

#### `runtime.txt`
Specifies Python version for cloud platforms.

#### `setup.sh`
Automated setup script.

**Features:**
- Environment setup
- Dependency installation
- Test generation
- Docker build
- Deployment guide

**Usage:**
```bash
chmod +x setup.sh
./setup.sh
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| API_KEY | Authentication key | hackathon-api-key-2024 |
| PORT | Server port | 5000 |
| FLASK_ENV | Environment | production |
| FLASK_DEBUG | Debug mode | False |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/detect` | POST | Voice detection |
| `/stats` | GET | Usage statistics |

## 📊 API Response Format

### Success Response (200)
```json
{
  "success": true,
  "request_id": "abc123",
  "result": {
    "is_ai_generated": false,
    "confidence": 0.7543,
    "prediction": "Human",
    "language": "en",
    "audio_format": "mp3",
    "audio_duration_seconds": 3.45,
    "sample_rate": 22050
  },
  "metadata": {
    "model_version": "2.0.0",
    "processing_time_seconds": 1.234,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Error Response (4xx/5xx)
```json
{
  "error": "Bad Request",
  "message": "audio_base64 field is required",
  "request_id": "xyz789"
}
```

## 🧪 Testing Workflow

### 1. Unit Testing
```bash
# Run comprehensive test suite
python3 test_suite.py http://localhost:5000 api-key sample.mp3
```

### 2. Integration Testing
```bash
# Test with multiple files
python3 batch_test.py http://localhost:5000/detect api-key ./test_files/
```

### 3. Load Testing
```bash
# Test performance under load
python3 load_test.py http://localhost:5000/detect api-key sample.mp3 concurrent 100 10
```

### 4. Monitoring
```bash
# Monitor API health
python3 monitor.py http://localhost:5000 api-key 30
```

## 🚀 Deployment Options

### 1. Render.com (Free Tier)
- Auto-deployment from Git
- Free HTTPS
- Easy scaling

### 2. Railway.app
- Simple Git integration
- Generous free tier
- Automatic HTTPS

### 3. Heroku
- Popular platform
- Easy CLI deployment
- Add-ons ecosystem

### 4. Google Cloud Run
- Serverless
- Pay per use
- Auto-scaling

### 5. Docker
- Run anywhere
- Consistent environments
- Easy replication

## 📈 Performance Optimization

### Tips:
1. Use caching for repeated audio files
2. Implement rate limiting
3. Use connection pooling
4. Enable gzip compression
5. Use CDN for static files

### Scaling:
- Horizontal: Multiple instances behind load balancer
- Vertical: Increase server resources
- Caching: Redis for frequent requests
- Queue: Celery for async processing

## 🔐 Security

### Best Practices:
1. Rotate API keys regularly
2. Use HTTPS in production
3. Implement rate limiting
4. Validate all inputs
5. Monitor for anomalies
6. Keep dependencies updated

### Rate Limiting:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.headers.get('x-api-key'))
@app.route('/detect', methods=['POST'])
@limiter.limit("100 per hour")
def detect():
    ...
```

## 📝 Troubleshooting

### Common Issues:

**Port Already in Use:**
```bash
lsof -ti:5000 | xargs kill -9
# or
PORT=8000 python3 app.py
```

**Dependencies Not Installing:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Audio Processing Errors:**
```bash
# Linux
sudo apt-get install libsndfile1 ffmpeg

# macOS
brew install libsndfile ffmpeg
```

**Docker Build Fails:**
```bash
docker-compose build --no-cache
```

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [librosa Documentation](https://librosa.org/doc/latest/)
- [API Best Practices](https://restfulapi.net/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - Free for hackathons and personal projects

---

**For questions or issues, create a GitHub issue or contact the maintainers.**

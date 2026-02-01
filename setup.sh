#!/bin/bash

# AI Voice Detection API - Setup Script
# Automates environment setup and deployment

set -e  # Exit on error

echo "================================================================"
echo "AI Voice Detection API - Setup Script"
echo "================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if Python is installed
echo "Checking requirements..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

# Check if pip is installed
if command -v pip3 &> /dev/null; then
    print_success "pip found"
else
    print_error "pip not found. Please install pip."
    exit 1
fi

echo ""
echo "================================================================"
echo "Setup Options"
echo "================================================================"
echo "1. Local Development Setup"
echo "2. Install Dependencies Only"
echo "3. Generate Test Audio"
echo "4. Run Tests"
echo "5. Start Development Server"
echo "6. Create Docker Image"
echo "7. Deploy to Cloud (Guide)"
echo "8. Full Setup (All of the above)"
echo ""

read -p "Select option (1-8): " option

case $option in
    1|8)
        echo ""
        echo "Setting up local development environment..."
        
        # Create virtual environment
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
        
        # Activate virtual environment
        print_info "Activating virtual environment..."
        source venv/bin/activate
        print_success "Virtual environment activated"
        
        # Upgrade pip
        print_info "Upgrading pip..."
        pip install --upgrade pip > /dev/null 2>&1
        print_success "pip upgraded"
        
        # Install dependencies
        print_info "Installing dependencies..."
        pip install -r requirements.txt
        print_success "Dependencies installed"
        
        # Create .env file if it doesn't exist
        if [ ! -f .env ]; then
            print_info "Creating .env file..."
            cp .env.example .env
            print_success ".env file created"
            print_info "Please edit .env file to set your API_KEY"
        fi
        
        print_success "Local development setup complete!"
        ;;&  # Continue to next case
    
    2)
        echo ""
        print_info "Installing dependencies..."
        pip3 install -r requirements.txt
        print_success "Dependencies installed"
        ;;
    
    3|8)
        echo ""
        print_info "Generating test audio..."
        if [ -f "generate_test_audio.py" ]; then
            python3 generate_test_audio.py
            print_success "Test audio generated"
        else
            print_error "generate_test_audio.py not found"
        fi
        ;;&
    
    4|8)
        echo ""
        print_info "Running health check..."
        if curl -s http://localhost:5000/health > /dev/null 2>&1; then
            print_success "API is running and healthy"
        else
            print_error "API is not responding. Start the server first."
        fi
        ;;&
    
    5)
        echo ""
        print_info "Starting development server..."
        export API_KEY=${API_KEY:-hackathon-api-key-2024}
        export FLASK_DEBUG=True
        python3 app.py
        ;;
    
    6)
        echo ""
        print_info "Building Docker image..."
        if command -v docker &> /dev/null; then
            docker build -t ai-voice-detection .
            print_success "Docker image built: ai-voice-detection"
            echo ""
            print_info "To run the container:"
            echo "  docker run -p 5000:5000 -e API_KEY=your-key ai-voice-detection"
        else
            print_error "Docker not found. Please install Docker."
        fi
        ;;
    
    7)
        echo ""
        echo "================================================================"
        echo "Cloud Deployment Guide"
        echo "================================================================"
        echo ""
        echo "Option 1: Render.com (Recommended)"
        echo "  1. Push code to GitHub"
        echo "  2. Go to render.com and create new Web Service"
        echo "  3. Connect your GitHub repo"
        echo "  4. Set build command: pip install -r requirements.txt"
        echo "  5. Set start command: gunicorn --bind 0.0.0.0:\$PORT app:app"
        echo "  6. Add environment variable: API_KEY=your-secret-key"
        echo "  7. Deploy!"
        echo ""
        echo "Option 2: Railway.app"
        echo "  1. Connect GitHub repo on railway.app"
        echo "  2. Add environment variable: API_KEY=your-secret-key"
        echo "  3. Railway auto-deploys!"
        echo ""
        echo "Option 3: Heroku"
        echo "  1. heroku create ai-voice-detection"
        echo "  2. heroku config:set API_KEY=your-secret-key"
        echo "  3. git push heroku main"
        echo ""
        ;;
    
    8)
        echo ""
        print_success "Full setup complete!"
        echo ""
        echo "================================================================"
        echo "Next Steps"
        echo "================================================================"
        echo "1. Edit .env file to set your API_KEY"
        echo "2. Run: source venv/bin/activate"
        echo "3. Run: python3 app.py"
        echo "4. Test at: http://localhost:5000"
        echo "5. Open api_tester.html in browser for easy testing"
        echo ""
        ;;
    
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "================================================================"
print_success "Setup script completed!"
echo "================================================================"

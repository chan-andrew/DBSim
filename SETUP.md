# NeuroTwin Setup Guide

## Quick Setup Instructions

### Step 1: Backend Setup
```bash
cd neurotwin/backend
pip install -r requirements.txt
python app.py
```

### Step 2: Frontend Setup
```bash
cd neurotwin/frontend
npm install
npm start
```

### Step 3: Access Application
Open http://localhost:3000 in your web browser

## Detailed Installation

### Prerequisites Check
```bash
# Check Python version (3.8+ required)
python --version

# Check Node.js version (16+ required)
node --version

# Check npm version
npm --version
```

### Backend Installation
```bash
# Navigate to backend directory
cd neurotwin/backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

Expected output:
```
Initializing NeuroTwin models...
✓ Brain tissue model initialized
✓ DBS electrode model initialized
✓ DBS parameter explorer initialized
✓ Disease model manager initialized
NeuroTwin initialization complete!
Starting NeuroTwin API server...
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[::1]:5000
```

### Frontend Installation
```bash
# Navigate to frontend directory
cd neurotwin/frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

Expected output:
```
Compiled successfully!

You can now view neurotwin-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

## Troubleshooting

### Backend Issues

#### Import Errors
```bash
# If you get import errors, ensure virtual environment is activated
# and all dependencies are installed
pip list  # Check installed packages
pip install -r requirements.txt  # Reinstall if needed
```

#### Port Already in Use
```bash
# If port 5000 is in use, modify app.py:
# Change: app.run(host='0.0.0.0', port=5000, debug=True)
# To:     app.run(host='0.0.0.0', port=5001, debug=True)
# Also update package.json proxy: "http://localhost:5001"
```

### Frontend Issues

#### npm install Failures
```bash
# Clear npm cache and try again
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### CORS Errors
```bash
# Ensure backend is running on port 5000
# Check package.json has: "proxy": "http://localhost:5000"
```

### Network Issues

#### Backend Not Accessible
```bash
# Test backend health
curl http://localhost:5000/api/health

# Should return:
# {"status":"healthy","message":"NeuroTwin API is running","models_initialized":true}
```

#### Frontend Can't Connect to Backend
1. Verify backend is running on port 5000
2. Check browser console for CORS errors
3. Ensure proxy setting in package.json is correct

## Environment Variables

### Optional Backend Configuration
Create `.env` file in backend directory:
```
FLASK_ENV=development
FLASK_DEBUG=1
GRID_SIZE=30  # Smaller for faster performance
```

### Optional Frontend Configuration
Create `.env` file in frontend directory:
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_DEBUG=true
```

## Production Deployment

### Backend Production
```bash
# Install production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Production
```bash
# Build for production
npm run build

# Serve with static server
npm install -g serve
serve -s build -l 3000
```

## System Requirements

### Minimum Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Dual-core processor
- **Storage**: 2GB free space
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

### Recommended Requirements
- **RAM**: 16GB for optimal performance
- **CPU**: Quad-core processor
- **Storage**: 5GB free space
- **Graphics**: Dedicated GPU for 3D visualization

## Performance Notes

### Optimization Tips
1. **Reduce Grid Size**: Edit `brain_tissue.py` grid_size parameter
2. **Limit Simulation Time**: Reduce simulation duration in parameters
3. **Browser Performance**: Close other tabs during use
4. **Memory Usage**: Restart application if performance degrades

### Expected Performance
- **Simulation Time**: 2-10 seconds per run
- **Memory Usage**: 200-500MB browser, 100-300MB backend
- **GPU Usage**: Moderate for 3D visualization
- **Network**: Local communication only (no external dependencies)

## Development Mode

### Hot Reloading
Both frontend and backend support hot reloading:
- **Frontend**: Automatic reload on file changes
- **Backend**: Set `debug=True` in app.py for auto-restart

### Debugging
```bash
# Backend debugging
export FLASK_DEBUG=1
python app.py

# Frontend debugging
# Open browser developer tools (F12)
# Check Console and Network tabs for errors
```

## Next Steps

1. **Complete Installation**: Follow steps above
2. **Run Tutorial**: Click "Tutorial Mode" in the application
3. **Read Documentation**: Review README.md for detailed usage
4. **Explore Features**: Try different parameters and conditions
5. **Educational Use**: Integrate into coursework or self-study

## Getting Help

If you encounter issues:
1. Check this setup guide
2. Review the main README.md
3. Check browser console for errors
4. Verify all prerequisites are installed
5. Create GitHub issue with error details

## Success Indicators

You'll know the setup worked when:
- ✅ Backend shows "NeuroTwin initialization complete!"
- ✅ Frontend loads at http://localhost:3000
- ✅ Status indicator shows "Backend: healthy"
- ✅ You can run a simulation without errors
- ✅ 3D visualization displays properly

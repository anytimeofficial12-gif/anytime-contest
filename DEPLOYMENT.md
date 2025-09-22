# ANYTIME Contest Landing Page - Deployment Guide

This guide will help you deploy the ANYTIME Contest Landing Page to production environments.

## Project Structure

```
lnd/
├── Frontend (Static Files)
│   ├── index.html          # Main landing page
│   ├── script.js           # Frontend JavaScript
│   ├── config.js           # Configuration file
│   ├── style.css           # Additional styles (if used)
│   ├── anytime-logo.png    # Logo image
│   ├── vercel.json         # Vercel configuration
│   └── package.json        # Node.js package info
│
├── Backend (FastAPI)
│   ├── app.py              # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── Procfile           # Heroku deployment
│   ├── runtime.txt        # Python version
│   └── env.example        # Environment variables template
│
└── Documentation
    └── DEPLOYMENT.md      # This file
```

## Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (free tier available)
- GitHub repository with your code

### Steps

1. **Prepare the Frontend**
   - Update `config.js` with your production backend URL:
   ```javascript
   API_BASE_URL: 'https://your-backend-url.railway.app'
   ```

2. **Deploy to Vercel**
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Deploy
   vercel
   
   # Or connect your GitHub repo to Vercel dashboard
   ```

3. **Configure Environment Variables** (if needed)
   - Go to Vercel Dashboard → Project Settings → Environment Variables
   - Add any required environment variables

4. **Update Backend CORS**
   - After getting your Vercel URL, update the backend CORS configuration
   - Add your Vercel URL to `ALLOWED_ORIGINS` in `app.py`

## Backend Deployment Options

### Option 1: Railway (Recommended)

Railway provides easy Python deployment with automatic scaling.

#### Steps:
1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy Backend**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   railway init
   railway up
   ```

3. **Configure Environment Variables**
   - Go to Railway Dashboard → Variables
   - Add the following variables:
   ```
   ENVIRONMENT=production
   GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
   GOOGLE_SPREADSHEET_ID=your-spreadsheet-id
   GOOGLE_SHEET_RANGE=Sheet1!A:D
   ```

4. **Get Backend URL**
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Update your frontend `config.js` with this URL

### Option 2: Render

Render offers free tier for Python applications.

#### Steps:
1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**
   - Connect your GitHub repository
   - Choose "Web Service"
   - Configure:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

3. **Configure Environment Variables**
   - Add the same variables as Railway

### Option 3: Heroku

Heroku provides reliable hosting with easy deployment.

#### Steps:
1. **Create Heroku Account**
   - Go to [heroku.com](https://heroku.com)
   - Install Heroku CLI

2. **Deploy**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-app-name
   
   # Set environment variables
   heroku config:set ENVIRONMENT=production
   heroku config:set GOOGLE_CREDENTIALS_JSON='{"type":"service_account",...}'
   heroku config:set GOOGLE_SPREADSHEET_ID=your-spreadsheet-id
   
   # Deploy
   git push heroku main
   ```

## Google Sheets Setup

### 1. Create Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable Google Sheets API
4. Create Service Account:
   - Go to IAM & Admin → Service Accounts
   - Create Service Account
   - Download JSON key file

### 2. Share Spreadsheet
1. Open your Google Spreadsheet
2. Click "Share" button
3. Add the service account email (from JSON file)
4. Give "Editor" permissions

### 3. Configure Environment Variables
For production, use the JSON content as an environment variable:
```bash
GOOGLE_CREDENTIALS_JSON='{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}'
```

## Configuration Updates

### Frontend Configuration (`config.js`)
```javascript
const CONFIG = {
    API_BASE_URL: 'https://your-backend-url.railway.app', // Update this
    // ... other settings
};
```

### Backend CORS Configuration (`app.py`)
```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Local development
    "https://your-frontend-url.vercel.app",  # Update this
]
```

## Testing Deployment

### 1. Test Backend
```bash
# Health check
curl https://your-backend-url.railway.app/health

# Expected response:
{
  "status": "healthy",
  "environment": "production",
  "google_sheets": "connected",
  "cors_origins": [...],
  "timestamp": "..."
}
```

### 2. Test Frontend
1. Visit your Vercel URL
2. Open browser developer tools
3. Check console for any errors
4. Test form submission

### 3. Test Integration
1. Fill out the contest form
2. Submit and verify success message
3. Check Google Sheets for new entry

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure frontend URL is in backend's `ALLOWED_ORIGINS`
   - Check that backend is running and accessible

2. **Google Sheets Connection Failed**
   - Verify service account JSON is correct
   - Ensure spreadsheet is shared with service account email
   - Check environment variables are set correctly

3. **Form Submission Fails**
   - Check browser network tab for error details
   - Verify backend URL in `config.js`
   - Ensure backend is running and healthy

4. **Static Assets Not Loading**
   - Verify all file paths are relative
   - Check that all files are included in deployment

### Debug Mode
Enable debug mode by setting `ENVIRONMENT=development` in backend environment variables.

## Security Considerations

1. **Environment Variables**
   - Never commit sensitive data to version control
   - Use environment variables for all secrets
   - Rotate service account keys regularly

2. **CORS Configuration**
   - Only allow necessary origins in production
   - Avoid using wildcard (*) in production

3. **Input Validation**
   - Backend validates all form inputs
   - Frontend provides user-friendly error messages

## Monitoring

### Backend Health
- Use `/health` endpoint for monitoring
- Check logs for errors and performance issues

### Frontend Performance
- Monitor page load times
- Check for JavaScript errors in browser console
- Verify form submissions are working

## Updates and Maintenance

### Frontend Updates
1. Update code in your repository
2. Vercel will automatically redeploy
3. Test the updated site

### Backend Updates
1. Update code in your repository
2. Redeploy using your chosen platform's method
3. Test API endpoints

### Configuration Changes
1. Update environment variables in your deployment platform
2. Restart the application
3. Test functionality

## Support

For issues or questions:
- Check the troubleshooting section above
- Review platform-specific documentation
- Check application logs for error details

## Cost Considerations

### Free Tiers
- **Vercel**: Free for personal projects
- **Railway**: $5/month after free tier
- **Render**: Free tier available
- **Heroku**: No longer offers free tier

### Scaling
- Monitor usage and upgrade plans as needed
- Consider caching strategies for high traffic
- Optimize images and assets for better performance

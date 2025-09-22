# ANYTIME Contest Landing Page

A modern, responsive landing page for the ANYTIME contest with Google Sheets integration for storing submissions.

## 🚀 Quick Start

### Local Development

1. **Setup Environment**
   ```bash
   python setup_local.py
   ```

2. **Start Backend**
   ```bash
   python app.py
   ```

3. **Open Frontend**
   - Open `index.html` in your browser, or
   - Use a local server: `python -m http.server 3000`

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
- **Frontend**: Deploy to Vercel
- **Backend**: Deploy to Railway/Render/Heroku
- **Update**: Backend URL in `config.js`

## 📁 Project Structure

```
├── Frontend Files
│   ├── index.html          # Main landing page
│   ├── script.js           # Frontend logic
│   ├── config.js           # Configuration
│   └── anytime-logo.png    # Logo
│
├── Backend Files
│   ├── app.py              # FastAPI server
│   ├── requirements.txt    # Dependencies
│   └── Procfile           # Heroku config
│
└── Documentation
    ├── DEPLOYMENT.md       # Deployment guide
    └── README.md          # This file
```

## ⚙️ Configuration

### Frontend Configuration (`config.js`)
```javascript
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',  // Backend URL
    // ... other settings
};
```

### Backend Configuration
Set environment variables:
- `ENVIRONMENT=production`
- `GOOGLE_CREDENTIALS_JSON=...`
- `GOOGLE_SPREADSHEET_ID=...`

## 🔧 Features

- ✅ Responsive design
- ✅ Form validation
- ✅ Google Sheets integration
- ✅ Error handling
- ✅ Loading states
- ✅ Accessibility features
- ✅ SEO optimized
- ✅ Production ready

## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Responsive design
- Modern CSS animations

**Backend:**
- Python 3.8+
- FastAPI
- Google Sheets API
- CORS enabled

## 📱 Browser Support

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## 🔒 Security

- Input validation
- CORS configuration
- Environment variables for secrets
- HTTPS in production

## 📊 Monitoring

- Health check endpoint: `/health`
- Error logging
- Performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues or questions:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
2. Review the troubleshooting section
3. Check application logs
4. Open an issue on GitHub

## 🎯 Contest Details

- **Prize**: ₹500 for top 10 accurate guesses
- **Duration**: September 20 - October 5, 2025
- **App Launch**: October 6, 2025

---

**ANYTIME** - Revolutionary Service Platform

# Security Guidelines

## 🔐 API Key Security

**IMPORTANT**: Never commit API keys or sensitive information to the repository!

### Protected Files

The following files are automatically excluded from Git:
- `.env` - Contains your actual API keys
- `user_preferences.json` - Contains user data

### Setup Instructions

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`:**
   ```
   YOUTUBE_API_KEY=your_actual_youtube_key_here
   GEMINI_API_KEY=your_actual_gemini_key_here
   ```

3. **Never commit `.env` file!**

### If You Accidentally Committed API Keys

If you've already committed API keys to Git:

1. **Immediately revoke the exposed keys:**
   - YouTube: https://console.cloud.google.com/apis/credentials
   - Gemini: https://makersuite.google.com/app/apikey

2. **Remove from Git history:**
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Force push (if already pushed):**
   ```bash
   git push origin --force --all
   ```

4. **Generate new API keys** and update your `.env` file

### Best Practices

- ✅ Always use `.env.example` as a template
- ✅ Add `.env` to `.gitignore` (already done)
- ✅ Never hardcode API keys in source code
- ✅ Use environment variables for all secrets
- ✅ Rotate keys periodically
- ✅ Use different keys for development and production

### Checking for Exposed Keys

Before committing, check for exposed keys:
```bash
# Search for potential API keys in code
grep -r "AIzaSy" --exclude-dir=venv --exclude-dir=.git .
grep -r "sk-" --exclude-dir=venv --exclude-dir=.git .
```

If any keys are found in source files, remove them immediately!


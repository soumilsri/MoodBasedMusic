# Pre-Commit Security Checklist

Before pushing to a public Git repository, verify the following:

## ✅ Security Checklist

- [ ] `.env` file is in `.gitignore` ✓ (Already done)
- [ ] `.env` file is NOT tracked by Git
- [ ] No API keys are hardcoded in source files
- [ ] `.env.example` only contains placeholder values
- [ ] `user_preferences.json` is in `.gitignore` ✓ (Already done)

## 🔍 Quick Check Commands

### 1. Verify .env is ignored:
```bash
git status
# .env should NOT appear in the list
```

### 2. If .env is tracked, remove it:
```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
```

### 3. Run security check:
```bash
python check_secrets.py
```

### 4. Search for potential keys:
```bash
# Windows PowerShell
Select-String -Path "*.py" -Pattern "AIzaSy" -Exclude ".env"
```

## 🚨 If You Find Exposed Keys

1. **Immediately revoke the keys** in their respective consoles
2. **Remove from Git history** (see SECURITY.md)
3. **Generate new keys**
4. **Update your local .env file**

## 📝 Safe to Commit

These files are safe to commit:
- ✅ `.env.example` (placeholders only)
- ✅ `.gitignore` (protects sensitive files)
- ✅ `SECURITY.md` (guidelines)
- ✅ All Python source files (no hardcoded keys)
- ✅ `README.md`
- ✅ `requirements.txt`

## ❌ Never Commit

- ❌ `.env` (contains real API keys)
- ❌ `user_preferences.json` (contains user data)
- ❌ Any file with actual API keys


# Free LLM Setup Guide

This app now uses **FREE LLM options** instead of paid OpenAI. You have multiple free options:

## Option 1: Hugging Face (Recommended - No API Key Needed!)

**Default option** - Works immediately without any setup!

- ✅ **Completely free** - No API key required
- ✅ **No signup needed** for basic use
- ✅ **Works out of the box**
- ⚠️ Can be slower (uses rule-based interpretation)

### Optional: Get Hugging Face API Key (Faster)

1. Go to https://huggingface.co/
2. Sign up (free, no credit card)
3. Go to https://huggingface.co/settings/tokens
4. Create a new token
5. Add to `.env`:
   ```
   HUGGINGFACE_API_KEY=your_token_here
   ```

## Option 2: Google Gemini (Free Tier)

**Best quality** - Free tier with good limits!

- ✅ **Free tier**: 60 requests per minute
- ✅ **High quality** responses
- ✅ **No credit card** required for free tier
- ⚠️ Requires API key setup

### Setup Steps:

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key
5. Add to `.env`:
   ```
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_api_key_here
   ```

## Option 3: No LLM (Simple Fallback)

If you don't want to use any LLM:

1. Set in `.env`:
   ```
   LLM_PROVIDER=none
   ```

The app will use simple keyword matching (still works, but less intelligent).

## Comparison

| Provider | Setup | Speed | Quality | Free Tier |
|----------|-------|-------|---------|-----------|
| Hugging Face (no key) | ✅ None | ⚠️ Slow | ⚠️ Basic | ✅ Unlimited |
| Hugging Face (with key) | ⚠️ Easy | ✅ Fast | ⚠️ Basic | ✅ Free |
| Google Gemini | ⚠️ Easy | ✅ Fast | ✅ High | ✅ 60/min |
| None (fallback) | ✅ None | ✅ Instant | ⚠️ Basic | ✅ Unlimited |

## Recommendation for POC

**Start with Hugging Face (default)** - It works immediately without any setup!

If you want better quality, add a Gemini API key (takes 2 minutes, completely free).

## Current Configuration

Check your `.env` file:
```
LLM_PROVIDER=huggingface  # or "gemini" or "none"
```

The app will automatically use the configured provider.


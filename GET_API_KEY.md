# How to Get YouTube Data API v3 Key

Follow these step-by-step instructions to obtain your YouTube Data API v3 key:

## Step 1: Go to Google Cloud Console

1. Open your web browser and go to: **https://console.cloud.google.com/**
2. Sign in with your Google account (or create one if you don't have it)

## Step 2: Create a New Project (or Select Existing)

1. Click on the **project dropdown** at the top of the page (next to "Google Cloud")
2. Click **"New Project"**
3. Enter a project name (e.g., "Mood Music App")
4. Click **"Create"**
5. Wait for the project to be created, then select it from the dropdown

## Step 3: Enable YouTube Data API v3

1. In the left sidebar, go to **"APIs & Services"** → **"Library"**
2. In the search bar, type: **"YouTube Data API v3"**
3. Click on **"YouTube Data API v3"** from the results
4. Click the **"Enable"** button
5. Wait for the API to be enabled (this may take a few seconds)

## Step 4: Create API Credentials

1. Go to **"APIs & Services"** → **"Credentials"** (in the left sidebar)
2. Click **"+ CREATE CREDENTIALS"** at the top
3. You may see options for "User Data" or "Public Data":
   - **Select "Public Data"** (this is what you need for searching public videos)
   - If you don't see this option, just select **"API key"** directly
4. Your API key will be generated and displayed in a popup

## Step 5: Copy Your API Key

1. **Copy the API key** that appears in the popup
2. **Important**: Save it somewhere safe - you won't be able to see it again in full
3. Click **"Close"** (you can restrict the key later if needed)

## Step 6: Add API Key to Your App

1. Open the `.env` file in your `mood_music_app` folder:
   ```
   C:\Users\ssrivastava\mood_music_app\.env
   ```
2. Replace `your_youtube_api_key_here` with your actual API key:
   ```
   YOUTUBE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
3. Save the file

## Step 7: (Optional) Restrict API Key (Recommended for Security)

For better security, you can restrict your API key:

1. Go back to **"APIs & Services"** → **"Credentials"**
2. Click on your API key
3. Under **"API restrictions"**, select **"Restrict key"**
4. Check **"YouTube Data API v3"** only
5. Under **"Application restrictions"**, you can add restrictions (optional)
6. Click **"Save"**

## Troubleshooting

### "API key not valid" error
- Make sure you copied the entire key (they're long!)
- Check that there are no extra spaces in the `.env` file
- Verify the API key is enabled in Google Cloud Console

### "Quota exceeded" error
- YouTube Data API has a default quota of 10,000 units per day
- Each search request uses 100 units
- You can request a quota increase in Google Cloud Console if needed

### "API not enabled" error
- Go back to Step 3 and make sure YouTube Data API v3 is enabled
- It may take a few minutes for the API to be fully activated

## Free Tier Limits

- **Default quota**: 10,000 units per day
- **Search request**: 100 units per request
- This means approximately **100 searches per day** (more than enough for personal use!)

## Need Help?

If you encounter any issues:
1. Check that your Google account has billing enabled (even if you won't be charged for free tier)
2. Make sure the project is selected in the top dropdown
3. Verify the API is enabled in the "APIs & Services" → "Enabled APIs" section


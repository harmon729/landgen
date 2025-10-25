# 🚀 LandGen Quick Setup Guide

## Step 1: Install Dependencies

```bash
# Install frontend dependencies
npm install

# Install backend dependencies (in api/ folder)
cd api
pip install -r requirements.txt
cd ..
```

## Step 2: Get Your Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Step 3: Configure Environment Variables

Create a `.env.local` file in the root directory:

```bash
GEMINI_API_KEY=your_api_key_here
```

## Step 4: Run the Application

### Option A: Run everything together (Recommended)

```bash
npm run dev:all
```

### Option B: Run frontend and backend separately

Terminal 1:

```bash
npm run dev
```

Terminal 2:

```bash
npm run dev:api
```

## Step 5: Open in Browser

Visit: http://localhost:3000

## Test It!

Try these GitHub usernames:

- torvalds (Linus Torvalds)
- gaearon (Dan Abramov, React core team)
- tj (TJ Holowaychuk)
- sindresorhus (Sindre Sorhus)

---

## Troubleshooting

### "Module not found" errors

```bash
npm install
cd api && pip install -r requirements.txt
```

### API not working

- Check your `.env.local` file has GEMINI_API_KEY
- Restart the dev server

### Port already in use

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

---

Need help? Check README.md for full documentation.

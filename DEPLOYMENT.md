# Deployment Guide for LandGen

## 🚀 Deploy to Vercel (Recommended)

### Step 1: Prepare Your Repository

1. Initialize git (if not already done):

```bash
git init
git add .
git commit -m "Initial commit: LandGen v0.1"
```

2. Create a GitHub repository and push:

```bash
git remote add origin https://github.com/YOUR_USERNAME/landgen.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `./`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

### Step 3: Add Environment Variables

In the Vercel dashboard, add these environment variables:

**Required:**

- `GEMINI_API_KEY`: Your Google Gemini API key

**Optional:**

- `GITHUB_TOKEN`: For higher GitHub API rate limits

### Step 4: Deploy

Click "Deploy" and wait for the build to complete (usually 2-3 minutes).

Your app will be live at: `https://your-project.vercel.app`

---

## 🔧 Environment Variables

### For Local Development

Create `.env.local` in the root directory:

```env
GEMINI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here  # Optional
```

### For Production (Vercel)

Add in Vercel Dashboard → Settings → Environment Variables:

1. **GEMINI_API_KEY** (Required)

   - Get from: https://makersuite.google.com/app/apikey
   - Used for: AI-powered project summaries

2. **GITHUB_TOKEN** (Optional)
   - Get from: https://github.com/settings/tokens
   - Used for: Higher API rate limits (60 → 5000 requests/hour)
   - Scopes needed: None (public access only)

---

## 🎯 Post-Deployment Checklist

- [ ] Test with different GitHub usernames
- [ ] Verify AI summaries are generating
- [ ] Check mobile responsiveness
- [ ] Test error handling (invalid username)
- [ ] Monitor API rate limits
- [ ] Set up custom domain (optional)

---

## 🐛 Common Issues

### Build fails on Vercel

**Error: "Module not found"**

```bash
# Solution: Ensure all dependencies are in package.json
npm install --save [missing-package]
git add package.json package-lock.json
git commit -m "Fix dependencies"
git push
```

**Error: "Python runtime error"**

- Check `vercel.json` configuration
- Ensure `api/index.py` exists
- Verify `api/requirements.txt` is correct

### API returns 500 error

**Missing API key:**

- Add `GEMINI_API_KEY` in Vercel environment variables
- Redeploy the project

### GitHub API rate limit

**Error: "API rate limit exceeded"**

- Add `GITHUB_TOKEN` environment variable
- Or wait for rate limit to reset (1 hour)

---

## 📊 Monitoring

After deployment, monitor:

1. **Vercel Analytics**: Built-in traffic analytics
2. **Function Logs**: Check for API errors
3. **Build Logs**: Ensure successful deployments

Access logs in: Vercel Dashboard → Your Project → Deployments → [Latest] → Functions

---

## 🔄 Update Deployment

To update your deployed app:

```bash
git add .
git commit -m "Update: [your changes]"
git push origin main
```

Vercel will automatically redeploy on push to `main` branch.

---

## 🌐 Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain (e.g., `landgen.com`)
3. Follow DNS configuration instructions
4. Wait for DNS propagation (5-30 minutes)

---

## 💡 Tips

- Use Vercel's preview deployments for testing
- Monitor function execution time (serverless timeout: 10s)
- Enable automatic HTTPS (included by default)
- Use Vercel Speed Insights for performance monitoring

---

Need help? Check the [Vercel documentation](https://vercel.com/docs) or [create an issue](https://github.com/yourusername/landgen/issues).

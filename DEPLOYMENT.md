# 🚀 Cloud Deployment Guide (Streamlit & Docker)

Since you are preparing to defend this project in an interview, knowing how to deploy it on the cloud is a huge flex! Here are the two standard ways you can mention (and use) for deploying this Cloud-Native AI Tutor.

---

## Method 1: Streamlit Community Cloud (The Easy Way)
This is the fastest, free method for pure Streamlit apps.

**Steps:**
1. **Push to GitHub:** Commit all files (except `.env` and `.venv`) and push to a new GitHub repository.
2. **Login to Streamlit Cloud:** Go to [share.streamlit.io](https://share.streamlit.io) and login with your GitHub account.
3. **Deploy:** Click "New App", select your repository, branch, and `app.py` as the main file path.
4. **Add Secrets (Crucial!):** Before clicking deploy, click on **Advanced Settings**. In the "Secrets" text box, paste your API keys like this:
   ```toml
   GEMINI_API_KEY="your_actual_key"
   PINECONE_API_KEY="your_actual_key"
   PINECONE_INDEX_NAME="ai-tutor-index"
   ```
5. Click **Deploy!** In 2 minutes, your app will be live on a public URL.

---

## Method 2: Docker Container (The Professional/Enterprise Way)
If the interviewer asks *"How would you deploy this in a real enterprise environment like AWS or Google Cloud?"*, your answer should be **Docker**.

We have added a `Dockerfile` to your project. Here is how it works:

**Steps to run via Docker (locally or on a cloud VPS):**
1. **Build the Image:**
   ```bash
   docker build -t cloud-ai-tutor .
   ```
2. **Run the Container (passing your .env file):**
   ```bash
   docker run -p 8501:8501 --env-file .env cloud-ai-tutor
   ```
Your app will be available at `http://localhost:8501`.

### Where to host the Docker Image?
- **Render.com / Railway.app:** Free tier, connect your GitHub, and they will automatically build and run the Dockerfile.
- **Hugging Face Spaces:** Choose "Docker" template, upload your files, add secrets in their UI, and it runs for free.
- **AWS EC2 / DigitalOcean Droplet:** SSH into a Linux server, clone your repo, and run the two docker commands above.

# Epsilon TeXpedition Hackathon Submission

This document contains the exact text, descriptions, and details for your final project submission on the hackathon platform. Copy and paste the sections below directly into the submission form.

---

### FIELD 1: Title
**TraitTrace — Privacy-First Cookie-less Personalization via Zero-Party Knowledge Graphs**

---

### FIELD 2: Description
#### The Problem
In the modern AdTech and MarTech landscape, cookies and stealth third-party trackers are dying. Regulatory frameworks like GDPR and CCPA, coupled with browser tracking blocks (like Apple's App Tracking Transparency and Google's Sandbox), have made traditional consumer tracking obsolete. Marketers are left with a critical challenge: *How do we serve personalized storefront experiences and product recommendations without invading user privacy or storing tracking cookies?*

#### Our Solution: TraitTrace
**TraitTrace** is a privacy-first AdTech personalization engine built for the next generation of consumer marketing. Instead of tracking users invisibly, it relies on **Explicit Zero-Party Consent** and gamified interactions. 
1. **Intake Index Cards**: The consumer interacts with a physical-styled card deck to design their visual, pricing, and lifestyle profiles.
2. **In-Memory Knowledge Graph**: Every interaction is mapped dynamically into a session-isolated **NetworkX DiGraph** on the backend. This builds a real-time behavioral graph path of the consumer.
3. **Groq Llama 3.1 Personalization**: Our graph-text compiler translates the paths into a semantic summary, which is queried through a fast, open-source LLM (`llama-3.1-8b-instant` via Groq) to serve hyper-personalized storefront headers, banners, and product catalog placements in under 150ms.
4. **Interactive Marketplaces Re-routing**: Once the user's profile is fully synthesized, the system renders a tailored selection of hardware smartwatches with direct checkout links to local marketplaces (**Amazon.in**, **Flipkart**, and **Google Shop**).

#### Visual & Architecture Design
The frontend uses a dual-concept split-screen interface:
*   **The Manila Folder (Left)**: Warm kraft card-stock styling representing the consumer's readable case file. This is where they explicitly tell the merchant what they like.
*   **The Control Room (Right)**: An inverted, dark marketer's dashboard showing the live, updating 2D force-directed knowledge graph and the API prompt logs compiled for LLM reasoning.
*   *The Perforation Divider Seam*: A vertical dashed separator representing the hard consent boundary between the browser and the database.

#### Tech Stack
*   **Frontend**: Next.js 14 App Router, TypeScript, Tailwind CSS v3, Framer Motion (swipe gestures), `react-force-graph-2d` (interactive graph visualization).
*   **Backend**: Python, FastAPI (REST API routes), NetworkX (ephemeral graph database logic), Groq Python Client (Llama 3.1 inference).
*   **Testing**: Pytest & TestClient (with 100% test coverage for path compiling and client-setup fallbacks).

---

### FIELD 3: Repository URL
`https://github.com/Aakash10032005/TRAITTRACE.git`

---

### FIELD 4: Demo Link
`http://localhost:3000` *(Local host prototype)*

---

### FIELD 5: Instructions to Run

Copy and paste these exact instructions for the reviewers to spin up your project:

```markdown
### Prerequisites
- Node.js 18+
- Python 3.10+
- A Groq API Key (get a free key at https://console.groq.com/)

### Step 1: Environment Variables
Create a file named `.env` in the root directory of the project and add your Groq API Key:
```env
GROQ_API_KEY=gsk_your_groq_api_key_goes_here
```

### Step 2: Spin Up FastAPI Backend
Run the following commands in your terminal to set up the Python environment, install dependencies, and run the backend server:
```bash
# Navigate to backend folder
cd backend

# Create and activate Python virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r ../requirements.txt

# Run the FastAPI server on port 8000
uvicorn main:app --reload --port 8000
```
*(Verify health at http://localhost:8000/health)*

### Step 3: Spin Up Next.js Frontend
In a separate terminal session, navigate to the frontend directory, install npm packages, and start the development server:
```bash
# Navigate to frontend folder
cd frontend

# Install Node dependencies
npm install

# Run the dev server on port 3000
npm run dev
```

### Step 4: Access the Prototype
Open your browser to `http://localhost:3000/`. Click "Start a new file" and begin swiping cards to see the storefront adapt dynamically!

### Running Backend Tests
To verify the NetworkX engine and Groq client exception resiliency:
```bash
# From the root directory (with venv active)
python -m pytest
```
```

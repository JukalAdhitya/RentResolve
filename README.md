# RentResolve 🏠⚖️
> **AI-Powered Rental Dispute Resolution Platform**

RentResolve is a modern web application designed to bridge the gap between Tenants and Landlords using Generative AI. It helps tenants structure professional complaints and gives landlords tools to manage and respond to issues effectively.

---

## 🚀 Key Features

### 🤖 Generative AI Agents (PydanticAI)
- **Tenant Agent**: Analyzes raw complaint details (e.g., "water leakage", "deposit issue") and a lease agreement (optional) to generate a full **Legal Complaint Kit**:
    - Professionally worded Email Draft.
    - Professional WhatsApp Message.
    - Evidence Checklist.
    - Escalation Timeline.
    - **Complaint Strength Score (non-legal)** (0-100). *Note: Not legal advice. For guidance only.*
- **Landlord Agent**: Helps landlords analyze incoming complaints and draft professional, legally sound replies.
- **Agent Framework**: AI Agents built using **PydanticAI** with strict schema validation.

### 👥 User Roles & Profiles
- **Tenants**: Dashboard to report issues, view status, and access AI-generated kits.
- **Landlords**: Dashboard to view all tenant issues, analyze them, and reply.
- **Profile Management**: Centralized profile page for updating personal details (Name, Phone, Address).

### ⭐ High-Impact "SaaS" Features
- **Case Timeline**: Interactive vertical timeline tracking every status change and update.
- **Evidence Vault**: Secure file upload system for tenants to store photos, receipts, and documents.
- **AI Reply Assistant**: One-click professional reply generator for Landlords with robust customization (Tone, Stance).

### 📧 Notifications
- **Email System**: Automated email notifications when issues are reported or updated (Supports Real SMTP & Mock Mode).
- **Mock Mode**: For development, emails are logged directly to the console.

### 🎨 Modern UI/UX
- **Cyberpunk / High-Tech Aesthetic**: Glassmorphism, neon accents, and dynamic backgrounds.
- **Theme Support**: Fully functional **Dark Mode** and **Light Mode** with high-contrast distinct styles.
- **Responsive**: Built for desktop and mobile.

### ✅ Reliability & Safety
- **Pydantic Schema Validation**: Ensures all AI outputs strictly adhere to defined JSON schemas.
- **Retries & Recovery**: Automatically retries generation if output fails validation.
- **Fallbacks**: Graceful error handling with fallback response templates.
- **Centralized Logging**: Comprehensive logging for agent runs and email delivery status.

---

## 🛠️ Technology Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python).
- **Database**: MongoDB (via Motor/Beanie ODM).
- **AI Model**: Gemini Flash (or OpenRouter model).
- **Agent Orchestration**: PydanticAI (tool calling + structured outputs + retries).
- **Tasks**: BackgroundTasks for Email.

### Frontend
- **Framework**: [Next.js 15](https://nextjs.org/) (React)
- **Styling**: Tailwind CSS, Framer Motion (Animations), Lucide React (Icons).
- **State/Form**: React Hook Form, Axios.

---

## 📂 Project Structure

```bash
RentResolve/
├── rentresolve-backend/       # FastAPI Server
│   ├── app/
│   │   ├── agents/            # AI Agents (PydanticAI Schemas & Prompts)
│   │   ├── core/              # Config, Security (JWT)
│   │   ├── db/                # MongoDB Models (User, Issue)
│   │   ├── routes/            # API Endpoints
│   │   ├── services/          # Email Service
│   │   └── main.py            # Entry Point
│   ├── requirements.txt       # Dependencies
│   └── .env                   # Env Variables
│
└── rentresolve-frontend/      # Next.js Application
    ├── app/
    │   ├── landlord/          # Landlord Dashboard
    │   ├── tenant/            # Tenant Dashboard
    │   ├── profile/           # User Profile
    │   ├── login/             # Auth Pages
    │   └── globals.css        # Theme Variables
    ├── components/            # UI Components
    └── lib/                   # API Utilities
```

---

## ⚡ API Endpoints

Clean and RESTful API architecture:

- `POST /auth/signup` - Register new Tenant/Landlord
- `POST /auth/login` - Authenticate user
- `POST /issues` - Create new rental issue
- `GET /issues` - Fetch user-specific issues
- `GET /issues/{id}` - Get detailed issue view
- `POST /analyze/tenant` - AI Agent for Tenant Complaint Kit
- `POST /analyze/landlord` - AI Agent for Landlord Reply
- `POST /users/me` - Get/Update Profile
- `POST /email/send` - Trigger email notifications

---

## ⚡ How to Run Locally

### 1. Backend Setup
```bash
cd rentresolve-backend
python -m venv venv
.\venv\Scripts\Activate  # Windows
pip install -r requirements.txt
# Ensure .env has GOOGLE_API_KEY & DATABASE_URL
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd rentresolve-frontend
npm install
npm run dev
```

---
*Built by Jukal Adhitya*

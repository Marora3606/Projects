# AI Toolkit Hub (Multi-Domain Intelligence Platform)

An interactive, multi-domain AI intelligence dashboard built with Python and Streamlit. Features secure user authentication (bcrypt + JWT), domain-specific AI analysis, cybersecurity incident classification, ticket reporting, and a ChatGPT assistant interface supporting custom OpenAI-compatible proxy gateways (e.g., Bluesminds, OneAPI, local LLMs).

---

## 🌟 Key Features

* 🔐 **Secure User Authentication:** Login and Registration with `bcrypt` password hashing and JWT token management.
* 💬 **Domain-Specific AI Chatbot:** Interactive assistant tailored for **Cybersecurity**, **Data Science**, and **IT Operations**.
* 📊 **Analytics & Incident Reporting:** Visual charts (Plotly) for security incidents and IT tickets with automated AI root-cause analysis.
* 🌐 **Custom API Base URL Support:** Fully compatible with official OpenAI endpoints (`https://api.openai.com/v1`) as well as third-party OpenAI-compatible proxies (such as `https://api.bluesminds.com/v1` or local Ollama endpoints).
* ⚙️ **User & Appearance Settings:** Theme customization, password updates, and account management.

---

## 📁 Project Structure

```text
AI Toolkit Hub/
├── Home.py                  # Main entry point (Login, Signup, Overview Dashboard)
├── DATA/                    # Sample CSV datasets (Cyber incidents, IT tickets, metadata)
├── database/                # SQLite database connection module
├── models/                  # Database table schemas
├── services/                # Backend services (Auth, User Service, AI Assistant)
├── pages/
│   ├── 1_Dashboard.py       # Metrics & High-level overview
│   ├── 2_Analytics.py       # Visual analytics & AI incident analysis
│   ├── 4_Settings.py        # User profile & security settings
│   └── 5_Chatbot.py          # ChatGPT assistant with custom model support
├── .streamlit/
│   └── secrets.toml         # Secure API keys & Base URL configuration
├── pyproject.toml           # Project dependencies & package metadata
└── readme.md                # Project documentation
```

---

## 🛠️ Configuration (`.streamlit/secrets.toml`)

Create or update your `.streamlit/secrets.toml` file to configure your API keys and custom gateway endpoints:

### Using Official OpenAI Keys:
```toml
OPENAI_API_KEY = "sk-proj-your-official-openai-key"
OPENAI_BASE_URL = "https://api.openai.com/v1"
```

### Using Third-Party API Gateways (e.g., Bluesminds Proxy):
```toml
OPENAI_API_KEY = "sk-your-bluesminds-key"
OPENAI_BASE_URL = "https://api.bluesminds.com/v1"
```

---

## 🚀 How to Run the App

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   # OR
   pip install streamlit pandas plotly openai bcrypt pyjwt
   ```

2. **Launch Streamlit:**
   ```bash
   cd "AI Toolkit Hub"
   streamlit run Home.py
   ```

3. **Access the App:**
   Open your browser at `http://localhost:8501`.

---

## ❓ Troubleshooting

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **`401 Invalid API Key`** | OpenAI rejected a proxy key because `base_url` was missing. | Ensure `OPENAI_BASE_URL = "https://api.bluesminds.com/v1"` is set in `.streamlit/secrets.toml`. |
| **`403 Model Permission Denied`** | The provided API key does not have access to `gpt-4o-mini`. | Select an accessible model (such as `gpt-5.5`) in the Chatbot sidebar. |
| **Stuck on "Thinking..." / 504 Timeout** | Proxy gateway latency or stream chunking hang. | Chatbot automatically falls back to reliable non-streaming mode with a 30s timeout and clear error messages. |

---

## 👨‍💻 Author

**Manan Arora**  
*Built for Multi-Domain Intelligence & Security Analysis.*

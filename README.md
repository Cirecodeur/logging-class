# Hybrid AI Chatbot: OpenAI & Ollama

This project is a flexible AI assistant designed to bridge the gap between powerful cloud-based models and private, local execution. Whether you need the advanced reasoning of **GPT-4** or the privacy and cost-efficiency of **Ollama**, this tool handles both with integrated session logging.



## 🌟 Key Features

* **Dual-Model Support:** Switch instantly between OpenAI (Cloud) and Ollama (Local).
* **Persistent Logging:** All interactions are automatically saved to `chatbot_logs.json`.
* **Environment Safety:** Uses `.env` files to protect sensitive API credentials.
* **Clean CLI:** Simple command-line interface for seamless interaction.

---

## 🏗️ Project Structure

```text
.
├── app.py                 # Main entry point (CLI logic)
├── mest_chat_logging.py   # ChatBot class and logging engine
├── requirements.txt       # List of Python dependencies
├── .env                   # Sensitive API keys (ignored by Git)
├── .gitignore             # Files to exclude from Version Control
└── chatbot_logs.json      # Generated conversation history
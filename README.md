Oakstone Bank is a secure, modern, and lightweight web-based banking application developed with Python and Streamlit. It provides a premium "Obsidian" themed interface for users to manage their accounts, perform financial transactions, and maintain a detailed history of their banking activities.

🌟 Key Features
User Authentication: Secure account creation and PIN-protected login.

Transaction Engine: Perform seamless deposits and withdrawals with real-time balance updates.

Transaction Logs: An automated, chronological record of all financial movements.

Persistent Storage: Data is stored locally via a JSON file, ensuring information is saved between sessions.

Premium UI: A consistent, high-end "Obsidian" (dark) aesthetic that provides a sleek user experience.

🛠️ Tech Stack
Language: Python 3.x

Framework: Streamlit (UI & Web Server)

Database: JSON (Local data persistence)

Styling: Custom CSS/Markdown (Theme Engine)

🏗️ Project Architecture
The application is designed for modularity and ease of maintenance:

Data Vault: Handles all file I/O operations, ensuring account data is parsed from and saved to oakstone_users.json consistently.

UI/UX Layer: Uses custom CSS injection within st.markdown to enforce a unified brand identity across the entire application.

Logic Flow: Utilizes Streamlit's session management to route users through the "Our Story," "Login," and "Account Creation" modules.

💡 Future Scope
Cloud Database: Transitioning from local JSON storage to a cloud-based database like MongoDB Atlas or PostgreSQL.

Enhanced Security: Implementing Two-Factor Authentication (2FA) and hash-based password protection.

Notification System: Integrating automated email alerts for successful transactions.

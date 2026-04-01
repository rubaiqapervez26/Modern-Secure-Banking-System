# 🏦 Modern Secure Banking System

### 🌟 Project Overview
This project is a high-fidelity banking simulation that integrates **Object-Oriented Programming (OOP)** with core **Cybersecurity principles**. It provides a secure environment for users to manage finances while offering administrators a powerful dashboard for system oversight.

### 🛡️ Security Features
Security was the primary focus during development, moving beyond simple functionality to include:
* **Cryptographic Hashing:** User passwords are never stored in plaintext. We utilize **SHA-256** to create irreversible digital fingerprints of credentials.
* **Input Validation:** Extensive use of **Regular Expressions (Regex)** ensures that usernames and passwords meet complexity requirements and prevent injection attempts.
* **Secure Recovery:** A "Security Question" mechanism allows for safe password resets without exposing old credentials.
* **Audit Logging:** Every login attempt is recorded in `login_attempts.log` for forensic monitoring.



### 👥 Role-Based Dashboards

#### **1. User/Customer Features**
* **Unique Identity:** Every user is assigned a random 6-digit User ID upon registration.
* **Financial Tools:** Perform Deposits, Withdrawals (with balance checks), and peer-to-peer Transfers.
* **History:** Access a complete, timestamped history of all personal transactions.
* **UI Customization:** Integrated **Dark Mode** toggle for enhanced user experience.

#### **2. Administrator Features**
* **User Management:** View, search, and manage all registered accounts and roles.
* **System Analytics:** Real-time generation of transaction graphs (Deposits vs. Withdrawals) using **Matplotlib**.
* **Security Monitoring:** Access and review system-wide login logs to detect suspicious activity.



### 🛠️ Technical Stack
* **Language:** Python 3.x
* **GUI:** Tkinter (Custom themed with Dark Mode)
* **Data Storage:** JSON (structured persistence)
* **Cryptography:** Hashlib (SHA-256)
* **Visualization:** Matplotlib (Admin analytics)

### 📂 Repository Structure
* **`main.py`**: The primary entry point for the application (formerly `FINAL PROJECT.py`).
* **`users.json`**: (Auto-generated) Stores hashed user data and account balances.
* **`login_attempts.log`**: (Auto-generated) The security audit trail.
* **`Modern_Banking_Presentation.pptx`**: Visual guide to the system workflow and UI.

### 🚀 How to Run
1. Clone the repository.
2. Install the required visualization library:
   ```bash
   pip install matplotlib

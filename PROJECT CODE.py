# Modern Banking App with Dark Mode, Unique ID, and Admin Graphs
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import hashlib
import json
import os
import re
import random
from matplotlib import pyplot as plt

# --------- Helper Functions ---------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as file:
        return json.load(file)

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

def generate_user_id(users):
    while True:
        uid = str(random.randint(100000, 999999))
        if all(user.get("user_id") != uid for user in users.values()):
            return uid

# --------- Main Application Class ---------
class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Banking App")
        self.users = load_users()
        self.current_user = None
        self.dark_mode = False

        self.security_questions = [
            "What is your mother's maiden name?",
            "What was your first pet's name?",
            "What was your first school?",
            "What is your favorite food?",
            "What is your favorite color?"
        ]

        self.build_main_panel()

    def apply_theme(self):
        bg = "#2e2e2e" if self.dark_mode else "#ffffff"
        fg = "#ffffff" if self.dark_mode else "#000000"
        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_main_panel(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Modern Bank", font=("Helvetica", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="Admin", width=20, command=self.build_admin_login).pack(pady=10)
        tk.Button(self.root, text="User", width=20, command=self.build_user_login_panel).pack(pady=10)
        tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_theme).pack(pady=10)

    def build_user_login_panel(self):
        self.clear_screen()
        tk.Label(self.root, text="User Panel", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Button(self.root, text="Login", width=20, command=self.build_login_ui).pack(pady=10)
        tk.Button(self.root, text="Register", width=20, command=self.build_register_ui).pack(pady=10)
        tk.Button(self.root, text="Forgot Password", width=20, command=self.recover_password_ui).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.build_main_panel).pack(pady=10)

    def build_admin_login(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Login", font=("Helvetica", 16, "bold")).pack(pady=20)
        tk.Label(self.root, text="Enter Admin Password:").pack()
        pass_entry = tk.Entry(self.root, show="*")
        pass_entry.pack(pady=5)

        def validate():
            if pass_entry.get() == "admin123":
                self.current_user = "ADMIN"
                self.build_admin_panel()
            else:
                messagebox.showerror("Error", "Incorrect admin password")

        tk.Button(self.root, text="Login", command=validate).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.build_main_panel).pack(pady=5)

    def build_login_ui(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = hash_password(password_entry.get())
            user = self.users.get(username)
            if user and user["password"] == password:
                if user["role"] == "USER":
                    self.current_user = username
                    self.build_user_dashboard()
                else:
                    messagebox.showerror("Error", "Admin must login via Admin panel")
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.root, text="Login", command=login).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.build_user_login_panel).pack()

    def build_register_ui(self):
        self.clear_screen()
        tk.Label(self.root, text="Register", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        tk.Label(self.root, text="Security Question").pack()
        question_var = tk.StringVar()
        question_var.set(self.security_questions[0])
        question_menu = tk.OptionMenu(self.root, question_var, *self.security_questions)
        question_menu.pack()

        tk.Label(self.root, text="Answer").pack()
        answer_entry = tk.Entry(self.root)
        answer_entry.pack()

        def validate_username(name):
            return name.isalpha()

        def validate_password(password):
            return (len(password) >= 6 and
                    re.search(r'[A-Z]', password) and
                    re.search(r'[a-z]', password) and
                    re.search(r'[0-9]', password) and
                    re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

        def register():
            uname = username_entry.get()
            pwd = password_entry.get()
            ans = answer_entry.get()
            if not validate_username(uname):
                messagebox.showerror("Invalid Username", "Username must contain only letters")
                return
            if not validate_password(pwd):
                messagebox.showerror("Invalid Password", "Password must be strong with upper, lower, number, special char")
                return
            if not ans:
                messagebox.showerror("Missing Answer", "Please answer the security question")
                return
            if uname in self.users:
                messagebox.showerror("Error", "Username already exists")
                return
            uid = generate_user_id(self.users)
            self.users[uname] = {
                "user_id": uid,
                "password": hash_password(pwd),
                "role": "USER",
                "balance": 0.0,
                "transactions": [],
                "sec_q": question_var.get(),
                "sec_a": ans.lower()
            }
            save_users(self.users)
            messagebox.showinfo("Success", f"Registered. Your ID: {uid}")
            self.build_user_login_panel()

        tk.Button(self.root, text="Register", command=register).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.build_user_login_panel).pack()

    def recover_password_ui(self):
        self.clear_screen()
        tk.Label(self.root, text="Recover Password", font=("Helvetica", 16, "bold")).pack(pady=10)
        uname_entry = tk.Entry(self.root)
        uname_entry.pack()

        def ask_question():
            uname = uname_entry.get()
            user = self.users.get(uname)
            if not user:
                messagebox.showerror("Error", "User not found")
                return
            ans = simpledialog.askstring("Security Check", user["sec_q"])
            if ans and ans.lower() == user["sec_a"]:
                new_pass = simpledialog.askstring("Reset Password", "Enter new password", show='*')
                if new_pass:
                    user["password"] = hash_password(new_pass)
                    save_users(self.users)
                    messagebox.showinfo("Success", "Password reset successfully")
                    self.build_user_login_panel()
            else:
                messagebox.showerror("Error", "Wrong answer")

        tk.Button(self.root, text="Next", command=ask_question).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.build_user_login_panel).pack()

    def build_user_dashboard(self):
        self.clear_screen()
        user = self.users[self.current_user]
        tk.Label(self.root, text=f"Welcome {self.current_user} (User)", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Balance: ₹{user['balance']:.2f}", font=("Arial", 12)).pack(pady=5)


        def show_my_id():
            user = self.users[self.current_user]
            messagebox.showinfo("Your User ID", f"User ID: {user.get('user_id', 'N/A')}")


        def deposit():
            amt = simpledialog.askfloat("Deposit", "Enter amount")
            if amt and amt > 0:
                user["balance"] += amt
                user["transactions"].append(f"Deposited ₹{amt}")
                save_users(self.users)
                self.build_user_dashboard()

        def withdraw():
            amt = simpledialog.askfloat("Withdraw", "Enter amount")
            if amt and 0 < amt <= user["balance"]:
                user["balance"] -= amt
                user["transactions"].append(f"Withdrew ₹{amt}")
                save_users(self.users)
                self.build_user_dashboard()
            else:
                messagebox.showerror("Error", "Insufficient funds")

        def transfer():
            target = simpledialog.askstring("Transfer", "Transfer to username")
            amt = simpledialog.askfloat("Amount", "Enter amount")
            if target in self.users and target != self.current_user and amt and 0 < amt <= user["balance"]:
                self.users[target]["balance"] += amt
                self.users[target]["transactions"].append(f"Received ₹{amt} from {self.current_user}")
                user["balance"] -= amt
                user["transactions"].append(f"Transferred ₹{amt} to {target}")
                save_users(self.users)
                self.build_user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid transfer")

        def show_history():
            history_win = tk.Toplevel(self.root)
            history_win.title("Transaction History")
            for tx in user["transactions"]:
                tk.Label(history_win, text=tx).pack()

        def reset_password():
            ans = simpledialog.askstring("Security Check", user["sec_q"])
            if ans and ans.lower() == user["sec_a"]:
                new_pass = simpledialog.askstring("New Password", "Enter new password", show='*')
                if new_pass:
                    user["password"] = hash_password(new_pass)
                    save_users(self.users)
                    messagebox.showinfo("Success", "Password updated")
            else:
                messagebox.showerror("Error", "Wrong answer")

        tk.Button(self.root, text="Deposit", width=20, command=deposit).pack(pady=2)
        tk.Button(self.root, text="Withdraw", width=20, command=withdraw).pack(pady=2)
        tk.Button(self.root, text="Transfer", width=20, command=transfer).pack(pady=2)
        tk.Button(self.root, text="Transaction History", width=20, command=show_history).pack(pady=2)
        tk.Button(self.root, text="Show My User ID", width=20, command=show_my_id).pack(pady=2)
        tk.Button(self.root, text="Reset Password", width=20, command=reset_password).pack(pady=2)
        tk.Button(self.root, text="Logout", command=self.build_user_login_panel).pack(pady=10)

    def build_admin_panel(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome Admin", font=("Arial", 14)).pack(pady=10)

        def view_graph():
            deposits = withdrawals = 0
            for u in self.users.values():
                for tx in u["transactions"]:
                    if "Deposited" in tx:
                        deposits += float(tx.split("₹")[-1])
                    elif "Withdrew" in tx:
                        withdrawals += float(tx.split("₹")[-1])
            plt.bar(["Deposits", "Withdrawals"], [deposits, withdrawals], color=["green", "red"])
            plt.title("Bank Transaction Summary")
            plt.ylabel("Amount (₹)")
            plt.show()
 
        
        def list_users():
            user_win = tk.Toplevel(self.root)
            user_win.title("All Users")
            for uname, info in self.users.items():
                tk.Label(user_win, text=f"{uname} - ₹{info['balance']:.2f}").pack()

        def view_user_profile():
            uname = simpledialog.askstring("User Profile", "Enter username")
            if uname in self.users:
                info = self.users[uname]
                msg = f"Username: {uname}\nBalance: ₹{info['balance']:.2f}\nTransactions: {len(info['transactions'])}"
                messagebox.showinfo("User Profile", msg)
            else:
                messagebox.showerror("Error", "User not found")

        def reset_user_password():
            target = simpledialog.askstring("Reset Password", "Enter username")
            if target in self.users:
                new_pass = simpledialog.askstring("New Password", "Enter new password", show='*')
                if new_pass:
                    self.users[target]["password"] = hash_password(new_pass)
                    save_users(self.users)
                    messagebox.showinfo("Success", f"Password reset for {target}")
            else:
                messagebox.showerror("Error", "User not found")

        def view_transactions_summary():
            deposits = withdrawals = 0
            for u in self.users.values():
                for tx in u["transactions"]:
                    if "Deposited" in tx:
                        deposits += float(tx.split("\u20b9")[-1])
                    elif "Withdrew" in tx:
                        withdrawals += float(tx.split("\u20b9")[-1])
            total_users = len(self.users)
            total_balance = sum(u['balance'] for u in self.users.values())
            messagebox.showinfo("System Summary", f"Total Users: {total_users}\nTotal Balance: ₹{total_balance}\nTotal Deposits: ₹{deposits}\nTotal Withdrawals: ₹{withdrawals}")

        def delete_user():
            uname = simpledialog.askstring("Delete User", "Enter username")
            if uname in self.users:
                del self.users[uname]
                save_users(self.users)
                messagebox.showinfo("Deleted", f"User {uname} removed.")
            else:
                messagebox.showerror("Error", "User not found")

        def view_login_logs():
            if not os.path.exists("login_attempts.log"):
                messagebox.showinfo("Login Logs", "No logs available.")
                return
            with open("login_attempts.log", "r") as log:
                logs = log.read()
            log_win = tk.Toplevel(self.root)
            log_win.title("Login Attempts Log")
            txt = tk.Text(log_win, width=60, height=20)
            txt.insert(tk.END, logs)
            txt.pack()

        tk.Button(self.root, text="List Users", width=25, command=list_users).pack(pady=5)
        tk.Button(self.root, text="View User Profile", width=25, command=view_user_profile).pack(pady=5)
        tk.Button(self.root, text="Reset User Password", width=25, command=reset_user_password).pack(pady=5)
        tk.Button(self.root, text="Delete User", width=25, command=delete_user).pack(pady=5)
        tk.Button(self.root, text="System Summary", width=25, command=view_transactions_summary).pack(pady=5)
        tk.Button(self.root, text="View Login Logs", width=25, command=view_login_logs).pack(pady=5)
        tk.Button(self.root, text="Show Transaction Graph", width= 25, command=view_graph).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.build_main_panel).pack(pady=10)
# --------- Launch App ---------
root = tk.Tk()
root.geometry("400x500")
app = BankingApp(root)
root.mainloop()
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import hashlib
import json
import os
import re

# --------- Helper Functions ---------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as file:
        return json.load(file)

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

# --------- Banking App Class ---------
class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Banking App")
        self.root.geometry("400x450")
        self.users = load_users()
        self.build_login_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------- UI Builders ----------
    def build_login_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.login_username = tk.Entry(self.root)
        self.login_username.pack()

        tk.Label(self.root, text="Password").pack()
        self.login_password = tk.Entry(self.root, show="*")
        self.login_password.pack()

        tk.Button(self.root, text="Login", width=20, command=self.login).pack(pady=10)
        tk.Button(self.root, text="Forgot Password", command=self.password_recovery_ui).pack()
        tk.Button(self.root, text="Register", command=self.build_register_ui).pack(pady=5)

    def build_register_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Register", font=("Arial", 18, "bold")).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.reg_username = tk.Entry(self.root)
        self.reg_username.pack()

        tk.Label(self.root, text="Password").pack()
        self.reg_password = tk.Entry(self.root, show="*")
        self.reg_password.pack()

        tk.Label(self.root, text="Security Question (e.g., Your pet's name?)").pack()
        self.reg_sec_q = tk.Entry(self.root)
        self.reg_sec_q.pack()

        tk.Label(self.root, text="Answer").pack()
        self.reg_sec_a = tk.Entry(self.root)
        self.reg_sec_a.pack()

        tk.Button(self.root, text="Register", width=20, command=self.register_user).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.build_login_ui).pack()

    def password_recovery_ui(self):
        username = simpledialog.askstring("Password Recovery", "Enter your username:")
        if username not in self.users:
            messagebox.showerror("Error", "Username not found.")
            return

        user_data = self.users[username]
        question = user_data.get("security_question", "")
        answer = simpledialog.askstring("Security Question", question)
        if hash_password(answer) == user_data.get("security_answer"):
            new_password = simpledialog.askstring("Reset Password", "Enter new password:")
            if not new_password:
                return
            if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', new_password):
                messagebox.showerror("Error", "Password must be at least 8 characters with upper, lower case letters and a number.")
                return
            self.users[username]["password"] = hash_password(new_password)
            save_users(self.users)
            messagebox.showinfo("Success", "Password reset successful!")
        else:
            messagebox.showerror("Error", "Incorrect answer.")

    # ---------- Logic ----------
    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        if username not in self.users or self.users[username]['password'] != hash_password(password):
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        self.build_user_panel(username)
        self.build_user_dashboard()


    def register_user(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get().strip()
        sec_q = self.reg_sec_q.get().strip()
        sec_a = self.reg_sec_a.get().strip()

        # -------- Validation Start --------
        if not username or not password or not sec_q or not sec_a:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not re.match("^[a-zA-Z0-9_]+$", username):
            messagebox.showerror("Error", "Username must be alphanumeric (no spaces or special characters).")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
            return

        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', password):
            messagebox.showerror("Error", "Password must be at least 8 characters with upper, lower case letters and a number.")
            return
        # -------- Validation End --------

        uid = generate_user_id(self.users)
        self.users[username] = {
            "user_id": uid,
            "password": hash_password(password),
            "security_question": sec_q,
            "security_answer": hash_password(sec_a),
            "balance": 0,
            "transactions": []
        }
        save_users(self.users)
        messagebox.showinfo("Success", f"Registered. Your ID: {uid}")
        self.build_login_ui()
def build_user_dashboard(self):
    self.clear_screen()
    user = self.users[self.current_user]

    tk.Label(self.root, text=f"Welcome {self.current_user} (User)", font=("Arial", 14)).pack(pady=10)
    tk.Label(self.root, text=f"Your User ID: {user['user_id']}", font=("Arial", 12)).pack(pady=5)
    tk.Label(self.root, text=f"Balance: ₹{user['balance']:.2f}", font=("Arial", 12)).pack(pady=5)

    def show_my_id():
        user = self.users[self.current_user]
        messagebox.showinfo("Your User ID", f"User ID: {user.get('user_id', 'N/A')}")

    def deposit():
        amt = simpledialog.askfloat("Deposit", "Enter amount")
        if amt and amt > 0:
            user["balance"] += amt
            user["transactions"].append(f"Deposited ₹{amt}")
            save_users(self.users)
            self.build_user_dashboard()

    def withdraw():
        amt = simpledialog.askfloat("Withdraw", "Enter amount")
        if amt and 0 < amt <= user["balance"]:
            user["balance"] -= amt
            user["transactions"].append(f"Withdrew ₹{amt}")
            save_users(self.users)
            self.build_user_dashboard()
        else:
            messagebox.showerror("Error", "Insufficient funds")

    def transfer():
        target = simpledialog.askstring("Transfer", "Enter recipient username")
        target_id = simpledialog.askstring("Transfer", "Enter recipient User ID")
        amt  = simpledialog.askfloat("Amount", "Enter amount")

    if (
        target in self.users and
        self.users[target]["user_id"] == target_id and
        target != self.current_user and
        amt and 0 < amt <= user["balance"]
    ):
        sender_id = self.users[self.current_user]["user_id"]
        sender_name = self.current_user

        # Update receiver's account
        self.users[target]["balance"] += amt
        self.users[target]["transactions"].append(
            f"Received ₹{amt:.2f} from {sender_name} (ID: {sender_id})"
        )

        # Update sender's account
        user["balance"] -= amt
        user["transactions"].append(
            f"Transferred ₹{amt:.2f} to {target} (ID: {target_id})"
        )

        save_users(self.users)
        messagebox.showinfo("Success", f"Transferred ₹{amt:.2f} to {target} (ID: {target_id})")
        self.build_user_dashboard()
    else:
        messagebox.showerror("Error", "Invalid transfer details")


    def show_history():
        history_win = tk.Toplevel(self.root)
        history_win.title("Transaction History")
        for tx in user["transactions"]:
            tk.Label(history_win, text=tx).pack()

    def reset_password():
        ans = simpledialog.askstring("Security Check", user["sec_q"])
        if ans and ans.lower() == user["sec_a"]:
            new_pass = simpledialog.askstring("New Password", "Enter new password", show='*')
            if new_pass:
                user["password"] = hash_password(new_pass)
                save_users(self.users)
                messagebox.showinfo("Success", "Password updated")
        else:
            messagebox.showerror("Error", "Wrong answer")

    # Buttons
    tk.Button(self.root, text="💰 Deposit", width=20, command=deposit).pack(pady=2)
    tk.Button(self.root, text="💸 Withdraw", width=20, command=withdraw).pack(pady=2)
    tk.Button(self.root, text="🔁 Transfer", width=20, command=transfer).pack(pady=2)
    tk.Button(self.root, text="📜 Transaction History", width=20, command=show_history).pack(pady=2)
    tk.Button(self.root, text="🆔 Show My User ID", width=20, command=show_my_id).pack(pady=2)
    tk.Button(self.root, text="🔐 Reset Password" , width=20, command=reset_password).pack(pady=2)
    tk.Button(self.root, text="🚪 Logout", command=self.build_user_login_panel).pack(pady=10)

    def build_admin_panel(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome Admin", font=("Arial", 14)).pack(pady=10)

        def view_graph():
            deposits = withdrawals = 0
            for u in self.users.values():
                for tx in u["transactions"]:
                    if "Deposited" in tx:
                        deposits += float(tx.split("₹")[-1])
                    elif "Withdrew" in tx:
                        withdrawals += float(tx.split("₹")[-1])
            plt.bar(["Deposits", "Withdrawals"], [deposits, withdrawals], color=["green", "red"])
            plt.title("Bank Transaction Summary")
            plt.ylabel("Amount (₹)")
            plt.show()
 
        
        def list_users():
            users_win = tk.Toplevel(self.root)
            users_win.title("All Users")
            for username, data in self.users.items():
                tk.Label(users_win, text=f"Username: {username}, User ID: {data['user_id']}, Balance: ₹{data['balance']:.2f}").pack()


        def view_user_profile():
            uname = simpledialog.askstring("User Profile", "Enter username")
            if uname in self.users:
                info = self.users[uname]
                msg = f"Username: {uname}\nUser ID: {info.get('user_id', 'N/A')}\nBalance: ₹{info['balance']:.2f}\nTransactions: {len(info['transactions'])}"
                messagebox.showinfo("User Profile", msg)
            else:
                messagebox.showerror("Error", "User not found")

        def reset_user_password():
            target = simpledialog.askstring("Reset Password", "Enter username")
            if target in self.users:
                new_pass = simpledialog.askstring("New Password", "Enter new password", show='*')
                if new_pass:
                    self.users[target]["password"] = hash_password(new_pass)
                    save_users(self.users)
                    messagebox.showinfo("Success", f"Password reset for {target}")
            else:
                messagebox.showerror("Error", "User not found")

        def view_transactions_summary():
            deposits = withdrawals = 0
            for u in self.users.values():
                for tx in u["transactions"]:
                    if "Deposited" in tx:
                        deposits += float(tx.split("\u20b9")[-1])
                    elif "Withdrew" in tx:
                        withdrawals += float(tx.split("\u20b9")[-1])
            total_users = len(self.users)
            total_balance = sum(u['balance'] for u in self.users.values())
            messagebox.showinfo("System Summary", f"Total Users: {total_users}\nTotal Balance: ₹{total_balance}\nTotal Deposits: ₹{deposits}\nTotal Withdrawals: ₹{withdrawals}")

        def delete_user():
            uname = simpledialog.askstring("Delete User", "Enter username")
            if uname in self.users:
                del self.users[uname]
                save_users(self.users)
                messagebox.showinfo("Deleted", f"User {uname} removed.")
            else:
                messagebox.showerror("Error", "User not found")

        def view_login_logs():
            if not os.path.exists("login_attempts.log"):
                messagebox.showinfo("Login Logs", "No logs available.")
                return
            with open("login_attempts.log", "r") as log:
                logs = log.read()
            log_win = tk.Toplevel(self.root)
            log_win.title("Login Attempts Log")
            txt = tk.Text(log_win, width=60, height=20)
            txt.insert(tk.END, logs)
            txt.pack()

        tk.Button(self.root, text="📋 List Users", width=25, command=list_users).pack(pady=5)
        tk.Button(self.root, text="👤 View User Profile", width=25, command=view_user_profile).pack(pady=5)
        tk.Button(self.root, text="🔐 Reset User Password", width=25, command=reset_user_password).pack(pady=5)
        tk.Button(self.root, text="🗑️ Delete User", width=25, command=delete_user).pack(pady=5)
        tk.Button(self.root, text="📊 System Summary", width=25, command=view_transactions_summary).pack(pady=5)
        tk.Button(self.root, text="🧾 View Login Logs", width=25, command=view_login_logs).pack(pady=5)
        tk.Button(self.root, text="📈 Show Transaction Graph", width= 25, command=view_graph).pack(pady=5)
        tk.Button(self.root, text="🚪 Logout", command=self.build_main_panel).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()

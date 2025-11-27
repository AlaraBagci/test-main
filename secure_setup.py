import os
import getpass
from database import Database
from auth import AuthManager

def create_secure_base_data():
    if os.path.exists("wellbeing.db"):
        os.remove("wellbeing.db")
        print("🗑️  Old database deleted.")

    db = Database("wellbeing.db")
    auth = AuthManager(db)

    print("\n--- 🛡️ SECURE SYSTEM SETUP ---")
    
    # 1. Create ADMIN
    print("1. Creating ADMIN account...")
    admin_pass = getpass.getpass("   Set Password for 'admin': ")
    auth.register("admin", admin_pass, role="admin")

    # 2. Create PROFESSOR
    print("2. Creating PROFESSOR account...")
    prof_pass = getpass.getpass("   Set Password for 'prof_smith': ")
    auth.register("prof_smith", prof_pass, role="professor")

    print("\n🎉 Setup Complete.")

if __name__ == "__main__":
    create_secure_base_data()
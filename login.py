import streamlit as st
import os
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Login - AI Attendance System",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for login page
st.markdown("""
<style>
    .main {
        background-color: #111;
        color: white;
    }
    .stButton > button {
        background-color: #FF0000;
        color: white;
        border: 2px solid #FF0000;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #CC0000;
        border-color: #CC0000;
    }
    .login-container {
        background-color: #222;
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #FF0000;
        margin: 20px auto;
        max-width: 400px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Default admin credentials
DEFAULT_ADMIN = {
    "admin": "admin123",
    "manager": "manager123",
    "user": "user123"
}

# Load custom credentials if exists
def load_credentials():
    cred_file = "credentials.json"
    if os.path.exists(cred_file):
        try:
            with open(cred_file, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_ADMIN
    return DEFAULT_ADMIN

# Save credentials
def save_credentials(credentials):
    with open("credentials.json", 'w') as f:
        json.dump(credentials, f, indent=2)

# Login function
def authenticate(username, password):
    credentials = load_credentials()
    return username in credentials and credentials[username] == password

# Main login page
def login_page():
    st.markdown("<h1 style='text-align: center; color: #FF0000;'>🔐 AI Attendance System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>Login Required</h3>", unsafe_allow_html=True)
    
    # Login container
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
        
        if submit:
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Default credentials info
    st.markdown("---")
    st.markdown("### 📋 Default Credentials:")
    st.markdown("""
    - **Admin**: `admin` / `admin123`
    - **Manager**: `manager` / `manager123`
    - **User**: `user` / `user123`
    """)

# Admin panel for managing users
def admin_panel():
    st.markdown("<h2 style='color: #FF0000;'>👨‍💼 Admin Panel</h2>", unsafe_allow_html=True)
    
    credentials = load_credentials()
    
    # Add new user
    with st.expander("➕ Add New User"):
        with st.form("add_user"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            add_user = st.form_submit_button("Add User")
            
            if add_user and new_username and new_password:
                credentials[new_username] = new_password
                save_credentials(credentials)
                st.success(f"✅ User '{new_username}' added successfully!")
    
    # Remove user
    with st.expander("🗑️ Remove User"):
        with st.form("remove_user"):
            users = list(credentials.keys())
            user_to_remove = st.selectbox("Select user to remove", users)
            remove_user = st.form_submit_button("Remove User")
            
            if remove_user and user_to_remove != "admin":
                del credentials[user_to_remove]
                save_credentials(credentials)
                st.success(f"✅ User '{user_to_remove}' removed successfully!")
            elif user_to_remove == "admin":
                st.error("❌ Cannot remove admin user!")
    
    # View all users
    with st.expander("👥 View All Users"):
        st.markdown("### Current Users:")
        for user in credentials.keys():
            st.markdown(f"- **{user}**")
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

# Main app logic
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        # Show welcome message
        st.markdown(f"<h2 style='color: #FF0000;'>Welcome, {st.session_state.username}!</h2>", unsafe_allow_html=True)
        
        # Admin panel for admin user
        if st.session_state.username == "admin":
            admin_panel()
        
        # Logout button
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🎯 Next Steps:")
        st.markdown("1. **Start Face Recognition**: Run the face recognition app")
        st.markdown("2. **Open Attendance Dashboard**: Run the main attendance app")
        st.markdown("3. **Monitor Attendance**: Watch for live face detections")

if __name__ == "__main__":
    main() 
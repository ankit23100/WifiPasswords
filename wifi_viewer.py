import subprocess
import streamlit as st
import platform

def get_wifi_profiles():
    """Fetch all Wi-Fi profiles."""
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], stderr=subprocess.DEVNULL).decode('utf-8', errors="ignore").split('\n')
        return [i.split(":")[1].strip() for i in data if "All User Profile" in i]
    except subprocess.CalledProcessError as e:
        return [("Error fetching profiles", str(e))]

def get_wifi_password(profile):
    """Fetch Wi-Fi password for a given profile."""
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], stderr=subprocess.DEVNULL).decode('utf-8', errors="ignore").split('\n')
        passwords = [b.split(":")[1].strip() for b in results if "Key Content" in b]
        return passwords[0] if passwords else "None"
    except subprocess.CalledProcessError:
        return "Error retrieving password"


st.title("🔐 Wi-Fi Profiles and Passwords Viewer")
st.write("This application retrieves and displays saved Wi-Fi profiles and their passwords (Windows Only).")

if platform.system() != "Windows":
    st.error("This app only works on Windows systems.")
else:
    if st.button("Show Wi-Fi Profiles"):
        profiles = get_wifi_profiles()
        
        if not profiles:
            st.warning("No Wi-Fi profiles found or an error occurred.")
        else:
            wifi_data = {"Wi-Fi Profile": [], "Password": []}
            for profile in profiles:
                password = get_wifi_password(profile)
                wifi_data["Wi-Fi Profile"].append(profile)
                wifi_data["Password"].append(password)

            st.dataframe(wifi_data)

    if st.button("Refresh"):
        st.experimental_rerun()

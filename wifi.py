import subprocess

def get_wifi_passwords():
    # Get the list of all Wi-Fi profiles
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    profiles = [line.split(":")[1].strip() for line in data if "All User Profile" in line]

    for profile in profiles:
        try:
            # Show the profile details including the password
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
            # Extract the password
            password = [b.split(":")[1].strip() for b in results if "Key Content" in b]
            print(f"Wi-Fi: {profile} | Password: {password[0] if password else 'None'}")
        except subprocess.CalledProcessError:
            print(f"Could not retrieve password for {profile}")

if __name__ == "__main__":
    get_wifi_passwords()
    input("\nPress Enter to exit...")

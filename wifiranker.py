import subprocess
import time
import speedtest

def connect_to_wifi(ssid):
    try:
        subprocess.run(["nmcli", "device", "wifi", "connect", ssid], check=True)
        print(f"Connected to {ssid}")
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to connect to {ssid}")
        return False

def get_wifi_speed():
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1000000  # Convert to Mbps
        return download_speed
    except (speedtest.ConfigRetrievalError, speedtest.SpeedtestException):
        print("Unable to perform speed test. Network may be unreachable.")
        return None

def disconnect_wifi():
    subprocess.run(["nmcli", "device", "disconnect", "wlp1s0"], check=True)             # change wlp1s0 to your wifi adapter name wlan0 maybe you can check by ifconfig
    print("Disconnected from Wi-Fi")

def format_time(seconds):
    if seconds >= 60:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    else:
        return f"{seconds:.2f} seconds"

def main():
    start_time = time.time()  # Record the start time

    wifi_networks = [                                   #add networks here
        #"Boys Hostel SF 4G",
        #"Boys Hostel FF 4G",
        #"Boys Hostel GF 4G",
        #"Boys Hostel SF 5G"
    ]

    network_speeds = {}

    for network in wifi_networks:
        print(f"\nTesting {network}")
        if connect_to_wifi(network):
            time.sleep(5)  # Wait for connection to stabilize
            speed = get_wifi_speed()
            if speed is not None:
                network_speeds[network] = speed
                print(f"Speed: {speed:.2f} Mbps")
            disconnect_wifi()
        time.sleep(2)  # Wait before next connection

    if network_speeds:
        best_network = max(network_speeds, key=network_speeds.get)
        print(f"\nBest network: {best_network} with speed {network_speeds[best_network]:.2f} Mbps")
        connect_to_wifi(best_network)
    else:
        print("No networks could be tested successfully.")

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time
    print(f"\nTotal time taken: {format_time(total_time)}")

if __name__ == "__main__":
    main()

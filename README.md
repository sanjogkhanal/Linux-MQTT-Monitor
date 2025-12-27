# 🌟 Linux-MQTT-Monitor - Monitor Your Linux Server Effortlessly

[![Download Latest Release](https://img.shields.io/badge/Download%20Latest%20Release-v1.0-blue)](https://github.com/sanjogkhanal/Linux-MQTT-Monitor/releases)

## 🚀 Getting Started

Linux-MQTT-Monitor is a simple Python script designed to monitor the health of your Linux server. It checks CPU usage, RAM, temperatures, Docker containers, and services. The data is then sent to an MQTT broker, making it easy to track your server's health. This tool is especially useful for Home Assistant users as it uses MQTT Auto-Discovery to automatically add sensors without the need for manual setup.

## 📥 Download & Install

To start using Linux-MQTT-Monitor, follow these steps:

1. Visit the [Releases page](https://github.com/sanjogkhanal/Linux-MQTT-Monitor/releases) to download the latest version.
2. Look for the version number you want to download.
3. Download the appropriate file for your system. You may find options for different Linux distributions or platforms.
4. After the download is complete, locate the file on your computer, and follow the instructions below to run it.

## ⚙️ System Requirements

Before you begin, ensure your system meets the following:

- A Linux-based operating system (Ubuntu, Debian, CentOS, etc.)
- Python 3.7 or later installed
- Access to an MQTT broker (like Mosquitto)
- Basic familiarity with running scripts in your terminal

## 🔧 Running the Script

After downloading the script, here's how to run it:

1. Open your terminal.
2. Navigate to the folder where the script is saved. You can do this by typing `cd /path/to/your/folder`.
3. Make the script executable by running:
   ```bash
   chmod +x linux_mqtt_monitor.py
   ```
4. Run the script with the following command:
   ```bash
   python3 linux_mqtt_monitor.py
   ```

## 📊 Configuration

To customize the monitoring settings, you need to edit the configuration file:

1. Inside the folder where the script is located, find `config.json`. 
2. Open it with any text editor.
3. Modify the parameters to match your server setup and MQTT broker information. Key settings to look for include:
   - MQTT broker address
   - Username and password (if required)
   - Sensor update intervals

Be sure to save your changes before closing the editor.

## ✅ Features

- **Health Monitoring**: Tracks CPU, RAM, temperatures, Docker containers, and system services.
- **MQTT Integration**: Sends data to any MQTT broker.
- **Automatic Sensor Discovery**: Works seamlessly with Home Assistant, eliminating the need for manual YAML configuration.
- **Lightweight**: Designed to consume minimal system resources.

## 💡 Troubleshooting

If you encounter issues, consider the following:

- Ensure Python 3.7+ is correctly installed. You can check by running:
  ```bash
  python3 --version
  ```
  
- Verify your MQTT broker is running and accessible. You can do this using tools like MQTT Explorer.

- Check if the configuration file matches your broker settings. 

For additional help, feel free to open an issue in the [GitHub repository](https://github.com/sanjogkhanal/Linux-MQTT-Monitor/issues).

## 🛠️ Contributing

If you'd like to contribute, please follow these guidelines:

1. Fork the project on GitHub.
2. Create your feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

## ⚡ License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🌐 Stay Connected

For updates and community discussions, follow the repository. You can also check out discussions around server monitoring, automation, and Home Assistant on platforms like Reddit and various forums.

## 📚 Additional Resources

- [Home Assistant - Getting Started](https://www.home-assistant.io/getting-started/)
- [MQTT Protocol Overview](https://mqtt.org/)
- [Python Official Documentation](https://docs.python.org/3/)

[![Download Latest Release](https://img.shields.io/badge/Download%20Latest%20Release-v1.0-blue)](https://github.com/sanjogkhanal/Linux-MQTT-Monitor/releases)
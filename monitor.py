#!/usr/bin/env python3

import json
import os
import re
import socket
import subprocess
import sys
import time
from signal import SIGINT, SIGTERM, signal

import paho.mqtt.client as mqtt
import psutil

# ──────────────────────────────────────────────────────────────────────────────
#  User‑specific settings
# ──────────────────────────────────────────────────────────────────────────────
BROKER            = "xxx.xxx.xxx.xxx"
PORT              = 1883
USERNAME          = "YOUR_USERNAME"
PASSWORD          = "YOUR_PASSWORD"
TOPIC             = "home/server/stats"          
DISCOVERY_PREFIX  = "homeassistant"
DEVICE_NAME       = "main_server"                
POLL_INTERVAL_SEC = 15

CONTAINERS = [                                   # list the container *names*
    "plex", "paho_mqtt_broker", "ntopng",
    "cloudflare-cloudflared-1", "photoprism",
    "ntfy", "filebrowser", "portainer",
]
CPU_CORES = psutil.cpu_count(logical=True) or 1  
# ──────────────────────────────────────────────────────────────────────────────


CLIENT_ID = f"server_stats_{socket.gethostname()}"


# ═════════════════════════════════════════════════════════════════════════════
#  Helper functions
# ═════════════════════════════════════════════════════════════════════════════
def get_first_cpu_temp() -> float | None:
    temps = psutil.sensors_temperatures(fahrenheit=False)
    if not temps:
        return None

    for entries in temps.values():         
        for entry in entries:
            if entry.current is not None:
                return round(entry.current, 1)
    return None                            


def get_uptime() -> str:
    return subprocess.check_output("uptime -p", shell=True).decode().strip()


def get_docker_status() -> dict:
    try:
        out = subprocess.check_output(
            ["docker", "ps", "-a", "--format", "{{.Names}}={{.Status}}"]
        )
        lines = out.decode().splitlines()
        return {ln.split("=", 1)[0]: ln.split("=", 1)[1] for ln in lines}
    except Exception as exc:
        return {"error": str(exc)}


def get_jellyfin_status() -> str:
    try:
        out = subprocess.check_output(["systemctl", "is-active", "jellyfin"])
        return out.decode().strip()
    except subprocess.CalledProcessError:
        return "unknown"


def get_stats() -> dict:
    return {
        "cpu_per_core": psutil.cpu_percent(percpu=True),
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "uptime": get_uptime(),
        "load_avg": os.getloadavg(),
        "temp_c": get_first_cpu_temp(),
        "docker": get_docker_status(),
        "jellyfin": get_jellyfin_status(),
        # add more if needed 
    }


# ═════════════════════════════════════════════════════════════════════════════
#  MQTT discovery
# ═════════════════════════════════════════════════════════════════════════════
def publish_discovery(client: mqtt.Client) -> None:
    for container in CONTAINERS:
        object_id = container.replace("_", "-")
        topic_cfg = f"{DISCOVERY_PREFIX}/sensor/{DEVICE_NAME}/{object_id}/config"

        value_tmpl = (
            "{{ 'running' if value_json.docker.get('"
            + container
            + "', '') | regex_match('^Up') else 'stopped' }}"
        )

        payload = {
            "name": f"{container} Container",
            "state_topic": TOPIC,
            "value_template": value_tmpl,
            "unique_id": f"{DEVICE_NAME}_{object_id}_container",
            "icon": "mdi:docker",
            "device": {
                "identifiers": [DEVICE_NAME],
                "name": "Main Server",
                "manufacturer": "Farouk Server",
                "model": "Linux MQTT Monitor",
            },
        }
        client.publish(topic_cfg, json.dumps(payload), retain=True)

    for idx in range(CPU_CORES):
        obj_id = f"cpu_core_{idx+1}"
        topic_cfg = f"{DISCOVERY_PREFIX}/sensor/{DEVICE_NAME}/{obj_id}/config"
        payload = {
            "name": f"CPU Core {idx+1}",
            "state_topic": TOPIC,
            "unit_of_measurement": "%",
            "value_template": f"{{{{ value_json.cpu_per_core[{idx}] }}}}",
            "state_class": "measurement",
            "unique_id": f"{DEVICE_NAME}_{obj_id}",
            "device": {
                "identifiers": [DEVICE_NAME],
                "name": "Main Server",
                "manufacturer": "Farouk Server",
                "model": "Linux MQTT Monitor",
            },
        }
        client.publish(topic_cfg, json.dumps(payload), retain=True)

    generic_defs = [
        ("cpu_total", "CPU Total", "%", "{{ value_json.cpu_percent }}", True),
        ("ram_usage", "RAM Usage", "%", "{{ value_json.ram_percent }}", True),
        ("temp", "CPU Temp", "°C", "{{ value_json.temp_c }}", True),
        ("load_1m", "Load 1m", None, "{{ value_json.load_avg[0] }}", False),
        ("load_5m", "Load 5m", None, "{{ value_json.load_avg[1] }}", False),
        ("load_15m", "Load 15m", None, "{{ value_json.load_avg[2] }}", False),
        ("uptime", "System Uptime", None, "{{ value_json.uptime }}", False),
        ("jellyfin", "Jellyfin Status", None, "{{ value_json.jellyfin }}", False),
    ]

    for obj_id, name, unit, template, measurable in generic_defs:
        topic_cfg = f"{DISCOVERY_PREFIX}/sensor/{DEVICE_NAME}/{obj_id}/config"
        payload = {
            "name": name,
            "state_topic": TOPIC,
            "value_template": template,
            "unique_id": f"{DEVICE_NAME}_{obj_id}",
            "device": {
                "identifiers": [DEVICE_NAME],
                "name": "Main Server",
                "manufacturer": "Farouk Server",
                "model": "Linux MQTT Monitor",
            },
        }
        if unit:
            payload["unit_of_measurement"] = unit
        if measurable:
            payload["state_class"] = "measurement"

        client.publish(topic_cfg, json.dumps(payload), retain=True)


# ═════════════════════════════════════════════════════════════════════════════
#  MQTT callbacks & main loop
# ═════════════════════════════════════════════════════════════════════════════
def on_connect(client, _userdata, _flags, rc):
    print(f"[MQTT] Connected, result code {rc}")
    publish_discovery(client)


def on_disconnect(_client, _userdata, rc):
    print(f"[MQTT] Disconnected (rc={rc})")


def graceful_exit(_sig_num, _frame):
    print("\nExiting …")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    sys.exit(0)


if __name__ == "__main__":
    signal(SIGTERM, graceful_exit)
    signal(SIGINT, graceful_exit)

    mqtt_client = mqtt.Client(client_id=CLIENT_ID)
    mqtt_client.username_pw_set(USERNAME, PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect

    mqtt_client.connect(BROKER, PORT, keepalive=60)
    mqtt_client.loop_start()

    try:
        while True:
            mqtt_client.publish(TOPIC, json.dumps(get_stats()), qos=0, retain=False)
            time.sleep(POLL_INTERVAL_SEC)
    finally:
        graceful_exit(None, None)

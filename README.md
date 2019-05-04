# Somecomfort Homie

Homie 3 implementation of Honeywell Total Connect Comfort for North American models

Uses the somecomfort library (https://github.com/kk7ds/somecomfort)

Install using 

```
pip install Somecomfort-Homie-3
```

To start as a service on raspbian 

Create somecomfort_homie.yml in /etc using the following settings:

```yaml
somecomfort:
  username: 
  password: 

mqtt:
  MQTT_BROKER: Broker
  MQTT_PORT: 1883
  MQTT_USERNAME: null
  MQTT_PASSWORD: null
```

Create somecomfort-homie.service in /etc/systemd/system

```service
[Unit]
Description=Somecomfort Homie
After=multi-user.target

[Service]
User=pi
Type=simple
ExecStart=/usr/bin/python3 /usr/local/bin/somecomfort_homie_start.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

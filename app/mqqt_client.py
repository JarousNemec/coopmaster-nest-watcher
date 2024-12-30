import paho.mqtt.client as mqtt

class NestMQTTClient:
    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set("admin", "password")

    def connect(self):
        self.mqtt_client.connect(self.broker, self.port, 60)
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Úspěšně připojeno k brokeru")
            # Přihlášení k odběru tématu
            client.subscribe("test/tema")
        else:
            print("Připojení selhalo, kód výsledku: ", rc)

    # Definice callback funkce při přijetí zprávy
    def on_message(self, client, userdata, msg):
        print(f"Přijatá zpráva z {msg.topic}: {msg.payload.decode()}")






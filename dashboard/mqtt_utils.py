import paho.mqtt.client as mqtt
import ssl
from .models import MQTTData
from django.db import transaction
import time

class MyMQTTData:
    def __init__(self):
        self.data = {'temperature': None}

    def update(self, topic, payload):
        self.data[topic] = float(payload)

    def save(self):
        with transaction.atomic():
            mqtt_data = MQTTData(
                temperature=self.data['temperature']
            )
            mqtt_data.save()
            print("Data saved:", self.data)

mqtt_data = MyMQTTData()  # Gunakan kelas MyMQTTData

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()

    mqtt_data.update(topic, payload)

    # Jika ada data untuk kedua topik, simpan ke dalam database
    if all(value is not None for value in mqtt_data.data.values()):
        mqtt_data.save()
        print(f"Received message on topics 'current' and 'temperature': {mqtt_data.data['temperature']}")
        # time.sleep(.5)
        client.loop_stop()
        
    

def subscribe_to_hivemq():
    client = mqtt.Client()
    client.on_message = on_message

    # Konfigurasi TLS jika diperlukan (pastikan Anda memiliki sertifikat TLS)
    sslContext = ssl.create_default_context()
    client.tls_set_context(sslContext)

    # Konfigurasi otentikasi jika diperlukan (ganti dengan informasi otentikasi Anda)
    client.username_pw_set(username='RamaPMPD', password='Kerasakti123')

    # Hubungkan ke broker HiveMQ (ganti dengan alamat host dan port HiveMQ yang sesuai)
    client.connect('b5208bedc9794c2397ead6f7870bb494.s1.eu.hivemq.cloud', port=8883)

    # Berlangganan ke topik tertentu (ganti dengan topik yang sesuai dengan kebutuhan Anda)
    client.subscribe('temperature')
    

    # Mulai loop untuk mendengarkan pesan
    client.loop_start()

    
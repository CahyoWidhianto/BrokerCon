import paho.mqtt.client as mqtt
import ssl
from dashboard.models import MQTTData
from django.db import transaction
import time
import json
import paho.mqtt.subscribe as subscribe


class MyMQTTData:
    def __init__(self):
        self.data = {'current': None, 'temperature': None, 'vibration': None}

    def update(self, topic, payload):
        # self.data[topic] = float(payload)
        # Mengubah payload menjadi dictionary
        data_list = payload.split(' ')
        self.data = {
            'temperature': float(data_list[0]),
            'current': float(data_list[1]),
            'vibration': float(data_list[2])
        }

    def save(self):
        # with transaction.atomic():
        mqtt_data = MQTTData(
            temperature=self.data['temperature'],
            current=self.data['current'],
            vibration=self.data['vibration'],
         )
        mqtt_data.save()

mqtt_data = MyMQTTData()  # Gunakan kelas MyMQTTData
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    
    mqtt_data.update(topic, payload)
    print(f"Received message on topic '{topic}': {payload}")
    if mqtt_data.data['current'] == 0:
        status = {"status": "Server is offline"}
    else:
        if all(value is not None for value in mqtt_data.data.values()):
            mqtt_data.save()
            # time.sleep(.5)
            client.loop_stop()
            status = {"status": "Server is online"}
    print(status)

    # publish_to_hivemq('status', status)
    
    # if mqtt_data.data['current'] != 0:
    # # Jika ada data untuk topik, simpan ke dalam database
    #     if all(value is not None for value in mqtt_data.data.values()):
    #         mqtt_data.save()
    #         time.sleep(.5)
    #         client.loop_stop()
        

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
    client.subscribe('dataSensor')
    # client.subscribe('vibration')
    # client.subscribe('temperature')
    # client.subscribe('current')

    # Mulai loop untuk mendengarkan pesan
    # client.loop_forever()
    client.loop_start()
    

def publish_to_hivemq(topic, message):
    # Buat klien MQTT
    client = mqtt.Client()

    # Konfigurasi TLS jika diperlukan (pastikan Anda memiliki sertifikat TLS)
    sslContext = ssl.create_default_context()
    client.tls_set_context(sslContext)

    # Konfigurasi otentikasi jika diperlukan (ganti dengan informasi otentikasi Anda)
    client.username_pw_set(username='RamaPMPD', password='Kerasakti123')

    # Hubungkan ke broker HiveMQ (ganti dengan alamat host dan port HiveMQ yang sesuai)
    client.connect('b5208bedc9794c2397ead6f7870bb494.s1.eu.hivemq.cloud', port=8883)

    # Publish pesan ke topik tertentu
    client.publish(topic, message)

    # Menunggu pesan diproses dan kemudian menutup koneksi dengan broker
    client.loop_forever()


def subs_baru():
    username = "RamaPMPD"
    password = "Kerasakti123"
    host = "b5208bedc9794c2397ead6f7870bb494.s1.eu.hivemq.cloud"
    port = 8883
    topic = "dataSensor"
    # Subscribe to the specified topic using subscribe.simple()
    msg = subscribe.simple(
        topic,
        hostname=host,
        port=port,
        auth={"username": username, "password": password},
        tls={"ca_certs": None, "certfile": None, "keyfile": None},
    )
    
    mqtt_data = MyMQTTData()
    
    mqtt_data.update(payload=msg.payload.decode())
    

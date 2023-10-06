from django.shortcuts import render
from dashboard.models import MQTTData
from django.http import HttpResponse,JsonResponse
from .mqtt_utils import subscribe_to_hivemq
import threading

# Create your views here.
def start_hivemq_subscription(request):
    subscribe_thread = threading.Thread(target=subscribe_to_hivemq)
    subscribe_thread.start()
    return HttpResponse("HiveMQ subscription started successfully")

# def last_mqtt_data(request):
#     # Ambil data terakhir dari model MQTTData
#     latest_data = MQTTData.objects.latest('timestamp')
#     # Render template dengan data terakhir
#     return render(request, 'last_mqtt_data.html', {'latest_data': latest_data})

def dashboard(request):
    return render(request, 'dashboard.html')


def get_dashboard_data(request):
    
    subscribe_thread = threading.Thread(target=subscribe_to_hivemq)
    subscribe_thread.start()
    
    # Get dashboard data from sensor record database
    #ketika arus != 0 data di harapkan di save ke dalam database, namun jika current bernilai 0 diharapkan proses add data berhenti
    
    data_sensor = MQTTData.objects.order_by("-pk")[0]
    # print(data_sensor.temperature, data_sensor.current)
    sensorValue = {
        "currentValue" : data_sensor.current,
        "temperatureValue" : data_sensor.temperature,
        "vibrationValue" : data_sensor.vibration,
    }
    # print(sensorValue)
    return JsonResponse(sensorValue)


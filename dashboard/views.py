from django.shortcuts import render
from dashboard.models import MQTTData
from django.http import HttpResponse,JsonResponse
from .mqtt_utils import subscribe_to_hivemq, publish_to_hivemq, mqtt_data
import threading

# Create your views here.
def start_hivemq_subscription(request):
    subscribe_thread = threading.Thread(target=subscribe_to_hivemq)
    subscribe_thread.start()
    return HttpResponse("HiveMQ subscription started successfully")

def publish_message(request):
    # Panggil fungsi publish_to_hivemq dengan parameter yang sesuai
    publish_to_hivemq('warning', 'warning')
    return HttpResponse("asu asu")

def dashboard(request):
    return render(request, 'dashboard.html')

def get_status(request):
    status = "Server is online" if mqtt_data.data['current'] != 0 else "Server is offline"
    response_data = {'status': status}
    return JsonResponse(response_data)


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


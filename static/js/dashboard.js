// All variables are stored here
const dashboardCard = {
  temperatureValue: document.querySelector("#temperature-value .card-text"),
  currentValue: document.querySelector("#current-value .card-text"),
  vibrationValue: document.querySelector("#vibration-value .card-text"),
};

updateRealTimeClock();
async function updateRealTimeClock() {
  const realTimeClockElement = document.getElementById("real-time-clock");
  const currentDate = new Date();
  const options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  };
  const formattedDateTime = currentDate.toLocaleDateString(undefined, options);
  realTimeClockElement.innerText = formattedDateTime;
  console.log(formattedDateTime);
}
setInterval(updateRealTimeClock, 1000);



getDashboardData();
async function getDashboardData() {
  let prevMinute = null;

  async function updateTime() {
    const nowMinute = new Date().getMinutes();

    if (nowMinute !== prevMinute) {
      await getSensorData();
      prevMinute = nowMinute;
    }
  }

  async function getSensorData() {
    try {
      const response = await fetch("/get-dashboard-data/");
      const data = await response.json();
      const sensorValue = {
        currentValue: data["currentValue"],
        temperatureValue: data["temperatureValue"],
        vibrationValue: data["vibrationValue"],
      };
      console.log(sensorValue);
      for (const key in dashboardCard) {
        console.log(key);
        if (dashboardCard.hasOwnProperty(key)) {
          const value = sensorValue[key];
          dashboardCard[key].textContent = value;
        }
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
  // Call updateTime every 100 milliseconds
  setInterval(updateTime, 100);
}

async function getStatus() {
    try {
      const response = await fetch('/get-status/');
      const data = await response.json();
      document.getElementById('status').textContent = `Status: ${data.status}`;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  // Panggil getStatus saat halaman dimuat
  getStatus();

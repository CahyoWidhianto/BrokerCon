// All variables are stored here
const dashboardCard = {
    temperatureValue: document.querySelector("#temperature-value .card-text"),
};


// The end of stored variables

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

            // Update sensor values on the dashboard
            const sensorValue = data["temperatureValue"];
            console.log(sensorValue);
            for (const key in dashboardCard) {
                console.log(key);
                if (dashboardCard.hasOwnProperty(key)) {
                    const value = sensorValue;
                    dashboardCard[key].textContent = value;
                }
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    // Call updateTime every 100 milliseconds
    setInterval(updateTime, 1000);
}
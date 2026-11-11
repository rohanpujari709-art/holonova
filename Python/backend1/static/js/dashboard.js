async function loadDashboard() {

    try {

        const response = await fetch("/api/dashboard");

        const data = await response.json();

        document.getElementById("totalHolograms").innerHTML =
            data.total_holograms;

        document.getElementById("totalUploads").innerHTML =
            data.total_uploads;

        document.getElementById("cloudStorage").innerHTML =
            data.cloud_storage;

        document.getElementById("espStatus").innerHTML =
            data.esp32_status;

    }

    catch (error) {

        console.log(error);

    }

}

loadDashboard();
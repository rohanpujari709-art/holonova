const fileInput = document.getElementById("fileInput");
const previewBtn = document.getElementById("previewBtn");
const previewArea = document.getElementById("previewArea");

previewBtn.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    // Preview
    previewArea.innerHTML = "";

    if (file.type.startsWith("image")) {

        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.style.width = "350px";
        img.style.marginTop = "20px";

        previewArea.appendChild(img);

    }

    else if (file.type.startsWith("video")) {

        const video = document.createElement("video");
        video.src = URL.createObjectURL(file);
        video.controls = true;
        video.style.width = "400px";

        previewArea.appendChild(video);

    }

    // Upload to FastAPI
    const formData = new FormData();
    formData.append("file", file);

    try {

        previewBtn.disabled = true;
        previewBtn.innerText = "Uploading...";

        const response = await fetch("http://127.0.0.1:8000/upload", {

            method: "POST",
            body: formData

        });

        const result = await response.json();

        console.log(result);

        if (result.success) {

            alert(
                "Upload Successful!\n\n" +
                "Hologram ID : " + result.hologram_id +
                "\nResolution : " +
                result.width +
                " x " +
                result.height
            );

        }

        else {

            alert("Upload Failed");

        }

    }

    catch (error) {

        console.error(error);

        alert("Cannot connect to FastAPI backend.");

    }

    finally {

        previewBtn.disabled = false;
        previewBtn.innerText = "Preview";

    }

});
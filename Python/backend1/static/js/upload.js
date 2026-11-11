const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const uploadBtn = document.getElementById("uploadBtn");
const statusDiv = document.getElementById("status");


// ==========================================================
// IMAGE PREVIEW
// ==========================================================

imageInput.addEventListener("change", () => {

    const file = imageInput.files[0];

    if (!file) {
        return;
    }

    preview.src = URL.createObjectURL(file);

    preview.style.display = "block";
});


// ==========================================================
// UPLOAD
// ==========================================================

uploadBtn.addEventListener("click", async () => {

    const file = imageInput.files[0];


    if (!file) {

        alert("Please select an image.");

        return;
    }


    statusDiv.innerHTML = `
        <p style="color:#38bdf8;">
            Uploading and creating hologram...
        </p>
    `;


    const formData = new FormData();

    formData.append(
        "file",
        file
    );


    try {

        const response = await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );


        const result = await response.json();


        console.log(
            "UPLOAD RESPONSE:",
            result
        );


        // --------------------------------------------------
        // CHECK ERROR
        // --------------------------------------------------

        if (!response.ok) {

            throw new Error(
                result.detail ||
                "Upload failed"
            );
        }


        // --------------------------------------------------
        // SUCCESS
        // --------------------------------------------------

        if (
            result.success &&
            result.hologram_id
        ) {

            statusDiv.innerHTML = `
                <h3 style="color:#22c55e;">
                    Upload Successful
                </h3>

                <p>
                    Opening hologram preview...
                </p>

                <p>
                    Hologram ID:
                    <br>
                    <b>${result.hologram_id}</b>
                </p>
            `;


            // ----------------------------------------------
            // REDIRECT TO HOLOGRAM PREVIEW
            // ----------------------------------------------

            setTimeout(() => {

                window.location.href =
                    `/hologram/${result.hologram_id}`;

            }, 800);

        }

        else {

            throw new Error(
                "Hologram ID was not returned"
            );
        }


    }

    catch (error) {

        console.error(
            "UPLOAD ERROR:",
            error
        );


        statusDiv.innerHTML = `
            <p style="color:#ef4444;">
                Upload failed:
                ${error.message}
            </p>
        `;
    }

});
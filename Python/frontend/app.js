// ============================================================
// HOLONOVA WEB APP
// ============================================================

const API_BASE_URL = "http://127.0.0.1:8000";


// ============================================================
// GET HTML ELEMENTS
// ============================================================

const fileInput =
    document.getElementById("fileInput");

const fileInfo =
    document.getElementById("fileInfo");

const uploadBtn =
    document.getElementById("uploadBtn");

const mediaPreview =
    document.getElementById("mediaPreview");

const savedHolograms =
    document.getElementById("savedHolograms");

const ledCanvas =
    document.getElementById("ledCanvas");

const preview =
    document.getElementById("preview");


// ============================================================
// CANVAS
// ============================================================

let ctx = null;

if (ledCanvas) {

    ctx =
        ledCanvas.getContext("2d");

}


// ============================================================
// APPLICATION START
// ============================================================

console.log("======================================");
console.log("       HOLONOVA WEB APP STARTED");
console.log("======================================");

console.log(
    "Backend:",
    API_BASE_URL
);

console.log(
    "File input:",
    fileInput
);

console.log(
    "Media preview:",
    mediaPreview
);

console.log(
    "LED canvas:",
    ledCanvas
);


// Load saved holograms when page opens

loadSavedHolograms();


// ============================================================
// IMAGE SELECT
// ============================================================

if (fileInput) {

    fileInput.addEventListener(
        "change",
        handleFileSelect
    );

}


// ============================================================
// HANDLE FILE SELECT
// ============================================================

function handleFileSelect(event) {

    console.log("");
    console.log(
        "======================================"
    );

    console.log(
        "IMAGE SELECTED"
    );

    console.log(
        "======================================"
    );


    const file =
        event.target.files[0];


    // ------------------------------------------
    // CHECK FILE
    // ------------------------------------------

    if (!file) {

        console.log(
            "No file selected."
        );

        return;
    }


    console.log(
        "Filename:",
        file.name
    );

    console.log(
        "File type:",
        file.type
    );

    console.log(
        "File size:",
        file.size,
        "bytes"
    );


    // ------------------------------------------
    // CHECK IMAGE
    // ------------------------------------------

    if (
        !file.type.startsWith("image/")
    ) {

        alert(
            "Please select an image file."
        );

        return;
    }


    // ------------------------------------------
    // SHOW FILE INFORMATION
    // ------------------------------------------

    if (fileInfo) {

        fileInfo.innerHTML = `

            <strong>
                ${escapeHTML(file.name)}
            </strong>

            <br>

            Size:
            ${(file.size / 1024).toFixed(2)}
            KB

            <br>

            Type:
            ${escapeHTML(file.type)}

        `;

    }


    // ------------------------------------------
    // SHOW ORIGINAL IMAGE
    // ------------------------------------------

    showMediaPreview(file);


    // ------------------------------------------
    // SHOW UPLOAD BUTTON
    // ------------------------------------------

    if (uploadBtn) {

        uploadBtn.style.display =
            "inline-block";

        uploadBtn.disabled =
            false;

        uploadBtn.textContent =
            "Process Hologram";

    }

}


// ============================================================
// MEDIA PREVIEW
// ============================================================

function showMediaPreview(file) {

    console.log(
        "Creating media preview..."
    );


    if (!mediaPreview) {

        console.error(
            "ERROR: mediaPreview element not found."
        );

        return;
    }


    // ------------------------------------------
    // CLEAR PREVIOUS IMAGE
    // ------------------------------------------

    mediaPreview.innerHTML = "";


    // ------------------------------------------
    // CREATE IMAGE URL
    // ------------------------------------------

    const imageURL =
        URL.createObjectURL(file);


    console.log(
        "Image URL created."
    );


    // ------------------------------------------
    // CREATE IMAGE ELEMENT
    // ------------------------------------------

    const img =
        document.createElement("img");


    img.src =
        imageURL;


    img.alt =
        "Selected image preview";


    // ------------------------------------------
    // IMAGE STYLE
    // ------------------------------------------

    img.style.display =
        "block";

    img.style.maxWidth =
        "100%";

    img.style.width =
        "auto";

    img.style.maxHeight =
        "400px";

    img.style.height =
        "auto";

    img.style.margin =
        "20px auto";

    img.style.objectFit =
        "contain";

    img.style.border =
        "2px solid #38bdf8";

    img.style.borderRadius =
        "10px";


    // ------------------------------------------
    // IMAGE LOADED
    // ------------------------------------------

    img.onload =
        function () {

            console.log(
                "Media preview loaded successfully."
            );

            console.log(
                "Original image resolution:",
                img.naturalWidth,
                "x",
                img.naturalHeight
            );

            // Release temporary URL
            URL.revokeObjectURL(
                imageURL
            );

        };


    // ------------------------------------------
    // IMAGE ERROR
    // ------------------------------------------

    img.onerror =
        function () {

            console.error(
                "Could not load media preview."
            );


            mediaPreview.innerHTML = `

                <p
                    style="
                        color:red;
                        text-align:center;
                    "
                >
                    Could not display image preview.
                </p>

            `;


            URL.revokeObjectURL(
                imageURL
            );

        };


    // ------------------------------------------
    // ADD IMAGE
    // ------------------------------------------

    mediaPreview.appendChild(
        img
    );


    console.log(
        "Media preview added to page."
    );

}


// ============================================================
// UPLOAD BUTTON
// ============================================================

if (uploadBtn) {

    uploadBtn.addEventListener(
        "click",
        uploadHologram
    );

}


// ============================================================
// UPLOAD HOLOGRAM
// ============================================================

async function uploadHologram() {

    console.log("");
    console.log(
        "======================================"
    );

    console.log(
        "UPLOADING HOLOGRAM"
    );

    console.log(
        "======================================"
    );


    // ------------------------------------------
    // GET FILE
    // ------------------------------------------

    if (
        !fileInput ||
        !fileInput.files[0]
    ) {

        alert(
            "Please select an image first."
        );

        return;
    }


    const file =
        fileInput.files[0];


    console.log(
        "Uploading:",
        file.name
    );


    // ------------------------------------------
    // DISABLE BUTTON
    // ------------------------------------------

    uploadBtn.disabled =
        true;

    uploadBtn.textContent =
        "Processing...";


    try {

        // --------------------------------------
        // FORM DATA
        // --------------------------------------

        const formData =
            new FormData();


        formData.append(
            "file",
            file
        );


        // --------------------------------------
        // SEND TO FASTAPI
        // --------------------------------------

        const response =
            await fetch(
                `${API_BASE_URL}/upload`,
                {
                    method: "POST",
                    body: formData
                }
            );


        console.log(
            "Upload status:",
            response.status
        );


        // --------------------------------------
        // CHECK RESPONSE
        // --------------------------------------

        if (!response.ok) {

            const errorText =
                await response.text();


            throw new Error(
                errorText
            );
        }


        // --------------------------------------
        // READ JSON
        // --------------------------------------

        const result =
            await response.json();


        console.log(
            "Upload result:",
            result
        );


        // --------------------------------------
        // CHECK ID
        // --------------------------------------

        if (
            !result.hologram_id
        ) {

            throw new Error(
                "Hologram ID was not returned."
            );
        }


        console.log(
            "Hologram created:",
            result.hologram_id
        );


        // --------------------------------------
        // RELOAD SAVED HOLOGRAMS
        // --------------------------------------

        await loadSavedHolograms();


        // --------------------------------------
        // OPEN CREATED HOLOGRAM
        // --------------------------------------

        await openSavedHologram(
            result.hologram_id
        );


        uploadBtn.textContent =
            "Processed ✓";


    }
    catch (error) {

        console.error(
            "UPLOAD ERROR:",
            error
        );


        if (fileInfo) {

            fileInfo.innerHTML = `

                <strong
                    style="color:red;"
                >
                    Upload failed
                </strong>

                <br><br>

                ${escapeHTML(
                    error.message
                )}

            `;

        }


        uploadBtn.textContent =
            "Process Hologram";

    }
    finally {

        uploadBtn.disabled =
            false;

    }

}


// ============================================================
// LOAD SAVED HOLOGRAMS
// ============================================================

async function loadSavedHolograms() {

    console.log("");
    console.log(
        "Loading saved holograms..."
    );


    if (!savedHolograms) {

        console.error(
            "savedHolograms element not found."
        );

        return;
    }


    savedHolograms.innerHTML = `

        <p>
            Loading holograms...
        </p>

    `;


    try {

        // --------------------------------------
        // REQUEST
        // --------------------------------------

        const response =
            await fetch(
                `${API_BASE_URL}/holograms`
            );


        console.log(
            "Holograms status:",
            response.status
        );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );

        }


        // --------------------------------------
        // JSON
        // --------------------------------------

        const result =
            await response.json();


        console.log(
            "Holograms result:",
            result
        );


        const holograms =
            result.holograms || [];


        // --------------------------------------
        // CLEAR
        // --------------------------------------

        savedHolograms.innerHTML =
            "";


        // --------------------------------------
        // EMPTY
        // --------------------------------------

        if (
            holograms.length === 0
        ) {

            savedHolograms.innerHTML = `

                <p>
                    No holograms found.
                </p>

            `;

            return;
        }


        // --------------------------------------
        // CREATE CARDS
        // --------------------------------------

        holograms.forEach(
            function (hologram) {

                const card =
                    document.createElement(
                        "div"
                    );


                card.className =
                    "saved-card";


                card.innerHTML = `

                    <h3>
                        ${escapeHTML(
                            hologram.image_name ||
                            "Hologram"
                        )}
                    </h3>


                    <p>

                        Resolution:
                        ${hologram.width}
                        ×
                        ${hologram.height}

                    </p>


                    <p>

                        Frames:
                        ${hologram.total_frames}

                    </p>


                    <p>

                        Status:
                        ${escapeHTML(
                            hologram.status ||
                            "unknown"
                        )}

                    </p>


                    <button
                        type="button"
                        class="open-hologram-btn"
                    >

                        Open Hologram

                    </button>

                `;


                const button =
                    card.querySelector(
                        ".open-hologram-btn"
                    );


                button.addEventListener(
                    "click",
                    function () {

                        openSavedHologram(
                            hologram.id
                        );

                    }
                );


                savedHolograms.appendChild(
                    card
                );

            }
        );


        console.log(
            "Saved holograms loaded:",
            holograms.length
        );

    }
    catch (error) {

        console.error(
            "LOAD HOLOGRAM ERROR:",
            error
        );


        savedHolograms.innerHTML = `

            <p
                style="color:red;"
            >

                Could not load saved holograms.

            </p>

        `;

    }

}


// ============================================================
// OPEN SAVED HOLOGRAM
// ============================================================

async function openSavedHologram(
    hologramId
) {

    console.log("");
    console.log(
        "======================================"
    );

    console.log(
        "OPENING HOLOGRAM"
    );

    console.log(
        "Hologram ID:",
        hologramId
    );

    console.log(
        "======================================"
    );


    try {

        // ====================================================
        // GET HOLOGRAM INFORMATION
        // ====================================================

        const hologramResponse =
            await fetch(
                `${API_BASE_URL}/hologram/${hologramId}`
            );


        console.log(
            "Hologram response:",
            hologramResponse.status
        );


        // ------------------------------------------
        // CHECK RESPONSE
        // ------------------------------------------

        if (
            !hologramResponse.ok
        ) {

            const errorText =
                await hologramResponse.text();


            console.error(
                "Hologram API error:",
                errorText
            );


            throw new Error(
                "Could not load hologram information."
            );

        }


        // ------------------------------------------
        // GET JSON
        // ------------------------------------------

        const hologramResult =
            await hologramResponse.json();


        console.log(
            "Hologram result:",
            hologramResult
        );


        // ------------------------------------------
        // GET HOLOGRAM OBJECT
        // ------------------------------------------

        const hologram =
            hologramResult.hologram;


        if (!hologram) {

            throw new Error(
                "Hologram object is missing."
            );

        }


        console.log(
            "Hologram:",
            hologram
        );


        // ====================================================
        // GET LED FRAME
        // ====================================================

        const ledResponse =
            await fetch(
                `${API_BASE_URL}/led-frame/${hologramId}`
            );


        console.log(
            "LED response:",
            ledResponse.status
        );


        // ------------------------------------------
        // CHECK LED RESPONSE
        // ------------------------------------------

        if (
            !ledResponse.ok
        ) {

            const errorText =
                await ledResponse.text();


            console.error(
                "LED API error:",
                errorText
            );


            throw new Error(
                "Could not load LED frame."
            );

        }


        // ------------------------------------------
        // JSON
        // ------------------------------------------

        const ledFrame =
            await ledResponse.json();


        console.log(
            "LED frame:",
            ledFrame
        );


        // ------------------------------------------
        // GET LED DATA
        // ------------------------------------------

        const ledData =
            ledFrame.led_data;


        if (!ledData) {

            throw new Error(
                "LED data is missing."
            );

        }


        if (
            !Array.isArray(ledData)
        ) {

            throw new Error(
                "LED data is not an array."
            );

        }


        if (
            ledData.length === 0
        ) {

            throw new Error(
                "LED data is empty."
            );

        }


        console.log(
            "LED height:",
            ledData.length
        );


        console.log(
            "LED width:",
            ledData[0].length
        );


        console.log(
            "First pixel:",
            ledData[0][0]
        );


        // ====================================================
        // DRAW MATRIX
        // ====================================================

        drawLEDMatrix(
            ledData
        );


        // ====================================================
        // SHOW INFORMATION
        // ====================================================

        showHologramInfo(
            hologram
        );


        // ====================================================
        // SCROLL TO PREVIEW
        // ====================================================

        if (preview) {

            preview.scrollIntoView({

                behavior:
                    "smooth",

                block:
                    "start"

            });

        }


        console.log(
            "Hologram opened successfully."
        );

    }
    catch (error) {

        console.error(
            "OPEN HOLOGRAM ERROR:",
            error
        );


        alert(
            error.message
        );

    }

}


// ============================================================
// DRAW LED MATRIX
// ============================================================

function drawLEDMatrix(
    ledData
) {

    console.log("");
    console.log(
        "======================================"
    );

    console.log(
        "DRAWING LED MATRIX"
    );

    console.log(
        "======================================"
    );


    // ------------------------------------------
    // CHECK CANVAS
    // ------------------------------------------

    if (!ledCanvas) {

        console.error(
            "ledCanvas not found."
        );

        return;
    }


    if (!ctx) {

        console.error(
            "Canvas context not found."
        );

        return;
    }


    // ------------------------------------------
    // CHECK DATA
    // ------------------------------------------

    if (
        !Array.isArray(ledData)
    ) {

        console.error(
            "LED data is not an array."
        );

        return;
    }


    if (
        ledData.length === 0
    ) {

        console.error(
            "LED data is empty."
        );

        return;
    }


    const height =
        ledData.length;


    const width =
        ledData[0].length;


    console.log(
        "Matrix:",
        width,
        "x",
        height
    );


    // ------------------------------------------
    // CANVAS SIZE
    // ------------------------------------------

    ledCanvas.width =
        512;

    ledCanvas.height =
        512;


    // ------------------------------------------
    // BLACK BACKGROUND
    // ------------------------------------------

    ctx.fillStyle =
        "black";


    ctx.fillRect(
        0,
        0,
        ledCanvas.width,
        ledCanvas.height
    );


    // ------------------------------------------
    // PIXEL SIZE
    // ------------------------------------------

    const pixelWidth =
        ledCanvas.width /
        width;


    const pixelHeight =
        ledCanvas.height /
        height;


    // ------------------------------------------
    // DRAW PIXELS
    // ------------------------------------------

    for (
        let y = 0;
        y < height;
        y++
    ) {

        const row =
            ledData[y];


        if (
            !Array.isArray(row)
        ) {

            continue;
        }


        for (
            let x = 0;
            x < width;
            x++
        ) {

            const pixel =
                row[x];


            if (
                !Array.isArray(pixel) ||
                pixel.length < 3
            ) {

                continue;
            }


            let r =
                Number(pixel[0]);


            let g =
                Number(pixel[1]);


            let b =
                Number(pixel[2]);


            // Clamp RGB values

            r =
                Math.max(
                    0,
                    Math.min(
                        255,
                        r
                    )
                );


            g =
                Math.max(
                    0,
                    Math.min(
                        255,
                        g
                    )
                );


            b =
                Math.max(
                    0,
                    Math.min(
                        255,
                        b
                    )
                );


            // Set pixel color

            ctx.fillStyle =
                `rgb(${r}, ${g}, ${b})`;


            // Draw pixel

            ctx.fillRect(

                x * pixelWidth,

                y * pixelHeight,

                Math.ceil(
                    pixelWidth
                ) + 1,

                Math.ceil(
                    pixelHeight
                ) + 1

            );

        }

    }


    console.log(
        "LED matrix drawn successfully."
    );

}


// ============================================================
// SHOW HOLOGRAM INFORMATION
// ============================================================

function showHologramInfo(
    hologram
) {

    if (!preview) {

        return;
    }


    let info =
        document.getElementById(
            "hologramInfo"
        );


    // ------------------------------------------
    // CREATE INFO BOX
    // ------------------------------------------

    if (!info) {

        info =
            document.createElement(
                "div"
            );


        info.id =
            "hologramInfo";


        preview.appendChild(
            info
        );

    }


    // ------------------------------------------
    // DISPLAY INFORMATION
    // ------------------------------------------

    info.innerHTML = `

        <h3>
            Hologram Information
        </h3>


        <p>

            <strong>
                Image:
            </strong>

            ${escapeHTML(
                hologram.image_name ||
                "Unknown"
            )}

        </p>


        <p>

            <strong>
                Resolution:
            </strong>

            ${hologram.width || 0}
            ×
            ${hologram.height || 0}

        </p>


        <p>

            <strong>
                Frames:
            </strong>

            ${hologram.total_frames || 0}

        </p>


        <p>

            <strong>
                Status:
            </strong>

            ${escapeHTML(
                hologram.status ||
                "Unknown"
            )}

        </p>


        <p>

            <strong>
                Hologram ID:
            </strong>

            ${escapeHTML(
                hologram.id ||
                ""
            )}

        </p>

    `;

}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(
    value
) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";
    }


    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}               
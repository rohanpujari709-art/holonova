async function loadGallery() {

    try {

        const response = await fetch("/api/gallery");

        const holograms = await response.json();

        const container = document.getElementById("galleryContainer");

        container.innerHTML = "";

        if (holograms.length === 0) {

            container.innerHTML = `
                <div class="card">
                    <h2>No holograms uploaded yet.</h2>
                </div>
            `;

            return;
        }

        holograms.forEach(item => {

            container.innerHTML += `

                <div class="card">

                    <h2>${item.image_name}</h2>

                    <hr>

                    <p><strong>ID</strong></p>

                    <small>${item.id}</small>

                    <br><br>

                    <p><strong>Resolution</strong></p>

                    <p>${item.width} × ${item.height}</p>

                    <br>

                    <p><strong>Total Frames</strong></p>

                    <p>${item.total_frames}</p>

                    <br>

                    <p><strong>Status</strong></p>

                    <p>${item.status}</p>

                    <br>

                    <button
                        onclick="window.location.href='/hologram/${item.id}'">
                        View Details
                    </button>

                </div>

            `;

        });

    }

    catch (error) {

        console.error("Gallery Error:", error);

        document.getElementById("galleryContainer").innerHTML = `
            <div class="card">
                <h2>Failed to load gallery.</h2>
            </div>
        `;

    }

}

loadGallery();
const apiBaseUrl = "http://127.0.0.1:8000/images";

// Create a new image
document.getElementById("create-image-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const slug = document.getElementById("slug").value;
  const imageUrl = document.getElementById("image-url").value;

  try {
    const response = await fetch(`${apiBaseUrl}/create_image/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, slug, image: imageUrl }),
    });
    const data = await response.json();
    alert(response.ok ? "Image created successfully!" : `Error: ${JSON.stringify(data.errors)}`);
  } catch (error) {
    console.error("Error creating image:", error);
  }
});

// Fetch all images
document.getElementById("fetch-images").addEventListener("click", async () => {
  try {
    const response = await fetch(`${apiBaseUrl}/list_image/`);
    const data = await response.json();

    // Log the data for debugging purposes
    console.log("Response from /list_image/: ", data);

    const imageList = document.getElementById("image-list");
    imageList.innerHTML = "";

    for (const item of data) {
      const imageCard = document.createElement("div");
      imageCard.className = "image-card";

      // Use title as the slug fallback
      const slug = item.title || "Unknown slug";

      const imageSrc = item.image.startsWith("http") ? item.image : `/media/${item.image}`;

      imageCard.innerHTML = `
        <h3>${item.title}</h3>
        <img src="${imageSrc}" alt="${item.title}" style="max-width: 100%; height: auto;">
        <p>Slug: ${slug}</p>
        <p>Page Location: ${item.page_location || "Unknown"}</p>
        <p>Section: ${item.section || "Unknown"}</p>
      `;
      imageList.appendChild(imageCard);
    }
  } catch (error) {
    console.error("Error fetching images:", error);
    alert("An error occurred while fetching the images.");
  }
});




// Get a specific image by slug
document.getElementById("get-image-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const slug = document.getElementById("image-slug").value;
  
  if (!slug) {
    alert("Please enter a slug.");
    return;
  }

  try {
    const response = await fetch(`/images/get_image/${slug}/`);
    const data = await response.json();

    const singleImageResult = document.getElementById("single-image-result");

    if (response.ok) {
      // Fix here - don't prepend '/media/' redundantly if the URL is already absolute
      const imagePath = data.image.image.startsWith("http") 
        ? data.image.image 
        : `/media/${data.image.image}`;

      singleImageResult.innerHTML = `
        <h3>${data.image.name}</h3>
        <img src="${imagePath}" alt="${data.image.name}" style="max-width: 100%; height: auto;">
        <p>Slug: ${data.image.slug_field}</p>
        <p>Page Location: ${data.image.page_location}</p>
        <p>Section: ${data.image.section}</p>
      `;
    } else {
      singleImageResult.innerHTML = `<p>Error: ${JSON.stringify(data.errors)}</p>`;
    }
  } catch (error) {
    console.error("Error fetching image:", error);
    alert("An error occurred while fetching the image. Please try again.");
  }
});

const apiBaseUrl = "http://127.0.0.1:8000/images";

// Function to fetch CSRF token from cookies
function getCSRFToken() {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    if (cookie.trim().startsWith('csrftoken=')) {
      return cookie.trim().split('=')[1];
    }
  }
  return '';
}

// Handle the form submission
document.getElementById("create-image-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  
  // Get the form values
  const name = document.getElementById("name").value;
  const slug_field = document.getElementById("slug_field").value;
  const page_location = document.getElementById("page_location").value;
  const section = document.getElementById("section").value;
  const image_url = document.getElementById("image_url").value;
  const imageFile = document.getElementById("image").files[0];

  // Check if a file was selected
  if (!imageFile) {
    alert("Please select an image file.");
    return;
  }

  try {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('slug_field', slug_field);
    formData.append('page_location', page_location);
    formData.append('section', section);
    formData.append('image_url', image_url);
    formData.append('image', imageFile);

    const response = await fetch(`${apiBaseUrl}/create_image/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(), // Include CSRF token
      },
      body: formData,
    });

    const result = await response.json();

    if (response.ok) {
      document.getElementById("response-message").innerText = result.message;
      console.log("Server Response:", result);
    } else {
      document.getElementById("response-message").innerText = `Error: ${JSON.stringify(result.errors)}`;
      console.error("Server Response Error:", result.errors);
    }
  } catch (error) {
    console.error("Error creating image:", error);
    document.getElementById("response-message").innerText = "An error occurred.";
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

      // Correctly map the slug from the server response
      const slug = item.slug_field || "Unknown slug";
      const pageLocation = item.page_location || "Unknown";
      const section = item.section || "Unknown";

      // Handle image path
      const imageSrc = item.image.startsWith("http") ? item.image : `/media/${item.image}`;

      imageCard.innerHTML = `
        <h3>${item.name}</h3>
        <img src="${imageSrc}" alt="${item.name}" style="max-width: 100%; height: auto;">
        <p>Slug: ${slug}</p>
        <p>Page Location: ${pageLocation}</p>
        <p>Section: ${section}</p>
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

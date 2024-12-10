const apiBaseUrl = "http://127.0.0.1:8000/images";

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('image-form');
  const responseMessage = document.getElementById('response-message');
  
  // Extract CSRF token from cookies
  const getCSRFToken = () => {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith('csrftoken=')) {
              return cookie.split('=')[1];
          }
      }
      return '';
  };

  form.addEventListener('submit', async (event) => {
      event.preventDefault();

      const formData = new FormData(form);

      try {
          const response = await fetch('/create_image/', {
              method: 'POST',
              headers: {
                  'X-CSRFToken': getCSRFToken(), // Send CSRF token in request header
              },
              body: formData,
          });

          const data = await response.json();

          if (response.ok) {
              responseMessage.innerHTML = `<p style="color: green;">Image uploaded successfully! Response: ${JSON.stringify(data)}</p>`;
          } else {
              responseMessage.innerHTML = `<p style="color: red;">Error: ${JSON.stringify(data.errors)}</p>`;
          }
      } catch (error) {
          responseMessage.innerHTML = `<p style="color: red;">Unexpected error occurred: ${error.message}</p>`;
      }
  });
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

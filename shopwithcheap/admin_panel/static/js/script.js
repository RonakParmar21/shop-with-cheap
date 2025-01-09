function validateForm() {
  let isValid = true;

  // Clear previous error messages
  const errorElements = document.querySelectorAll(".error");
  errorElements.forEach((error) => (error.innerHTML = ""));

  // Email validation
  const email = document.getElementById("email").value;
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  if (email.trim() === "") {
    document.getElementById("emailError").textContent = "Email is required.";
    isValid = false;
  } else if (!emailPattern.test(email)) {
    document.getElementById("emailError").textContent =
      "Please enter a valid email.";
    isValid = false;
  }

  // Password validation
  const password = document.getElementById("password").value;
  if (password.trim() === "") {
    document.getElementById("passwordError").textContent =
      "Password is required.";
    isValid = false;
  }

  return isValid;
}

// Event listener for form submission
// document
//   .getElementById("loginForm")
//   .addEventListener("submit", function (event) {
//     if (!validateForm()) {
//       event.preventDefault();
//     }
//   });

/**
 *
 * add sub category
 *
 */

document
  .getElementById("add-subcategory-form")
  .addEventListener("click", () => console.log("Button click"));

document
  .getElementById("add-subcategory-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const category = document.getElementById("category-select").value;
    const subcategory = document.getElementById("subcategory-input").value;

    if (category && subcategory) {
      alert(`Category: ${category}\nSubcategory: ${subcategory}`);
      // Reset the form after submission
      this.reset();
    } else {
      alert("Please fill in all fields.");
    }
  });

/***
 *
 * success model popup
 *
 */
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("success-modal");
  if (modal) {
    setTimeout(() => {
      modal.style.display = "none";
    }, 3000);
  }
});

document.addEventListener('DOMContentLoaded', function() {
  // Event listener for category change
  document.getElementById('category-select').addEventListener('change', function() {
      const category = this.value;
      
      // Make an AJAX call to fetch subcategories based on selected category
      fetch(`?category=${category}`)
          .then(response => response.text())
          .then(data => {
              // Update subcategory dropdown options based on response data
              document.getElementById('category-select-subcategory').innerHTML = data;
          });
  });
});

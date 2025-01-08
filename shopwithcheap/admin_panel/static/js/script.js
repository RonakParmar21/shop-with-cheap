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
document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    if (!validateForm()) {
      event.preventDefault();
    }
  });

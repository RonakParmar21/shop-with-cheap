const bar = document.getElementById("bar");
const cross = document.getElementById("cross");
const menu = document.querySelector("nav ul");

bar.addEventListener("click", () => {
  menu.classList.add("show-menu");
  cross.style.display = "block";
  bar.style.display = "none";
});

cross.addEventListener("click", () => {
  menu.classList.remove("show-menu");
  cross.style.display = "none";
  bar.style.display = "block";
});

// slider code

let sliderImages = document.querySelectorAll(".slide"),
  arrowLeft = document.querySelector("#arrow-left"),
  arrowRight = document.querySelector("#arrow-right"),
  current = 0;

// Clear all images
function reset() {
  for (let i = 0; i < sliderImages.length; i++) {
    sliderImages[i].style.display = "none";
  }
}

// Initial slide
function startSlide() {
  reset();
  sliderImages[0].style.display = "block";
}

// Show previous
function slideLeft() {
  reset();
  sliderImages[current - 1].style.display = "block";
  current--;
}

// Show next
function slideRight() {
  reset();
  sliderImages[current + 1].style.display = "block";
  current++;
}

// Left arrow click
arrowLeft.addEventListener("click", function () {
  if (current === 0) {
    current = sliderImages.length;
  }
  slideLeft();
});

// Right arrow click
arrowRight.addEventListener("click", function () {
  if (current === sliderImages.length - 1) {
    current = -1;
  }
  slideRight();
});

startSlide();


// contact form 
document.getElementById('contactForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent form submission

  let isValid = true;

  // Clear previous errors
  document.querySelectorAll('.error').forEach(el => el.textContent = '');

  // Name validation
  const name = document.getElementById('name').value.trim();
  if (!name) {
      isValid = false;
      document.getElementById('nameError').textContent = 'Name is required';
  } else if (name.length < 3) {
      isValid = false;
      document.getElementById('nameError').textContent = 'Name must be at least 3 characters';
  }

  // Email validation
  const email = document.getElementById('email').value.trim();
  const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
  if (!email) {
      isValid = false;
      document.getElementById('emailError').textContent = 'Email is required';
  } else if (!emailRegex.test(email)) {
      isValid = false;
      document.getElementById('emailError').textContent = 'Enter a valid email';
  }

  // Mobile validation
  const mobile = document.getElementById('mobile').value.trim();
  const mobileRegex = /^[0-9]{10}$/;
  if (!mobile) {
      isValid = false;
      document.getElementById('mobileError').textContent = 'Mobile number is required';
  } else if (!mobileRegex.test(mobile)) {
      isValid = false;
      document.getElementById('mobileError').textContent = 'Enter a valid 10-digit mobile number';
  }

  // Message validation
  const message = document.getElementById('message').value.trim();
  if (!message) {
      isValid = false;
      document.getElementById('messageError').textContent = 'Message is required';
  } else if (message.length < 10) {
      isValid = false;
      document.getElementById('messageError').textContent = 'Message must be at least 10 characters';
  }

  if (isValid) {
      alert('Form submitted successfully!');
      // You can submit the form data to the server here.
  }
});

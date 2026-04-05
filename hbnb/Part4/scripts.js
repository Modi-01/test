const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

function getCookie(name) {
  const cookieString = `; ${document.cookie}`;
  const parts = cookieString.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  return null;
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function createOrGetMessageElement(container, id = 'page-message') {
  let messageElement = document.getElementById(id);
  if (!messageElement) {
    messageElement = document.createElement('p');
    messageElement.id = id;
    container.prepend(messageElement);
  }
  return messageElement;
}

function showMessage(container, message, isError = false, id = 'page-message') {
  const messageElement = createOrGetMessageElement(container, id);
  messageElement.textContent = message;
  messageElement.style.color = isError ? 'red' : 'green';
}

function updateLoginLinkVisibility() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'inline-block';
  }
  return token;
}

async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Login failed');
  }

  document.cookie = `token=${data.access_token}; path=/`;
  window.location.href = 'index.html';
}

function initializeLoginPage() {
  const loginForm = document.getElementById('login-form');
  if (!loginForm || !document.getElementById('email') || !document.getElementById('password')) {
    return;
  }

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
      await loginUser(email, password);
    } catch (error) {
      showMessage(loginForm, error.message, true, 'login-message');
    }
  });
}

function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) {
    return;
  }

  priceFilter.innerHTML = '';
  ['10', '50', '100', 'All'].forEach((value) => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    priceFilter.appendChild(option);
  });
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) {
    return;
  }

  placesList.innerHTML = '';

  places.forEach((place) => {
    const card = document.createElement('article');
    card.className = 'place-card';
    card.dataset.price = place.price;

    card.innerHTML = `
      <h2>${place.title}</h2>
      <p class="place-price">$${place.price} / night</p>
      <p>${place.description || 'No description available.'}</p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;

    placesList.appendChild(card);
  });
}

function applyPriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  const placeCards = document.querySelectorAll('#places-list .place-card');

  if (!priceFilter) {
    return;
  }

  const selectedValue = priceFilter.value;

  placeCards.forEach((card) => {
    const cardPrice = Number(card.dataset.price);
    if (selectedValue === 'All' || cardPrice <= Number(selectedValue)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

async function fetchPlaces(token) {
  const headers = {};
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}/places/`, { headers });
  if (!response.ok) {
    throw new Error('Failed to fetch places');
  }

  const places = await response.json();
  displayPlaces(places);
  applyPriceFilter();
}

async function initializeIndexPage() {
  if (!document.getElementById('places-list') || !document.getElementById('price-filter')) {
    return;
  }

  const token = updateLoginLinkVisibility();
  populatePriceFilter();
  document.getElementById('price-filter').addEventListener('change', applyPriceFilter);

  try {
    await fetchPlaces(token);
  } catch (error) {
    showMessage(document.querySelector('main'), error.message, true, 'places-message');
  }
}

function buildAmenitiesMarkup() {
  return `
    <ul class="amenities-list">
      <li><img src="images/icon_wifi.png" alt="Wi-Fi icon"> Amenities are not available from the current API response.</li>
    </ul>
  `;
}

function displayPlaceDetails(place) {
  const detailsSection = document.getElementById('place-details');
  if (!detailsSection) {
    return;
  }

  detailsSection.innerHTML = `
    <div class="place-title-row">
      <h1>${place.title}</h1>
      <span class="price-tag">$${place.price} / night</span>
    </div>
    <div class="place-info">
      <div>
        <h3>Description</h3>
        <p>${place.description || 'No description available.'}</p>
      </div>
      <div>
        <h3>Location</h3>
        <p><strong>Latitude:</strong> ${place.latitude}</p>
        <p><strong>Longitude:</strong> ${place.longitude}</p>
      </div>
      <div>
        <h3>Amenities</h3>
        ${buildAmenitiesMarkup()}
      </div>
    </div>
  `;
}

function displayReviews(reviews) {
  const reviewsSection = document.getElementById('reviews');
  if (!reviewsSection) {
    return;
  }

  reviewsSection.innerHTML = '<h2>Reviews</h2>';

  if (!reviews.length) {
    reviewsSection.innerHTML += '<p class="review-card">No reviews yet.</p>';
    return;
  }

  reviews.forEach((review) => {
    const reviewCard = document.createElement('article');
    reviewCard.className = 'review-card';
    reviewCard.innerHTML = `
      <p><strong>User:</strong> ${review.user_name || 'Anonymous'}</p>
      <p><strong>Rating:</strong> ${review.rating}/5</p>
      <p>${review.text}</p>
    `;
    reviewsSection.appendChild(reviewCard);
  });
}

function updatePlacePageReviewAccess(token, placeId) {
  const addReviewSection = document.getElementById('add-review');
  if (!addReviewSection) {
    return;
  }

  if (!token) {
    addReviewSection.style.display = 'none';
    return;
  }

  addReviewSection.style.display = 'block';
  addReviewSection.innerHTML = `
    <h2>Add a Review</h2>
    <a class="details-button" href="add_review.html?id=${placeId}">Go to review form</a>
  `;
}

async function fetchPlaceDetails(token, placeId) {
  const headers = {};
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });
  if (!response.ok) {
    throw new Error('Failed to fetch place details');
  }

  return response.json();
}

async function fetchPlaceReviews(placeId) {
  const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`);
  if (!response.ok) {
    throw new Error('Failed to fetch reviews');
  }

  return response.json();
}

async function initializePlacePage() {
  if (!document.getElementById('place-details')) {
    return;
  }

  const placeId = getPlaceIdFromURL();
  const token = updateLoginLinkVisibility();
  updatePlacePageReviewAccess(token, placeId);

  if (!placeId) {
    showMessage(document.querySelector('main'), 'Place ID is missing from the URL.', true, 'place-message');
    return;
  }

  try {
    const [place, reviews] = await Promise.all([
      fetchPlaceDetails(token, placeId),
      fetchPlaceReviews(placeId)
    ]);

    displayPlaceDetails(place);
    displayReviews(reviews);
  } catch (error) {
    showMessage(document.querySelector('main'), error.message, true, 'place-message');
  }
}

function checkAddReviewAuthentication() {
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
    return null;
  }
  return token;
}

function populateRatingOptions() {
  const ratingSelect = document.getElementById('rating');
  if (!ratingSelect) {
    return;
  }

  ratingSelect.innerHTML = '';
  [1, 2, 3, 4, 5].forEach((value) => {
    const option = document.createElement('option');
    option.value = String(value);
    option.textContent = String(value);
    ratingSelect.appendChild(option);
  });
}

async function fetchPlaceSummary(token, placeId) {
  const headers = {};
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });
  if (!response.ok) {
    throw new Error('Failed to fetch place information');
  }

  return response.json();
}

async function submitReview(token, placeId, reviewText, rating) {
  const response = await fetch(`${API_BASE_URL}/reviews/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      text: reviewText,
      rating: Number(rating),
      place_id: placeId
    })
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Failed to submit review');
  }
  return data;
}

async function initializeAddReviewPage() {
  const reviewForm = document.getElementById('review-form');
  const reviewTextField = document.getElementById('review');
  const ratingField = document.getElementById('rating');

  if (!reviewForm || !reviewTextField || !ratingField) {
    return;
  }

  const token = checkAddReviewAuthentication();
  if (!token) {
    return;
  }

  updateLoginLinkVisibility();

  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    showMessage(document.querySelector('main'), 'Place ID is missing from the URL.', true, 'review-message');
    return;
  }

  populateRatingOptions();

  const placeInfoSection = document.getElementById('place-review-info');
  if (placeInfoSection) {
    try {
      const place = await fetchPlaceSummary(token, placeId);
      placeInfoSection.innerHTML = `<p><strong>Reviewing place:</strong> ${place.title}</p>`;
    } catch (error) {
      placeInfoSection.innerHTML = `<p><strong>Reviewing place ID:</strong> ${placeId}</p>`;
    }
  }

  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const reviewText = reviewTextField.value.trim();
    const rating = ratingField.value;

    try {
      await submitReview(token, placeId, reviewText, rating);
      showMessage(reviewForm, 'Review submitted successfully!', false, 'review-message');
      reviewForm.reset();
      populateRatingOptions();
    } catch (error) {
      showMessage(reviewForm, error.message, true, 'review-message');
    }
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  updateLoginLinkVisibility();
  initializeLoginPage();
  await initializeIndexPage();
  await initializePlacePage();
  await initializeAddReviewPage();
});

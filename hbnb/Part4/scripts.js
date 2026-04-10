const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

function getCookie(name) {
  const cookieString = `; ${document.cookie}`;
  const parts = cookieString.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  return null;
}

function deleteCookie(name) {
  document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
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
  const authLink = document.getElementById('auth-link');

  if (!authLink) {
    return token;
  }

  if (token) {
    authLink.textContent = 'Logout';
    authLink.href = '#';

    authLink.onclick = function (event) {
      event.preventDefault();
      deleteCookie('token');
      window.location.href = 'login.html';
    };
  } else {
    authLink.textContent = 'Login';
    authLink.href = 'login.html';
    authLink.onclick = null;
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

function populateCountryFilter(places) {
  const countryFilter = document.getElementById('country-filter');
  if (!countryFilter) {
    return;
  }

  countryFilter.innerHTML = '';

  const allOption = document.createElement('option');
  allOption.value = 'All';
  allOption.textContent = 'All';
  countryFilter.appendChild(allOption);

  const famousCountries = [
    'Saudi Arabia',
    'UAE',
    'Egypt',
    'Jordan',
    'France',
    'Spain',
    'Switzerland',
    'USA',
    'UK',
    'Morocco',
    'Japan',
    'Germany',
    'Italy',
    'Canada',
    'Turkey',
    'India',
    'China',
    'Brazil',
    'Australia',
    'South Korea'
  ];

  const apiCountries = places
    .map((place) => place.country)
    .filter((country) => country && country.trim() !== '');

  const mergedCountries = [...new Set([...famousCountries, ...apiCountries])].sort();

  mergedCountries.forEach((country) => {
    const option = document.createElement('option');
    option.value = country;
    option.textContent = country;
    countryFilter.appendChild(option);
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
    card.dataset.country = place.country || 'Unknown Country';
    card.dataset.price = String(place.price ?? 0);

    card.innerHTML = `
      <h2>${place.title}</h2>
      <p class="place-country">🌍 ${place.country || 'Unknown Country'}</p>
      <p class="place-price">$${place.price} / night</p>
      <p>${place.description || 'No description available.'}</p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;

    placesList.appendChild(card);
  });
}

function applyCountryFilter() {
  const countryFilter = document.getElementById('country-filter');
  const priceFilter = document.getElementById('price-filter');
  const placeCards = document.querySelectorAll('#places-list .place-card');
  const placesList = document.getElementById('places-list');

  if (!countryFilter || !priceFilter || !placesList) {
    return;
  }

  const selectedCountry = countryFilter.value;
  const selectedPrice = priceFilter.value;

  let visibleCount = 0;

  placeCards.forEach((card) => {
    const cardCountry = card.dataset.country || '';
    const rawPrice = card.dataset.price || '0';
    const cardPrice = parseFloat(rawPrice);

    const countryMatch =
      selectedCountry === 'All' || cardCountry === selectedCountry;

    const priceMatch =
      selectedPrice === 'All' ||
      (!Number.isNaN(cardPrice) && cardPrice <= parseFloat(selectedPrice));

    if (countryMatch && priceMatch) {
      card.style.display = 'block';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });

  let emptyMessage = document.getElementById('no-results-message');

  if (visibleCount === 0) {
    if (!emptyMessage) {
      emptyMessage = document.createElement('p');
      emptyMessage.id = 'no-results-message';
      emptyMessage.textContent = 'No places match the selected filters';
      emptyMessage.style.textAlign = 'center';
      emptyMessage.style.marginTop = '20px';
      emptyMessage.style.fontWeight = 'bold';
      placesList.appendChild(emptyMessage);
    }
  } else if (emptyMessage) {
    emptyMessage.remove();
  }
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

  populateCountryFilter(places);
  displayPlaces(places);
  applyCountryFilter();
}

async function initializeIndexPage() {
  if (
    !document.getElementById('places-list') ||
    !document.getElementById('country-filter') ||
    !document.getElementById('price-filter')
  ) {
    return;
  }

  const token = updateLoginLinkVisibility();

  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  document.getElementById('country-filter').addEventListener('change', applyCountryFilter);
  document.getElementById('price-filter').addEventListener('change', applyCountryFilter);

  try {
    await fetchPlaces(token);
  } catch (error) {
    showMessage(document.querySelector('main'), error.message, true, 'places-message');
  }
}

function buildAmenitiesMarkup(amenities = []) {
  if (!amenities.length) {
    return `
      <ul class="amenities-list">
        <li>No amenities available.</li>
      </ul>
    `;
  }

  return `
    <ul class="amenities-list">
      ${amenities.map((amenity) => `<li>${amenity.name}</li>`).join('')}
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
        <p><strong>Country:</strong> ${place.country || 'Unknown Country'}</p>
      </div>
      <div>
        <h3>Amenities</h3>
        ${buildAmenitiesMarkup(place.amenities)}
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
    window.location.href = 'login.html';
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
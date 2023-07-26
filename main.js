const registerForm = document.getElementById('register-form');

registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = new FormData(registerForm);
  const userData = {
    username: formData.get('username'),
    email: formData.get('email'),
    password: formData.get('password'),
  };

  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });

    const data = await response.json();
    alert(data.message); // Display success message or error message
    registerForm.reset();
  } catch (error) {
    console.error('Error:', error);
  }
});

// User Login
const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = new FormData(loginForm);
  const userData = {
    username: formData.get('login-username'),
    password: formData.get('login-password'),
  };

  try {
    const response = await fetch('/api/login', {
      method 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });

    if (response.ok) {
      const data = await response.json();
      alert(`Login successful. User ID: ${data.user_id}`);
    } else {
      alert('Invalid credentials. Please try again.');
    }

    loginForm.reset();
  } catch (error) {
    console.error('Error:', error);
  }
});

// Khoj the Search
const khojForm = document.getElementById('khoj-form');
const khojResult = document.getElementById('khoj-result');

khojForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = new FormData(khojForm);
  const khojData = {
    user_id: 1, // Replace with the actual user ID after successful login
    input_values: formData.get('input-values'),
    search_value: formData.get('search-value'),
  };

  try {
    const response = await fetch('/api/khoj', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(khojData),
    });

    const data = await response.json();
    khojResult.innerHTML = `Search Result: ${data.result}`;
    khojForm.reset();
  } catch (error) {
    console.error('Error:', error);
  }
});

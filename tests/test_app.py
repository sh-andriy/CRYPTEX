class TestRegister:
    """
    Class to that make a unit tests for a
    user registration
    """
    def test_register_get_page(self, client):
        """Test the registration page is accessible"""
        response = client.get('/register')
        assert response.status_code == 200

    def test_register_empty_data(self, client):
        """Test that submitting an empty registration form results in an error message"""
        response = client.post('/register', data={})
        assert response.status_code == 200
        assert b'This field is required.' in response.data

    def test_register_invalid_email(self, client):
        """
        Test that submitting a registration form with invalid email
        results in an error message
        """
        response = client.post(
            '/register',
            data={'email': 'invalidemail', 'password': 'password123'}
        )
        assert response.status_code == 200
        assert b'Invalid email address.' in response.data

    def test_register_successful(self, client):
        """
        Test that submitting a registration form with valid credentials
        redirects to home page
        """
        response = client.post(
            '/register',
            data={'email': 'test@example.com', 'password': 'password123'},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'User Registered Successfully!', 'success' in response.data


class TestLogin:
    """
    Class that make unit tests for a
    user login
    """
    def test_login_get_page(self, client):
        """Send a GET request to the login page"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'<h2>Login Page</h2>' in response.data

    def test_login_successful(self, client):
        """
        Send a POST request with correct credentials
        """

        response = client.post(
            '/login',
            data={'email': 'test@example.com', 'password': 'password'}
        )
        assert response.status_code == 200  # Redirect
        # Check that the user was logged in and redirected to the home page
        assert b'User Logged Successfully!', 'success' in response.data

    def test_login_invalid_credentials(self, client):
        """
        Send a POST request with incorrect credentials
        """
        response = client.post(
            '/login',
            data={'email': 'test@example.com', 'password': 'wrongpassword'}
        )

        # Check that the user was not logged in and an error message
        # was displayed

        assert b'Sorry, Wrong Credentials! Try Again...', 'danger' in response.data


class TestLogout:
    """
    Class that makes unit tests for a user
    logout
    """
    def test_logout_create_user(self, client):
        """Create a new user"""
        email = 'test@example.com'
        password = 'password'
        response = client.post('/register', data={'email': email, 'password': password})
        assert response.status_code == 200

        # """Log in the user"""
        response = client.post('/login', data={'email': email, 'password': password})
        assert response.status_code == 200

    def test_logout_successful(self, client):
        """Log out the user"""
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

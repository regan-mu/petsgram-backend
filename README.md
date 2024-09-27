# 🐾 Petsgram Backend API

Welcome to the Petsgram Backend API, the backend service for an Instagram-like social media application where users can share, like, and comment on pet photos! This API, built using Django and Django REST Framework, provides the core functionality for user authentication, profile management, post creation, and interactions with pet posts.
The UI for the app can be viewed at [Live](https://petsgram-client.vercel.app/)

## 📋 Features

* **User Authentication:** Register, login, and manage user sessions using JWT authentication.
* **Profile Management:** Create and update user profiles, including avatars and bio descriptions.
* **Post Creation**: Users can create posts with photos and captions showcasing their pets.
* **Likes and Comments:** Users can like and comment on posts.
* **Followers System:** Users can follow and unfollow others to see their pet posts in the feed.
* **Feed and Search:** A personalized feed for followed users and a search for discovering new pets.
* **Password Reset:** Secure workflow for users to reset their passwords via email.

## 🛠️ Installation

### 1. Clone the Repository

```bash
    git clone https://github.com/regan-mu/petsgram-backend
    cd petsgram-backend
```

### 2. Create and Activate a Virtual Environment

```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
    pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a **.env** file in the project root and add the environment variables as specified **.env-sample** file.

### 5. Run Migrations

```bash
    python manage.py migrate
```

### 6. Create a Superuser

```bash
    python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
    python manage.py runserver
```

## 🤝 Contributing

Feel free to submit issues, fork the repository, and send pull requests! Make sure to follow best practices in Django development and maintain a high code quality. The project can use a few improvements all contributions are welcome.

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.

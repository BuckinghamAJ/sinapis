# Sinapis
**_NOTE:_**  Sinapis is Latin for Mustard (as in the kingdom growing from the faith of a mustard seed)

Welcome to the Christian content Sharing Platform! This is a personal project inspired by daily.dev where users can share Christian prayers, meditation, videos, and blog posts. Users can also comment and upvote content.
This personal project has been in development off and on for a few months. Below is an example of it in use:


https://github.com/user-attachments/assets/a52a3bdd-b81e-4fa2-9ff4-0855bda3f34d


## Tech Stack

- **Backend**: Django
- **Frontend**: HTMX & Alpine.js for a Single Page Application (SPA) feel
- **Styling**: Tailwind CSS via django-tailwind along with daisy-ui components
- **Caching**: Memcache
- **Database**: PostgreSQL

## Features

- Share Christian prayers, meditation, videos, and blog posts
- Comment on and upvote shared content
- User authentication and profile management

## Getting Started

Follow these instructions to set up the project locally on your machine.

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- PostgreSQL
- Memcached

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/BuckinghamAJ/sinapis.git
    cd sinapis
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```


4. **Set up the PostgreSQL database:**

    - Create a new PostgreSQL database and user.
    - Update the `DATABASES` setting in `settings.py` with your database credentials.

5. **Run database migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Set up Memcached:**

    - Ensure Memcached is installed and running on your machine.
    - Update the `CACHES` setting in `settings.py` if necessary.

7. **Set up Tailwind CSS:**

    - Initialize Tailwind:

        ```bash
        python manage.py tailwind init
        ```

    - Install Tailwind:

        ```bash
        python manage.py tailwind install
        ```

8. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```



### Local Run

1. **Run Tailwind CSS:**

    ```bash
    python manage.py tailwind start
    ```

2. **Run the development server:**

    In another terminal window, run:

    ```bash
    python manage.py runserver
    ```

3. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000`.

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, feel free to reach out to me at adamjbuckingham7@gmail.com.

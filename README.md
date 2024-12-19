# SpotTheSong
SpotTheSong is a Flask-based web application that uses Spotify's API to create an interactive quiz about the user's musical preferences and listening habits. The application allows users to log in with their Spotify account, take a quiz based on their top tracks and artists, view their results, and explore their listening data categorized by time ranges.

## Features

1. **Spotify Authentication**: Users can securely log in using their Spotify account.
2. **Dynamic Quiz**: Generates quiz questions based on the user's top tracks and artists in three categories:
    - Last month (short term).
    - Last Year (medium term).
    - All time (long term).
3. **Quiz Results**: Provides feedback on user guesses with the correct answers.
4. **Data Overview**: Displays the user's top tracks, artists, and albums categorized by time ranges.

## Installation

### Step 1: Clone the Repository

```bash
git clone <https://github.com/ma-wm/SpotTheSong.git>
cd spotthesong

```

### Step 2: Set Up the Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows, use venv\\Scripts\\activate

```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```
**PS:** Using the Spotify API requires credentials in their Spotify Developer Dashboard (`client_id`, `client_secret`, and `redirect_uri`). For the purposes of these examination,this application already exists and has credentials on my account. However. If you'd like to run the app locally with your own Spotify credentials, follow these steps:
- Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
- Create a new application and obtain your `client_id`, `client_secret`, and `redirect_uri`.
- You can then either place these credentials in the code directly (as shown in the project) or use an `.env` file for security.
## Usage

### Run the Application

```bash
python app.py

```
  
### Access the Application

Visit `http://127.0.0.1:5000/` in your browser.

### Workflow

1. Visit the app in your browser
2. Log in with your Spotify account.
3. Take the quiz about your listening habits.
4. View your quiz results and compare your guesses with actual Spotify data.
5. Explore your top artists, songs, and albums by different time ranges.

## Technologies Used:
- **Backend**: Python, Flask
- **Spotify API**: Spotipy library for interacting with Spotify's API.
- **Frontend**: HTML, CSS (custom design with Spotify branding)
- **Version Control**: Git, GitHub
  
## Folder Structure

```
SpotTheSong/
│
├── app.py                # Core Flask application logic
├── templates/            # HTML templates
│   ├── welcome.html      # Welcome page
│   ├── quiz.html         # Quiz page
│   └── quiz_result.html  # Quiz results page
├── static/               # Static assets (e.g., CSS, images)
│   ├── styles.css        # Custom styling
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

```

## Key Files

**1. `app.py`**

Main Flask application with the following routes:

- `/`: Displays the welcome page.
- `/login`: Redirects users to Spotify's login page.
- `/callback`: Handles Spotify's callback after successful login.
- `/quiz`: Generates and renders the quiz page.
- `/quiz_result`: Displays quiz results and Spotify data overview.

**2. `templates/`**

- **`welcome.html`**: Welcome page with Spotify login prompt.
- **`quiz.html`**: Quiz interface showing dynamically generated questions.
- **`quiz_result.html`**: Displays quiz results and user data overview.

**3. `static/`**

Custom CSS for styling the application.

## Frontend Explanation:
### HTML Templates:
- The templates use Flask's `render_template` function to dynamically generate pages with data passed from the backend (e.g., quiz data, results).
- **Welcome Page (`welcome.html`)**: Displays an introductory message and a login button for users to authenticate via Spotify.
- **Quiz Page (`quiz.html`)**: Displays quiz questions and options. Users select answers, and their responses are submitted to the `/quiz_result` endpoint.
- **Results Page (`result.html`)**: Displays the user's score and the correct answers.

### CSS Styling:
The CSS is designed to give the app a Spotify-inspired look with the brand's green color scheme and dark background.

## How It Works

1. **Spotify Authentication**
    - The app uses OAuth 2.0 to authenticate users and fetch their data.
2. **Fetching User Data**
    - Spotify API endpoints are used to retrieve the user's top tracks and artists for short, medium, and long terms.
3. **Quiz Logic**
    - Quiz questions and options are dynamically generated based on the user's listening data.
4. **Result Validation**
    - User answers are compared to the actual data to calculate the score.
5. **Data Visualization**
    - Top tracks, artists, and albums are displayed with album artwork and artist images.
  
## Error Handling:
- **Spotify Token Expiration**: The app automatically handles expired tokens by prompting users to re-authenticate when necessary.
- **API Errors**: Any errors from the Spotify API (e.g., if a request fails) are caught and logged to the console. The app continues functioning, and users are given an error message if data cannot be fetched.

## Restrictions

- **Time Range Limitations**: 
  Spotify's API only categorizes user data into three distinct time ranges:
    - **Last Month** (`short_term`)
    - **Last Six Months** (`medium_term`)
    - **All Time** (`long_term`)
  
  For the purpose of this project, the "Last Year" category is used as an approximation. Specifically, the **Medium Term** (`medium_term`) data, which represents the last 6 months of listening habits, is used as a proxy for **Last Year**. Please note that this is a design decision made for aesthetic and simplicity reasons, as the API does not provide a direct "last year" category.

- **Data Accuracy**: 
  While this project strives to provide an accurate representation of user listening habits, the data may not perfectly match the exact "last year" timeframe due to the limitations of the Spotify API's available time ranges.

## Resources

Throughout the development of this project, several resources were utilized. Below is a list of resources used:

1. **ChatGPT**  
   ChatGPT was used throughout the project, particularly in providing guidance and assistance with debugging issues. It helped with:
   - Understanding and troubleshooting Python and Flask code.
   - Writing clean and well-documented code.
   - Offering CSS and HTML styling advice.
   - Generating solutions for integrating Spotify’s API and handling edge cases.

2. **Spotify Developer Documentation**  
   The official [Spotify Developer API Documentation](https://developer.spotify.com/documentation/web-api/) was used for understanding how to interact with Spotify’s Web API.

3. **Flask Documentation**  
   The [Flask Documentation](https://flask.palletsprojects.com/) provided information on how to build and manage web applications with Python.

4. **W3Schools**  
   [W3Schools](https://www.w3schools.com/) was a helpful resource for HTML, CSS, and JavaScript tutorials.



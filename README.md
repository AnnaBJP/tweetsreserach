# Wayback Tweets

Wayback Tweets is a Flask application that allows users to retrieve archived tweets from the Wayback Machine. The application provides functionality to search for tweets by username and date range, and it allows users to download the results in various formats such as CSV, JSON, and HTML.

## Project Structure

```
waybacktweets
├── src
│   ├── app.py                # Main Flask application
│   ├── templates
│   │   └── index.html        # HTML template for the main page
│   └── static                # Directory for static files (CSS, JS, images)
├── runtime.txt               # Specifies the Python runtime version
├── requirements.txt          # Lists Python dependencies
├── netlify.toml              # Configuration for Netlify deployment
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd waybacktweets
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python src/app.py
   ```

5. Open your web browser and navigate to `http://localhost:5000` to access the application.

## Usage

- Enter a Twitter username and select a date range to search for archived tweets.
- Use the provided options to download the results in your preferred format (CSV, JSON, HTML).

## Deployment

This application can be deployed on Netlify. Ensure that the `runtime.txt` and `requirements.txt` files are correctly configured for the deployment environment.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.
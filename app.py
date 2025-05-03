from flask import Flask, render_template, request, send_file, jsonify
from datetime import datetime, timedelta
import io
import base64
import pandas as pd
from waybacktweets.api.export import TweetsExporter
from waybacktweets.api.parse import TweetsParser
from waybacktweets.api.request import WaybackTweets
from waybacktweets.api.visualize import HTMLTweetsVisualizer    
from waybacktweets.config import FIELD_OPTIONS, config

# Configure verbose mode
config.verbose = False

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB
# Default date range
start_date = datetime.now() - timedelta(days=30 * 6)
end_date = datetime.now()


def get_archived_tweets(username, collapse, start_date, end_date, limit, offset, matchtype):
    response = WaybackTweets(username, collapse, start_date, end_date, limit, offset, matchtype)
    return response.get()


def parse_tweets(archived_tweets, username):
    parser = TweetsParser(archived_tweets, username, FIELD_OPTIONS)
    return parser.parse()


def export_tweets(parsed_tweets, username):
    exporter = TweetsExporter(parsed_tweets, username, FIELD_OPTIONS)
    return exporter.dataframe, exporter.filename


@app.route('/', methods=['GET', 'POST'])
def index():
    tweets_data = None
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
        limit = request.form.get('limit') or None
        offset = request.form.get('offset') or None
        unique = request.form.get('unique') == 'on'

        collapse = 'urlkey' if unique else None
        matchtype = 'prefix' if unique else None

        try:
            tweets = get_archived_tweets(
                username,
                collapse,
                datetime.strptime(from_date, '%Y-%m-%d'),
                datetime.strptime(to_date, '%Y-%m-%d'),
                limit,
                offset,
                matchtype
            )

            if not tweets:
                raise ValueError("No archived tweets found.")

            parsed = parse_tweets(tweets, username)
            df, filename = export_tweets(parsed, username)

            html_visualizer = HTMLTweetsVisualizer(username, df.to_json(orient='records'))
            html_content = html_visualizer.generate()

            tweets_data = {
                'count': len(df),
                'csv': base64.b64encode(df.to_csv(index=False).encode()).decode(),
                'json': base64.b64encode(df.to_json(orient='records').encode()).decode(),
                'html': base64.b64encode(html_content.encode()).decode(),
                'filename': filename,
                'table': df.to_html(classes='table table-bordered', index=False, escape=False)
            }

        except Exception as e:
            error = str(e)

    return render_template('./index.html', tweets_data=tweets_data, error=error, today=end_date.strftime('%Y-%m-%d'), six_months_ago=start_date.strftime('%Y-%m-%d'))


@app.route('/download/<format>', methods=['POST'])
def download(format):
    data = request.form['data']
    filename = request.form['filename']
    decoded = base64.b64decode(data)
    buffer = io.BytesIO(decoded)
    buffer.seek(0)

    mime_type = {
        'csv': 'text/csv',
        'json': 'application/json',
        'html': 'text/html'
    }.get(format, 'application/octet-stream')

    return send_file(
        buffer,
        mimetype=mime_type,
        as_attachment=True,
        download_name=f"{filename}.{format}"
    )


if __name__ == '__main__':
    app.run(debug=True)
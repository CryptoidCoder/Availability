from flask import Flask, request, render_template
from functions import *

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    current_light_colour = events_now_all_calendars()
    if current_light_colour == 'red':
          current_message = 'CryptoidCoder Is Unable To Talk / Message Currently.'
    elif current_light_colour == 'amber':
          current_message = 'CryptoidCoder Is Free To Message & Can Only Be Called If An Emergency.'
    elif current_light_colour == 'green':
          current_message = 'CryptoidCoder Is Free To Talk / Message / Call Currently.'
    return render_template('index.html', light_colour=current_light_colour, message=current_message)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 80))
	app.run(host='0.0.0.0', port=port)
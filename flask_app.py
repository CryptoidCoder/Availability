from flask import Flask, request, render_template
from functions import *

app = Flask(__name__)

def get_colour():
      global light_colour
      print(eventsnow())
      if eventsnow() != None: # if events then not available
            return 'red', 'CryptoidCoder Is Unable To Talk / Message Currently.'
      elif eventsnow() == None or eventsnow() == 'None': #if no events - then clear
            return 'green', 'CryptoidCoder Is Free To Talk / Message Currently.'

@app.route('/')
def index():
    current_light_colour, current_message = get_colour()
    #return render_template('traffic_light_stylish.html', light_colour=current_light_colour, message=current_message)
    return render_template('index.html', light_colour=current_light_colour, message=current_message)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 80))
	app.run(host='0.0.0.0', port=port)
from flask import Flask, request, render_template, redirect, flash,url_for
from functions import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()


@app.route('/', methods=['GET'])
def index():
      current_light_colour = events_now_all_calendars()
      return render_template('index.html', light_colour=current_light_colour, message=parsemessage(current_light_colour), current_status='Current Availability')

@app.route('/index', methods=['GET'])
def anotherindex():
      current_light_colour = events_now_all_calendars()
      return render_template('index.html', light_colour=current_light_colour, message=parsemessage(current_light_colour), current_status='Current Availability')

@app.route('/results', methods=['POST', 'GET'])
def results():
      if request.method == 'GET':
        return redirect(url_for('index'), code=302)
      if request.method == 'POST':
            form_data = request.form
            if form_data['date'] != '' and form_data['starttime'] != '' and form_data['endtime'] != '': #if all form boxes have data
                  formdate = form_data['date']
                  formstarttime = form_data['starttime']
                  formendtime = form_data['endtime']
                  current_light_colour = eventscheck_all_calendars(formdate, formstarttime, formendtime)
                  return render_template('index.html', light_colour=current_light_colour, message=parsemessage(current_light_colour), current_status=f'Availability On {formdate}, {formstarttime} -> {formendtime}')
            else:
                  return render_template('failed.html')
      

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 80))
	app.run(host='0.0.0.0', port=port)
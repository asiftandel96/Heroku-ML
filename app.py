from flask import Flask, render_template, request
import pickle

app = Flask(__name__)  # initializing a flask app


@app.route('/', methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])  # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            pickup_longitude = float(request.form['pickup_longitude'])
            pickup_latitude = float(request.form['pickup_latitude'])
            dropoff_longitude = float(request.form['dropoff_longitude'])
            dropoff_latitude = float(request.form['dropoff_latitude'])
            passengerInTaxi = float(request.form['passengerInTaxi'])
            is_weekday = request.form['week_day']
            if is_weekday == 'Monday':
                week_day = 0
            elif is_weekday == 'Tuesday':
                week_day = 1
            elif is_weekday == 'Wednesday':
                week_day = 2
            elif is_weekday == 'Thursday':
                week_day = 3
            elif is_weekday == 'Friday':
                week_day = 4
            elif is_weekday == 'Saturday':
                week_day = 5
            elif is_weekday == 'Sunday':
                week_day = 6
            else:
                week_day = -1
            hours = float(request.form['hours'])
            filename = 'decision_model.pkl'
            loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from the storage
            # predictions using the loaded model file
            prediction = loaded_model.predict(
                [[pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passengerInTaxi,
                  week_day, hours]])
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html', prediction=prediction[0])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001, debug=True)
    app.run(debug=True)  # running the app

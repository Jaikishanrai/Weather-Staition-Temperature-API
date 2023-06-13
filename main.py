# Flask is a lightweight Python web framework that provides useful tools and features for creating web applications
#                                                                                            in the Python Language.
# Flask looks for templates in the template's directory, which is called templates, so the name is important.
# Make sure you’re inside the flask_app directory and run the following command to create the template's directory.
# good practice to use __name__
# render_template -->   renders the template with information and serves it to the browser.
# @app.route("xyz")---> App routing is used to map the specific URL with the associated function that is intended to
#                                                                                                  perform some task.
# app.run(debug=True)---> Running the app in debug mode will show an interactive traceback and console in the browser
#                                                                                              when there is an error.
# app.run(debug=True, port=5001 )---> flask apps always run on port 5000 by you can change the port of the app
# str(station).zfill(6)----> add zeros to the string
"""
parse_dates=['    DATE']----> We can use the parse_dates parameter to convince pandas to turn things into real
 datetime types. parse_dates takes a list of columns (since you could want to parse multiple columns into datetimes ).
"""
"""
.squeeze() ----> This method is most useful when you don't know if your object is a Series or DataFrame, but you do know
 it has just a single column. In that case you can safely call squeeze to ensure you have a Series. A specific axis to
  squeeze. By default, all length-1 axes are squeezed.

"""
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data-small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


# when user visits /home , tutorial.html is called


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())
    # data=stations.to_html() gives entire data in table form in html page


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data-small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])

    temperature = df.loc[df['    DATE'] == date]["   TG"].squeeze() / 10
    # from entire dataframe showing temp of date = 1860-01-05

    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data-small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    # converting the dataframe to dictionary
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "data-small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    # to convert ['    DATE'] col in string type
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)

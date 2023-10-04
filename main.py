#!/usr/bin/env python

from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json
import snowmate_collector

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']

            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(
                json.loads(json_predictions)))
        elif request.form is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(
                json.loads(json_predictions)))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRouteClient():
    try:
        # if request.json['folderPath'] is not None:
        folder_path = "Training_Batch_Files"
        # path = request.json['folderPath']
        if folder_path is not None:
            path = folder_path

            train_valObj = train_validation(path)  # object initialization

            train_valObj.train_validation()  # calling the training_validation function

            trainModelObj = trainModel()  # object initialization
            trainModelObj.trainingModel()  # training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    # PROJECT_ID = "650c6fe0a66c94ade6d4718d"
    # SNOWMATE_CLIENT_ID = "5bce3783-b47c-4dbe-9322-f3cdbae21b6a"
    # SNOWMATE_CLIENT_SECRET = "0df1783e-fa9e-420f-a9f2-72396be9a1d4"
    PROJECT_ID = "650a786ba66c94ade6d4718b"
    SNOWMATE_CLIENT_ID = "2c7508a0-b155-4440-ada8-b97fd1d519ad"
    SNOWMATE_CLIENT_SECRET = "f2cc9bd1-13d1-4a9c-8473-838b9b863fb9"
    snowmate_collector.start(
        sanity=False,
        project_path="/mnt/c/Work/wafer_circleci",
        project_id=PROJECT_ID,
        client_id=SNOWMATE_CLIENT_ID,
        secret_key=SNOWMATE_CLIENT_SECRET,
        # data_sink=snowmate_collector.DataSinks.PRINT,
        # metrics_sink=snowmate_collector.MetricsDataSinks.PRINT,
        _sampling_percentage=50,
    )
    path="Prediction_Batch_files"
    pred_val = pred_validation(path)  # object initialization
    pred_val.prediction_validation()  # calling the prediction_validation function
    pred = prediction(path)  # object initialization
    print("Prediction File created at !!!" + str(path))

    # folder_path = "Training_Batch_Files"
    # # path = request.json['folderPath']
    # train_valObj = train_validation(folder_path)  # object initialization

    # train_valObj.train_validation()  # calling the training_validation function

    # trainModelObj = trainModel()  # object initialization
    # trainModelObj.trainingModel()  # training the model for the files in the table
    # host = '0.0.0.0'
    # # port = 5000
    # httpd = simple_server.make_server(host, port, app)
    # # print("Serving on %s %d" % (host, port))
    # httpd.serve_forever()

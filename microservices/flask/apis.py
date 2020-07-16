from flask import Flask, request
from flask_restful import Resource, Api
from nameko.standalone.rpc import ServiceRpcProxy
import os


def rpc_proxy():
    config = {"AMQP_URI": os.getenv("RMQ")}
    return ServiceRpcProxy("tasks", config)


app = Flask(__name__)
api = Api(app)


@app.route("/", methods=["GET"])
def root():
    return {"Hello": "World"}


class Fibojob(Resource):
    def get(self, number):
        with rpc_proxy() as task_proxy:
            task_id = task_proxy.start_task("fibonacci", number)
        return {"task_id": task_id}


class Fiboresult(Resource):
    def get(self, task_id):
        with rpc_proxy() as task_proxy:
            result = task_proxy.get_result(task_id)
        return {"result": result}


api.add_resource(Fibojob, "/fibo/<int:number>")
api.add_resource(Fiboresult, "/fiboresult/<string:task_id>")

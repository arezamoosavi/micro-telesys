from fastapi import FastAPI, File, UploadFile
from nameko.standalone.rpc import ServiceRpcProxy
import os


def rpc_proxy():
    # the ServiceRpcProxy instance isn't thread safe so we constuct one for
    # each request; a more intelligent solution would be a thread-local or
    # pool of shared proxies
    config = {"AMQP_URI": os.getenv("RMQ")}
    return ServiceRpcProxy("tasks", config)


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("app started")


@app.on_event("shutdown")
def shutdown_event():
    print("app stoped")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/fibo/{number}")
def fiboo(number: int):
    with rpc_proxy() as task_proxy:
        task_id = task_proxy.start_task("fibonacci", number)
    return {"task_id": task_id}


@app.get("/task/{id}")
def task_result(id: str):
    with rpc_proxy() as task_proxy:
        result = task_proxy.get_result(id)

    return {"result": result}

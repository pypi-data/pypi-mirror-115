# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation and Dapr Contributors.
# Licensed under the MIT License.
from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse

app = App()


@app.method(name="test")
def mymethod(request: InvokeMethodRequest) -> InvokeMethodResponse:
    print(request.metadata, flush=True)
    print(request.text(), flush=True)

    return InvokeMethodResponse(b"INVOKE_RECEIVED", "text/plain; charset=UTF-8")


if __name__ == "__main__":
    app.run(50051)

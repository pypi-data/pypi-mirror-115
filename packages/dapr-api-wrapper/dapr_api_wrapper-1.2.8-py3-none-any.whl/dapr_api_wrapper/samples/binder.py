# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation and Dapr Contributors.
# Licensed under the MIT License.
from dapr.ext.grpc import App, BindingRequest

app = App()


@app.binding("kafkaBinding")
def binding(request: BindingRequest):
    print(request.text(), flush=True)


if __name__ == "__main__":
    app.run(50051)

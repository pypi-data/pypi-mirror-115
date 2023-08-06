# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation and Dapr Contributors.
# Licensed under the MIT License.
from cloudevents.sdk.event import v1
from dapr.ext.grpc import App

app = App()


@app.subscribe(pubsub_name="dapr-redis-pubsub", topic="TOPIC_A")
def mytopic(event: v1.Event) -> None:
    print(event.Data(), flush=True)


if __name__ == "__main__":
    app.run(50051)

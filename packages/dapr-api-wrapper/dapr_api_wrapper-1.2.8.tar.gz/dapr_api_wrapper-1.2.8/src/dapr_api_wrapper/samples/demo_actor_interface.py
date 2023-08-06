# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation and Dapr Contributors.
# Licensed under the MIT License.

from dapr.actor import ActorInterface, actormethod


class DemoActorInterface(ActorInterface):
    @actormethod(name="test")
    async def get_my_data(self) -> object:
        return {"success": True, "message": "test from tv-svc"}

    @actormethod(name="SetMyData")
    async def set_my_data(self, data: object) -> None:
        # Do something with data
        return {"success": True, "message": "test from tv-svc"}

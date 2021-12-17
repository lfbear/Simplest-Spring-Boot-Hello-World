#!/usr/bin/env python3
import os
from aws_cdk import core
import myapp

app = core.App()
myapp.MyAppStack(app, "myapp", "v1")
app.synth()

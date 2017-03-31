#!/bin/bash

gunicorn -D -w 4 -b 0.0.0.0:60407 server:app

#!/bin/bash

gunicorn -D -w 4 -b 127.0.0.1:60407 server:app

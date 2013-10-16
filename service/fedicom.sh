#!/bin/bash

pkill -9 -f fedicom_service.py
nohup python fedicom_service.py &

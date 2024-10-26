# Seat Comfort System
This repository contains the software part of a prototype of a system thought for autonomous cars to automatically adapt the position of the seat of the passenger depending on her/his needs in terms of comfort.
## General Description
The prototype is able to detect the needs of the user by looking to her/his eyes and the emotions captured by facial expressions. Depending on the detection the position of the seat (represented in a GUI) is changed.
## Software Architecture
The prototype is written in Python, divided in a client and a software part. The client part is thought to be executed on a Raspberry Pi with a camera connected which takes the photos of the face of the user. The server part receives such photos and makes the prediction using AI models. The result of the prediction is thus sent to the client side, which operates on the seat position, if needed. Facial recognition is used to save user profiles, containing their comfort preferences.

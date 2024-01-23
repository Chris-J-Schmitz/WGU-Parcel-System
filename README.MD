# WGU Parcel System

## Overview
This project, developed as part of the WGU C950 course, implements a parcel delivery system. 
It efficiently manages packages across multiple trucks, considering delivery times, distances, and special instructions.

## Features
* Package Management: Utilizes a hash table to efficiently store and retrieve package information.
* Truck Routing: Implements a delivery algorithm to optimize truck routes and minimize overall miles driven.
* User Interface: Provides a user-friendly command-line interface for querying package status and delivery information.

## Getting Started
### Prerequisites
* Python 3.x
* CSV files for addresses and distances

### Usage
#### Running the Program
```bash
python main.py
```

### Interacting with the UI
Follow the on-screen instructions to input a specific time and package IDs for status updates. 
The program will display the current status of the selected packages.

## Algorithm and Data Structures
The project employs a greedy algorithm for package delivery optimization and a hash table for efficient data retrieval.


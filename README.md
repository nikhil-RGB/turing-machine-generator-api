### Description:

- The [turing machine generator](https://github.com/nikhil-RGB/turing-machine-generator) is a cross platform application I created with flutter and dart to allow users to create, model, run, save and share Turing Machines.
- The application's "share" feature serializes the machine to a JSON string and allows it to be shared in this format.
- I am now aiming to create a fastapi+postgresql backend where users can store machines and group them online rather than locally, though I intend to keep both options available.
- This repository contains the code for the FastAPI application that connects the turing machine simulator application to it's relational db.

# HBNC Where Ya At App
# David Meyer


## Introduction
The main goal of the web app is accessibility and ease of use. Below are the main functions for the web app:
- This application will have a check-in check-out service that will log both the location and time when the staff/tech/subcontractor visits a jobsite to complete a work order.
- Users will be able to take photos or upload existing photos of job conditions, progress, or completion. These photos will be resized to be between 100 KB and 300 KB and then uploaded to a project-specific folder on Google Drive.
- The user will be able to upload signed documents or upload documents and sign them through the application itself.



## File Structure
- flaskr
  - flaskr
    - static
    - templates
    - init.py
    - flaskr.db
    - lib.py
    - model.py
    - views.py
  - setup.py
- flaskr.wsgi
- README.md
Descriptions of each file can be found within the files themselves.

## General Running Instructions
- For local execution the following commands are needed:
- Make sure you have python installed, pip installed, and that you have installed `flask, Flask, SQLAlchemy, flask-alchemy` with pip install. Then run the following commands <br/>
  `cd flaskr`<br/>
  `set FLASK_APP=flaskr`<br/>
  `set FLASK_DEBUG=true`<br/>
  `python -m flask run`<br/>

- To deploy on a web server you will need to do the following:
- Go to this website: https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps and follow the instructions.

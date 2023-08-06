# Flask Scheduler
Flask Scheduler is a simple Flask extension that allows you to schedule tasks to run at specific times.
It uses the APScheduler library to schedule tasks.

## Installation
Install Flask Scheduler using pip:
```shell
pip install Flask-Scheduler
```

## Usage
To use Flask Scheduler, import the extension and initialize it with your Flask app:
```python
from flask import Flask
from flask_scheduler import Scheduler

app = Flask(__name__)

# Initialize the extension
scheduler = Scheduler(app)

# scheduler config interval
app.config['SCHEDULER_API_INTERVAL'] = 5 # in seconds

@scheduler.runner()
def my_task():
    print('hi im running every 5 seconds')

# if you have separate task, and you don't want to run it every 5 seconds
# you can use interval argument in decorator
@scheduler.runner(interval=10)
def my_task1():
    print('hi im running every 10 seconds')
```

## Contributing
Contributions are welcome! Please submit a pull request.
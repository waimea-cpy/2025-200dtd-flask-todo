#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import register_error_handlers, not_found_error
from app.helpers.time import register_datetime_handlers, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Setup a session for messages, etc.
init_session(app)

# Handle 404 and 500 errors
register_error_handlers(app)

# Deal with UTC dates in timestamps
register_datetime_handlers(app)



#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        # Get all the incomplete tasks from the DB
        sql = """
            SELECT id, name, timestamp, priority, complete
            FROM tasks
            WHERE complete = 0
            ORDER BY priority DESC
        """
        result = client.execute(sql)
        incomplete = result.rows

        # Get all the complete tasks from the DB
        sql = """
            SELECT id, name, timestamp, priority, complete
            FROM tasks
            WHERE complete = 1
            ORDER BY priority DESC
        """
        result = client.execute(sql)
        complete = result.rows

        # And show them on the page
        return render_template("pages/home.jinja", incomplete=incomplete, complete=complete)


#-----------------------------------------------------------
# Route for adding a task, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_thing():
    # Get the data from the form
    name  = request.form.get("name")
    priority = request.form.get("priority")

    # Sanitise the inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the task to the DB
        sql = "INSERT INTO tasks (name, priority) VALUES (?, ?)"
        values = [name, priority]
        client.execute(sql, values)

        # Go back to the home page
        return redirect("/")


#-----------------------------------------------------------
# Route for completing a task, Id given in the route
#-----------------------------------------------------------
@app.get("/complete/<int:id>")
def task_complete(id):
    with connect_db() as client:
        # Update the status of the task
        sql = "UPDATE tasks SET complete=1 WHERE id=?"
        values = [id]
        client.execute(sql, values)

        # Go back to the home page
        return redirect("/")


#-----------------------------------------------------------
# Route for not completing a task, Id given in the route
#-----------------------------------------------------------
@app.get("/incomplete/<int:id>")
def task_incomplete(id):
    with connect_db() as client:
        # Update the status of the task
        sql = "UPDATE tasks SET complete=0 WHERE id=?"
        values = [id]
        client.execute(sql, values)

        # Go back to the home page
        return redirect("/")


#-----------------------------------------------------------
# Route for deleting a task, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_task(id):
    with connect_db() as client:
        # Delete the task from the DB
        sql = "DELETE FROM tasks WHERE id=?"
        values = [id]
        client.execute(sql, values)

        # Go back to the home page
        return redirect("/")



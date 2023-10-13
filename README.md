# FP Budget Manager
#### Video Demo:  https://youtu.be/KLz7eCboQU0
#### Description: A budgeting / expenses managing and presentation web app
## General Info
This is a budgeting and expenses managing and presentation app. It offers a minimum functionallity to login, logout, register a user based on the CS50 financial app.
It offers a Dashboard, an Add and a graph page with different functionalities.
## Login - Logout - Register
There are not many things to say about those link and routing points. They are identical to the CS50 financial app and where reused as any code should to prevent reinventing the wheel.
## Dashboard
Here is the entry point of any logedin user.\
This page shows a pie chart with the 10 most recent expenses for the current user grouped by category.\
Below the pie chart is a table with the 10 most recent transactions saved for the current user ordered by date. This table has the functionality that the user can delete any of the transactions shown. The design decision was made that the user should be able to delete the recent ones as it is less likely to have made a mistake that the user did not correct preciously.\
When a transaction is deleted the database is updated and the page is reloaded to show the newest most recent 10 transactions.\
The user can in this way delete is he persists all his transactions.\
If the user has no transactions saved this page prompts the user to click a link to the add page.
The pie chart is from chart.js.\
and the data shown are passed to the frontend with the falsk render_template() function. There they are used by a javascript to populate the piechart and the subsequent table.\
## Add
Here the user can fill a form and eventually add a transaction to the transactions table in the database.\
The inputs are validated i the frontend to help inexperienced users to avoid mistakes and in the backend to deter any foul actors from damaging the app.\
When the user presses the submit button a db.query is executed in the backround and the transaction if valid is entered to the transactions table.\
Then the user is redirected to the dashboard to she his newly latest entries.\
## Graphs
Here the user lands in the monthly expenses page.\
Where he is shown this months expenses grouped by category in a piechart form charts.js\
Bellow the pie chart is a baerhart where the user is shown his expenses for the current month grouped by date.\
The philosofy of population is the same as in the dashboard page.\
There are to green links in the page one to land back in the monthly expenses and ony to lande to the eyarly expenses.\
### yearly
Here the user is shown the expenses recored fo rthis current year grouped by category int he piechart.\
And the expenses sum grouped by month in the barchart bellow.\

## database.
The schema consist of 3 tables.\
A users table that stores username id and a hashed password.\
A transactions table that stores a trasaction id, user_id, type, amound and a spent_at information that is used to populate all the nodes and pages.\
A tr_type table that stores the different predifined transactions.\




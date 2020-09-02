# Invoice Generator

This project demonstrate how to build a simple flask app to generate pdf invoices using flask, flask-sqlalchemy, bootstrap and weasyprint. A common and pure python way to create PDFs is using Reportlab. The problem with Reportlab is that it can be quite time consuming to get the PDFs' design as you want it to be. In this project I'm going to weasyprint to create PDF invoice from a HTML template.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow the instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in `app.py` and can reference `models.py`. 

- [WeasyPrint](https://weasyprint.readthedocs.io/en/stable/index.html) is a smart solution helping web developers to create PDF documents. In this project it turns a simple HTML page into a PDF invoice.

### Running the server

From within the project directory first ensure you are working using your created virtual environment. All environment variables are set within the `.flaskenv` file:
- Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
- Setting the `FLASK_APP` variable to `app.py` from the project directory will tell the terminal the application to work with.

To run the server, execute in the terminal from within the proect directory:

```bash
flask run
```
## Models
- Positions: Entries represent the individual Positions for the PDF invoices.
- InvoiceDetails: Entry represents the invoice details like client information and invoicing period.

## Endpoints

### Index
```
GET '/'
```
- Returns the `index.html` template with jinja2 template inheritance of the `main.html` template.
### PositionsForm, Positions Table ad InvoiceForm
```
GET '/invoice_data'
```
- Returns the `invoice_form.html` template with jinja2 template inheritance of the `main.html` template.
- On the first run of the application it just renders the `PoitionsForm`.
- If there are entries in `Positions`, it renders them the positions table and renders the InvoiceForm.
- If there is an entry in `InvoiceDetails`, it prefills the `InvoiceForm`.
### Add Position
```
POST '/invoice_data'
PositionsForm submission
```
- Does a server side form validation of `PositionsForm` via `flask-wtf`.
- Adds the new position to the database via the class function `insert()`.
### Create Invoice
```
POST '/invoice_data'
InvoiceForm submission
```
- Does a server side form validation of `InvoiceForm` via `flask-wtf`.
- Adds the provided invoice details to the database via the class function `insert()` if no entry is in `InvoiceDetails`.
- If an entry exists it overwrites it via the class funtion `update(**kwargs)`
- Note: There will only be one entry in `InvoiceDetails`.
### Delete Positions
```
DELETE '/position_delete'
```
- Deletes a certain position from `Positions` specified by the id in the request body.

Request body:
```
{
    "position_id": "<position id>"
}
```
Response data:
```
{
    "url": "<url invoice form endpoint (GET)>"
}
```
### Create Invoice PDF
```
POST '/invoice_pdf'
```
- Queries for the previously added data in `Positions` and `InvoiceDetails` to fill the invoice template.
- Passes the rendered template as a string to weasyprints' `HTML` and serves the PDF as an in-memory object via flasks' `send_file`.
- BytesIO is used, because it is neccessary to hand an object to `send_file` which has a read() method.

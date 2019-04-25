# ATTENTION!!! README.md STILL UNDER DEVELOPMENT, PLEASE IGNORE!!

## HTTP Request / Response

### Retrieving All Tables Available

- Method : `GET /`
- Should connect to database `fuelControl.db` and show all tables available

_**Response**_

- `200 OK`
  - This is the only response possible, since there is no additional parameters to be provided
  - This shall return a list with all Tables available in current database
```json
[
    "car002",
    "car004",
    "car003"
]
```

### Creating a new Table

- Method : `POST /`
- Should connect to database `fuelControl.db` and create a table with all parameters needed
- See _Database Schema_ at the end of this document to check out the parameters
- Input should be an array of only one element, being it the table's names the user wants to create
```json
[
    "car002"
]
```

_**Response**_

- `201 Created`
  - If the table's creation was a success
- `400 Bad Request`
  - When the input has more than one element
- `406 Not Acceptable`
  - When user's input is not a list
- `409 Conflict`
  - When there is already a table for the given input
  - Also returns all tables available
```json
[
    "car002",
    "car004",
    "car003"
]
```


### Accessing Database Information

- Method : `GET /<carName>`
- Should connect to database `fuelControl.db` and show all information by default

_**Response**_

- `404 Not Found`
  - If there is no `<carName>` table in current database
- `200 OK`
  - If the request was a success
  - Should also return the information in a JSON format
```json
[
  {
      "date" : "2018-09-20",
      "mileage" : 10000,
      "pricePerLitre" : 4.000,
      "litreTotal" : 20.0,
      "payTotal" : 80.00,
      "fuelType" : "Gasolina Comum",
      "mileageDiff" : 0,
      "efficiency" : 0.00,
      "pricePerKm" : 0.00,
      "comments" : "..."
  },
  {
      "date" : "2018-09-23",
      "mileage" : 10500,
      "pricePerLitre" : 4.000,
      "litreTotal" : 25.0,
      "payTotal" : 100.00,
      "fuelType" : "Gasolina Comum",
      "mileageDiff" : 500,
      "efficiency" : 20.00,
      "pricePerKm" : 0.20,
      "comments" : "insert comment"
  }
]
```

### Inputing data to Database

- Method : `POST /<carName>`
- Should connect to `fuelControl.db` database and input information into it
- The format of the data to be provided in this method is also a JSON
```json
{
    "date" : "2018-09-20",
    "mileage" : 10000,
    "pricePerLitre" : 4.000,
    "litreTotal" : 20.0,
    "fuelType" : "Gasolina Comum",
    "comments" : "insert comment"
}
```

_**Response**_

- `500 Internal Server Error`
  - If the input data results in some calculation error. Most likely the mileage parameter passed is equal or less than the previous one in database.
- `404 Not Found`
  - If there is no `<carName>` table in current database
- `400 Bad Request`
  - If the data type for some of the input values is wrong
  - Or if data type is not a dictionary
  - Should return a json with an example of input
- `200 OK`
  - If the request was a success

### Changing Table's Content

- Method : `PUT /<carName>/`
- Should connect to `fuelControl.db` and `<carName>` and change the table's content according to the input
- The format of the data to be provided in this method is a JSON
    - The only mandatory field to be provided is "rowId
```json
{
    "rowId" : 5,
    "date" : "2018-09-23",
    "mileage" : 10500,
    "pricePerLitre" : 4.000,
    "litreTotal" : 25.0,
    "payTotal" : 100.00,
    "fuelType" : "Gasolina Comum",
    "mileageDiff" : 500,
    "efficiency" : 20.00,
    "pricePerKm" : 0.20,
    "comments" : "insert comment"
}
```

_**Response**_

- `400 Bad Request`
  - If the data type for some of the input values is wrong
- `200 OK`
  - If the request was a success

### Deleting Car from database

- Method : `DELETE /<carName>`
- Should connect to `fuelControl.db` database and delete the `<carName>` table

_**Response**_

- `404 Not Found`
  - Means that there is no `<carName>` table to be deleted
- `200 OK`
  - If the request was a success

### Accessing Table's Parameters

- Method : `GET /<carName>/paramaters`
- Should connect to `fuelControl.db` and `<carName>` table to provide its parameters

_**Response**_

- `404 Not Found`
  - Means that there is no `<carName>` table to be accessed
- `200 OK`
  - If the request was a success
  - Should also return a JSON with a list of parameters
```
[
  "date",
  "mileage",
  "pricePerLitre",
  "litreTotal",
  "payTotal",
  "fuelType",
  "mileageDiff",
  "efficiency",
  "pricePerKm",
  "comments"
]
```

## Database Schema
```
CREATE TABLE buyingStock (
    date DATE, 
    stock VARCHAR(20), 
    quantity INTEGER, 
    value FLOAT, 
    totalValue FLOAT, 
    totalValuePaid FLOAT
);

CREATE TABLE sellingStock (
    date DATE, 
    stock VARCHAR(20), 
    quantity INTEGER, 
    value FLOAT, 
    totalValue FLOAT, 
    totalValueReceived FLOAT
);          
```
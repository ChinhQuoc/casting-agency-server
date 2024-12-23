# Backend - Casting Agency

## Setting up the Backend

### Install Dependencies

1. **Python 3.7**

2. Open terminal and run command:

```bash
pip install -r requirements.txt
```

### Set up the Database

With Postgres running, create a `casting_agency` database:

```bash
createdb casting_agency
```

Populate the database using the `casting_agency.psql` file provided. Open terminal run:

```bash
psql casting_agency < casting_agency.psql
```

### Run the Server

On the folder project, Open terminal and run:

```bash
python run.py
```

## Documenting your Endpoints

`GET '/movies'`

- Get list movies
- Returns: An object with the following keys:
  - `success`: A boolean indicating the request status.
  - `movies`: A list of question objects, each containing `id`, `releaseDate`, and `title`.

```json
{
  "movies": [
    {
      "id": 2,
      "releaseDate": "Tue, 24 Dec 2024 00:00:00 GMT",
      "title": "ggi uu kiguf"
    },
    {
      "id": 1,
      "releaseDate": "Wed, 20 May 2020 00:00:00 GMT",
      "title": "Bad Boys for Life update"
    }
  ],
  "success": true
}
```

`GET '/actors'`

- Get list actor
- Returns: An object with the following keys:
  - `success`: A boolean indicating the request status.
  - `actors`: A list of question objects, each containing `id`, `age`, `gender`, and `name`.

```json
{
  "actors": [
    {
      "age": 57,
      "gender": "male",
      "id": 1,
      "name": "Johnny Depp"
    },
    {
      "age": 5,
      "gender": "female",
      "id": 3,
      "name": "fwe Anna"
    },
    {
      "age": 13,
      "gender": "male",
      "id": 4,
      "name": "Gta de fff"
    },
    {
      "age": 9,
      "gender": "female",
      "id": 6,
      "name": "hgf uuy 1"
    }
  ],
  "success": true
}
```

`GET '/movies/<int:id>'`

- Get a specific movie identified by its unique id.
- URL Parameters:
  - `id`: An integer representing the unique identifier of the question to be deleted.
- Returns: An object with the following keys:
  - `success`: A boolean indicating the request status.
  - `movie`: A object movie and along with the corresponding actor list, each containing `id`, `releaseDate`, `title`, and `name`.

```json
{
  "movie": {
    "actors": [
      {
        "age": 5,
        "gender": "female",
        "id": 3,
        "name": "fwe Anna"
      },
      {
        "age": 13,
        "gender": "male",
        "id": 4,
        "name": "Gta de fff"
      }
    ],
    "id": 2,
    "releaseDate": "Tue, 24 Dec 2024 00:00:00 GMT",
    "title": "ggi uu kiguf"
  },
  "success": true
}
```

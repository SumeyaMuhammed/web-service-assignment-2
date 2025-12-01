# Web Service Assignment II
This project is a simple Flask-based web service that integrates with The Movie Database (TMDB) API. It demonstrates web service integration, authentication, data transformation, and error handling.

## Features

- Fetch movie details from TMDB
- List popular movies
- JWT login + protected route
- HTML movie summary page
- Error-testing endpoint
- Logs stored in movie_app.log

## Technologies Used
          
- Python 3       
- Flask          
- Requests       
- TMDB API       
- PyJWT         
- python-dotenv  
- Logging module 
- HTML/CSS       
- Postman        


## Main Endpoints
| Endpoint            | Description         |
| ------------------- | ------------------- |
| `/movie?id=ID`      | Fetch movie by ID   |
| `/movies/list`      | List popular movies |
| `/movies/summary`   | HTML summary page   |
| `/auth/login`       | Get JWT token       |
| `/auth/profile`     | Protected route     |
| `/movie/error-test` | Trigger error       |


## Conclusion

This project successfully demonstrates REST API integration, authentication with JWT, data transformation, and error handling using Flask. It fulfills all assignment requirements in a simple, well-organized structure.
<h2> project crawl careerbuilder </h2>

###  Download source code : [here](https://github.com/LynnGG/CDNLT/releases/tag/v1.0.0)
### AUTO API
  - Turn on docker
  - Run `Docker compose up -d` and using :D thank u

## how to use
- ### Turn on Server MySQL
  
  - Crawl step by step
      - `docker-compose up -d`
      - `Cd scraper`
      - Run `python jobs_scraper.py`
    
  - Open Api
    - `Cd api`
    - Run `uvicorn api:app --reload`
  

## Info Docker
  - Database: job_data
  - User: jobuser
  - Password: jobpassword
  - Table: job_data

## DOCKER 
  -  `docker kill $(docker ps -q)` / STOP ALL 
  -  `docker rmi -f $(docker images -aq)` / KILL ALL
## Testing Api
  -  http://34.170.190.29:8080/docs
  -  http://34.170.190.29:8080/

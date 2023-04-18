<h2> project crawl careerbuilder </h2>


### AUTO API
  - Turn on docker
  - Run `Docker compose up -d` and using :D thank u
## how to use
- ### Turn on Server MySQL
  - If u dont want to run crawl again, u can download if image in here : 
  [Download Image](https://drive.google.com/drive/folders/17wPx4fKYMTzCtkLi7DxQPS8CyqxKDO5t)
      - docker load -i database_careerbuilder.tar
      - docker run database_careerbuilder
  <p></p>
  
  - If u want to run the code 
      - docker-compose up -d
      - Cd scraper
      - Run python jobs_scraper.py
    
- ### Turn on Docker API
  - ...
## Info Docker
  - Database: job_data
  - User: jobuser
  - Password: jobpassword
  - Table: job_data

## DOCKER 
  -  docker kill $(docker ps -q) / STOP ALL 
  -  docker rmi -f $(docker images -aq) / KILL ALL
## Testing Api
  -  http://34.170.190.29:8080/docs
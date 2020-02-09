# Description
Docker-compose for scrape top news from Reuters every hour and store it into postgres and mongo

# Install and run:
 - Install docker and docker-compose
 - Run command
 `docker-compose build`
 - Run command
 `docker-compose start`

 After that parse process will repeat every hour.
 Database and scheme created automatically. You can change database settings in .env file 

# Retreive csv file
To get csv file with news on speciefic date run command: 
`./scraper.sh --get <date string>`

# Run parsing manually
To run parsing process manually run command:
`./scraper.sh --parse`

# Run without docker

 - Install dependencies:
 `pip install -r requirements.txt`

 - Set db settings to environ
 ```export DB_USER=test_user
    export DB_PASS=test_pass
    export DB_NAME=news_db
    export DB_TABLE=news
    export MONGO_HOST=mongo
    export POSTGRES_HOST=postgres
 ```

 - Create database and schema:
    `bash ./postgres/init.sh`

 - Run scraper continious process:
 `python scraper/scraper.py --parse_forever`

 - Get data for speciefic date:
 `python scraper/scraper.py --get <date string>`

 - Parse data:
 `python scraper/scraper.py --parse`
# URL shortener
This URL Shortener is a simple yet powerful service designed to shorten long URLs into more manageable and shareable links. It's built using Python and Django, providing a lightweight and efficient solution for generating short URLs on the fly.

## Features covered
- URL Shortening: Convert long URLs into short, easy-to-share links.
- Customization: Optionally customize shortened URLs to make them more memorable.
- Analytics: Track clicks and view statistics for each shortened URL e.g. access frequency of URLs for a particular day
- API Integration: Integrate URL shortening functionality into other applications using the provided API endpoints.
- Postman Collection: Interface for generating and managing shortened URLs.

## Technologies used
1. Python
2. Django
3. Redis
4. MySQL

## Services
1. Compress: Minify the full URLs into short URLs or slugs
2. Sluggen: Store precomputed slugs in DB, and a subset of these slugs is kept in Redis
3. Analytics: Maintain the access frequency of each URL

## Essential settings before starting the app have to configured in 

`url_shortener/url_shortener/settings.py`

``CACHES =
DATABASES = 
POPULATE_SLUGS_DB_BATCH_SIZE = 
SLUGS_IN_REDIS_COUNT = ``

Although, default values have been provided, you might need to update endpoint and credentials of Redis
inside CACHES variable. Also, if you want to use a different database e.g. MySQL.

Inside redis, three separate databases have been taken for storing 
requested shortened URLs, slugs, and stats of URLs accessed.

## Steps to get started:
1. First we have to precompute the slugs using

    `python manage.py generate_slugs_in_db` 
2. Store some slugs in Redis from database, to enable sluggen to provide an unused slug for each URL using

    `python manage.py populate_slugs_in_redis`
3. Ready to launch the project, do it using

    `python manage.py runserver`

Now your application should start running on port 8000 on your localhost.

Do refer the POSTMAN collection `URL Shortener.postman_collection.json`, to expedite the process. To do so, just set
an ENV value of `domain` to `http://127.0.0.1:8000` before requesting respective APIs.

## Few essential commands:
1. To populate our database with fresh slugs, when we are running out of slugs. 
   This has to be put as a cron based on how frequently they are getting consumed.

    `python manage.py generate_slugs_in_db` 
2. Sluggen will provide fresh slugs from Redis. To ensure Sluggen has sufficient slugs
   this again has to be put in cron.

    `python manage.py populate_slugs_in_redis`
3. Since analytics is assumed to be a non essential service. We cab persist data 
   from Redis into database on hourly basis. Once persisted that data can be deleted from Redis. 
   Following is command to be scheduled hourly to fetch data of previous hour and persist that
   into database.

    `python manage.py persist_stats_from_redis`


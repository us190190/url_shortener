**'URL shortener' app**

Features covered:
1. Provide a URL and get a short URL
2. Fetch full URL from the short URL
3. Search for suggestions of a string based on stored URLs in the system
4. Fetch access frequency of URLs for a particular day

The project has been implemented using Django, Redis and SQLite.

Consists of three applications:
1. compress (to minify the full URLs into short URLs or slugs)
2. sluggen (to store precomputed slugs in DB, and a subset of these slugs is kept in Redis)
3. analytics (to maintain the access frequency of each URL)

Few essential settings before starting the app have to configured in 

`_url_shortener/url_shortener/settings.py_`

`CACHES = `

`DATABASES = `

`POPULATE_SLUGS_DB_BATCH_SIZE = `

`SLUGS_IN_REDIS_COUNT = `

Although, default values have been provided, you might need to update endpoint and credentials of Redis
inside CACHES variable. Also, if you want to use a different database e.g. MySQL.

Inside redis, three separate databases have been taken for storing 
requested shortened URLs, slugs, and stats of URLs accessed.

Steps to get started:
1. First we have to precompute the slugs using

    `_python manage.py generate_slugs_in_db_` 
2. Store some slugs in Redis from database, to enable sluggen to provide an unused slug for each URL using

    `_python manage.py populate_slugs_in_redis_`
3. Ready to launch the project, do it using

    `_python manage.py runserver_`

Now your application should start running on port 8000 on your localhost.

Do refer the POSTMAN collection _`URL Shortener.postman_collection.json`_, to expedite the process. To do so, just set
an ENV value of `_domain_` to `_http://127.0.0.1:8000_` before requesting respective APIs.

Few essential commands:
1. To populate our database with fresh slugs, when we are running out of slugs. 
   This has to be put as a cron based on how frequently they are getting consumed.

    `_python manage.py generate_slugs_in_db_` 
2. Sluggen will provide fresh slugs from Redis. To ensure Sluggen has sufficient slugs
   this again has to be put in cron.

    `_python manage.py populate_slugs_in_redis_`
3. Since analytics is assumed to be a non essential service. We cab persist data 
   from Redis into database on hourly basis. Once persisted that data can be deleted from Redis. 
   Following is command to be scheduled hourly to fetch data of previous hour and persist that
   into database.

    `_python manage.py persist_stats_from_redis_`


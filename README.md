# timeseries-demo
Demo distributed application collecting, storing, and showing time-series weather data for Baton Rouge, Louisiana

### setup
(Recommend installing on a Mac or Linux machine - developed on Ubuntu)
- Install python 3.10+
- Install docker
- Install docker-compose

From the project root:
1. `docker-compose build`
2. `docker-compose up`

This will start the web application, data collector application, and timescaledb.

From there...

3. Make a call (browser is okay!) to `localhost:8002/collect`
4. Go to `localhost:8001` to view the simple web ui.
5. Go to `localhost:8001/api/weather_hours` and localhost:8001/api/weather_timeseries to view
the raw data and chart datapoints directly.

Reach out to me at Michael.B.Kolbeck@gmail.com with any questions!
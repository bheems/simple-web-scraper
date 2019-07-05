# Web Scraper (template)

  Fetches commodity futures data (extracts only date/price fields, here), and locally stores into a .csv file relative to the commodity type/name -- (fetch.py)
  
  Flask application starts an API web-service on port 8080 (GET), which returns scraped data with selected descriptive        statistics of price points -- (api.py)
  
  Example API call (input):
  
    curl 'http://127.0.0.1:8080/commodity?start_date=2017-05-10&end_date=2017-05-22&commodity_type=gold' 

  Example API call (output)
    
     { 
      "data": { 
     "2017-05-10": 1253.06, 
     "2017-05-11": 1280.46, 
     "2017-05-12": 1278.21 
      } 
    "mean": 1270.57, 
    "variance": 231.39 
    } 


  Main packages used: 
  
    1. BeautifulSoup
    2. Flask
    3. Pandas
    4. requests

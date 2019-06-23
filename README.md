# ScrapePlayStoreReviews
APIs to extract reviews from Google Play Store don't work beyond Page 111. This scraper is intended to scrape ALL reviews from an app.
It works by automating the human action of scrolling play store reviews (via Selenium) and saving each review visible on the page.
Some caveats to the code from my experience running it:
  - Depending on the number of reviews, scrolling to the earliest review can take over two days.
  - The Google Play Store window controlled by the code must always be active for the page to load on scrolling. I had a spare monitor that I connected to my laptop to keep the window active, while I continued to use my laptop as usual.
  - The speed of loading a page on scrolling will depend on the speed of your Internet connection. You can adjust the sleep time based on your Internet speed.
  - If you lose Internet connection for too long, webdriver will lose the chrome window. In this case, use the scroll_open_browser code to reconnect to the window and begin scrolling from where it left off. Remember to change the driver_id and counter value to that provided by scroll.py

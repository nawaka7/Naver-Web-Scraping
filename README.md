# Naver-Web-Scraping
Naver (네이버) 지식인  크롤링 (Crawling / Scraping)
This project was to investigate the publicly perceived brand images of the three Korean telecommunication companies.
The project looked into both broadband internet and IPTV business but here I only introduce a part of the codes: only the broadband part.
Furthermore, the text data preprocessing was carried out by another analyst. That part was also not uploaded.


## Crawler_Naver_Final.py
The keywords preselected through surveys are listed. These keywords are searched in Naver's DB.

## Crawler_Depth_Final.py
With the URLs collected from the Crawler_Naver_Final file, this python file runs the main scraping function and saves the text data.

## Duplicity_Check_Final.py
Since there could be webpages that are repeatedly scraped despite the different search keywords, the Duplicity_Check_Final checks if a certain webpage(document) is overrepresented in the data.

## Crawler_Apriori.py
This python file runs apriori functions and visualize the data with graphs. In the real final report, other various visualization and analytic technics were employed


# Web-Scrapping-Covid-Data
Application to crawl web pages and extracting the required information from them by creating suitable grammar rules. Data is being extracted for the following given countries.
<details>
  <summary>Country list</summary>

  *   <details>
      <summary>Europe</summary>

       <p>
          France | UK | Russia | Italy | Germany | Spain | Poland | Netherlands | Ukraine | Belgium
        </p>
      </details>
 
  *   <details>
      <summary>North America</summary>

       <p>
          USA | Mexico | Canada | Cuba | Costa Rica | Panama
        </p>
      </details>
 
  *   <details>
      <summary>Asia</summary>

       <p>
          India | Turkey | Iran | Indonesia | Philippines | Japan | Israel | Malaysia | Thailand | Vietnam | Iraq | Bangladesh | Pakistan
        </p>
      </details>
 
  *   <details>
      <summary>South America</summary>

       <p>
          Brazil | Argentina | Colombia | Peru | Chile | Bolivia | Uruguay | Paraguay | Venezuela
        </p>
      </details>
  *   <details>
      <summary>Africa</summary>

       <p>
          South Africa | Morocco | Tunisia | Ethiopia | Libya | Egypt | Kenya | Zambia | Algeria | Botswana | Nigeria | Zimbabwe
        </p>
      </details>
  *   <details>
      <summary>Oceania</summary>

       <p>
          Australia | Fiji | Papua New Guinea | New Caledonia | New Zealand
        </p>
      </details>
 
  </details>
  
## Crawling worldometers

 [Worldometer](https://www.worldometers.info/coronavirus/) is a website where you will find all the coronavirus-related statistics world/continent/country-wise, like total cases, active cases, total death, new death, total recovered, serious/critical cases, total tests are done, etc.<br/>
 Extracting yesterday's data to find the following queries for the world, all continents, and below given countries. 
 <details>
  <summary>Queries</summary>
  <p>Total cases | Active cases | Total deaths | Total recovered | Total tests | Death/million | Tests/million | New case | New death | New recovered</p>
</details>

<img src="https://user-images.githubusercontent.com/47922035/160141954-41ffac31-6eb9-4cd8-a886-1edd3ac09c9a.jpg" width="1100" height="380">

## Extraxting Countries Covid date-wise data.

Given a country name, start, and end date, application answers the following queries
 <details>
  <summary>Queries</summary>
 
   * Change in active cases in %
   * Change in daily death in %
   * Change in new recovered in %
   * Change in new cases in %
   * Closest country similar to Change in active cases in %
   * Closest country similar to Change in daily death in %
   * Closest country similar to Change in new recovered in %
   * Closest country similar to Change in new cases in %
</details>


<img src="https://user-images.githubusercontent.com/47922035/160142506-f4382b87-793a-4113-a552-b4aa2f9fc6a6.png" width="900" height="500">

# Web-Scrapping-Covid-News

## Extracting Covid worldwide News/Response

[Timeline of Covid-19](https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic) is a website managed by wikipedia. It reports all the coivd  related world/country specific news/response.<br/>
Given a Start date and End date, the application extracts all the worldwide covid related news/response between the two dates. Also It Plots a <b>Word Cloud</b> with all words present in the news
![ss](https://user-images.githubusercontent.com/47922035/160137422-6f67ddb6-231c-4658-8df6-f359f7099480.jpg)

## Plotting word cloud and finding covid words

For the below operations, stopwords are ignored.
Given two non-overlapping date range
* Application extracts all the common words and also covid common words. Covid Words are given in the folder.
* Finds the percentage of covid words in common words
* Find the top-20 common and covid common words
* 
<img src="https://user-images.githubusercontent.com/47922035/160137569-3e225706-5316-4e67-9728-e4aaf13b3d19.png" width="900" height="500">

## Extracting Date Range
 
 Given a country, Extracting the start and end date for which country's covid news is available

## Extracting the country specific covid news 

Given a country and date range, 
* Application extracts all the covid news related to that country between given dates.
* Plotting a word cloud(Ignoring Word cloud) with all the words in the news extracted.
<img src="https://user-images.githubusercontent.com/47922035/160139529-e33084d1-e69c-4efb-9cb2-bb983bb51d48.png" width="900" height="500">

## Finding Top 3 closest countries according to Jaccard Similarity
Given a country and a date range,
* Application finds the top-3 countries with most similar word match according to Jaccard Similarity
* Application finds the top-3 countries with most similar covid word match according to Jaccard Similarity
    ```
   J(A,B) = |A ∩ B|/|A ∪ B| where, A & B are the set of words extracted from news between given range
   ```

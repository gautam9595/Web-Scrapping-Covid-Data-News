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
# Web-Scrapping-Covid-News

## Extracting Covid worldwide News/Response

[Timeline of Covid-19](https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic) is a website managed by wikipedia. It reports all the coivd  related world/country specific news/response.<br/>
Given a Start date and End date, the application extracts all the worldwide covid related news/response between the two dates. Also It Plots a <b>Word Cloud</b> with all words present in the news.
![Screenshot from 2022-03-25 19-01-30](https://user-images.githubusercontent.com/47922035/160131559-2e94a8fb-f427-4191-9d4e-3ce7decb2194.png)

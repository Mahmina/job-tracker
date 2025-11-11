<h1>Job Tracker (StepStone Scraper)</h1>
<br />

<h2>Description</h2>
This is a Python automation tool using Selenium that searches StepStone for Frontend jobs in Germany, filters by part-time, 5km radius and posted in the last 24h. Then it sends the results to a Google Sheet with an email summary. It uses Selenium with a persisted Chrome profile for reliable browsing, posts job data to a REST endpoint, and notifies via Gmail SMTP.<br />


<h2>Languages and Utilities Used</h2>

- <b>Python</b> 
- <b>Selenium</b>
- <b>SMTP (smtplib)</b>
- <b>Sheety API</b>



<h2>Program walk-through:</h2>
- Log into Sheety with your Google Account (the same account that owns the Google Sheet)
<br />
- Make sure you give Sheety permission to access your Google sheets.
<br />
- Under your Google Account Security settings, you should see that Sheety has access. Double-check that you see Sheety listed as an authorized app. Otherwise, Python code can't access your spreadsheet.
<br />
- In project page, click on "New Project" and create a new project in Sheety and paste in the URL of your own Google Sheet.
<br />
- Click on the API endpoint and enable GET and POST.
<br />
<br />
<br />
<p align="center">
Environment Variables: <br/>
<img src="https://imgur.com/P0sbkkf.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />



<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>

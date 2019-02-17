# Stout Django App

This Django app gives stats about your favorite beer, restaurants, and more! Utilizes large example data sample inserted, edited and stored within Amazon RDS and deployed with AWS Elastic Beanstalk. 

The web application has five tabs. Bar, Beer, Drinker, Modification, and Query. Bar, Beer, Drinker tabs will show their respective data, bar plots, and summary.

## Screenshots
![Drinker Information Search](https://i.imgur.com/JtpvUTQ.png "Drinker Information")
You can look up the drinker at the top bar. The web application will help fill in the name for you. 


![Drinker Information Summary](https://i.imgur.com/lo7kJc4.png "Drinker Summary")
Some of the button in the body page will give summaries of the drinker. 


![Drinker Information Bar](https://i.imgur.com/RvIv7pc.png "Drinker Bargraph")
Using AngularJS, the web application will depict some information about the drinker you asked for. 


## ER Diagram
![ER Diagram](https://i.imgur.com/EBEmUQe.png "ER Diagram" )
Visualization of the relationships of elements within entities. 

## Database Schema
Drinkers[d_id, first_name, last_name, phone_number, street, city, state, zip]

Transactions[t_id, date, time, weekday, total_price, tip, d_id(FK), license(FK)]

Bars[name, license, phone_number, street, city, state, zip]

Frequents[drinker(FK), bar(FK)]

Hours[bar_license(FK), day(FK), open_hour, close_hour, happy_hour_start, happy_hour_end] Items[name, type, manf]

Items_Sold[transaction(FK), item(FK), price]

Likes[drinker(FK), item(FK)]

Sells[bar(FK), item(FK), price, happy_hour]




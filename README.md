# MarathonMentor
A Web Application that is able to create a tailored Marathon training plan. This is my CS50w Final Project.

### Note: You will need to run
```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Log of progress
As of 15/10/2023, I have decided to keep a log of what I am doing, what needs to be done, etc., for my own personal convenience. I hope to use this in the future
for documnetation.

| **Date**    | **Status**    | **TODO for next time**    | **Notes**    |
|---------------- | --------------- | --------------- | --------------- |
| 15/10/2023    | Getting back into the project after a hiatus    | ~~Create the form for the user sign-up and Marathon Plan creation~~ | N/A |
| 16/10/2023    | Creating form. Found bug in plan_algo.py: overload factor not used. Changed to progression factor for each of the phases. Now looking to see if this works. Things work, runs scheduled| 1) The algorithm is very slow, might need to rethink things. ~~2) The progression factor esculates ridicously fast, might need a logarithmic function that decreaes as time goes on. 3) Ensure that the sets, on and off are done correctly.~~ 4) Make sure that the taper week is done correctly  | Can recommend beginners to have at least 180 day plan. |
| 17/10/2023    | Started messing around with correct implemenation of overload factors | Implement the duration overload factor, and then continue with the other attributes in plan_algo.py | ~~Change the database? How much does sqlite scale too? Maybe rethink the implemenation of the db? Or just need a faster alogrithm~~ |
| 20/10/2023    | Want to change the slqlite3 database to mySQL in django, also realised that the default runs are no longer saved as I used .gitignore, not sure if it's worth making a larger hash table instead to combine a lot of data, system design is a real thing! Things seem to work now and it's faster. | There are runs added to the db on the same date and the dates of runs are very messed up | I will need to implement an extension of the plan_algo to update the runs when a user has completed a run to better predict distance, duration, pace, etc. |
| 21/10/2023    | Going to fix the issue with the run dates, ~~and then that should mean I can start work on the front end~~. No, need to create the taper week. Updated algorithm so plans are created successfully with a taper week into the martathon date | Update the docstrings within the plan_algo file, tidy up types and return values, and then begin to work on the front end | I should create a way to log in and test creating a plan and then wipe all the test users  |
| 22/10/2023    | Used crisp forms for the forms on the front end, utilized djangos built in auth models, started work on the front end and installed bootstrap | Try to get a sidebar working instead of a navigation bar | I should create a way to log in and test creating a plan and then wipe all the test users  | Hard to get the side bar working, but take some time to do it but learn! |
| 24/10/2023    | Managed to do the side bar, I think before I carry on with the homepage, make sure that the login and registration pages and system are working ->|I have just seen for the registration, I need to make the user aware of constraints for birth date, marathon date, recommendation for length of marathon for fitness levels etc. Want to create a user and then have the user create a plan if they then want to, i.e., marathon date is optional | Use JS to generate anything dynamic on the page |
| 26/10/2023    | Have refactored and adjusted the password forgotten/reset loop. Have created the homepage and have started it, realised that for a SPA I will have to write all the pages in JS! | Get a home page sorted in JS | I am going to use vanilla JS to understand it more before using a framework for the next web app|
| 27/10/2023    | I have decided that I am going to try and learn react because why not and desgin the index page in react instead and save myself some headache. Doing react tutorial to get the syntax down| | |
| 29/10/2023    | ~~Completed the react tutorial, looking now at implementing it into my app~~ React is causing more issues than it's worth so will just use plain js | | |
| 30/10/2023    | Working on the homepage and implementing showing the runs, need to: ~~1) Verify what the difference is for Distance and interval runs to show it on the screen 2) Implement the "Upcoming runs..." to show the next 3 runs on the homepage 3) Use JS on the Scheduled Runs (ex. calendar) to display all the schedueled runs by month~~ 4) Find a way to implement the "completed runs" and then update the home page, scheduled runs, and completed runs 5) Strava integration and auto complete the runs | To note: What happens to the home page when I finish a plan, what happens to the upcomming runs after I finish a plan, what happens to the pages after I finish a plan. Carry on with point 3| Might be worth adding some colouring onto the runs so visually you can see what zones you will be working in|
| 02/11/2023    | Todya's work: 4) Find a way to implement the "completed runs" and then update the home page, scheduled runs, and completed runs 5) Strava integration and auto complete the runs |||

### Potential bugs / features to implement
- What happens to the home page when I finish a plan, what happens to the upcomming runs after I finish a plan, what happens to the pages after I finish a plan

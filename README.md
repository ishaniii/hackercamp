# TV Series Email Updater

Script written in Python 3 which helps keep a track of multiple TV series of the user's choice and sends an email update of their upcoming episode's air date (as mentioned in IMDb)

## Getting Started

* Open config.py and make sure you assign all the variables with accurate values for the database connection.
* The email address of the sender of the email and his password should be updated in config file.
* Install all required modules before executing the code. The Prerequisites are mentioned below.

### Prerequisites

The script uses following libraries and these must be installed prior to running:

* PyMySQL: A library that connects SQL with the Python script.
* SMTPLIB: This will be used to send emails from Python script using SMTP server.
* IMDbPY: This is a Python package useful to retrieve and manage the data of the IMDb movie database.

### Requirements
To install all above mentioned requirements, run
 ```pip3 install -r requirements.txt```

## Running the Main Script

Use ```python3 ./main.py``` to run the script.

At the prompt, enter the accurate email address of receiver and names (comma-separated) of TV shows of which you want updates of.

Examples:
```
$ python3 main.py
Number of users: 1
Email: receiveremail@gmail.com
Series: friends


$ python main.py
Number of users: 2
Email: receiver1mail@gmail.com
Series: Game of Thrones, Friends, Suits

Email: receiver2mail@gmail.com
Series: Big Bang Theory, Suits

```

## Key Features
  * Database maintaining the details of users (can be easily expanded as per need) and status of email success.
  * Database can be further used and exploited to make reports of user preferences and popularity of tv series.
  * Basic verification of email address entered at Input prompt.
  * Smart search for all kinds of inputs given as names of tv series.
  * Email feature to update the users with the latest status of the tv series of their choice.

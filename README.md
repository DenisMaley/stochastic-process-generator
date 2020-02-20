## Stochastic process generator

The aim of this project is to build three simple components that interact with each other. 
They should all run without manual intervention. 
So, for example, you should also handle the scenario where one of the components breaks down.

#### Time Server

This calculates the time left (in days) until the end of this year. 
While calculating this, each Saturday should be counted as 0.75 days, and each Sunday should be counted as 0.5 days. 
On every day, the time passes linearly from midnight to midnight. For example, on 26th of December 2018, at 15:40, 
the time left until the end of the year should be (25 / 72 + 3 + 0.75 + 0.5) days. 
Here 25/72 is the time left on 26th of December, 0.75 and 0.5 are for the Saturday and Sunday, 
and 3 is for remaining days. We call this the “virtual time” until end of the year.

This can also set an alarm. That is, given a period, this server can send an alarm signal after that period. 
For example, if the period is 0.04 days, then it will send a signal after 0.04 virtual days has elapsed. 
(Note that in real time, this means the alarm signal will be sent after 0.08 real days on Sundays.)

#### Parameter Server

This server does the following:
Step1: Set p = 0.
Step2: Generate a random number r between 0 and 0.02. Sleep for r days.
Step3: Generate a random number s between 0 and 1. Set p = p + s.
Step4: Publish/broadcast p to all interested parties.
Step5: Go back to Step2.

#### The printer

The aim of this component is to print (say to a log file) the parameter p (as indicated by the parameter) 
and the time left until the end of this year. It should print whenever p changes and also if 0.01 virtual days 
has passed since the last print.  


## Running

`$ docker-compose up -d`

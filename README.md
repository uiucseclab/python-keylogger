# python-keylogger

Windows keylogger for my security lab project using python 3.4.

The program implements multithreading to simultaneously log keypresses, take screenshots, and send/receive data via an email account specified in main.py.  
To start the program, run runme.cmd. This will download and update any required libraries (provided python is already installed on the victim machine).  The program will then begin to record keypresses, take screenshots and save them in their respective output directories. After a desired interval (default is 2 hours) the key logging and screen capturing threads will pause, all current output will be zipped, emailed and deleted. Key logging and screen capturing will subsequently resume. 
There are also a few commands that can be sent to the program via the email account. Any command must have the word “action” as the subject line, otherwise it will be ignored. If the body of the email contains the word “send” then the program will zip and send all current data when it receives the message. This does not reset the two hour timer. If the body of the email contains the word “capture” then the program will take and save a screenshot. If the body of the email contains “stop” then the program will exit. The commands “move x y” and “click x y” will respectively move and click the mouse at x,y.
If one or more attachments are sent with an email (“action” as the subject is still required) then the program will stop, copy the attachments into the source directory, overriding files as needed, and then restart via the cmd script. This allows for dynamically updating the code. Since the program restarts from the cmd script, it enables the installation of additional packages once a computer has already been infected. 

Future upgrades:
Better input control (bad inputs may cause a crash)
Persistence over resets 
Enable the program to send strings as if from a keyboard
Run in the background
Faster sending of data; it would be more efficient to use a server for communication, albeit less interesting.

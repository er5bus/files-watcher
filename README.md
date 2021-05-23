# challenge

Running environment :
---------------------

Client : Linux box, Debian-based Distributions, preferably Ubuntu Desktop (No headless)
Server : Will be Ubuntu Server 21.04 LTS
Classic environment : no Docker, no Proxies. Use default Linux tools only.

Environment Variables :
-----------------------

Path of folder to watch 		: /var/tmp/files
Path of "done" folder  		: /var/tmp/files/archive
Server Path to copy new files to 	: /home/app/uploads
Server IP : <some.ip.address>
Server Login :
	user : root
	pass : password

Objective :
-----------

Build a watcher to detect a new file has been copied to /var/tmp/files
When a new file has been detected, the following actions need to be executed :

For every new file detected
{

- open an SFTP connection to the remote server
	- Transparent login (no user input is needed)
	=> Think of an exchange of certificates between client and server

- upload the new file to the remote path, /home/app/uploads
	- Needs to ensure file upload has succeeded
	- Needs to retry if something went wrong (ex: connexion lost)

- close the connexion

- invoke a web service (endpoint) to notify about the new file has been uploaded
	- the payload should include the following :
		- File name
		- timestamp of upload completed
		- message : <file_name> has been received at <formatted_timestamp>

- Move the uploaded file locally :
	- From 	: /var/tmp/files
	-To 	: /var/tmp/files/archive

}

=> Actions need to be carried out sequentially

Simplify your complex processes with easy-to-use interactive decision trees to collect and deliver the right information.

## Project Requirements:

In order to get the project running you need to install docker or python3.6

#### Install :

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

[Get Docker](https://docs.docker.com/get-docker/).

Python is an interpreted high-level general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use of significant indentation.

[Get Python](https://www.python.org/downloads/).


## Setting the Project Locally:

#### Cloning the project:

Once you have all the needed requirements installed, clone the project:

``` bash
git clone https://github.com/er5bus/file_watcher.git
```

#### Configure .env file:

Before you can run the project you need to set the envirment varibles:

``` bash
cp .env.example .env
```

Update environment varibles

#### Run the Project:

to run the project in python virtual environment:

``` bash
python3 -m venv venv
source venv/bin/activate
source .env
python3 src/main.py
```

to run the project in docker container:

``` bash
docker-compose up --build
```

That's it.

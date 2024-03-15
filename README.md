# auto-reconnect-portal
- Not supposed to be useful for someone else, but could be used as a template for a similar project
- I use this script to automatically to a portal, the steps are:
1. execute a first command that tweaks my network configuration
2. connect to the portal using selenium interaction
3. execute a second command that tweaks my network configuration
4. sleep until 7 hours (default), then display a warning pop up. When this pop up is closed, restart at step 1
## set Up
- `pip3 install pipenv` install the pipenv lib to use the command below
- `virtualenv .` create the virtual env
- `source ./bin/activate` means 'execute the file passed as argument of source'. You should NOT make it an executable
- `pip3 install -r requirements.txt` 
- `cd main; cp .env.template .env` then fill your .env variables as instructed
- `https://stackoverflow.com/questions/69603788/how-to-pip-install-tkinter#answers` download tkinter if not installed
## usage
- `cd main; python3 main.py`
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
### chrome/chromedriver binaries
- to avoid chrome/chromedriver conflicts, I used a static version (similar to what the requirements.txt file is for python)
- (in main/)
- `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash` install nvm, to get an up to date npm/node version (if that's not the case)
- `nvm install node`
- `npm install @puppeteer/browsers -y` the npm package to get the binaries
- `npx @puppeteer/browsers install chrome@121` get the chrome binary
- `npx @puppeteer/browsers install chromedriver@121`
- `rm -rf node_modules; rm package.json package-lock.json`
## usage
- `cd main; python3 main.py`

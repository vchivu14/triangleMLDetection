# triangle problem
This is a test project

## Get started
*You will need to have [Node.js](https://nodejs.org) installed & [Python 3](https://www.python.org/downloads/release/python-3810/) * [Python package manager](https://pip.pypa.io/en/stable/installation/)*

1st: clone the app & enter the project
```bash
git clone https://github.com/vladChivu/triangle.git
cd proj
```

2nd: install the dependencies for the backend
```bash
pipx install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3rd: install the dependencies for the svelte app
```bash
cd svelte-client
npm i
```

4th: build the svelte app
```bash
npm run build
```

EXPOSE THE APPLICATION to port 8000 with gunicorn
```bash
cd ..
gunicorn -b 0.0.0.0:8000 app:app
```
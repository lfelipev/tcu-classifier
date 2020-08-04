### Download the files on drive bellow and copy then to the service folder

https://drive.google.com/drive/folders/1egRMfEvARvy3Ij-qopVxGxzkxIhHYil_?usp=sharing

### Build the Backend (Service)
Move inside the service folder and run the Flask app:

```sh
virtualenv -p Python3 .
source bin/activate
pip install -r requirements.txt
FLASK_APP=app.py flask run
```

### Build the Backend (UI)
Move inside the ui folder and run the UI server app:

```sh
npm install -g serve
npm run build
serve -s build -l 3000
```

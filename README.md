# Como funciona o site?

- Consulte o Tribunal de Contas da União para pegar o número, ano e o colegiado do Acórdão que você deseja saber o assunto.

- Preencha os campos Número, Ano e Colegiado corretamente e o site irá consultar se o Acórdão existe na nossa base própria.

- No campo 'Conteúdo do Acórdão', o modelo irá predizer o assunto que está escrito neste campo e irá desconsiderar os campos Número, Ano e Colegiado. 


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

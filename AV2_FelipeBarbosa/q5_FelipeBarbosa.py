from flask import Flask, request, url_for, redirect
from cryptography.fernet import Fernet

chave = Fernet.generate_key()
cipher_suite = Fernet(chave)
forms = []
app = Flask(__name__)
user = {
    "login": "felipe",
    "password": "1234",
}
userfn = lambda user, password, crypt_fn : {"login": user, "password": crypt_fn(password)}
crypt_fn = lambda password : cipher_suite.encrypt(str(password).encode()).decode()
decrypt_fn = lambda password : cipher_suite.decrypt(password).decode()
FORM_HTML = lambda : """
    <form method="POST">
        <div style="margin-bottom: 1rem;">
            <div style="margin-top: 1rem;">
                <h3>Digite seu nome de usuário.</h3>
                <input style="background-color: #f7f7f7; height: 40px; width: 512px; border-radius: 8px; border: 1px solid #121212;" type="text" name="user">
                <h3>Digite sua senha.</h3>
                <input style="background-color: #f7f7f7; height: 40px; width: 512px; border-radius: 8px; border: 1px solid #121212;" type="password" name="password">
            </div>
            <div style="margin-top: 1rem;">
                <h3>Escolha a tabela.</h3>
                <select style="background-color: #f7f7f7; height: 40px; width: 512px; border-radius: 8px; border: 1px solid #121212;" name="table">
                    <option value="Users">Users</option>
                    <option value="Games">Games</option>
                    <option value="Company">Company</option>
                    <option value="Videogames">Videogames</option>
                </select>
            </div>
            <div style="margin-top: 1rem;">
                <h3>Escolha o tipo de query.</h3>
                <select style="background-color: #f7f7f7; height: 40px; width: 512px; border-radius: 8px; border: 1px solid #121212;" name="querytype">
                    <option value="INSERT INTO">INSERT</option>
                    <option value="SELECT">SELECT</option>
                    <option value="DELETE FROM">DELETE</option>
                </select>
            </div>
            <div style="margin-top: 1rem;">
                <h3>Digite sua query.<br>Ex.: <br>Para consultas ou remoção: WHERE id = 9;<br>Para inserção: (field1, field2) VALUES (value1, value2);</h3>
                <input style="background-color: #f7f7f7; height: 40px; width: 512px; border-radius: 8px; border: 1px solid #121212;" type="text" name="query">
            </div>
        </div>
        <input type="submit">
    </form>
    """
@app.route('/')
def home():
    return HELLO_HTML()

app.route('/login')(lambda: FORM_HTML())

@app.route('/login', methods=['POST'])
def my_form_post():
    request_user = lambda : request.form['user']
    request_password = lambda : request.form['password']
    table = lambda : request.form['table']
    query = lambda : request.form['query']
    query_table = lambda : request.form['querytype']
    add_to_form = lambda items : [forms.append(item) for item in items]
    credential_validation = lambda : user['login'] == request_user() and decrypt_fn(user["password"]) == request_password()
    add_to_form([query_table(), table(), query()]) and credential_validation()
    next_route = lambda validation : 'success_route' if validation else 'fail_route'
    return(redirect(url_for(next_route(credential_validation()))))
        
@app.route('/success')
def success_route():
    html_to_return = lambda : "<h1>{} {} {};</h1>".format(forms[0], forms[1], forms[2])
    return html_to_return()
@app.route('/fail')
def fail_route():
    html_to_return = lambda : "<h1>Senha e/ou usuário inválido(s).</h1>"
    return html_to_return()


HELLO_HTML = """
    <html><body>
        <h1>Hello, {0}!</h1>
        The time is {1}.
        <button>Hello</button>
    </body></html>"""

user = userfn('felipe', '1234', crypt_fn)
app.run(host="localhost", debug=True) and __name__ == "__main__"
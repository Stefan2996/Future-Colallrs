from flask import Flask, render_template

app = Flask(__name__)

# DECORATORS
@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/purchase")
def purchase():
    return render_template("purchase.html")

@app.route("/sale")
def sale():
    return render_template("sale.html")

@app.route("/balance_change")
def balance_change():
    return render_template("balance_change.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/base")
def base():
    return render_template("base.html")

# код запуска программы
if __name__ == '__main__': # если наш файл единственный, то он значится как main и запускает всю программу
    app.run(debug=True)
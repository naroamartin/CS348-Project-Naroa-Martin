from flask import Flask, render_template, redirect

app = Flask(__name__) 


@app.route("/")

def home():
  return render_template ("home.html")

@app.route('/add')
def add():
    return render_template('add.html')
  
@app.route('/delete')
def delete():
      return render_template('delete.html')
  
@app.route('/edit')
def edit():
      return render_template('edit.html')
  
@app.route('/info')
def info():
    return render_template('info.html')
  
if __name__ == '__main__':        
  app.run(host='0.0.0.0', debug=True)
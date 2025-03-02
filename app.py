from flask import Flask, request, render_template
import main_1  # Terminalde çalışan SMS programın (sms_program.py dosyan olmalı)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        result = main_1.send_sms(phone_number)  # Terminal programını çağır
        return f"Mesaj Gönderildi: {result}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
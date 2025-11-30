from flask import Flask
import random, datetime, re

app = Flask(__name__)

@app.route('/bin=<b>')
def gen(b):
    b = re.sub(r'[^0-9xX]', '', b).upper()
    if len(b) < 6: return "Invalid BIN", 400
    
    fixed = ''.join('0' if c=='X' else c for c in b)
    need = 15 - len(fixed)
    rand = ''.join(str(random.randint(0,9)) for _ in range(need))
    
    num = fixed + rand
    total = 0
    for i, d in enumerate(reversed(num)):
        digit = int(d)
        if i % 2 == 1:
            digit *= 2
            if digit > 9: digit -= 9
        total += digit
    check = (10 - total % 10) % 10
    
    full = (b + rand + str(check))[:16]
    full = ''.join(str(random.randint(0,9)) if c=='X' else c for c in full)
    
    m = random.randint(1,12)
    y = str(datetime.datetime.now().year + random.randint(2,6))[-2:]
    cvv = random.randint(100,999)
    
    return f"{full}|{m:02d}|{y}|{cvv}"

@app.route('/')
def home():
    return "API အလုပ်လုပ်နေပါပြီ<br>/bin=453241"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

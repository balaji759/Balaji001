from flask import Flask, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management

# Simple in-memory user database (for demonstration only)
users_db = {}

@app.route("/")
def home():
    if 'username' in session:
        # User is logged in, show the main page
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Balaji</title>
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
          <style>
            body {
              margin: 0;
              padding: 0;
              font-family: 'Courier New', monospace;
              background: black;
              color: #00ff00;
              overflow: hidden;
            }

            header {
              background: rgba(0, 255, 0, 0.1);
              padding: 15px 30px;
              display: flex;
              justify-content: space-between;
              align-items: center;
              border-bottom: 1px solid #00ff00;
            }

            .logo {
              font-size: 24px;
              font-weight: bold;
            }

            nav a {
              color: #00ff00;
              margin: 0 15px;
              text-decoration: none;
            }

            nav a:hover {
              text-decoration: underline;
            }

            .hero {
              text-align: center;
              margin-top: 100px;
              z-index: 2;
              position: relative;
            }

            .glow-text {
              font-size: 48px;
              color: #00ff00;
              text-shadow: 0 0 5px #00ff00,
                           0 0 10px #00ff00,
                           0 0 20px #00ff00;
              animation: glow 2s ease-in-out infinite alternate;
            }

            .glow-red {
              color: red;
              font-weight: bold;
              font-size: 22px;
              text-shadow: 0 0 5px red, 0 0 10px red, 0 0 20px red;
            }

            @keyframes glow {
              from {
                text-shadow: 0 0 5px #00ff00;
              }
              to {
                text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00, 0 0 40px #00ff00;
              }
            }

            .telegram {
              margin-top: 30px;
            }

            .telegram a {
              color: #00ff00;
              font-size: 28px;
              text-decoration: none;
            }

            .telegram a:hover {
              color: #33ff33;
            }

            .buttons {
              margin-top: 30px;
              display: flex;
              justify-content: center;
              gap: 20px;
              flex-wrap: wrap;
            }

            .glow-button {
              background: black;
              border: 1px solid #00ff00;
              color: #00ff00;
              padding: 15px 30px;
              font-size: 18px;
              text-transform: uppercase;
              cursor: pointer;
              border-radius: 8px;
              box-shadow: 0 0 10px #00ff00;
              transition: 0.3s ease;
              text-decoration: none;
            }

            .glow-button:hover {
              box-shadow: 0 0 20px #00ff00, 0 0 40px #00ff00;
              background: #003300;
            }

            .matrix {
              position: fixed;
              top: 0;
              left: 0;
              width: 100%;
              height: 100%;
              z-index: 1;
              background: black;
              pointer-events: none;
            }

            .welcome-message {
              color: #00ff00;
              font-size: 24px;
              margin-bottom: 20px;
              text-shadow: 0 0 5px #00ff00;
            }

          </style>
        </head>
        <body>

        <div class="matrix">
          <canvas id="matrix"></canvas>
        </div>

        <header>
          <div class="logo">Balaji</div>
          <nav>
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="/logout">Logout</a>
          </nav>
        </header>

        <div class="hero">
          <h1 class="glow-text">Welcome</h1>
          <div class="welcome-message">Hello, ''' + session['username'] + '''!</div>
          <p class="glow-red">I'm <strong>Balaji</strong></p>

          <div class="telegram">
            <a href="https://t.me/v_4tx" target="_blank">
              <i class="fab fa-telegram-plane"></i> Contact on Telegram
            </a>
          </div>

          <div class="buttons">
            <a class="glow-button" href="https://t.me/+vzmcUSCAru5iMmU1" target="_blank">Channel</a>
            <a class="glow-button" href="https://t.me/+DVng8ROQZC84YjVl" target="_blank">Chat GC</a>
            <a class="glow-button" href="/jacking">JACKING FILE</a>
          </div>
        </div>

        <script>
          // Matrix rain effect
          const canvas = document.getElementById("matrix");
          const ctx = canvas.getContext("2d");

          canvas.height = window.innerHeight;
          canvas.width = window.innerWidth;

          let letters = "01";
          letters = letters.split("");

          let fontSize = 14;
          let columns = canvas.width / fontSize;

          let drops = [];
          for (let x = 0; x < columns; x++) drops[x] = 1;

          function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0F0";
            ctx.font = fontSize + "px monospace";

            for (let i = 0; i < drops.length; i++) {
              let text = letters[Math.floor(Math.random() * letters.length)];
              ctx.fillText(text, i * fontSize, drops[i] * fontSize);

              if (drops[i] * fontSize > canvas.height && Math.random() > 0.975)
                drops[i] = 0;

              drops[i]++;
            }
          }

          setInterval(draw, 33);
        </script>

        </body>
        </html>
        '''
    else:
        # User is not logged in, redirect to signup
        return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db:
            error = 'Username already exists!'
        else:
            users_db[username] = password
            session['username'] = username
            return redirect(url_for('home'))
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Sign Up - Balaji</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        body {
          margin: 0;
          padding: 0;
          font-family: 'Courier New', monospace;
          background: black;
          color: #ff0000;
          overflow: hidden;
        }

        .signup-container {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 400px;
          padding: 40px;
          background: rgba(0, 0, 0, 0.7);
          box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
          border-radius: 10px;
          z-index: 10;
        }

        .signup-title {
          text-align: center;
          margin-bottom: 30px;
          font-size: 36px;
          color: #ff0000;
          text-shadow: 0 0 5px #ff0000,
                      0 0 10px #ff0000,
                      0 0 20px #ff0000;
          animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
          from {
            text-shadow: 0 0 5px #ff0000;
          }
          to {
            text-shadow: 0 0 20px #ff0000, 0 0 30px #ff0000, 0 0 40px #ff0000;
          }
        }

        .signup-form input {
          width: 100%;
          padding: 10px;
          margin-bottom: 20px;
          background: rgba(0, 0, 0, 0.5);
          border: 1px solid #ff0000;
          color: #ffffff;
          font-family: 'Courier New', monospace;
          font-size: 16px;
          border-radius: 5px;
        }

        .signup-form input:focus {
          outline: none;
          box-shadow: 0 0 10px #ff0000;
        }

        .signup-button {
          width: 100%;
          padding: 12px;
          background: black;
          border: 1px solid #ff0000;
          color: #ff0000;
          font-size: 18px;
          cursor: pointer;
          border-radius: 5px;
          transition: 0.3s ease;
          text-transform: uppercase;
          font-family: 'Courier New', monospace;
          font-weight: bold;
        }

        .signup-button:hover {
          background: rgba(255, 0, 0, 0.1);
          box-shadow: 0 0 15px #ff0000;
        }

        .error-message {
          color: #ff0000;
          text-align: center;
          margin-bottom: 20px;
          text-shadow: 0 0 5px #ff0000;
        }

        .login-link {
          text-align: center;
          margin-top: 20px;
        }

        .login-link a {
          color: #ff0000;
          text-decoration: none;
        }

        .login-link a:hover {
          text-decoration: underline;
        }

        .matrix {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 1;
          background: black;
          pointer-events: none;
        }

      </style>
    </head>
    <body>

    <div class="matrix">
      <canvas id="matrix"></canvas>
    </div>

    <div class="signup-container">
      <h1 class="signup-title">BALAJI</h1>
      ''' + (f'<div class="error-message">{error}</div>' if error else '') + '''
      <form class="signup-form" method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit" class="signup-button">Sign Up</button>
      </form>
      <div class="login-link">
        Already have an account? <a href="/login">Login</a>
      </div>
    </div>

    <script>
      // Matrix rain effect (red version)
      const canvas = document.getElementById("matrix");
      const ctx = canvas.getContext("2d");

      canvas.height = window.innerHeight;
      canvas.width = window.innerWidth;

      let letters = "01";
      letters = letters.split("");

      let fontSize = 14;
      let columns = canvas.width / fontSize;

      let drops = [];
      for (let x = 0; x < columns; x++) drops[x] = 1;

      function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#F00";
        ctx.font = fontSize + "px monospace";

        for (let i = 0; i < drops.length; i++) {
          let text = letters[Math.floor(Math.random() * letters.length)];
          ctx.fillText(text, i * fontSize, drops[i] * fontSize);

          if (drops[i] * fontSize > canvas.height && Math.random() > 0.975)
            drops[i] = 0;

          drops[i]++;
        }
      }

      setInterval(draw, 33);
    </script>

    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username not in users_db:
            error = 'Username does not exist!'
        elif users_db[username] != password:
            error = 'Invalid password!'
        else:
            session['username'] = username
            return redirect(url_for('home'))
    
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Login - Balaji</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        body {
          margin: 0;
          padding: 0;
          font-family: 'Courier New', monospace;
          background: black;
          color: #ff0000;
          overflow: hidden;
        }

        .login-container {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 400px;
          padding: 40px;
          background: rgba(0, 0, 0, 0.7);
          box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
          border-radius: 10px;
          z-index: 10;
        }

        .login-title {
          text-align: center;
          margin-bottom: 30px;
          font-size: 36px;
          color: #ff0000;
          text-shadow: 0 0 5px #ff0000,
                      0 0 10px #ff0000,
                      0 0 20px #ff0000;
          animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
          from {
            text-shadow: 0 0 5px #ff0000;
          }
          to {
            text-shadow: 0 0 20px #ff0000, 0 0 30px #ff0000, 0 0 40px #ff0000;
          }
        }

        .login-form input {
          width: 100%;
          padding: 10px;
          margin-bottom: 20px;
          background: rgba(0, 0, 0, 0.5);
          border: 1px solid #ff0000;
          color: #ffffff;
          font-family: 'Courier New', monospace;
          font-size: 16px;
          border-radius: 5px;
        }

        .login-form input:focus {
          outline: none;
          box-shadow: 0 0 10px #ff0000;
        }

        .login-button {
          width: 100%;
          padding: 12px;
          background: black;
          border: 1px solid #ff0000;
          color: #ff0000;
          font-size: 18px;
          cursor: pointer;
          border-radius: 5px;
          transition: 0.3s ease;
          text-transform: uppercase;
          font-family: 'Courier New', monospace;
          font-weight: bold;
        }

        .login-button:hover {
          background: rgba(255, 0, 0, 0.1);
          box-shadow: 0 0 15px #ff0000;
        }

        .error-message {
          color: #ff0000;
          text-align: center;
          margin-bottom: 20px;
          text-shadow: 0 0 5px #ff0000;
        }

        .signup-link {
          text-align: center;
          margin-top: 20px;
        }

        .signup-link a {
          color: #ff0000;
          text-decoration: none;
        }

        .signup-link a:hover {
          text-decoration: underline;
        }

        .matrix {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 1;
          background: black;
          pointer-events: none;
        }

      </style>
    </head>
    <body>

    <div class="matrix">
      <canvas id="matrix"></canvas>
    </div>

    <div class="login-container">
      <h1 class="login-title">BALAJI</h1>
      ''' + (f'<div class="error-message">{error}</div>' if error else '') + '''
      <form class="login-form" method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit" class="login-button">Login</button>
      </form>
      <div class="signup-link">
        Don't have an account? <a href="/signup">Sign Up</a>
      </div>
    </div>

    <script>
      // Matrix rain effect (red version)
      const canvas = document.getElementById("matrix");
      const ctx = canvas.getContext("2d");

      canvas.height = window.innerHeight;
      canvas.width = window.innerWidth;

      let letters = "01";
      letters = letters.split("");

      let fontSize = 14;
      let columns = canvas.width / fontSize;

      let drops = [];
      for (let x = 0; x < columns; x++) drops[x] = 1;

      function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#F00";
        ctx.font = fontSize + "px monospace";

        for (let i = 0; i < drops.length; i++) {
          let text = letters[Math.floor(Math.random() * letters.length)];
          ctx.fillText(text, i * fontSize, drops[i] * fontSize);

          if (drops[i] * fontSize > canvas.height && Math.random() > 0.975)
            drops[i] = 0;

          drops[i]++;
        }
      }

      setInterval(draw, 33);
    </script>

    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signup'))


@app.route("/jacking")
def jacking():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>JACKING FILE</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          display: flex;
          height: 100vh;
          font-family: monospace;
          background: black;
        }
        .half {
          width: 50%;
          height: 100%;
          overflow: hidden;
          position: relative;
        }
        canvas {
          position: absolute;
          width: 100%;
          height: 100%;
          top: 0; left: 0;
          z-index: 0;
        }
        .content {
          z-index: 1;
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          text-align: center;
          color: #00ff00;
        }
        .btn {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
          background: transparent;
          border: 2px solid #00ff00;
          color: #00ff00;
          padding: 12px 20px;
          margin: 10px auto;
          font-size: 18px;
          text-decoration: none;
          border-radius: 8px;
          box-shadow: 0 0 10px #00ff00;
          width: 220px;
        }
        .btn:hover {
          background: rgba(0,255,0,0.1);
        }
      </style>
    </head>
    <body>
      <div class="half">
        <canvas id="canvasRed"></canvas>
        <div class="content">
          <a class="btn" href="https://t.me/ERRORXFILES/3" target="_blank">
            <i class="fab fa-instagram"></i> HIGH FOLLOWER
          </a>

          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
          <a class="btn" href="#"><i class="fab fa-instagram"></i> COMING SOON</a>
        </div>
      </div>
      <div class="half">
        <canvas id="canvasGreen"></canvas>
      </div>
      <script>
        function startMatrix(canvasId, color) {
          const canvas = document.getElementById(canvasId);
          const ctx = canvas.getContext("2d");
          canvas.height = window.innerHeight;
          canvas.width = canvas.offsetWidth;
          const letters = "01".split("");
          const fontSize = 14;
          const columns = canvas.width / fontSize;
          const drops = Array.from({length: columns}).fill(1);
          function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = color;
            ctx.font = fontSize + "px monospace";
            drops.forEach((y, i) => {
              const text = letters[Math.floor(Math.random() * letters.length)];
              ctx.fillText(text, i * fontSize, y * fontSize);
              if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
              drops[i]++;
            });
          }
          setInterval(draw, 33);
        }
        startMatrix("canvasRed", "#ff0000");
        startMatrix("canvasGreen", "#00ff00");
      </script>
    </body>
    </html>
    '''


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
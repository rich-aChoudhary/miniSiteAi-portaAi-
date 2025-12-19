# routes/user_routes.py
from flask import Blueprint, request, jsonify
from controllers.userController import UserController

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    response, status = UserController.register_user(data)
    return jsonify(response), status

@user_routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status = UserController.login_user(data)
    return jsonify(response), status

@user_routes.route('/api/generate-portfolio', methods=['POST'])
def generate_portfolio():
    req = request.get_json()
    print(req)
    # Use .get() to avoid KeyError if 'title' is missing
    # response_text, status_code = UserController.process_ai(
    #     req.get('data'),
    #     req.get('title', ''),
    #     req.get('userId')
    # )
    response_text = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Raushan Ranjan - Portfolio</title>
  <style>
    body {
      font-family: 'Arial', sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
      color: #333;
    }
    section {
      padding: 80px 20px;
      text-align: center;
    }
    .hero {
      background-color: #3498db;
      color: #fff;
      padding: 100px 20px;
    }
    .hero a {
      background-color: #fff;
      color: #3498db;
      padding: 15px 30px;
      text-decoration: none;
      border-radius: 5px;
      font-weight: bold;
      display: inline-block;
    }
    .project-card {
      width: 300px;
      margin: 20px;
      background-color: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .project-card img {
      width: 100%;
      display: block;
    }
    .project-card h3 {
      font-size: 1.5em;
      margin: 10px 0;
      color: #333;
    }
    .project-card p {
      font-size: 1em;
      color: #555;
      line-height: 1.4;
    }
    .skills ul {
      list-style: none;
      padding: 0;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
    }
    .skills li {
      margin: 10px;
      padding: 10px 20px;
      background-color: #fff;
      border-radius: 5px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .contact form {
      display: flex;
      flex-direction: column;
      align-items: center;
      max-width: 600px;
      margin: 0 auto;
    }
    .contact input,
    .contact textarea {
      width: 100%;
      padding: 15px;
      margin-bottom: 20px;
      border: none;
      border-radius: 5px;
      font-size: 1em;
      color: #333;
    }
    .contact button {
      background-color: #fff;
      color: #3498db;
      padding: 15px 30px;
      border: none;
      border-radius: 5px;
      font-size: 1.1em;
      font-weight: bold;
      cursor: pointer;
    }
    footer {
      background-color: #2c3e50;
      color: #fff;
      text-align: center;
      padding: 30px 0;
    }
    footer a {
      color: #fff;
      text-decoration: none;
      margin: 0 10px;
    }
  </style>
</head>
<body>

  <!-- Hero Section -->
  <section class="hero">
    <h1>Hello, I'm Raushan Ranjan</h1>
    <p>MTech IT Student at NIT Raipur | Python Enthusiast</p>
    <a href="#contact">Contact Me</a>
  </section>

  <!-- About Me -->
  <section>
    <h2 style="color: #3498db;">About Me</h2>
    <p style="max-width: 800px; margin: 0 auto; font-size: 1.1em; line-height: 1.6; color: #555;">
      I am Raushan Ranjan, an MTech IT student at NIT Raipur with a passion for leveraging technology to solve real-world problems.
      With 2 years of experience in Python, I enjoy developing innovative solutions. I'm especially interested in Engagi AI, and
      look forward to new challenges and opportunities to grow as a developer.
    </p>
  </section>

  <!-- Projects -->
  <section style="background-color: #eee;">
    <h2 style="color: #3498db;">Projects</h2>
    <div style="display: flex; flex-wrap: wrap; justify-content: center;">
      <div class="project-card">
        <img src="https://via.placeholder.com/300x200" alt="Engagi AI Project" />
        <div style="padding: 20px;">
          <h3>Engagi AI</h3>
          <p>Description of the Engagi AI project goes here. Highlight key features and technologies used.</p>
        </div>
      </div>
      <div class="project-card">
        <img src="https://via.placeholder.com/300x200" alt="Project 2" />
        <div style="padding: 20px;">
          <h3>Project 2</h3>
          <p>Brief description of the project and its main goals. This is just placeholder text.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Skills -->
  <section class="skills">
    <h2 style="color: #3498db;">Skills & Technologies</h2>
    <ul>
      <li>Python</li>
      <li>Machine Learning</li>
      <li>Data Analysis</li>
      <!-- Add more skills as needed -->
    </ul>
  </section>

  <!-- Contact -->
  <section class="contact" id="contact" style="background-color: #3498db; color: #fff;">
    <h2>Contact Me</h2>
    <form>
      <input type="text" placeholder="Your Name" />
      <input type="email" placeholder="Your Email" />
      <textarea placeholder="Your Message" rows="5"></textarea>
      <button type="submit">Send Message</button>
    </form>
  </section>

  <!-- Footer -->
  <footer>
    <p>&copy; 2024 Raushan Ranjan. All rights reserved.</p>
    <div>
      <a href="#">LinkedIn</a>
      <a href="#">GitHub</a>
      <!-- Add more links -->
    </div>
  </footer>

</body>
</html>"""

    return jsonify(response_text), 200



@user_routes.route('/api/my-portfolios/<int:user_id>')
def get_user_portfolios(user_id):
    portfolios = UserController.get_user_portfolios(user_id)
    if not portfolios:
        result = {'message': 'No portfolios found for this user.'}
    else:
        result = portfolios
    return jsonify(result)

@user_routes.route('/api/portfolio/<int:portfolio_id>')
def get_portfolio(portfolio_id):
    portfolio = UserController.get_portfolio(portfolio_id)
    if not portfolio:
        return jsonify({'message': 'Portfolio not found.'}), 404
    return jsonify(portfolio['html_content'])
@user_routes.route('/api/portfolio/<int:portfolio_id>', methods=['DELETE'])
def delete_portfolio_route(portfolio_id):
    print(f"DELETE /api/portfolio/{portfolio_id} called")
    response, status = UserController.delete_portfolio(portfolio_id)
    print('Delete result:', response, 'status:', status)
    return jsonify(response), status
@user_routes.route('/api/save-portfolio/<int:portfolio_id>', methods=['PUT'])
def save_portfolio(portfolio_id):
    req = request.get_json()
    content = req.get('content', '')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    try:
        UserController.save_edited_changes(portfolio_id, content)
        return jsonify({'message': 'Portfolio saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
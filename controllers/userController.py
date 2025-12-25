from werkzeug.security import check_password_hash, generate_password_hash
from models.userModel import User
from utils.emailService import send_welcome_email
import google.generativeai as genai
from models.aiResponseModel import AIResponseModel
genai.configure(api_key="AIzaSyBxPute3C1p-hwSdGnmn6yzIj_dKlrfCgA")   

class UserController:
    @staticmethod
    def register_user(data):
        if not all(key in data for key in ('username', 'password', 'email')):
            return {'error': 'Missing required fields'}, 400

        email = data['email'].strip().lower()

        if User.find_by_email(email):
            return {'error': 'Email already exists'}, 400

        device_mac = data.get('device_mac')
        if device_mac and User.find_by_mac(device_mac):
            return {'error': 'This device is already registered'}, 400

        password_hash = generate_password_hash(data['password'])

        user = User.save(
            username=data['username'],
            password_hash=password_hash,   # ✅ HASH ONLY ONCE
            email=email,
            device_mac=device_mac
        )

        try:
            send_welcome_email(email, data['username'])
        except Exception as e:
            return {
                'message': 'User registered, email failed',
                'error': str(e),
                'user': user
            }, 202

        return {'message': 'User registered successfully', 'user': user}, 201
    @staticmethod
    def login_user(data):
        if not all(key in data for key in ('email', 'password')):
            return {'error': 'Missing required fields'}, 400

        email = data['email'].strip().lower()
        password = data['password']

        user = User.find_by_email(email)
        print(user)
        if not user:
            return {'error': 'User not found'}, 404

        # EXPECTED schema: dict with password_hash
        password_hash = user.get('password_hash')

        if not password_hash:
            return {'error': 'Password not set for this user'}, 500

        if not check_password_hash(password_hash, password):
            return {'error': 'Invalid email or password'}, 401

        return {
            'message': 'Login successful',
            'user': {
                'id': user.get('id'),
                'username': user.get('username'),
                'email': user.get('email')
            }
        }, 200
    @staticmethod
    def process_ai(data, title, user_id):
        # Ensure user exists and has enough credits (cost: 500 credits per response)
        try:
            user = User.find_by_id(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            # Extract credits safely
            try:
                credits = int(user.get('credits') if isinstance(user, dict) else user['credits'])
            except Exception:
                credits = 0

            if credits < 500:
                return {'error': 'Insufficient credits'}, 402

            model = genai.GenerativeModel('gemini-2.0-flash')
            prompt = (
                "You are a professional website developer and designer. Based on the following user input, generate a complete, visually appealing, responsive personal portfolio website using only HTML with inline CSS. "
                "The website must include sections such as: "
                "A clean hero section with a headline, subheadline, and call-to-action button; "
                "A professional About Me section with a short bio; "
                "A well-organized Projects or Work section showing past work or case studies; "
                "A Skills or Technologies section with relevant tech stack; "
                "A Contact Me section with a working form layout; "
                "A clean and modern footer with copyright and social links. "
                "Use modern font styles, harmonious colors, consistent spacing, and engaging copy. "
                "Make sure the entire layout is aesthetic, responsive, and suitable for a portfolio site. "
                "Output only valid raw HTML code with all styles written inline. "
                "Do not use external CSS, markdown, JavaScript, or include any code fences.\n"
                f"User Input is below:\n{data}"
            )
            response = model.generate_content(prompt)

            # Attempt to decrement credits after successful generation
            dec = User.decrement_credits(user_id, 500)
            if dec is False:
                # Race condition: user no longer has enough credits
                return {'error': 'Insufficient credits (race condition)'}, 409

            AIResponseModel.save_ai_response(user_id, title, response.text)
            return response.text, 200
        except Exception as e:
            print(f"Error during AI processing: {e}")
            return {"error": "Failed to get AI response"}, 500
    
    @staticmethod
    def get_user_portfolios(user_id):
        return AIResponseModel.get_portfolios_by_user_id(user_id)
    @staticmethod
    def get_portfolio(portfolio_id):
        return AIResponseModel.get_portfolio_by_id(portfolio_id)
    @staticmethod
    def save_edited_changes(portfolio_id, content):
        # Assuming content is already sanitized before saving
        AIResponseModel.save_toDB(portfolio_id, content)
        return {"message": "Portfolio saved successfully"}
    
    @staticmethod
    def delete_portfolio(portfolio_id):
        # Ensure portfolio exists
        try:
            print(f"Attempting to delete portfolio id={portfolio_id}")
            portfolio = AIResponseModel.get_portfolio_by_id(portfolio_id)
            print('Found portfolio:', portfolio)
            if not portfolio:
                return {'error': 'Portfolio not found'}, 404

            AIResponseModel.delete_portfolio(portfolio_id)
            print(f"Portfolio {portfolio_id} deleted")
            return {'message': 'Portfolio deleted successfully'}, 200
        except Exception as e:
            print(f"Error deleting portfolio {portfolio_id}:", e)
            return {'error': str(e)}, 500
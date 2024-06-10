from app.library import *
from app.chatbot import *

warnings.filterwarnings('ignore')

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    return render_template('home.html')

@main_routes.route('/about')
def about():
    return render_template('about.html')

@main_routes.route('/certifications')
def certifications():  # Change function name to 'certifications'
    return render_template('certifications.html')

@main_routes.route('/community_contribution')
def community_contribution():  # Change function name to 'community_contribution'
    return render_template('community_contribution.html')

@main_routes.route('/education')
def education():  # Change function name to 'education'
    return render_template('education.html')

@main_routes.route('/own_projects')
def own_projects():  # Change function name to 'own_projects'
    return render_template('own_projects.html')

@main_routes.route('/university_projects')
def university_projects():  # Change function name to 'university_projects'
    return render_template('university_projects.html')

@main_routes.route('/work_experience')
def work_experience():  # Change function name to 'work_experience'
    return render_template('work_experience.html')

@main_routes.route('/interest')
def interest():  # Change function name to 'work_experience'
    return render_template('interest.html')

@main_routes.route('/contact')
def contact():  # Change function name to 'work_experience'
    return render_template('contact.html')

@main_routes.route('/testimonial')
def testimonial():  # Change function name to 'work_experience'
    return render_template('testimonial.html')

@main_routes.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    user_id = request.json['user_id']
    response = process_chat_message(user_message, user_id)  # Chatbot logic function
    return jsonify({'response': response})

@main_routes.route('/get-session-id')
def get_session_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a unique user ID
    return {'user_id': session['user_id']}
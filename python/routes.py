from app import app, db
from flask import request, jsonify
from models import User

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.__dict__ for user in users])

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.__dict__)
    return jsonify({'message': 'User not found'}), 404

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.__dict__), 201

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.json
    user.username = data['username']
    user.email = data['email']
    user.password = data['password']
    
    db.session.commit()
    return jsonify(user.__dict__), 200

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)

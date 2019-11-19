from werkzeug.security import generate_password_hash, check_password_hash

password_hash = generate_password_hash('cat')
print(password_hash)
# password_hash = generate_password_hash('cat')
# print(password_hash)
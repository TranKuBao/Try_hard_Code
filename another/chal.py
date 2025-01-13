import bcrypt

def check_password(password, hashed_password):
    # Băm mật khẩu nhập vào để so sánh với hashed_password
    hashed_input_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Kiểm tra xem mật khẩu đã nhập có khớp với mật khẩu đã băm không
    if hashed_input_password == hashed_password:
        return True
    else:
        return False

# Ví dụ sử dụng
password = "password123"
# Đây là mật khẩu đã được băm từ trước
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Kiểm tra mật khẩu có khớp hay không
if check_password("password123", hashed_password):
    print("Mật khẩu khớp!")
else:
    print("Mật khẩu không khớp!")

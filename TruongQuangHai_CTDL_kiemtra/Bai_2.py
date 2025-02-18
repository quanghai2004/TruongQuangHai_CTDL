def count_chars(string):
    # Tạo một dictionary rỗng để lưu số lần xuất hiện của các ký tự
    char_count = {}
    
    # Duyệt qua từng ký tự trong chuỗi
    for char in string:
        # Nếu ký tự đã có trong dictionary, tăng giá trị đếm
        if char in char_count:
            char_count[char] += 1
        else:
            # Nếu ký tự chưa có, thêm vào dictionary và gán giá trị ban đầu là 1
            char_count[char] = 1
    
    return char_count

# Nhập chuỗi từ người dùng
string = input("Nhập chuỗi (string) cần đếm số lần xuất hiện các ký tự: ")

# Gọi hàm và in kết quả
result = count_chars(string)
print("Kết quả:", result)

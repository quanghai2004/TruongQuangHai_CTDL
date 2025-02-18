def word_count(file_path):
    """
    Hàm đếm số lần xuất hiện của các từ trong file văn bản.
    
    Args:
    - file_path (str): Đường dẫn đến file văn bản .txt.
    
    Returns:
    - dict: Dictionary với key là từ và value là số lần xuất hiện của từ đó.
    """
    word_count_dict = {}
    
    try:
        # Đọc nội dung file
        with open(file_path, 'r') as file:
            for line in file:
                # Tách các từ trong dòng, loại bỏ xuống dòng và khoảng trắng
                words = line.strip().split()
                
                # Duyệt qua các từ
                for word in words:
                    # Chuẩn hóa từ thành chữ thường
                    word = word.lower()
                    
                    # Đếm số lần xuất hiện
                    if word in word_count_dict:
                        word_count_dict[word] += 1
                    else:
                        word_count_dict[word] = 1
        
        return word_count_dict
    
    except FileNotFoundError:
        print(f"Lỗi: File '{file_path}' không tồn tại.")
        return {}
    except Exception as e:
        print(f"Lỗi: {e}")
        return {}

# Nhập đường dẫn file từ người dùng
file_path = "c:\\Users\\LENOVO\\Downloads\\P1_data.txt"


# Gọi hàm word_count và in kết quả
result = word_count(file_path)
print("Kết quả đếm từ:", result)

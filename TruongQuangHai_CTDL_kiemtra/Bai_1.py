from collections import deque

def sliding_window_max(num_list, k):
    if not num_list or k == 0:
        return []
    
    # Kết quả sẽ lưu giá trị lớn nhất của mỗi cửa sổ
    result = []
    # Deque để lưu chỉ số của các phần tử trong cửa sổ
    dq = deque()

    for i in range(len(num_list)):
        # Loại bỏ các phần tử không thuộc cửa sổ hiện tại
        if dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Loại bỏ các phần tử nhỏ hơn phần tử hiện tại
        while dq and num_list[dq[-1]] < num_list[i]:
            dq.pop()
        
        # Thêm chỉ số phần tử hiện tại vào deque
        dq.append(i)
        
        # Thêm giá trị lớn nhất của cửa sổ vào kết quả (sau khi cửa sổ có đủ k phần tử)
        if i >= k - 1:
            result.append(num_list[dq[0]])
    
    return result

# Nhập dữ liệu từ người dùng
try:
    # Nhập danh sách các số nguyên dưới dạng cú pháp ngoặc vuông
    num_list = eval(input("Nhập danh sách các số nguyên dưới dạng [a, b, c, ...]: "))
    
    # Kiểm tra danh sách có phải là list không
    if not isinstance(num_list, list) or not all(isinstance(x, int) for x in num_list):
        print("Dữ liệu không hợp lệ! Hãy nhập danh sách các số nguyên theo đúng định dạng [a, b, c, ...].")
    else:
        # Nhập giá trị k
        k = int(input("Nhập kích thước cửa sổ trượt k: "))
        
        if k <= 0 or k > len(num_list):
            print("Giá trị k phải lớn hơn 0 và nhỏ hơn hoặc bằng độ dài danh sách!")
        else:
            # Gọi hàm và in kết quả
            result = sliding_window_max(num_list, k)
            print("Kết quả:", result)
except (ValueError, SyntaxError):
    print("Dữ liệu không hợp lệ. Hãy nhập danh sách số nguyên hợp lệ và giá trị k là một số nguyên.")

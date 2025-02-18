def levenshtein_distance(S, T):
    m, n = len(S), len(T)
    # Tạo ma trận (m+1) x (n+1) để lưu trữ khoảng cách
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Khởi tạo hàng đầu tiên và cột đầu tiên
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Tính toán khoảng cách
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if S[i - 1] == T[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1,      # Xóa
                           dp[i][j - 1] + 1,      # Thêm
                           dp[i - 1][j - 1] + cost)  # Thay thế

    return dp[m][n]

# Ví dụ sử dụng
S = "windows"
T = "books"
print(f"Khoảng cách Levenshtein giữa '{S}' và '{T}' là {levenshtein_distance(S, T)}")
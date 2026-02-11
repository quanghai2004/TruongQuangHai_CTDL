import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
import tracemalloc
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FloydWarshall:
    def __init__(self):
        self.INF = float('inf')
        self.graph = None
        self.vertices = 0
        self.dist = None
        self.next = None
        self.execution_time = 0
        self.memory_usage = 0
    
    def initialize(self, graph):
        """Khởi tạo thuật toán với ma trận đồ thị đã cho"""
        self.graph = graph
        self.vertices = len(graph)
        
        # Khởi tạo ma trận khoảng cách và ma trận next
        self.dist = [row[:] for row in self.graph]
        self.next = [[None for _ in range(self.vertices)] for _ in range(self.vertices)]
        
        # Khởi tạo ma trận next
        for i in range(self.vertices):
            for j in range(self.vertices):
                if i != j and self.graph[i][j] != self.INF:
                    self.next[i][j] = j
    
    def run_algorithm(self):
        """Chạy thuật toán Floyd-Warshall"""
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # Thuật toán Floyd-Warshall
        for k in range(self.vertices):
            for i in range(self.vertices):
                for j in range(self.vertices):
                    if self.dist[i][k] != self.INF and self.dist[k][j] != self.INF:
                        if self.dist[i][j] > self.dist[i][k] + self.dist[k][j]:
                            self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                            self.next[i][j] = self.next[i][k]
        
        end_time = time.perf_counter()
        self.execution_time = end_time - start_time
        
        current, peak = tracemalloc.get_traced_memory()
        self.memory_usage = peak / 1024  # Chuyển đổi sang KB
        tracemalloc.stop()
    
    def construct_path(self, u, v):
        """Tạo đường đi từ đỉnh u đến v"""
        if self.next[u][v] is None:
            return []
            
        path = [u]
        while u != v:
            u = self.next[u][v]
            path.append(u)
        return path
    
    def get_results(self):
        """Trả về kết quả thuật toán"""
        return {
            'distance_matrix': self.dist,
            'next_matrix': self.next,
            'execution_time': self.execution_time,
            'memory_usage': self.memory_usage
        }

class GraphCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.graph = None
        self.node_positions = {}
        self.node_radius = 20
        self.edge_arrows = {}
        self.highlighted_path = None
        self.dragged_node = None
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def set_graph(self, graph, directed=True):
        """Thiết lập đồ thị và vẽ lại"""
        self.graph = graph
        self.directed = directed
        self.node_positions = {}
        self.edge_arrows = {}
        self.highlighted_path = None
        self.delete("all")
        
        n = len(graph)
        if n == 0:
            return
            
        # Tính toán vị trí các nút trên vòng tròn
        center_x = self.winfo_width() // 2
        center_y = self.winfo_height() // 2
        radius = min(center_x, center_y) - 50
        
        for i in range(n):
            angle = 2 * math.pi * i / n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[i] = (x, y)
        
        self.draw_graph()
    
    def draw_graph(self):
        """Vẽ đồ thị lên canvas"""
        self.delete("all")
        
        if not self.graph:
            return
            
        n = len(self.graph)
        
        # Vẽ các cạnh trước để nút nằm lên trên
        for i in range(n):
            for j in range(n):
                if i != j and self.graph[i][j] != float('inf'):
                    self.draw_edge(i, j, self.graph[i][j])
        
        # Vẽ các nút
        for i in range(n):
            x, y = self.node_positions[i]
            self.create_oval(x - self.node_radius, y - self.node_radius,
                            x + self.node_radius, y + self.node_radius,
                            fill="lightblue", outline="black", tags=f"node_{i}")
            self.create_text(x, y, text=str(i), font=('Arial', 12), tags=f"label_{i}")
        
        # Highlight đường đi nếu có
        if self.highlighted_path:
            for i in range(len(self.highlighted_path) - 1):
                u = self.highlighted_path[i]
                v = self.highlighted_path[i+1]
                self.draw_edge(u, v, self.graph[u][v], highlight=True)
    
    def draw_edge(self, u, v, weight, highlight=False):
        """Vẽ một cạnh từ u đến v"""
        x1, y1 = self.node_positions[u]
        x2, y2 = self.node_positions[v]
        
        # Tính vector hướng
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return
            
        # Tính điểm bắt đầu và kết thúc thực tế (trên biên của hình tròn)
        start_x = x1 + (dx * self.node_radius / length)
        start_y = y1 + (dy * self.node_radius / length)
        end_x = x2 - (dx * self.node_radius / length)
        end_y = y2 - (dy * self.node_radius / length)
        
        # Màu sắc và độ dày
        color = "red" if highlight else "black"
        width = 3 if highlight else 1
        
        # Kiểm tra nếu có cạnh ngược chiều (chỉ cho đồ thị có hướng)
        has_reverse = self.directed and self.graph[v][u] != float('inf') if self.graph else False
        
        # Tính góc của cạnh
        angle = math.atan2(dy, dx)
        
        # Điều chỉnh vị trí nếu có cạnh ngược chiều
        if has_reverse and u < v:  # Chỉ điều chỉnh 1 trong 2 chiều để tránh trùng lặp
            # Dịch chuyển đường đi hiện tại
            offset = 15  # Khoảng cách lệch
            start_x += offset * math.cos(angle + math.pi/2)
            start_y += offset * math.sin(angle + math.pi/2)
            end_x += offset * math.cos(angle + math.pi/2)
            end_y += offset * math.sin(angle + math.pi/2)
            
            # Điều chỉnh vị trí trọng số
            weight_offset = 25
        else:
            weight_offset = 10
        
        # Vẽ đường thẳng
        line = self.create_line(start_x, start_y, end_x, end_y, 
                               fill=color, width=width, arrow=tk.LAST if self.directed else tk.NONE,
                               tags=f"edge_{u}_{v}")
        
        # Vẽ mũi tên cho đồ thị có hướng
        if self.directed:
            self.draw_arrow(start_x, start_y, end_x, end_y, color)
        
        # Vẽ trọng số
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Điều chỉnh vị trí trọng số để tránh chồng lấn
        if has_reverse and u < v:
            mid_x += weight_offset * math.cos(angle + math.pi/2)
            mid_y += weight_offset * math.sin(angle + math.pi/2)
        
        self.create_text(mid_x, mid_y, text=str(weight), fill=color, font=('Arial', 10),
                        tags=f"weight_{u}_{v}")
    
    def draw_arrow(self, x1, y1, x2, y2, color):
        """Vẽ mũi tên cho cạnh có hướng"""
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        if length < 10:  # Quá ngắn thì không vẽ mũi tên
            return
            
        # Kích thước mũi tên
        arrow_size = 10
        angle = math.atan2(dy, dx)
        
        # Điểm cuối thực tế của mũi tên (lùi lại một chút)
        end_x = x2 - (dx * 10 / length)
        end_y = y2 - (dy * 10 / length)
        
        # Tính toán các điểm của mũi tên
        x3 = end_x - arrow_size * math.cos(angle - math.pi/6)
        y3 = end_y - arrow_size * math.sin(angle - math.pi/6)
        x4 = end_x - arrow_size * math.cos(angle + math.pi/6)
        y4 = end_y - arrow_size * math.sin(angle + math.pi/6)
        
        # Vẽ mũi tên
        self.create_polygon(end_x, end_y, x3, y3, x4, y4, fill=color, outline=color)
    
    def highlight_path(self, path):
        """Đánh dấu đường đi trên đồ thị"""
        self.highlighted_path = path
        self.draw_graph()
    
    def on_click(self, event):
        """Xử lý sự kiện click chuột"""
        for node, (x, y) in self.node_positions.items():
            if (x - event.x)**2 + (y - event.y)**2 <= self.node_radius**2:
                self.dragged_node = node
                return
    
    def on_drag(self, event):
        """Xử lý sự kiện kéo chuột"""
        if self.dragged_node is not None:
            self.node_positions[self.dragged_node] = (event.x, event.y)
            self.draw_graph()
    
    def on_release(self, event):
        """Xử lý sự kiện thả chuột"""
        self.dragged_node = None

class FloydWarshallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thuật toán Floyd-Warshall")
        self.root.geometry("1100x800")
        
        # Tạo đối tượng Floyd-Warshall
        self.fw = FloydWarshall()
        
        # Biến dữ liệu
        self.graph = None
        self.vertices = tk.IntVar(value=5)
        self.directed = tk.BooleanVar(value=True)
        self.graph_density = tk.DoubleVar(value=0.4)
        self.max_weight = tk.IntVar(value=10)
        
        # Dữ liệu hiệu năng
        self.performance_data = []
        
        # Tạo giao diện
        self.create_widgets()
    
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame điều khiển bên trái
        control_frame = ttk.LabelFrame(main_frame, text="Điều khiển", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Frame đồ thị và kết quả bên phải
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas để vẽ đồ thị
        self.canvas = GraphCanvas(right_frame, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Notebook để chứa các tab kết quả
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab ma trận khoảng cách
        self.dist_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dist_tab, text="Ma trận khoảng cách")
        
        # Tab hiệu năng
        self.perf_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.perf_tab, text="Hiệu năng")
        
        # Tab biểu đồ hiệu năng
        self.chart_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.chart_tab, text="Biểu đồ hiệu năng")
        
        # ==================== PHẦN ĐIỀU KHIỂN ====================
        
        # 1. Nhập số đỉnh
        vertex_frame = ttk.LabelFrame(control_frame, text="Số đỉnh", padding="10")
        vertex_frame.pack(fill=tk.X, pady=5)
        
        ttk.Spinbox(vertex_frame, from_=2, to=20, textvariable=self.vertices, width=10).pack()
        
        # 2. Chọn loại đồ thị
        graph_type_frame = ttk.LabelFrame(control_frame, text="Loại đồ thị", padding="10")
        graph_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(graph_type_frame, text="Có hướng", variable=self.directed, value=True).pack(anchor=tk.W)
        ttk.Radiobutton(graph_type_frame, text="Vô hướng", variable=self.directed, value=False).pack(anchor=tk.W)
        
        # 3. Mật độ cạnh
        density_frame = ttk.LabelFrame(control_frame, text="Mật độ cạnh", padding="10")
        density_frame.pack(fill=tk.X, pady=5)
        
        ttk.Scale(density_frame, from_=0.1, to=1.0, variable=self.graph_density, 
                 orient=tk.HORIZONTAL, length=150).pack()
        
        # 4. Khung tạo đồ thị
        graph_frame = ttk.LabelFrame(control_frame, text="Tạo đồ thị", padding="10")
        graph_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(graph_frame, text="Trọng số tối đa:").pack(anchor=tk.W)
        ttk.Spinbox(graph_frame, from_=1, to=100, textvariable=self.max_weight, width=8).pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(graph_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Ngẫu nhiên", command=self.generate_random_graph).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(btn_frame, text="Rỗng", command=self.create_empty_graph).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # 4.5. Thêm cạnh thủ công
        manual_frame = ttk.LabelFrame(control_frame, text="Thủ công", padding="10")
        manual_frame.pack(fill=tk.X, pady=5)

        ttk.Label(manual_frame, text="Nhập cạnh:").pack(anchor=tk.W)
        manual_input = ttk.Frame(manual_frame)
        manual_input.pack(fill=tk.X, pady=2)

        self.u_var = tk.IntVar(value=0)
        self.v_var = tk.IntVar(value=1)
        self.w_var = tk.IntVar(value=1)

        ttk.Label(manual_input, text="u:").pack(side=tk.LEFT)
        ttk.Spinbox(manual_input, from_=0, to=100, textvariable=self.u_var, width=3).pack(side=tk.LEFT)
        ttk.Label(manual_input, text="v:").pack(side=tk.LEFT)
        ttk.Spinbox(manual_input, from_=0, to=100, textvariable=self.v_var, width=3).pack(side=tk.LEFT)
        ttk.Label(manual_input, text="w:").pack(side=tk.LEFT)
        ttk.Spinbox(manual_input, from_=1, to=100, textvariable=self.w_var, width=4).pack(side=tk.LEFT)

        ttk.Button(manual_frame, text="Thêm cạnh", command=self.add_edge).pack(fill=tk.X, pady=5)
        
        # 5. Nút chạy thuật toán
        algo_frame = ttk.LabelFrame(control_frame, text="Thuật toán", padding="10")
        algo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(algo_frame, text="Chạy Floyd-Warshall", command=self.run_floyd_warshall).pack(fill=tk.X)
        
        # 6. Khung tìm đường đi
        path_frame = ttk.LabelFrame(control_frame, text="Tìm đường đi", padding="10")
        path_frame.pack(fill=tk.X, pady=5)
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_input_frame, text="Từ:").pack(side=tk.LEFT)
        self.source_var = tk.StringVar(value="0")
        self.source_combo = ttk.Combobox(path_input_frame, textvariable=self.source_var, width=5)
        self.source_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(path_input_frame, text="Đến:").pack(side=tk.LEFT)
        self.target_var = tk.StringVar(value="1")
        self.target_combo = ttk.Combobox(path_input_frame, textvariable=self.target_var, width=5)
        self.target_combo.pack(side=tk.LEFT)
        
        ttk.Button(path_frame, text="Tìm đường đi", command=self.find_path).pack(fill=tk.X)
        
        # 7. Nút xuất kết quả và xóa
        action_frame = ttk.Frame(control_frame)
        action_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(action_frame, text="Xuất kết quả", command=self.export_results).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(action_frame, text="Xóa", command=self.clear_data).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # 8. Nút hiển thị biểu đồ hiệu năng
        ttk.Button(control_frame, text="Hiển thị biểu đồ", command=self.show_performance_chart).pack(fill=tk.X, pady=5)
    
    def update_comboboxes(self):
        """Cập nhật giá trị cho các combobox"""
        if self.graph is None:
            return
            
        n = len(self.graph)
        values = [str(i) for i in range(n)]
        
        self.source_combo['values'] = values
        self.target_combo['values'] = values
        
        if n > 0:
            self.source_var.set("0")
            self.target_var.set("1" if n > 1 else "0")
    
    def generate_random_graph(self):
        """Tạo đồ thị ngẫu nhiên"""
        n = self.vertices.get()
        directed = self.directed.get()
        density = self.graph_density.get()
        max_weight = self.max_weight.get()
        
        # Tạo ma trận trọng số
        self.graph = [[float('inf') for _ in range(n)] for _ in range(n)]
        
        # Đặt đường chéo chính là 0
        for i in range(n):
            self.graph[i][i] = 0
        
        # Tạo các cạnh ngẫu nhiên
        edges_needed = int(density * n * (n - 1))
        if not directed:
            edges_needed = int(edges_needed / 2)
            
        edges_added = 0
        while edges_added < edges_needed:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            if i != j and self.graph[i][j] == float('inf'):
                weight = random.randint(1, max_weight)
                self.graph[i][j] = weight
                if not directed:
                    self.graph[j][i] = weight
                edges_added += 1
        
        # Cập nhật combobox và vẽ đồ thị
        self.update_comboboxes()
        self.canvas.set_graph(self.graph, directed)
        
        messagebox.showinfo("Thông báo", f"Đã tạo đồ thị ngẫu nhiên với {n} đỉnh")
    
    def create_empty_graph(self):
        """Tạo đồ thị rỗng"""
        n = self.vertices.get()
        self.graph = [[float('inf') for _ in range(n)] for _ in range(n)]
        
        # Đặt đường chéo chính là 0
        for i in range(n):
            self.graph[i][i] = 0
        
        # Cập nhật combobox và vẽ đồ thị
        self.update_comboboxes()
        self.canvas.set_graph(self.graph, self.directed.get())
        
        messagebox.showinfo("Thông báo", f"Đã tạo đồ thị rỗng với {n} đỉnh")
    
    def run_floyd_warshall(self):
        """Chạy thuật toán Floyd-Warshall"""
        if self.graph is None:
            messagebox.showerror("Lỗi", "Vui lòng tạo đồ thị trước")
            return
        
        # Khởi tạo và chạy thuật toán
        self.fw.initialize(self.graph)
        self.fw.run_algorithm()
        
        # Lưu dữ liệu hiệu năng
        n = len(self.graph)
        self.performance_data.append({
            'vertices': n,
            'time': self.fw.execution_time,
            'memory': self.fw.memory_usage,
            'complexity': n**3
        })
        
        # Hiển thị kết quả
        self.show_distance_matrix()
        self.show_performance()
        
        # Chuyển sang tab ma trận khoảng cách
        self.notebook.select(0)
        
        messagebox.showinfo("Thông báo", "Đã chạy thuật toán Floyd-Warshall thành công")
    
    def show_distance_matrix(self):
        """Hiển thị ma trận khoảng cách"""
        for widget in self.dist_tab.winfo_children():
            widget.destroy()
        
        if self.fw.dist is None:
            ttk.Label(self.dist_tab, text="Chưa có dữ liệu", padding=10).pack()
            return
            
        frame = ttk.Frame(self.dist_tab)
        frame.pack(fill=tk.BOTH, expand=True)
        
        scrollx = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrolly = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        
        tree = ttk.Treeview(frame, columns=[str(i) for i in range(len(self.fw.dist))], 
                          show='headings', xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        
        scrollx.config(command=tree.xview)
        scrolly.config(command=tree.yview)
        
        scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Thiết lập tiêu đề cột
        for i in range(len(self.fw.dist)):
            tree.heading(str(i), text=str(i))
            tree.column(str(i), width=60, anchor=tk.CENTER)
        
        # Thêm dữ liệu
        for i in range(len(self.fw.dist)):
            values = []
            for j in range(len(self.fw.dist)):
                if self.fw.dist[i][j] == float('inf'):
                    values.append("∞")
                else:
                    values.append(str(self.fw.dist[i][j]))
            tree.insert('', tk.END, text=str(i), values=values)
    
    def show_performance(self):
        """Hiển thị thông tin hiệu năng"""
        for widget in self.perf_tab.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(self.perf_tab, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        if self.fw.dist is None or self.fw.execution_time == 0:
            ttk.Label(frame, text="Vui lòng chạy thuật toán trước", padding=10).pack()
            return
        
        # Hiển thị thời gian thực thi
        exec_time = self.fw.execution_time
        time_unit = "giây"
        if exec_time < 0.001:
            exec_time *= 1_000_000
            time_unit = "micro giây"
        elif exec_time < 1:
            exec_time *= 1_000
            time_unit = "mili giây"
            
        ttk.Label(frame, text=f"Thời gian thực thi: {exec_time:.2f} {time_unit}", 
                 font=('Arial', 12)).pack(pady=5)
        
        # Hiển thị bộ nhớ sử dụng
        ttk.Label(frame, text=f"Bộ nhớ sử dụng: {self.fw.memory_usage:.2f} KB", 
                 font=('Arial', 12)).pack(pady=5)
        
        # Hiển thị độ phức tạp
        n = len(self.fw.dist)
        ttk.Label(frame, text=f"Độ phức tạp thời gian: O(V³) = O({n}³) = O({n**3})", 
                 font=('Arial', 12)).pack(pady=5)
    
    def show_performance_chart(self):
        """Hiển thị biểu đồ so sánh hiệu năng"""
        if len(self.performance_data) < 2:
            messagebox.showwarning("Cảnh báo", "Cần chạy thuật toán với ít nhất 2 đồ thị có kích thước khác nhau để vẽ biểu đồ")
            return
            
        # Sắp xếp dữ liệu theo số đỉnh
        sorted_data = sorted(self.performance_data, key=lambda x: x['vertices'])
        
        # Chuẩn bị dữ liệu
        vertices = [d['vertices'] for d in sorted_data]
        actual_times = [d['time'] * 1_000_000 for d in sorted_data]  # Chuyển sang micro giây
        predicted_times = [d['vertices']**3 * (actual_times[0] / vertices[0]**3) for d in sorted_data]
        
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(vertices, actual_times, 'b-o', label='Thực tế')
        ax.plot(vertices, predicted_times, 'r--', label='Dự đoán (O(V³))')
        
        ax.set_title('So sánh hiệu năng thuật toán Floyd-Warshall')
        ax.set_xlabel('Số đỉnh (V)')
        ax.set_ylabel('Thời gian thực thi (micro giây)')
        ax.legend()
        ax.grid(True)
        
        # Xóa nội dung cũ trong tab biểu đồ
        for widget in self.chart_tab.winfo_children():
            widget.destroy()
        
        # Nhúng biểu đồ vào giao diện
        canvas = FigureCanvasTkAgg(fig, master=self.chart_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Chuyển sang tab biểu đồ
        self.notebook.select(2)
    
    def find_path(self):
        """Tìm đường đi ngắn nhất giữa hai đỉnh"""
        if self.fw.dist is None:
            messagebox.showerror("Lỗi", "Vui lòng chạy thuật toán Floyd-Warshall trước")
            return
        
        try:
            source = int(self.source_var.get())
            target = int(self.target_var.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ cho đỉnh")
            return
        
        if self.graph is None:
            messagebox.showerror("Lỗi", "Chưa có đồ thị được tạo")
            return
            
        n = len(self.graph)
        if source < 0 or source >= n or target < 0 or target >= n:
            messagebox.showerror("Lỗi", f"Đỉnh phải nằm trong khoảng từ 0 đến {n-1}")
            return
        
        # Lấy đường đi
        path = self.fw.construct_path(source, target)
        
        if not path:
            messagebox.showinfo("Thông báo", f"Không có đường đi từ đỉnh {source} đến đỉnh {target}")
        else:
            # Highlight đường đi
            self.canvas.highlight_path(path)
            messagebox.showinfo("Thông báo", f"Đường đi từ {source} đến {target}: {' → '.join(map(str, path))}\nKhoảng cách: {self.fw.dist[source][target]}")
    
    def export_results(self):
        """Xuất kết quả ra file"""
        if self.fw.dist is None:
            messagebox.showerror("Lỗi", "Vui lòng chạy thuật toán Floyd-Warshall trước")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", ".txt"), ("All files", ".*")])
        
        if not filename:
            return
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("KẾT QUẢ THUẬT TOÁN FLOYD-WARSHALL\n\n")
                
                f.write(f"Số đỉnh: {self.fw.vertices}\n")
                f.write(f"Loại đồ thị: {'Có hướng' if self.directed.get() else 'Vô hướng'}\n\n")
                
                f.write("MA TRẬN TRỌNG SỐ BAN ĐẦU:\n")
                for i in range(self.fw.vertices):
                    for j in range(self.fw.vertices):
                        if self.graph[i][j] == float('inf'):
                            f.write("∞\t")
                        else:
                            f.write(f"{self.graph[i][j]}\t")
                    f.write("\n")
                
                f.write("\nMA TRẬN KHOẢNG CÁCH NGẮN NHẤT:\n")
                for i in range(self.fw.vertices):
                    for j in range(self.fw.vertices):
                        if self.fw.dist[i][j] == float('inf'):
                            f.write("∞\t")
                        else:
                            f.write(f"{self.fw.dist[i][j]}\t")
                    f.write("\n")
                
                f.write("\nTHÔNG TIN HIỆU NĂNG:\n")
                f.write(f"Thời gian thực thi: {self.fw.execution_time:.6f} giây\n")
                f.write(f"Bộ nhớ sử dụng: {self.fw.memory_usage:.2f} KB\n")
                f.write(f"Độ phức tạp thời gian: O(V³) = O({self.fw.vertices}³) = O({self.fw.vertices**3})\n")
            
            messagebox.showinfo("Thông báo", f"Đã xuất kết quả ra file {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xuất file: {str(e)}")
    
    def add_edge(self):
        """Thêm cạnh thủ công vào đồ thị"""
        if self.graph is None:
            messagebox.showerror("Lỗi", "Vui lòng tạo đồ thị rỗng trước")
            return

        n = len(self.graph)
        u = self.u_var.get()
        v = self.v_var.get()
        w = self.w_var.get()

        if u < 0 or u >= n or v < 0 or v >= n:
            messagebox.showerror("Lỗi", f"Chỉ số đỉnh phải nằm trong khoảng 0 đến {n-1}")
            return
        if u == v:
            messagebox.showwarning("Cảnh báo", "Không thể thêm cạnh từ một đỉnh tới chính nó")
            return

        self.graph[u][v] = w
        if not self.directed.get():
            self.graph[v][u] = w

        self.canvas.set_graph(self.graph, self.directed.get())
        messagebox.showinfo("Thành công", f"Đã thêm cạnh ({u} → {v}) trọng số {w}")
    
    def clear_data(self):
        """Xóa dữ liệu hiện tại"""
        self.graph = None
        self.fw = FloydWarshall()
        self.canvas.set_graph(None)
        self.performance_data = []
        for widget in self.dist_tab.winfo_children():
            widget.destroy()
        for widget in self.perf_tab.winfo_children():
            widget.destroy()
        for widget in self.chart_tab.winfo_children():
            widget.destroy()
        messagebox.showinfo("Thông báo", "Đã xóa dữ liệu hiện tại")

if __name__ == "__main__":
    root = tk.Tk()
    app = FloydWarshallApp(root)
    root.mainloop()
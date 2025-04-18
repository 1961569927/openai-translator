import tkinter as tk
from tkinter import ttk

def process_input():
    """处理用户输入并更新结果标签"""
    input_text = entry.get()  # 获取输入框内容
    if input_text:
        # 示例处理：反转字符串并统计字数
        reversed_text = input_text[::-1]
        word_count = len(input_text.split())
        result_text = f"反转内容: {reversed_text}\n字符数: {len(input_text)}\n单词数: {word_count}"
        result_label.config(text=result_text)
    else:
        result_label.config(text="请输入内容！")

# 创建主窗口
root = tk.Tk()
root.title("GUI 交互示例")
root.geometry("400x300")  # 设置窗口大小

# 使用主题样式
style = ttk.Style()
style.theme_use('clam')

# 创建界面组件
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True, fill='both')

label = ttk.Label(main_frame, text="请输入文本：")
label.grid(row=0, column=0, sticky='w', pady=5)

entry = ttk.Entry(main_frame, width=40)
entry.grid(row=1, column=0, pady=5)

process_btn = ttk.Button(main_frame, text="处理文本", command=process_input)
process_btn.grid(row=2, column=0, pady=10)

result_label = ttk.Label(main_frame, text="",
                        background='#f0f0f0',
                        padding=10,
                        wraplength=300,
                        justify='left')
result_label.grid(row=3, column=0, sticky='we', pady=5)

# 设置网格列权重
main_frame.columnconfigure(0, weight=1)

# 运行主循环
root.mainloop()
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re, os

class CodeEditor:
    """Редактор кода, написанный на Python с графическим интерфейсом и подсветкой ключевых слов при написании кода на Python.\nmaster: объект класса "Tk", встроенной библиотеки tkinter."""
    def __init__(self, master: tk.Tk):
        """Инициализация."""
        self.master = master
        master.title("Редактор кода")
        master.geometry("800x600")
        KEYWORD_COLOR = "#FF7F50"  # Coral
        STRING_COLOR = "#98FB98"   # PaleGreen
        COMMENT_COLOR = "#808080"  # Gray
        FUNCTION_COLOR = "#4682B4" # SteelBlue
        NUMBER_COLOR = "#BDB76B"   # DarkKhaki
        BUILTIN_COLOR = "#FFA07A"  # LightSalmon

        self.filename = None  # Current file

        # --- Widgets ---
        self.text_area = scrolledtext.ScrolledText(
            master, wrap=tk.WORD, undo=True, font=("Consolas", 12)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # --- Menu ---
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="новенький", command=self.new_file)
        self.file_menu.add_command(label="открыть", command=self.open_file)
        self.file_menu.add_command(label="сохранить", command=self.save_file)
        self.file_menu.add_command(label="Сохранить в директории...", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Назад", command=master.quit)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Отменить", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Вперёд", command=self.text_area.edit_redo)
        self.menu_bar.add_cascade(label="Изменить", menu=self.edit_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="о проге", command=self.show_about)
        self.menu_bar.add_cascade(label="помоги, плиз", menu=self.help_menu)


        self.text_area.bind("<KeyRelease>", self.highlight_syntax)  # Подсветка при вводе

        # --- Syntax Highlighting Tags ---
        self.text_area.tag_configure("keyword", foreground=KEYWORD_COLOR)
        self.text_area.tag_configure("string", foreground=STRING_COLOR)
        self.text_area.tag_configure("comment", foreground=COMMENT_COLOR)
        self.text_area.tag_configure("function", foreground=FUNCTION_COLOR)
        self.text_area.tag_configure("number", foreground=NUMBER_COLOR)
        self.text_area.tag_configure("builtin", foreground=BUILTIN_COLOR)

        # --- Keywords ---
        self.keywords = ["def", "class", "if", "else", "elif", "for", "while", "return", "import", "from", "try", "except", "finally", "with", "as", "assert", "break", "continue", "del", "global", "nonlocal", "in", "is", "lambda", "pass", "raise", "yield"]
        self.builtins = ["print", "len", "range", "str", "int", "float", "bool", "list", "tuple", "dict", "set", "open", "file", "input", "exit", "help", "dir", "type", "object"]
    def new_file(self):
        """Создает новый файл."""
        self.text_area.delete("1.0", tk.END)  # Clear the text area
        self.filename = None  # Reset filename
        self.master.title("Редактор кода - New File")

    def open_file(self):
        """Открыть файл."""
        filepath = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("C++ Files", "*.cpp")]
        )
        if filepath:
            try:
                with open(filepath, "r", encoding='UTF-8') as file:
                    content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
                self.filename = filepath
                self.master.title(f"Редактор кода - {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("ОШИБОЧКА", f"вот это:\n{e}")

    def save_file(self):
        """Сохранить файл."""
        if self.filename:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(self.filename, "w") as file:
                    file.write(content)
                messagebox.showinfo("успех", "файл сохранен.")
            except Exception as e:
                messagebox.showerror("ошибочка", f"лееее:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Сохранить файл как..."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("C++ Files", "*.cpp")]
        )
        if filepath:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(filepath, "w") as file:
                    file.write(content)
                self.filename = filepath
                self.master.title(f"Редактор кода - {os.path.basename(filepath)}")
                messagebox.showinfo("урыыы", "файл типо сохранен.")
            except Exception as e:
                messagebox.showerror("ошибОЧКА", f"посмотри сам:\n{e}")

    def show_about(self):
        """О программе."""
        messagebox.showinfo(
            "О проге", "Редактор кода от Флореста. Сделано с любовью."
        )
    def highlight_syntax(self, event=None):
        """Подсвечивает синтаксис Python."""
        # Удаляем все старые теги
        for tag in self.text_area.tag_names():
            self.text_area.tag_remove(tag, "1.0", tk.END)

        text = self.text_area.get("1.0", tk.END)

        # Подсветка комментариев
        for match in re.finditer(r"#.*", text):
            start = "1.0 + %dc" % match.start()
            end = "1.0 + %dc" % match.end()
            self.text_area.tag_add("comment", start, end)

        # Подсветка строк
        for match in re.finditer(r"(\".*\")|(\'.*\')", text):
            start = "1.0 + %dc" % match.start()
            end = "1.0 + %dc" % match.end()
            self.text_area.tag_add("string", start, end)

        # Подсветка ключевых слов
        for word in self.keywords:
            pattern = r'\b' + word + r'\b'  # Границы слова
            for match in re.finditer(pattern, text):
                start = "1.0 + %dc" % match.start()
                end = "1.0 + %dc" % match.end()
                self.text_area.tag_add("keyword", start, end)

        # Подсветка встроенных функций
        for word in self.builtins:
            pattern = r'\b' + word + r'\b'  # Границы слова
            for match in re.finditer(pattern, text):
                start = "1.0 + %dc" % match.start()
                end = "1.0 + %dc" % match.end()
                self.text_area.tag_add("builtin", start, end)

        # Подсветка чисел
        for match in re.finditer(r'\b\d+\b', text):
            start = "1.0 + %dc" % match.start()
            end = "1.0 + %dc" % match.end()
            self.text_area.tag_add("number", start, end)

        # Подсветка функций (очень упрощенно)
        for match in re.finditer(r'def\s+(\w+)\s*\(', text):
            start = "1.0 + %dc" % match.start(1) # Начало имени функции
            end = "1.0 + %dc" % match.end(1) # Конец имени функции
            self.text_area.tag_add("function", start, end)
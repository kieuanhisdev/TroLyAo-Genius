from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import ast

w = Tk()
w.geometry('925x500')
w.title('Login')
w.configure(bg='#ff4f5a')
w.minsize(925, 500)
w.iconbitmap(r'Image\theme1\ai.ico')

def signin():
    signin_win = Frame(w, width=925, height=500, bg='white')
    signin_win.place(x=0, y=0)
    f1 = Frame(signin_win, width=350, height=350, bg='white')
    f1.place(x=480, y=100)

    global img1
    img1 = ImageTk.PhotoImage(Image.open(r"Image\ai1.png"))
    Label(signin_win, image=img1, border=0, bg='white').place(x=50, y=50)

    l2 = Label(signin_win, text="Đăng nhập", fg='#ff4f5a', bg='white')
    l2.config(font=('Microsoft YaHei UI Light', 23, 'bold'))
    l2.place(x=570, y=60)

    def on_enter(e):
        e1.delete(0, 'end')

    def on_leave(e):
        if e1.get() == '':
            e1.insert(0, 'Tên đăng nhập')

    e1 = Entry(f1, width=25, fg='black', border=0, bg='white')
    e1.config(font=('Microsoft YaHei UI Light', 11, ))
    e1.bind("<FocusIn>", on_enter)
    e1.bind("<FocusOut>", on_leave)
    e1.insert(0, 'Tên đăng nhập')
    e1.place(x=30, y=60)

    Frame(f1, width=295, height=2, bg='black').place(x=25, y=87)

    # ------------------------------------------------------

    def on_enter(e):
        e2.delete(0, 'end')

    def on_leave(e):
        if e2.get() == '':
            e2.insert(0, 'Mật khẩu')

    e2 = Entry(f1, width=21, fg='black', border=0, bg='white')
    e2.config(font=('Microsoft YaHei UI Light', 11, ))
    e2.bind("<FocusIn>", on_enter)
    e2.bind("<FocusOut>", on_leave)
    e2.insert(0, 'Mật khẩu')
    e2.place(x=30, y=130)
    Frame(f1, width=295, height=2, bg='black').place(x=25, y=157)

    # -mech------------------------------------------------
    def signin_cmd():

        file = open('Database\datasheet.txt', 'r')
        d = file.read()
        r = ast.literal_eval(d)
        file.close()

        key = e1.get()
        value = e2.get()

        if key in r.keys() and value == r[key]:
            messagebox.showinfo("", "     đăng nhập thành công    ")
            w.destroy()
            import index
        else:
            messagebox.showwarning(
                'thử lại', 'tên đăng nhập hoặc mật khẩu sai')

    # ------------------------------------------------------
    Button(f1, width=39, pady=7, text='Đăng nhập', bg='#ff4f5a',
           fg='white', border=0, command=signin_cmd).place(x=35, y=204)
    l1 = Label(f1, text="Bạn không có tài khoản?", fg="black", bg='white')
    l1.config(font=('Microsoft YaHei UI Light', 9, ))
    l1.place(x=75, y=250)

    b2 = Button(f1, width=12, text='Tạo tài khoản', border=0,
                bg='white', fg='#ff4f5a', command=signup)
    b2.place(x=215, y=250)


def signup():
    signup_win = Frame(w, width=925, height=500, bg='white')
    signup_win.place(x=0, y=0)
    f1 = Frame(signup_win, width=350, height=350, bg='white')
    f1.place(x=480, y=70)

    global img2
    img2 = ImageTk.PhotoImage(Image.open(r"Image\ai1.png"))
    Label(signup_win, image=img2, border=0, bg='white').place(x=30, y=50)

    l2 = Label(signup_win, text="Đăng ký", fg='#ff4f5a', bg='white')
    l2.config(font=('Microsoft YaHei UI Light', 23, 'bold'))
    l2.place(x=600, y=60)

    def on_enter(e):
        e1.delete(0, 'end')

    def on_leave(e):
        if e1.get() == '':
            e1.insert(0, 'Tên đăng nhập')

    e1 = Entry(f1, width=25, fg='black', border=0, bg='white')
    e1.config(font=('Microsoft YaHei UI Light', 11, ))
    e1.bind("<FocusIn>", on_enter)
    e1.bind("<FocusOut>", on_leave)
    e1.insert(0, 'Tên đăng nhập')
    e1.place(x=30, y=60)

    Frame(f1, width=295, height=2, bg='black').place(x=25, y=87)

    # ------------------------------------------------------

    def on_enter(e):
        e2.delete(0, 'end')

    def on_leave(e):
        if e2.get() == '':
            e2.insert(0, 'Mật khẩu')

    e2 = Entry(f1, width=21, fg='black', border=0, bg='white')
    e2.config(font=('Microsoft YaHei UI Light', 11, ))
    e2.bind("<FocusIn>", on_enter)
    e2.bind("<FocusOut>", on_leave)
    e2.insert(0, 'Mật khẩu')
    e2.place(x=30, y=130)

    Frame(f1, width=295, height=2, bg='black').place(x=25, y=157)

    def on_enter(e):
        e3.delete(0, 'end')

    def on_leave(e):
        if e3.get() == '':
            e3.insert(0, 'Mật khẩu')

    e3 = Entry(f1, width=21, fg='black', border=0, bg='white')
    e3.config(font=('Microsoft YaHei UI Light', 11, ))
    e3.bind("<FocusIn>", on_enter)
    e3.bind("<FocusOut>", on_leave)
    e3.insert(0, 'Nhập lại mật khẩu')
    e3.place(x=30, y=130+70)

    Frame(f1, width=295, height=2, bg='black').place(x=25, y=157+70)

    # Mechenism------------------------------------------------

    def signup_cmd():
        key = e1.get()
        value = e2.get()
        value2 = e3.get()

        if value == value2:
            file = open('Database\datasheet.txt', 'r+')
            d = file.read()
            r = ast.literal_eval(d)
            print(r)

            dict2 = {key: value}
            print(dict2)
            r.update(dict2)
            print(r)
            file.truncate(0)
            file.close()
            print(r)
            file = open('Database\datasheet.txt', 'r+')
            w = file.write(str(r))

            messagebox.showinfo("", "     Tạo tài khoản thành công     ")

        else:
            messagebox.showwarning('Thử lại', 'Mật khẩu không hợp lệ ')

    # -------------------------------------------------------
    Button(f1, width=39, pady=7, text='Đăng ký', bg='#ff4f5a',
           fg='white', border=0, command=signup_cmd).place(x=35, y=204+60)
    l1 = Label(f1, text="Bạn đã có tài khoản?", fg="black", bg='white')
    l1.config(font=('Microsoft YaHei UI Light', 9, ))
    l1.place(x=70, y=250+63)

    b2 = Button(f1, width=10, text='Đăng nhập', border=0,
                bg='white', fg='#ff4f5a', command=signin)
    b2.place(x=210, y=250+63)


signin()  # default screen

w.mainloop()

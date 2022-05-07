import ttkbootstrap as ttk
import mvc.view as view

if __name__ == '__main__':
    app = ttk.Window("MyFaker", "superhero",
                     resizable=(False, False),)
    view.FakerUI(app)
    app.mainloop()

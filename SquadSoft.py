from customtkinter import *
from PIL import Image
from threading import Thread
from time import sleep
from keyboard import add_hotkey
from pynput import mouse
import os

main = CTk()
main.attributes('-fullscreen', 1)
main.attributes('-topmost', 1)
main.wm_attributes('-transparentcolor', '#242424')
main.overrideredirect(True)

class SquadSoft():
    def __init__(self, window):
        self.window = window
        self.main_canvas = CTkCanvas(self.window, width=main.winfo_screenwidth(), height=main.winfo_screenheight(), bg='#242424')
        self.main_canvas.place(x=-2, y=-2)

        self.load_settings()
        self.gp_table()
        self.calculate_distance()
    def window_leave(self):
        main.quit()
    def load_settings(self):
        #load
        self.settings = {}
        settings_path = 'settings.txt'
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as settings_file:
                for line in settings_file:
                    try:
                        key, value = line.strip().split('=')
                        self.settings[key] = value
                    except:
                        pass
        #keybind
        add_hotkey(self.settings['window_leave'], lambda: self.window_leave())
    def gp_table(self):
        self.gp_table_switch = True
        self.gp_weapons = {1: {'name': 'Австралия SL40 ', 'path': r'GP\sl40.png', 'size': (625, 330)},
                           2: {'name': 'Британия L123A2', 'path': r'GP\l123a2.png', 'size': (625, 290)},
                           3: {'name': 'Канада M203A1', 'path': r'GP\m203a1.png', 'size': (625, 290)},
                           4: {'name': 'Милита M203', 'path': r'GP\m203_mil.png', 'size': (625, 295)},
                           5: {'name': 'Милита/Бомжи/рф/ВДВ GP25', 'path': r'GP\gp25.png', 'size': (625, 330)},
                           6: {'name': 'Альянс HK79', 'path': r'GP\hk79.png', 'size': (625, 290)},
                           7: {'name': 'Китай QLG10', 'path': r'GP\qlg10.png', 'size': (625, 260)},
                           8: {'name': 'США M203', 'path': r'GP\m203_usa.png', 'size': (625, 190)},
                           9: {'name': 'МПСША M203', 'path': r'GP\m203_usa+.png', 'size': (625, 220)},
                           10: {'name': 'Турция AK40GL (ВСЁ летит левее на 2-3 градуса)', 'path': r'GP\ak40gl.png', 'size': (625, 250)},
                           11: {'name': 'Турция MGL Барабан', 'path': r'GP\mgl.png', 'size': (625, 330)},
                           12: {'name': 'Милита FN FAL Rifle Frag', 'path': r'GP\rifle_frag.png', 'size': (625, 150)}}
        self.gp_weapon = 5
        #gp_table_widget
        gp_tableL = CTkLabel(self.window, image=CTkImage(dark_image=Image.open(self.gp_weapons[self.gp_weapon]['path']), size=(625, 330)), text='')
        gp_tableL.place(x=25, y=25)
        gp_nameL = CTkLabel(self.window, text=self.gp_weapons[self.gp_weapon]['name'], font=('Arial Black', 15), text_color=self.settings['text_color'],fg_color='#242424')
        gp_nameL.place(x=25, y=365)
        #move_table
        self.gp_start_x, self.gp_start_y = 25, 25
        current_x, current_y = 25, 25
        def move_table(e):
            nonlocal current_x, current_y
            current_x += e.x_root - self.gp_start_x
            current_y += e.y_root - self.gp_start_y
            gp_tableL.place(x=current_x, y=current_y)
            gp_nameL.place(x=current_x, y=current_y+self.gp_weapons[self.gp_weapon]['size'][1]+10)
            self.gp_start_x, self.gp_start_y = e.x_root, e.y_root
        def mouse_press(event):
            self.gp_start_x, self.gp_start_y  = event.x_root, event.y_root
        gp_tableL.bind("<B1-Motion>", move_table)
        gp_tableL.bind("<ButtonPress-1>", mouse_press)
        # keybind
        def gp_table_switchF():
            if self.gp_table_switch:
                self.gp_table_switch = False
                gp_tableL.place_forget()
                gp_nameL.place_forget()
            else:
                self.gp_table_switch = True
                gp_tableL.place(x=current_x, y=current_y)
                gp_nameL.place(x=current_x, y=current_y + self.gp_weapons[self.gp_weapon]['size'][1] + 10)
        add_hotkey(self.settings['gp_switch'], gp_table_switchF)
        def gp_weapon_switchF():
            if self.gp_weapon < 12:
                self.gp_weapon += 1
            else:
                self.gp_weapon = 1
            gp_tableL.configure(image=CTkImage(dark_image=Image.open(self.gp_weapons[self.gp_weapon]['path']), size=(self.gp_weapons[self.gp_weapon]['size'])))
            gp_nameL.configure(text=self.gp_weapons[self.gp_weapon]['name'])
            gp_nameL.place(x=current_x, y=current_y + self.gp_weapons[self.gp_weapon]['size'][1] + 10)
        add_hotkey(self.settings['gp_weapon_switch'], gp_weapon_switchF)
    def calculate_distance(self):
        self.pix_distance = 0
        self.pnr_distance = 100

        def calculator(mode):
            self.click_count = 0
            x_coord = []
            xy_coords = []

            def on_click(x, y, button, pressed):
                if button == mouse.Button.left and pressed:
                    self.click_count += 1
                    if mode == 'start':
                        x_coord.append(x)
                    elif mode == 'real':
                        xy_coords.append((x, y))
                if self.click_count == 2:
                    listener.stop()
                    if mode == 'start':
                        self.pix_distance = abs(x_coord[1] - x_coord[0])
                    if mode == 'real':
                        if self.pix_distance != 0:
                            x1, y1 = xy_coords[0]
                            x2, y2 = xy_coords[1]
                            pix_dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                            real_dist = round(pix_dist / (self.pix_distance / self.pnr_distance))
                            def show_distance():
                                line = self.main_canvas.create_line(x1, y1, x2, y2, width=4, fill=self.settings['text_color'])
                                distanceL = CTkLabel(self.window, text=f'{real_dist}м', font=('Arial Black', 15),text_color=self.settings['text_color'], fg_color='#242424')
                                distanceL.place(x=x2, y=y2+5)
                                sleep(1.25)
                                distanceL.destroy()
                                self.main_canvas.delete(line)
                            Thread(target=show_distance).start()
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            listener.join()
        def switch_distance():
            if self.pnr_distance == 100:
                self.pnr_distance = 300
            elif self.pnr_distance == 300:
                self.pnr_distance = 900
            else:
                self.pnr_distance = 100
            def show_distance():
                distanceL = CTkLabel(self.window, text=f'{self.pnr_distance}м', font=('Arial Black', 25), text_color=self.settings['text_color'], fg_color='#242424')
                distanceL.place(relx=0.5, rely=0.5)
                sleep(1)
                distanceL.destroy()
            Thread(target=show_distance).start()
        add_hotkey(self.settings['distance_start'], lambda: calculator('start'))
        add_hotkey(self.settings['distance_calculate'], lambda: calculator('real'))
        add_hotkey(self.settings['distance_start_switch'], switch_distance)

if __name__ == '__main__':
    app = SquadSoft(main)


main.mainloop()
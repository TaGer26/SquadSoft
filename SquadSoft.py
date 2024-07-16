from customtkinter import *
from PIL import Image
from threading import Thread
from time import sleep
from keyboard import add_hotkey
from pynput import mouse
from pyautogui import screenshot
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
        self.version =0.2

        self.load_settings()
        self.gp_table()
        self.calculate_distance()
        self.menu()
        self.zoom()
    def window_leave(self):
        main.quit()
        exit()
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
    def menu(self):
        self.menu_switch = False
        self.menu_zoom_mul = 8
        menuF = CTkFrame(self.window, width=750, height=500)
        self.menuF_start_x, self.menuF_start_y = 300, 100
        current_x, current_y = 300, 100
        def move_menu(e):
            nonlocal current_x, current_y
            current_x += e.x_root - self.menuF_start_x
            current_y += e.y_root - self.menuF_start_y
            menuF.place(x=current_x, y=current_y)
            self.menuF_start_x, self.menuF_start_y = e.x_root, e.y_root
        def mouse_press(event):
            self.menuF_start_x, self.menuF_start_y = event.x_root, event.y_root
        menuF.bind("<B1-Motion>", move_menu)
        menuF.bind("<ButtonPress-1>", mouse_press)
        def switchF():
            if self.gp_table_switch:
                self.gp_table_switch = False
                menuF.place_forget()
            else:
                self.gp_table_switch = True
                menuF.place(x=current_x, y=current_y)
        add_hotkey(self.settings['menu_switch'], switchF)
        #menu_content
        soft_nameL = CTkLabel(menuF, text=f'SquadSoft v{self.version}', font=('Arial Black', 12)).place(x=5, y=0)
        gp_tableC = CTkCheckBox(menuF, text='Таблица ГП', font=('Arial Black', 12))
        gp_tableC.place(x=5, y=50)
        calculatorC = CTkCheckBox(menuF, text='Калькулятор расстояния', font=('Arial Black', 12))
        calculatorC.place(x=5, y=90)
        zoomC = CTkCheckBox(menuF, text='Приближение прицела', font=('Arial Black', 12))
        zoomC.place(x=5, y=130)
        def change_multiplier(value):
            zoom_multipliereL.configure(text=f'x{int(value)}')
            self.menu_zoom_mul = int(value)
        zoom_multiplier = CTkSlider(menuF, from_=1, to=16, number_of_steps=16, command=change_multiplier)
        zoom_multiplier.place(x=215, y=135)
        zoom_multipliereL = CTkLabel(menuF, text=f'x8', font=('Arial Black', 10))
        zoom_multipliereL.place(x=430, y=128)
        def apply_settings():
            if gp_tableC.get() == 1:
                self.gp_state = True
            else:
                self.gp_state = False
            if calculatorC.get() == 1:
                self.calculate_state = True
            else:
                self.calculate_state = False
            if zoomC.get() == 1:
                self.zoom_state = True
            else:
                self.zoom_state = False
            self.zoom_m = self.menu_zoom_mul
        applyB = CTkButton(menuF, text='Применить', font=('Arial Black', 12), command=apply_settings).place(x=5, y=460)

    def gp_table(self):
        self.gp_table_switch = False
        self.gp_state = True
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
        gp_tableL = CTkLabel(self.window, image=CTkImage(dark_image=Image.open(self.gp_weapons[self.gp_weapon]['path']), size=(625*float(self.settings['gp_scale']), 330*float(self.settings['gp_scale']))), text='')
        gp_nameL = CTkLabel(self.window, text=self.gp_weapons[self.gp_weapon]['name'], font=('Arial Black', 15), text_color=self.settings['text_color'],fg_color='#242424')
        #move_table
        self.gp_start_x, self.gp_start_y = 25, 25
        current_x, current_y = 25, 25
        def move_table(e):
            nonlocal current_x, current_y
            current_x += e.x_root - self.gp_start_x
            current_y += e.y_root - self.gp_start_y
            gp_tableL.place(x=current_x, y=current_y)
            gp_nameL.place(x=current_x, y=current_y+(self.gp_weapons[self.gp_weapon]['size'][1]*float(self.settings['gp_scale']))+10)
            self.gp_start_x, self.gp_start_y = e.x_root, e.y_root
        def mouse_press(event):
            self.gp_start_x, self.gp_start_y  = event.x_root, event.y_root
        gp_tableL.bind("<B1-Motion>", move_table)
        gp_tableL.bind("<ButtonPress-1>", mouse_press)
        # keybind
        def gp_table_switchF():
            if self.gp_state:
                if self.gp_table_switch:
                    self.gp_table_switch = False
                    gp_tableL.place_forget()
                    gp_nameL.place_forget()
                else:
                    self.gp_table_switch = True
                    gp_tableL.place(x=current_x, y=current_y)
                    gp_nameL.place(x=current_x, y=current_y + (self.gp_weapons[self.gp_weapon]['size'][1]*float(self.settings['gp_scale'])) + 10)
        add_hotkey(self.settings['gp_switch'], gp_table_switchF)
        def gp_weapon_switchF():
            if self.gp_state:
                if self.gp_weapon < 12:
                    self.gp_weapon += 1
                else:
                    self.gp_weapon = 1
                gp_tableL.configure(image=CTkImage(dark_image=Image.open(self.gp_weapons[self.gp_weapon]['path']), size=((self.gp_weapons[self.gp_weapon]['size'][0]*float(self.settings['gp_scale'])), (self.gp_weapons[self.gp_weapon]['size'][1]*float(self.settings['gp_scale'])))))
                gp_nameL.configure(text=self.gp_weapons[self.gp_weapon]['name'])
                gp_nameL.place(x=current_x, y=current_y + (self.gp_weapons[self.gp_weapon]['size'][1]*float(self.settings['gp_scale'])) + 10)
        add_hotkey(self.settings['gp_weapon_switch'], gp_weapon_switchF)
    def calculate_distance(self):
        self.calculate_state = True
        self.pix_distance = 0
        self.pnr_distance = 100

        def calculator(mode):
            if self.calculate_state:
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
            if self.calculate_state:
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
        
    def zoom(self):
        self.zoom_flag = False
        self.zoom_state = True
        self.zoom_m = 2
        def img_zoom(img, zoom):
            w, h = img.size
            zoom2 = zoom * 2
            img = img.crop((960 - w / zoom2, 540 - h / zoom2,
                            960 + w / zoom2, 540 + h / zoom2))
            return img
        def zoomF():
            self.zoom_flag = True
            def update_image():
                im = screenshot()
                im = img_zoom(im, 12)
                self.zoomL.configure(image=CTkImage(dark_image=im, size=(450, 300)))
                self.window.after(16, update_image)

            im = img_zoom(screenshot(), self.zoom_m)
            imT = CTkImage(im, size=(600, 600))
            self.zoomL = CTkLabel(self.window, image=imT, text='')
            self.zoomL.place(x=int(self.settings['zoom_position_x']), y=int(self.settings['zoom_position_y']))
            update_image()
        def zoom_switch():
            if self.zoom_state:
                if self.zoom_flag:
                    self.zoom_flag = False
                    self.zoomL.place_forget()
                else:
                    self.zoom_flag = True
                    Thread(target=zoomF).start()
        add_hotkey(self.settings['zoom'], zoom_switch)


if __name__ == '__main__':
    app = SquadSoft(main)


main.mainloop()

import customtkinter as ck 
import tkintermapview
from PIL import Image, ImageTk

ck.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ck.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ck.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("DragonFly")


        x_window = 1000
        y_window = 700

        columns = 2
        rows = 5
        pad = 15

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(f"{ x_window }x{ y_window }")


        ##------Create and config tree frames -----##
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ck.CTkFrame(master=self, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = ck.CTkFrame(master=self, corner_radius=0, fg_color=None)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")
  

        ###------- Right frame -----###
        self.frame_right.grid_rowconfigure(2, weight=2)
        self.frame_right.grid_rowconfigure(1, weight=0)
        self.frame_right.grid_rowconfigure(0, weight=0)

        self.frame_right.grid_columnconfigure(0, weight=2)
        self.frame_right.grid_columnconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(2, weight=1)



        ## MAP
        self.map_widget = tkintermapview.TkinterMapView(self.frame_right, corner_radius=10)
        self.map_widget.grid(row=2, rowspan=1, column=0, columnspan=4, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.set_address("Тула")

        title_map_optin_menu = ck.StringVar(value="Select map")
        self.map_option_menu = ck.CTkOptionMenu(self.frame_right, values=["Default","OpenStreetMap", "Google normal", "Google satellite", "Wikimedia Cloud Services"],
                                                font=("Monaco", 16), variable=title_map_optin_menu, command=self.change_map)
        self.map_option_menu.set("Default")
        self.map_option_menu.grid(row=0, column=0, pady=(0,2))

        # Info button
        info_icon = Image.open("images/info_btn.png")
        self.info_btn = ck.CTkButton(self.frame_right, image=ImageTk.PhotoImage(info_icon), anchor='e',
                                        text='', width=64, height=64, command=self.show_info)
        self.info_btn.grid(row=0, column=2, padx=(pad,pad), pady=(pad,pad))


        # Power button
        self.counter_conn_btn = 0
        conn_icon = Image.open("images/power_btn.png")
        self.conn_btn = ck.CTkButton(self.frame_right, image=ImageTk.PhotoImage(conn_icon), anchor='e',
                                        text='', width=64, height=64, command=self.connect_to_drone)
        self.conn_btn.grid(row=0, column=3, padx=(pad,pad), pady=(pad,pad))
        self.conn_btn.invoke()
        
        # Select USB port
        ports = self.scan_USB_ports()
        title_scrl = ck.StringVar(value="Select port  ")
        self.scaling_optionemenu_port = ck.CTkOptionMenu(self.frame_right, values=ports, anchor='e', variable=title_scrl,
                                                          font=("Monaco", 16), command=self.change_USB_port)
        self.scaling_optionemenu_port.grid(row=0, column=1, padx=(2,0), pady=(2,2))





        ###--------- Left Frame --------###
        self.frame_left.grid_columnconfigure(0, weight=1)

        self.frame_left.grid_rowconfigure(1, weight=1)
        self.frame_left.grid_rowconfigure(2, weight=1)
        self.frame_left.grid_rowconfigure(3, weight=4)
        self.frame_left.grid_rowconfigure(4, weight=5)

        # Uppest label 
        self.first_frame = ck.CTkFrame(self.frame_left, corner_radius=10, fg_color='white',height=160)
        self.first_frame.grid(row=0, column=0, padx=(pad,pad), pady=(pad,pad), sticky="nsew" )

        # Center label - Stats
        self.second_frame_scrollable = ck.CTkScrollableFrame(self.frame_left, label_text="Stats", 
                                                                        corner_radius=10, fg_color='white',height=110)
        self.second_frame_scrollable.grid(row=1, column=0, padx=(pad,pad), pady=(0,pad), sticky="nsew" )
        
        ##скорость, высота, заряд батареи
        title1 = ['скорость', 'высота', 'батарея']
        values1 = self.get_stats()
        self.titles = ck.CTkLabel(self.second_frame_scrollable, text=f'{title1[0]}    {title1[1]}    {title1[2]}', 
                                             fg_color=None, font=("Monaco", 16))
        self.titles.grid(row=0, column=0, padx=(5,5), pady=(0,5),sticky="nsew" )
        self.values1 = ck.CTkLabel(self.second_frame_scrollable, text='    '.join(values1), 
                                              fg_color=None, font=("Monaco", 28), text_color = 'red')
        self.values1.grid(row=1, column=0, padx=(5,5), pady=(0,5),sticky="nsew" )

        
        """
        ## На будущее
        
        title2 = ['123', '456', '789']
        values2 = self.get_stats2()
        self.titles = ck.CTkLabel(self.second_frame_scrollable, text=f'{title2[0]}     {title2[1]}  {title2[2]}', 
                                            fg_color=None, font=("Monaco", 16))
        self.titles.grid(row=0, column=0, padx=(5,5), pady=(0,5),sticky="nsew" )
        self.values1 = ck.CTkLabel(self.second_frame_scrollable, text='     '.join(values2), 
                                            fg_color=None, font=("Monaco", 25),text_color = 'red')
        self.values1.grid(row=1, column=0, padx=(5,5), pady=(0,5),sticky="nsew" )"""

        # Contron Panel
        lower_slider_value = 0
        upper_slider_value = 100
        self.slider_1 = ck.CTkSlider(self.frame_left, orientation="vertical", height=110, 
                                                from_=lower_slider_value, to=upper_slider_value, number_of_steps=10, hover=True)
        self.slider_1.grid(row=2, column=0, padx=(pad, pad), pady=(pad, pad), sticky="w")

        # Downest button - Controling (ON/OFF)
        self.couter_btn_control = 1
        self.btn_control = ck.CTkButton(self.frame_left,fg_color="red", height=50, corner_radius=10, text='Keyboard OFF', 
                                        anchor='s', font=("Monaco", 16), command=self.control_settings)
        self.btn_control.grid(row=3, column=0, padx=(pad,pad), pady=(pad, pad), sticky='wsne')
        self.btn_control.invoke()  #press on btn



    ###--------------- ACTIONS ------------------###
    def control_settings(self):
        if self.couter_btn_control % 2 != 0: ## enable button
            self.btn_control.configure(fg_color='green', text='Keyboard ON')
            self.couter_btn_control+=1
            pass
        else:                                 ## disable button
            self.btn_control.configure(fg_color='red', text='Keyboard OFF')
            self.couter_btn_control+=1
            pass

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga")
        elif new_map == "Wikimedia Cloud Services":
            self.map_widget.set_tile_server("https://tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png")  # detailed hiking
        elif new_map == "Default":
            self.map_widget.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")

    def get_stats(self):
        return ['00', '00', '00']
        '''try:
            pass
        except:
            return ['00', '00', '00']'''
        
    def connect_to_drone(self):
        if self.counter_conn_btn % 2 != 0: ## enable button
            self.conn_btn.configure(fg_color='green')
            self.counter_conn_btn+=1
            pass
        else:                                 ## disable button
            self.conn_btn.configure(fg_color='red')
            self.counter_conn_btn+=1
            pass

    def change_USB_port(self, port:str):
        pass

    def scan_USB_ports(self):
        pass # return ['COM1','COM2',...]

    def show_info(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
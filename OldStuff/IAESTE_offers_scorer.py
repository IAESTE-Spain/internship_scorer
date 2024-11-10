import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import LiteralString
import customtkinter
from PIL import Image
from tkinter import filedialog as fd
import os
import sys
import scorer_backend as backend

global info


class InformationSaver:
    def __init__(self):
        self.offers_id_all: list[str] = []
        self.actual_offer_id: str = ""
        self.actual_offer_row: list[str] = []
        self.file_csv: str = ""
        self.offers_id_bid: list[str] = []
        self.progress_bar_value: int = 0
        self.single_step: int = 0

        self.buttons: any = []
        self.index_selected_value: int = -1
        self.selected_value: str = ""


if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


def start_global():
    global info
    info = InformationSaver()


def change_appearance_mode_event(new_appearance_mode: str) -> None:
    customtkinter.set_appearance_mode(new_appearance_mode)


def setting_name_of_file() -> None:
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )

    info.file_csv = filename


def error_csv() -> None:
    messagebox.showerror("", "Tienes que elegir un documento!")


def start_bid() -> None:
    global info
    if info.file_csv == "":
        error_csv()
        return

    backend.initializer_file(info.file_csv)
    info.offers_id_all = backend.get_all_offers_id()
    info.single_step = 1 / len(info.offers_id_all)
    info.actual_offer_id = info.offers_id_all[0]
    info.actual_offer_row = backend.get_offer_info(info.actual_offer_id)
    fill_initial_components_values(info.actual_offer_row)


def fill_initial_components_values(row) -> None:
    titleTextBox.configure(text="Oferta: " + row['Ref.No'])
    textbox.configure(state="normal")
    textbox.delete("0.0", tk.END)

    if row['OtherRequirements'] != "":
        textbox.insert("0.0", row['OtherRequirements'])
    else:
        textbox.insert("0.0", "No requeriments")

    checkIsSecond.set(False)
    textbox.configure(state="disable")
    start_offer_buttons()
    button_next_offer.configure(state="active", fg_color="#1f538d")


def start_offer_buttons() -> None:
    for button_option in info.buttons:
        button_option.configure(state="active", fg_color='#1f538d')
    info.selected_value = None


def save_offer() -> None:
    for button_option in info.buttons:
        button_option.configure(state="disabled", fg_color="#1f538d")
    button_next_offer.configure(state="disabled", fg_color="#1f538d")
    save_bid()
    if len(info.offers_id_all) - 1 == info.offers_id_all.index(info.actual_offer_id):
        offersTable.insert(parent='', index=tk.END, values=info.actual_offer_id)
        info.progress_bar_value += info.single_step
        progress.set(info.progress_bar_value)
        finish_program()
    else:
        change_to_next_offer()
        info.actual_offer_row = backend.get_offer_info(info.actual_offer_id)
        fill_initial_components_values(info.actual_offer_row)
        start_offer_buttons()
        button_next_offer.configure(state="active", fg_color="#1f538d")


def update_selected_country(index, new_value) -> None:
    # Disable the selected button and enable others
    for index, button_option in enumerate(info.buttons):
        if index == index:
            button_option.configure(state="disabled", fg_color="yellow")
        else:
            button_option.configure(state="active", fg_color='#1f538d')
    # Update the corresponding variable
    info.selected_value = new_value
    info.index_selected_value = index


def change_to_next_offer() -> None:
    index_offer = info.offers_id_all.index(info.actual_offer_id)
    if info.actual_offer_id in info.offers_id_bid:
        info.actual_offer_id = info.offers_id_all[len(info.offers_id_bid)]
        return

    offersTable.insert(parent='', index=tk.END, values=info.actual_offer_id)
    info.offers_id_bid.append(info.actual_offer_id)
    info.actual_offer_id = info.offers_id_all[index_offer + 1]
    info.progress_bar_value += info.single_step
    progress.set(info.progress_bar_value)


def save_bid() -> None:
    config_bid = [info.actual_offer_id, textbox.get("1.0", tk.END), checkIsSecond.get()]
    if info.selected_value == None or info.selected_value == "":
        info.selected_value = "Sin restricción"
        info.index_selected_value = 5
    config_bid.append(info.index_selected_value)
    config_bid.append(info.selected_value)
    backend.save_bid_parameters(info.actual_offer_id, config_bid)


def fill_components_of_saved_bid(components_parameters: any) -> None:
    titleTextBox.configure(text="Oferta: " + components_parameters[0])
    info.actual_offer_id = components_parameters[0]
    textbox.configure(state="normal")
    textbox.delete("0.0", tk.END)

    textbox.insert("0.0", components_parameters[1])

    checkIsSecond.set(components_parameters[2])

    textbox.configure(state="disable")
    update_selected_country(components_parameters[3], components_parameters[4])
    info.selected_value = components_parameters[4]
    info.index_selected_value = components_parameters[3]

    button_next_offer.configure(state="active", fg_color="#1f538d")


def on_treeview_click(event: any) -> None:
    # error puedo seleccionar titulo
    item = offersTable.selection()[0]
    value = offersTable.item(item, 'values')[0]

    config_offer = backend.get_bid_parameters(value)
    fill_components_of_saved_bid(config_offer)


def finish_scores():
    messagebox.showinfo("", "Se han puntuado todas las ofertas!")
    window.destroy()
    print("finish----------")


def finish_program():
    # bk .startCheckingRules()
    print("program finish")
    finish_scores()
    pass


def resource_path(relative_path) -> LiteralString | str | bytes:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)


start_global()

# Data
maxOffers = 100

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# main window
window = customtkinter.CTk()
window.title('Puntuador IAESTE')
window.geometry(f"{1100}x{580}")

offersSelected = customtkinter.DoubleVar(value=1 / 100)

checkIsSecond = customtkinter.BooleanVar()

# Left frame
lFrame = customtkinter.CTkFrame(window, width=249, height=580, corner_radius=1)
lFrame.pack_propagate(False)
lFrame.pack(side="left")

IAESTELogo = customtkinter.CTkImage(light_image=Image.open(resource_path("assets/IAESTE_black_logo.png")),
                                    dark_image=Image.open(resource_path("assets/IAESTE_blue_logo.png")),
                                    size=(173, 200))

logoButton = customtkinter.CTkButton(lFrame, image=IAESTELogo, text="", fg_color="transparent", hover=False)
logoButton.pack_propagate(False)
logoButton.pack(side="top", pady=(10, 50))

button_csv_finder = customtkinter.CTkButton(lFrame, text="Select file...", fg_color="transparent", border_width=2,
                                            text_color=("gray10", "#DCE4EE"), command=setting_name_of_file)
button_csv_finder.pack(side="top")

button_start_offers = customtkinter.CTkButton(lFrame, text="Start", fg_color="transparent", border_width=2,
                                              text_color=("gray10", "#DCE4EE"), command=start_bid)
button_start_offers.pack(side="top")

appearance_mode_optionemenu = customtkinter.CTkOptionMenu(lFrame, values=["Light", "Dark"],
                                                          command=change_appearance_mode_event)
appearance_mode_optionemenu.set("Dark")
appearance_mode_optionemenu.pack(side="bottom", anchor='s', pady=(0, 10))

appearance_mode_label = customtkinter.CTkLabel(lFrame, text="Appearance Mode:")
appearance_mode_label.pack(side="bottom", anchor='s')

# Midle frame
mFrame = customtkinter.CTkFrame(window, width=531, height=580, corner_radius=1)
mFrame.pack_propagate(False)
mFrame.pack(side="left")

titleTextBox = customtkinter.CTkLabel(mFrame, text="Oferta: ", font=('Calibri bold', 24))
titleTextBox.pack(side="top", anchor='w', pady=(15, 0), padx=(10, 0))

second_frame = customtkinter.CTkFrame(mFrame, fg_color="transparent")
second_frame.pack(side="top", anchor='w', pady=(15, 15), padx=(10, 0))
is_second_offer = customtkinter.CTkLabel(second_frame, text="Segundo plazo: ", justify="left")
is_second_offer.pack(side="left", padx=(0, 20))

check_second_offer = customtkinter.CTkCheckBox(second_frame, text="", variable=checkIsSecond)
check_second_offer.pack(side="left")

information_frame = customtkinter.CTkFrame(mFrame, fg_color="transparent")
information_frame.pack(side="top")

textbox = customtkinter.CTkTextbox(information_frame, width=495)
textbox.pack(side="top", pady=(0, 20))

option_chooser = customtkinter.CTkFrame(mFrame)
option_chooser.pack(side="top")
option_chooser.grid_columnconfigure(5, weight=1)
option_chooser.grid_rowconfigure(2, weight=1)

for i, label in enumerate(
        ["Un solo pais", "Union Europea/Schengen/Otan", "Latinoamérica", "Otro grupo de paises", "Sin restricción"]):
    button = customtkinter.CTkButton(option_chooser, text=label,
                                     command=lambda label=label, i=i: update_selected_country(i, label),
                                     state="disabled")
    button.grid(row=i // 3, column=i % 3, padx=(20, 10), pady=(10, 10), sticky="ew")
    info.buttons.append(button)

finish_bid_selector = customtkinter.CTkFrame(mFrame)
finish_bid_selector.pack(side="bottom", pady=(0, 50))
button_next_offer = customtkinter.CTkButton(finish_bid_selector, text="Siguiente oferta", command=save_offer,
                                            state="disabled")
button_next_offer.pack(side="bottom", padx=(20, 20), pady=(10, 10))

# Right frame
rFrame = customtkinter.CTkFrame(window, width=320, height=580, corner_radius=1)
rFrame.pack_propagate(False)
rFrame.pack(side="left")

# Visaulizador todas las ofertas
tableFrame = customtkinter.CTkFrame(rFrame, width=263, height=476, corner_radius=1)
tableFrame.pack_propagate(False)
tableFrame.pack(pady=(20, 0))

offersTable = ttk.Treeview(tableFrame, columns=('Name'), show='headings')
offersTable.heading('Name', text='Name of offer')
offersTable.pack(fill='both', expand=True)
offersTable.bind('<ButtonRelease-1>', on_treeview_click)

for i in info.offers_id_bid:
    name = i
    offersTable.insert(parent='', index=tk.END, values=name)

# Slider para ver el progreso
progress = customtkinter.CTkProgressBar(rFrame, width=263, variable=offersSelected)
progress.pack(pady=(30, 0))

# Fin actualizacion
window.mainloop()

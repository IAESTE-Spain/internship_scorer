import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import customtkinter
from PIL import Image
from tkinter import filedialog as fd
import backend as bk
import os
import sys

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


# Data
offersIDAll = []
actualOfferID = ""
actualRowOffer = []
fileCSV = ""
offersIDBid = []

progressBarValue = 0
singleStep = 0

buttons = []
index_selected_value = -1
selected_value = None


def setting_name_of_file():
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )

    global fileCSV
    fileCSV = filename


def errorCSV():
    messagebox.showerror("", "Tienes que elegir un documento!")


def startBids():
    global fileCSV
    global actualOfferID
    global actualRowOffer
    global offersIDAll
    global singleStep
    if fileCSV == "":
        errorCSV()
        return
    fileNameSave = fileCSV.split("/")[-1].split(".")[0]
    bk.saveCSVName(fileNameSave)
    offersIDAll = bk.getOffersIds(fileCSV)
    singleStep = 1 / len(offersIDAll)
    actualOfferID = offersIDAll[0]
    actualRowOffer = bk.getOfferInfo(actualOfferID)
    fillComponentsInitial(actualRowOffer)


def fillComponentsInitial(row):
    titleTextBox.configure(text="Oferta: " + row['Ref.No'])
    textbox.configure(state="normal")
    textbox.delete("0.0", tk.END)

    if row['OtherRequirements'] != "":
        textbox.insert("0.0", row['OtherRequirements'])
    else:
        textbox.insert("0.0", "No requeriments")

    checkIsSecond.set(False)
    textbox.configure(state="disable")
    startOfferButtons()
    button_next_offer.configure(state="active", fg_color="#1f538d")


def saveOffer():
    global actualRowOffer
    global actualOfferID
    global offersIDAll
    global progressBarValue
    global singleStep

    for button in buttons:
        button.configure(state="disabled", fg_color="#1f538d")
    button_next_offer.configure(state="disabled", fg_color="#1f538d")
    saveBid()
    if len(offersIDAll) - 1 == offersIDAll.index(actualOfferID):
        offersTable.insert(parent='', index=tk.END, values=actualOfferID)
        progressBarValue += singleStep
        progress.set(progressBarValue)
        finishProgram()
    else:
        changeToNextOffer()
        actualRowOffer = bk.getOfferInfo(actualOfferID)
        fillComponentsInitial(actualRowOffer)
        startOfferButtons()
        button_next_offer.configure(state="active", fg_color="#1f538d")


def update_selected_country(index, new_value):
    global selected_value
    global index_selected_value
    # Disable the selected button and enable others
    for i, button in enumerate(buttons):
        if i == index:
            button.configure(state="disabled", fg_color="yellow")
        else:
            button.configure(state="active", fg_color='#1f538d')
    # Update the corresponding variable
    selected_value = new_value
    index_selected_value = index


def startOfferButtons():
    global selected_value
    for button in buttons:
        button.configure(state="active", fg_color='#1f538d')
    selected_value = None


def changeToNextOffer():
    global actualOfferID
    global offersIDAll
    global offersIDBid
    global progressBarValue
    global singleStep

    indexOffer = offersIDAll.index(actualOfferID)
    if actualOfferID in offersIDBid:
        actualOfferID = offersIDAll[len(offersIDBid)]
        return

    offersTable.insert(parent='', index=tk.END, values=actualOfferID)
    offersIDBid.append(actualOfferID)
    actualOfferID = offersIDAll[indexOffer + 1]
    progressBarValue += singleStep
    progress.set(progressBarValue)


def saveBid():
    global actualOfferID
    global selected_value
    global index_selected_value
    configBid = []
    configBid.append(actualOfferID)
    configBid.append(textbox.get("1.0", tk.END))
    configBid.append(checkIsSecond.get())
    if selected_value == None:
        selected_value = "Sin restricción"
        index_selected_value = 5
    configBid.append(index_selected_value)
    configBid.append(selected_value)
    bk.setOfferBidParameters(configBid)


def fillComponentsOfSavedBid(componentsParameters):
    global actualOfferID
    global selected_value
    global index_selected_value
    global actualOfferID
    global actualRowOffer

    titleTextBox.configure(text="Oferta: " + componentsParameters[0])
    actualOfferID = componentsParameters[0]
    textbox.configure(state="normal")
    textbox.delete("0.0", tk.END)

    textbox.insert("0.0", componentsParameters[1])

    checkIsSecond.set(componentsParameters[2])

    textbox.configure(state="disable")
    update_selected_country(componentsParameters[3], componentsParameters[4])
    selected_value = componentsParameters[4]
    index_selected_value = componentsParameters[3]

    button_next_offer.configure(state="active", fg_color="#1f538d")

    pass


def on_treeview_click(event):
    # error puedo seleccionar titulo
    item = offersTable.selection()[0]
    value = offersTable.item(item, 'values')[0]

    configOffer = bk.getOfferBidParameters(value)
    fillComponentsOfSavedBid(configOffer)


def finish_scores():
    messagebox.showinfo("", "Se han puntuado todas las ofertas!")
    window.destroy()
    print("finish----------")


def finishProgram():
    bk.startCheckingRules()
    print("program finish")
    finish_scores()
    pass


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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
                                              text_color=("gray10", "#DCE4EE"), command=startBids)
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
        ["Un solo pais", "Union Europea/Schengen", "Latinoamérica", "Otro grupo de paises", "Sin restricción"]):
    button = customtkinter.CTkButton(option_chooser, text=label,
                                     command=lambda label=label, i=i: update_selected_country(i, label),
                                     state="disabled")
    button.grid(row=i // 3, column=i % 3, padx=(20, 10), pady=(10, 10), sticky="ew")
    buttons.append(button)

finish_bid_selector = customtkinter.CTkFrame(mFrame)
finish_bid_selector.pack(side="bottom", pady=(0, 50))
button_next_offer = customtkinter.CTkButton(finish_bid_selector, text="Siguiente oferta", command=saveOffer,
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

for i in offersIDBid:
    name = offersIDBid[i]
    offersTable.insert(parent='', index=tk.END, values=name)

# Slider para ver el progreso
progress = customtkinter.CTkProgressBar(rFrame, width=263, variable=offersSelected)
progress.pack(pady=(30, 0))

# Fin actualizacion
window.mainloop()

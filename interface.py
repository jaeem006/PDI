fromTkinterimport*
fromtkFileDialogimportaskopenfilename
fromPILimportImageTk,Image
importutils
importfilters

original_PIL=None
original_CV2=None
panel2=None

defreload_filtered_img(w,filter_to_apply,extras):

fil=getattr(filters,filter_to_apply)
filtered_img=fil(original_img=original_CV2,extras=extras)
print'filtered_img:',filtered_img
print'original_CV2:',original_CV2
iffiltered_img.any():
filtered_img=cv2_to_PIL(filtered_img)
panel2.configure(image=filtered_img)
panel2.image=filtered_img
else:
print'nohaypic'

defload_image(w):
f=askopenfilename()
print'f:',f
original_img=utils.read_image(f)

globaloriginal_CV2
original_CV2=original_img

print'original_CV2:',original_CV2

original_img=cv2_to_PIL(original_img)

globaloriginal_PIL
original_PIL=original_img



panel=Label(w,image=original_img)
panel.pack(side="left")

defcv2_to_PIL(cv2_img):
ifcv2_img.any():
cv2_img=utils.swap_rgb(cv2_img)
cv2_img=Image.fromarray(cv2_img)
cv2_img=ImageTk.PhotoImage(cv2_img)
returncv2_img

defmain():

w=Tk()
w.title("filtros")
w.geometry("1280x720")
w.configure(background='gray')

globalpanel2
panel2=Label(w)
panel2.pack(side='right')

menu_bar=Menu(w)

file_menu=Menu(menu_bar,tearoff=0)
file_menu.add_command(label="Cargarimagen.",command=lambda:load_image(w))
file_menu.add_command(label="Guardarimagen.")
file_menu.add_command(label="Salir.",command=w.quit)

menu_bar.add_cascade(label="File",menu=file_menu)

filters_menu=Menu(menu_bar,tearoff=0)
filters_menu.add_command(label="Escaladegrises.",command=lambda:reload_filtered_img(w,"grey_scale",{}))
filters_menu.add_command(label="Brillo.",command=lambda:reload_filtered_img(w,"brightness",{"brightness":127}))
filters_menu.add_command(label="Rojo",command=lambda:reload_filtered_img(w,"one_channel",{'channel':'R'}))
filters_menu.add_command(label="Verde",command=lambda:reload_filtered_img(w,"one_channel",{'channel':'G'}))
filters_menu.add_command(label="Azul",command=lambda:reload_filtered_img(w,"one_channel",{'channel':'B'}))
filters_menu.add_command(label="Altocontraste",command=lambda:reload_filtered_img(w,"high_contrast",{'morsa':True}))
filters_menu.add_command(label="Altocontrastenomorsa",command=lambda:reload_filtered_img(w,"high_contrast",{}))
filters_menu.add_command(label="Inveso",command=lambda:reload_filtered_img(w,"inverse",{}))

menu_bar.add_cascade(label="Filtros",menu=filters_menu)

w.config(menu=menu_bar)

w.mainloop()


if__name__=='__main__':
main()
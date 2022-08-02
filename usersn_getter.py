import backend.common.register as com_register
import tkinter as tk
import tkinter.font as tk_font
    




def main():

    master = tk.Tk()
    master.title("User SN")
    master.geometry("590x110") #You want the size of the app to be 500x500
    master.resizable(0, 0) #Don't allow resizing in the x or y direction
    master.configure(background='#568695')
    master.iconbitmap('.\\img\\favicon.ico')
    msg=com_register.sha256encode(com_register.get_machineguid())
    #result.set(msg)
    fontStyle = tk_font.Font( family="Segoe UI", size=13)
    tk.Label(master, text="\nYour user SN is:", font=fontStyle,background='#568695',fg='white').grid(row=0, sticky=tk.W,padx=(10, 10))
    readOnlyText = tk.Text(master,height=2)
    readOnlyText.insert(1.0,msg)
    readOnlyText.configure(state='disabled')
    readOnlyText.grid(row=4, sticky=tk.W,padx=(10, 10))
    
        
    
    

    tk.mainloop()


if __name__ == '__main__':
    main()

   

    
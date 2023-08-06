"""
    Full name       : Minh Phuong BUI
    Email address   : phuong.buiminh00@gmail.com
    ENGINEERING MECHANICS major
    project         : "basic BMP"
"""

from tkinter import *
from tkinter import messagebox

class basic:
    """
    Use!!!: basic.exlbl()
    """

    @staticmethod
    def titleicon(root,title = 'B67',icon= ""):
        """type(icon) -> str"""
        root.title(title)
        root.iconbitmap(icon)

    @staticmethod
    def bgColorRoot(root,bgcolor='black',\
                    percent_bgcolor=1.0):
        """percent_bgcolor : 0 <= value <=1.0"""
        root.configure(background=bgcolor)
        if 0.1<= float(percent_bgcolor) <=1.0:
            root.attributes('-alpha',percent_bgcolor)
        else:root.attributes('-alpha',1)
    
    @staticmethod
    def lenWH(root,percent_screen=0.25):
        """return: tuple(screen_with,screen_height,root_width,root_height)"""
        sw,sh = root.winfo_screenwidth(),root.winfo_screenheight()
        rw,rh = int(sw*(float(percent_screen))),int(sh*(float(percent_screen)))
        return ('screen width: '+str(sw),'screen height: '\
            +str(sh),'root width: '+str(rw),'root height: '+str(rh))
    
    @staticmethod
    def centerScreen(root,percent_screen=0.25,full_screen=False,resizable=True):
        """return: tuple(info_Screen, Info_Root)"""
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        if full_screen == False :
            if 0.1 <= float(percent_screen) <=0.9 :
                rw = int(sw*(float(percent_screen)))
                rh = int(sh*(float(percent_screen)))
            else: rw,rh = int(sw*(float(0.25))),int(sh*(float(0.25)))
            wh_0 = int((sh-rh)/3)
            ww_0 = int((sw-rw)/2)
            root_size = str(rw)+'x'+str(rh)+'+'+str(ww_0)+'+'+str(wh_0)
            root.geometry(root_size)
        else:
            root.state("zoomed")
            rw,rh = sw,sh
        
        if int(resizable) == 1: root.resizable(width = True, height = True)
        else: root.resizable(width = False, height = False)
        return ('Screen->',(sw,sh),'Root->',(rw,rh))
    
    @staticmethod
    def frm(root,width=192,height=108,cursor='dot',\
        bd=0,highlightthicknes=0,background='#6495ED',\
        highlightcolor='red',highlightbackground='black',relief='flat'):
        """return: type(object, info_frame)"""
        return ((Frame(root,width=width,height=height, cursor= cursor,\
        relief=relief,bd=bd,highlightthickness= highlightthicknes,\
        background=background,highlightcolor=highlightcolor,\
        highlightbackground= highlightbackground)),(width,height))
    
    @staticmethod
    def lblfrm(root,width=192,height=108,cursor='dot',text="B67",\
        bd=1,highlightthicknes=1, background= '#00BFFF',font = ('Helvetica 5'),\
        highlightcolor= 'red', highlightbackground= '#FFD700', relief='ridge'):
        """return: type(object, info_LableFrame)"""
        return ((LabelFrame(root ,width=width,height=height,cursor=cursor,\
        relief=relief,bd=bd,text=text,font=font,background= background,\
        highlightthickness=highlightthicknes,highlightcolor=highlightcolor,\
        highlightbackground= highlightbackground)),\
        (width,height))
    
    @staticmethod
    def lbl(root,text='B67',\
        textvariable=False,fg='black',font=('Arial 10 bold'),justify='center',\
        padx = 1, pady = 1, underline = -1, bitmap= "",\
        background= '#00FF00',cursor='dot',bd=0,relief='ridge'):
        """
        if textvariable = Flase return: object\n
        if textvariable = True return: tuple(object,textvar)
        """
        if textvariable != True:
            return (Label(root,text=text,fg=fg,font=font,justify=justify,\
            padx=padx,pady=pady,underline=underline,bitmap=bitmap,\
            background=background,cursor=cursor,bd=bd,relief=relief))
        else:
            return (Label(root,textvariable=StringVar(),fg=fg,font=font,\
            justify=justify,padx=padx,pady=pady,underline=underline,\
            bitmap=bitmap,background=background,cursor=cursor,bd=bd,\
            relief=relief),StringVar())
    
    @staticmethod
    def btn(root,command='NONE',text='    ',font=('Arial 10 bold'),\
        fg="black",bg="#00BFFF",activebackground='#BDB76B',\
        activeforeground='#8B008B',highlightcolor='yellow',cursor='dot',\
        bd=1,justify='center',relief='raised',padx=1,pady=1,underline=-1):
        """return: type(object)"""
        return (Button(root,command=command,text=text,font=font,fg=fg,bg=bg,\
        activebackground=activebackground, activeforeground= activeforeground,\
        highlightcolor=highlightcolor,cursor=cursor,bd=bd,justify=justify,\
        relief=relief,padx=padx,pady=pady,underline=underline))

    @staticmethod
    def checkbtn(root,text='',font=('Arial 10 bold'),\
        fg="black",bg="#00BFFF",activebackground='#BDB76B',command='NONE',\
        activeforeground='#8B008B',highlightcolor='yellow',cursor='dot',\
        bd=1,justify='center',relief = 'raised',padx=1,pady=1,underline=-1):
        """return: type(object,intvar)"""
        intvar = IntVar()
        return ((Checkbutton(root,command=command,text=text,font=font,fg=fg,bg=bg,\
        activebackground=activebackground, activeforeground= activeforeground,\
        highlightcolor=highlightcolor,cursor=cursor,bd=bd,justify=justify,\
        relief=relief,variable=intvar,onvalue=1,offvalue=0,selectcolor='yellow',	
        disabledforeground='green',padx=padx,pady=pady,underline=underline)),intvar)

    @staticmethod
    def menubtn(root,text='    ',font=('Arial 10 bold'),\
        fg="#C0C0C0",bg="#2F4F4F",activebackground='#FFD700',direction='flush',\
        activeforeground='#FF4500',highlightcolor='yellow',cursor='dot',\
        bd=1,justify='center',relief='sunken',padx=1,pady=1,underline=-1):
        """return: type(object)"""
        return (Menubutton(root,text=text,font=font,fg=fg,bg=bg,\
        activebackground=activebackground, activeforeground= activeforeground,\
        highlightcolor=highlightcolor,cursor=cursor,bd=bd,justify=justify,\
        relief=relief,padx=padx,pady=pady,underline=underline,direction=direction))

    @staticmethod
    def menu(root,font=('Arial 10 bold'),fg="#C0C0C0",bg="#2F4F4F",\
        activebackground='#FFD700',activeforeground='#FF4500',cursor='dot',\
        bd=0,relief='sunken',tearoff=0):
        """return: type(object)"""
        return (Menu(root,font=font,fg=fg,bg=bg,tearoff=tearoff,\
        activebackground=activebackground, activeforeground= activeforeground,\
        cursor=cursor,bd=bd,relief=relief))

    @staticmethod
    def ent(root,text='',fg='black',font=('Arial 10 bold'),\
        justify='center',background='#00FF00',cursor='dot',bd=0,\
        show='',relief='ridge',highlightthicknes=0,highlightcolor='#8B008B',):
        """return: type(object)"""
        return (Entry(root,text=text,fg=fg,font=font,justify=justify,\
        background=background,cursor=cursor,bd=bd,relief=relief,show=show,
        highlightthicknes=highlightthicknes,highlightcolor=highlightcolor))

    @staticmethod
    def txt(root,bd=1,highlightthickness=1,cursor='dot',\
        font=('Arial 10'),padx=2,pady=2,wrap='word',relief='sunken',\
        background='#E6E6FA',fg='#080808',highlightcolor='#5F8575',\
        selectbackground='#0F52BA',insertbackground='black',
        selectborderwidth=0,width=50,height=5):
        """return: type(object)"""
        return (Text(root,bd=bd,cursor=cursor,font=font,background=background,\
            fg=fg,padx=padx,pady=pady,highlightcolor=highlightcolor,\
            highlightthickness=highlightthickness,selectbackground =selectbackground,\
            insertbackground=insertbackground,wrap=wrap,relief=relief,\
            selectborderwidth=selectborderwidth,width=width,height=height))

    @staticmethod
    def frm(root,width=192,height=108,cursor='dot',\
        bd=12,highlightthicknes=7,background='#00BFFF',\
        highlightcolor='red',highlightbackground='#FFD700',relief='ridge'):
        """return: type(object,info_frame)"""
        return ((Frame(root ,width=width,height=height, cursor= cursor,\
        relief = relief, bd = bd,highlightthickness=highlightthicknes,\
        background=background,highlightcolor=highlightcolor,\
        highlightbackground= highlightbackground)), (width,height))

    @staticmethod
    def mesbox(root,title='',content='',error=False,warnig=False,\
        info=False,askquestion=False,askokcancel=False,askyesno=False,\
        askretrycancel=False):
        """return : tuple(object)"""
        if error == True:return(messagebox.showerror(title, content))
        if warnig == True:return(messagebox.showwarning(title,content))
        if info == True:return(messagebox.showinfo(title,content))
        if askquestion == True:return(messagebox.askquestion(title,content))
        if askokcancel == True:return(messagebox.askokcancel(title,content))
        if askyesno == True:return(messagebox.askyesno(title,content))
        if askretrycancel == True:return(messagebox.askretrycancel(title,content))

    @staticmethod
    def exlblfrm(root,width=192,height=108,cursor='dot',text="MINH PHUONG",\
        bd=12,highlightthicknes=7,background='#00BFFF',font=('Arial 10 bold'),\
        highlightcolor= 'red', highlightbackground= '#FFD700', relief='ridge'):
        """return: type(object,info_frame)"""
        return ((LabelFrame(root ,width=width,height=height, cursor= cursor,\
        relief = relief, bd = bd, text = text,font= font,\
        highlightthickness= highlightthicknes, background= background,\
        highlightcolor=highlightcolor, highlightbackground= highlightbackground)),\
        (width,height))

    @staticmethod
    def exlbl( root,text= 'We are always looking for\nthe best solution',\
        textvariable= False,fg = '#800000',font = ('Arial 11 bold'),\
        justify = 'center',padx = 1, pady = 1, underline = -1, bitmap= "",\
        background= '#00FF00',cursor='dot',bd=0,relief='ridge'):
        """
        if textvariable = Flase return: object\n
        if textvariable = True return: tuple(object,textvar)
        """
        if textvariable != True:
            return (Label(root,text=text,fg=fg,font=font,justify=justify,\
            padx=padx,pady=pady,underline=underline,bitmap=bitmap,\
            background=background,cursor=cursor,bd=bd,relief=relief))
        else:
            return (Label(root,textvariable=StringVar(),fg=fg,font=font,\
            justify=justify,padx=padx,pady=pady,underline=underline,\
            bitmap=bitmap,background=background,cursor=cursor,bd=bd,\
            relief=relief),StringVar())

    @staticmethod
    def m_dict():
        """return: tuple(relief,cursor)"""
        my_relief  = {1:'flat',2:'raised',3:'sunken',4:'groove',5:'ridge'}
        my_cursor = {1:"arrow",2:"circle",3:"clock",4:"cross",5:"dotbox",\
        6:"exchange",7:"fleur",8:"heart",9:"heart",10:"man",11:"mouse",\
        12:"pirate",13:"plus",14:"shuttle",15:"sizing",16:"spider",\
        17:"spraycan",18:"star",19:"target",20:"tcross",21:"trek",22:"watch"}
        return ('relief:->',my_relief,'cursor:->',my_cursor)

def main(): pass
if __name__ == '__main__': main()
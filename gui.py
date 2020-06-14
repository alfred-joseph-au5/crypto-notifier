import sys
import os
import time
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import currency as currency
import variables
import src.defaults as defaults
import src.config as config
import src.pinger as pinger

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global w, root
    root = tk.Tk()
    root.iconbitmap(os.path.join(sys.path[0], 'cryptonotifier.ico'))
    variables.set_Tk_var()
    top = MainWindow (root)
    variables.init(root, top)
    root.mainloop()

w = None
def create_MainWindow(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_MainWindow(root, *args, **kwargs)' .'''
    global w, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    variables.set_Tk_var()
    top = MainWindow (w)
    variables.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_MainWindow():
    global w
    w.destroy()
    w = None

class MainWindow:
    
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.timetraveler = 0
        self.count = 0
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',bg=_bgcolor)
        self.style.configure('.',fg=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',bg=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("579x450+423+86")
        top.minsize(176, 10)
        top.maxsize(2812, 883)
        top.resizable(0, 0)
        top.title("Crypto Currency Notifier")
        top.configure(bg="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.frame_main = tk.Frame(top)
        self.frame_main.place(relx=0.0, rely=0.0, relheight=1.011
                , relwidth=1.009)
        self.frame_main.configure(relief='groove')
        self.frame_main.configure(borderwidth="2")
        self.frame_main.configure(relief="groove")
        self.frame_main.configure(bg="#d9d9d9")
        self.frame_main.configure(highlightbackground="#d9d9d9")
        self.frame_main.configure(highlightcolor="black")

        self.frame_content = tk.Frame(self.frame_main)
        self.frame_content.place(relx=0.033, rely=0.044, relheight=0.187
                , relwidth=0.921)
        self.frame_content.configure(relief='groove')
        self.frame_content.configure(borderwidth="2")
        self.frame_content.configure(relief="groove")
        self.frame_content.configure(bg="#d9d9d9")
        self.frame_content.configure(highlightbackground="#d9d9d9")
        self.frame_content.configure(highlightcolor="black")

        self.btn_run = tk.Button(self.frame_content)
        self.btn_run.place(relx=0.613, rely=0.353, height=24, width=77)
        self.btn_run.configure(activebackground="#ececec")
        self.btn_run.configure(activeforeground="#000000")
        self.btn_run.configure(bg="#d9d9d9")
        self.btn_run.configure(disabledforeground="#a3a3a3")
        self.btn_run.configure(fg="#000000")
        self.btn_run.configure(highlightbackground="#d9d9d9")
        self.btn_run.configure(highlightcolor="black")
        self.btn_run.configure(pady="0")
        self.btn_run.configure(text='''Run''')
        self.btn_run.configure(state='normal')
        self.btn_run.configure(command=self.startservice)

        self.btn_stop = tk.Button(self.frame_content)
        self.btn_stop.place(relx=0.799, rely=0.353, height=24, width=77)
        self.btn_stop.configure(activebackground="#ececec")
        self.btn_stop.configure(activeforeground="#000000")
        self.btn_stop.configure(bg="#d9d9d9")
        self.btn_stop.configure(disabledforeground="#a3a3a3")
        self.btn_stop.configure(fg="#000000")
        self.btn_stop.configure(highlightbackground="#d9d9d9")
        self.btn_stop.configure(highlightcolor="black")
        self.btn_stop.configure(pady="0")
        self.btn_stop.configure(text='''Stop''')
        self.btn_stop.configure(state='disabled')
        self.btn_stop.configure(command=self.stopservice)

        self.frame_display = tk.Frame(self.frame_main)
        self.frame_display.place(relx=0.067, rely=0.088, relheight=0.099
                , relwidth=0.488)
        self.frame_display.configure(relief='groove')
        self.frame_display.configure(borderwidth="2")
        self.frame_display.configure(relief="groove")
        self.frame_display.configure(bg="#d9d9d9")
        self.frame_display.configure(highlightbackground="#d9d9d9")
        self.frame_display.configure(highlightcolor="black")

        self.l_coin_price = tk.Label(self.frame_main)
        self.l_coin_price.place(relx=0.182, rely=0.101, height=32, width=129)
        self.l_coin_price.configure(activebackground="#f9f9f9")
        self.l_coin_price.configure(activeforeground="black")
        self.l_coin_price.configure(bg="#ffffff")
        self.l_coin_price.configure(disabledforeground="#a3a3a3")
        self.l_coin_price.configure(fg="#000000")
        self.l_coin_price.configure(highlightbackground="#d9d9d9")
        self.l_coin_price.configure(highlightcolor="black")
        self.l_coin_price.configure(relief="groove")
        self.l_coin_price.configure(text='''00.00''')

        self.dd_currency = ttk.Combobox(self.frame_main)
        self.dd_currency.place(relx=0.082, rely=0.101, relheight=0.07
                , relwidth=0.089)
        self.dd_currency.configure(textvariable=variables.dd_currency)
        self.dd_currency.configure(takefocus="")
        self.dd_currency.configure(cursor="hand2")
        self.dd_currency.configure(values=variables.currency_opt)
        self.dd_currency.set(defaults.CURRENCY)

        self.dd_coin = ttk.Combobox(self.frame_main)
        self.dd_coin.place(relx=0.418, rely=0.101, relheight=0.068
                , relwidth=0.12)
        self.dd_coin.configure(textvariable=variables.dd_coin)
        self.dd_coin.configure(takefocus="")
        self.dd_coin.configure(cursor="hand2")
        self.dd_coin.configure(values=variables.coin_opt)
        self.dd_coin.set(defaults.COIN)

        self.frame_advanced = tk.LabelFrame(self.frame_main)
        self.frame_advanced.place(relx=0.033, rely=0.242, relheight=0.714
                , relwidth=0.921)
        self.frame_advanced.configure(relief='groove')
        self.frame_advanced.configure(borderwidth="2")
        self.frame_advanced.configure(relief="groove")
        self.frame_advanced.configure(bg="#d9d9d9")
        self.frame_advanced.configure(highlightbackground="#d9d9d9")
        self.frame_advanced.configure(highlightcolor="black")
        self.frame_advanced.configure(text=' Advanced ')

        self.frame_options = tk.LabelFrame(self.frame_advanced)
        self.frame_options.place(relx=0.037, rely=0.020, relheight=0.631
                , relwidth=0.92)
        self.frame_options.configure(relief='groove')
        self.frame_options.configure(borderwidth="2")
        self.frame_options.configure(relief="groove")
        self.frame_options.configure(bg="#d9d9d9")
        self.frame_options.configure(highlightbackground="#d9d9d9")
        self.frame_options.configure(highlightcolor="black")
        self.frame_options.configure(text=' Options ')

        self.frame_options1 = tk.LabelFrame(self.frame_options)
        self.frame_options1.place(relx=0.02, rely=0.068, relheight=0.854
                , relwidth=0.475)
        self.frame_options1.configure(relief='groove')
        self.frame_options1.configure(borderwidth="2")
        self.frame_options1.configure(relief="groove")
        self.frame_options1.configure(bg="#d9d9d9")
        self.frame_options1.configure(highlightbackground="#d9d9d9")
        self.frame_options1.configure(highlightcolor="black")
        self.frame_options1.configure(text=' Notify ')

        self.cb_limit = tk.Checkbutton(self.frame_options1)
        self.cb_limit.place(relx=0.043, rely=0.114, relheight=0.143
                , relwidth=0.234)
        self.cb_limit.configure(activebackground="#ececec")
        self.cb_limit.configure(activeforeground="#000000")
        self.cb_limit.configure(bg="#d9d9d9")
        self.cb_limit.configure(disabledforeground="#a3a3a3")
        self.cb_limit.configure(fg="#000000")
        self.cb_limit.configure(highlightbackground="#d9d9d9")
        self.cb_limit.configure(highlightcolor="black")
        self.cb_limit.configure(justify='left')
        self.cb_limit.configure(text='''Limit''')
        self.cb_limit.configure(variable=variables.var_cb_limit)
        self.cb_limit.configure(command=lambda : self.freezeentries(variables.var_cb_limit, self.e_limit))

        self.e_limit = tk.Entry(self.frame_options1)
        self.e_limit.place(relx=0.306, rely=0.12,height=20, relwidth=0.443)
        self.e_limit.configure(bg="white")
        self.e_limit.configure(disabledforeground="#a3a3a3")
        self.e_limit.configure(font="TkFixedFont")
        self.e_limit.configure(fg="#000000")
        self.e_limit.configure(highlightbackground="#d9d9d9")
        self.e_limit.configure(highlightcolor="black")
        self.e_limit.configure(insertbackground="black")
        self.e_limit.configure(selectbackground="#c4c4c4")
        self.e_limit.configure(selectforeground="black")
        # self.e_limit.configure(type=float)
        self.e_limit.configure(state="disabled")

        self.cb_notify_interval = tk.Checkbutton(self.frame_options1)
        self.cb_notify_interval.place(relx=0.043, rely=0.343, relheight=0.143
                , relwidth=0.387)
        self.cb_notify_interval.configure(activebackground="#ececec")
        self.cb_notify_interval.configure(activeforeground="#000000")
        self.cb_notify_interval.configure(bg="#d9d9d9")
        self.cb_notify_interval.configure(disabledforeground="#a3a3a3")
        self.cb_notify_interval.configure(fg="#000000")
        self.cb_notify_interval.configure(highlightbackground="#d9d9d9")
        self.cb_notify_interval.configure(highlightcolor="black")
        self.cb_notify_interval.configure(justify='left')
        self.cb_notify_interval.configure(text='''Notify every''')
        self.cb_notify_interval.configure(variable=variables.var_cb_notify)
        self.cb_notify_interval.configure(command=lambda : self.freezenotifiers(variables.var_cb_notify, False))

        self.e_notify_interval = tk.Entry(self.frame_options1)
        self.e_notify_interval.place(relx=0.438, rely=0.354, height=20
                , relwidth=0.23)
        self.e_notify_interval.configure(bg="white")
        self.e_notify_interval.configure(disabledforeground="#a3a3a3")
        self.e_notify_interval.configure(font="TkFixedFont")
        self.e_notify_interval.configure(fg="#000000")
        self.e_notify_interval.configure(highlightbackground="#d9d9d9")
        self.e_notify_interval.configure(highlightcolor="black")
        self.e_notify_interval.configure(insertbackground="black")
        self.e_notify_interval.configure(selectbackground="#c4c4c4")
        self.e_notify_interval.configure(selectforeground="black")
        self.e_notify_interval.configure(state='disabled')

        self.l_notify_interval = tk.Label(self.frame_options1)
        self.l_notify_interval.place(relx=0.681, rely=0.349, height=21, width=52)

        self.l_notify_interval.configure(activebackground="#f9f9f9")
        self.l_notify_interval.configure(activeforeground="black")
        self.l_notify_interval.configure(bg="#d9d9d9")
        self.l_notify_interval.configure(disabledforeground="#a3a3a3")
        self.l_notify_interval.configure(fg="#000000")
        self.l_notify_interval.configure(highlightbackground="#d9d9d9")
        self.l_notify_interval.configure(highlightcolor="black")
        self.l_notify_interval.configure(text='''minutes.''')

        self.frame_options2 = tk.LabelFrame(self.frame_options)
        self.frame_options2.place(relx=0.505, rely=0.068, relheight=0.854
                , relwidth=0.475)
        self.frame_options2.configure(relief='groove')
        self.frame_options2.configure(borderwidth="2")
        self.frame_options2.configure(relief="groove")
        self.frame_options2.configure(bg="#d9d9d9")
        self.frame_options2.configure(highlightbackground="#d9d9d9")
        self.frame_options2.configure(highlightcolor="black")
        self.frame_options2.configure(text=' Subscribe ')

        self.cb_twitter = tk.Checkbutton(self.frame_options2)
        self.cb_twitter.place(relx=0.064, rely=0.114, relheight=0.143
                , relwidth=0.302)
        self.cb_twitter.configure(activebackground="#ececec")
        self.cb_twitter.configure(activeforeground="#000000")
        self.cb_twitter.configure(bg="#d9d9d9")
        self.cb_twitter.configure(disabledforeground="#a3a3a3")
        self.cb_twitter.configure(fg="#000000")
        self.cb_twitter.configure(highlightbackground="#d9d9d9")
        self.cb_twitter.configure(highlightcolor="black")
        self.cb_twitter.configure(justify='left')
        self.cb_twitter.configure(state='disabled')
        self.cb_twitter.configure(text='''Twitter   ''')
        self.cb_twitter.configure(variable=variables.var_cb_twitter)
        self.cb_twitter.configure(command=lambda : self.freezeentries(variables.var_cb_twitter, self.e_twitter))

        self.cb_email = tk.Checkbutton(self.frame_options2)
        self.cb_email.place(relx=0.043, rely=0.343, relheight=0.143
                , relwidth=0.26)
        self.cb_email.configure(activebackground="#ececec")
        self.cb_email.configure(activeforeground="#000000")
        self.cb_email.configure(bg="#d9d9d9")
        self.cb_email.configure(disabledforeground="#a3a3a3")
        self.cb_email.configure(fg="#000000")
        self.cb_email.configure(highlightbackground="#d9d9d9")
        self.cb_email.configure(highlightcolor="black")
        self.cb_email.configure(justify='left')
        self.cb_email.configure(state='disabled')
        self.cb_email.configure(text='''Email''')
        self.cb_email.configure(variable=variables.var_cb_email)
        self.cb_email.configure(command=lambda : self.freezeentries(variables.var_cb_email, self.e_email))

        self.cb_text_msg = tk.Checkbutton(self.frame_options2)
        self.cb_text_msg.place(relx=0.043, rely=0.571, relheight=0.143
                , relwidth=0.43)
        self.cb_text_msg.configure(activebackground="#ececec")
        self.cb_text_msg.configure(activeforeground="#000000")
        self.cb_text_msg.configure(bg="#d9d9d9")
        self.cb_text_msg.configure(disabledforeground="#a3a3a3")
        self.cb_text_msg.configure(fg="#000000")
        self.cb_text_msg.configure(highlightbackground="#d9d9d9")
        self.cb_text_msg.configure(highlightcolor="black")
        self.cb_text_msg.configure(justify='left')
        self.cb_text_msg.configure(state='disabled')
        self.cb_text_msg.configure(text='''Text Message''')
        self.cb_text_msg.configure(variable=variables.var_cb_text_msg)
        self.cb_text_msg.configure(command=lambda : self.freezeentries(variables.var_cb_text_msg, self.e_text_msg))

        self.e_twitter = tk.Entry(self.frame_options2)
        self.e_twitter.place(relx=0.426, rely=0.126,height=20, relwidth=0.481)
        self.e_twitter.configure(bg="white")
        self.e_twitter.configure(disabledforeground="#a3a3a3")
        self.e_twitter.configure(font="TkFixedFont")
        self.e_twitter.configure(fg="#000000")
        self.e_twitter.configure(highlightbackground="#d9d9d9")
        self.e_twitter.configure(highlightcolor="black")
        self.e_twitter.configure(insertbackground="black")
        self.e_twitter.configure(selectbackground="#c4c4c4")
        self.e_twitter.configure(selectforeground="black")
        self.e_twitter.configure(state='disabled')

        self.e_email = tk.Entry(self.frame_options2)
        self.e_email.place(relx=0.332, rely=0.349,height=20, relwidth=0.57)
        self.e_email.configure(bg="white")
        self.e_email.configure(disabledforeground="#a3a3a3")
        self.e_email.configure(font="TkFixedFont")
        self.e_email.configure(fg="#000000")
        self.e_email.configure(highlightbackground="#d9d9d9")
        self.e_email.configure(highlightcolor="black")
        self.e_email.configure(insertbackground="black")
        self.e_email.configure(selectbackground="#c4c4c4")
        self.e_email.configure(selectforeground="black")
        self.e_email.configure(state='disabled')

        self.e_text_msg = tk.Entry(self.frame_options2)
        self.e_text_msg.place(relx=0.477, rely=0.571,height=20, relwidth=0.421)
        self.e_text_msg.configure(bg="white")
        self.e_text_msg.configure(disabledforeground="#a3a3a3")
        self.e_text_msg.configure(font="TkFixedFont")
        self.e_text_msg.configure(fg="#000000")
        self.e_text_msg.configure(highlightbackground="#d9d9d9")
        self.e_text_msg.configure(highlightcolor="black")
        self.e_text_msg.configure(insertbackground="black")
        self.e_text_msg.configure(selectbackground="#c4c4c4")
        self.e_text_msg.configure(selectforeground="black")
        self.e_text_msg.configure(state='disabled')

        self.frame_graph = tk.Frame(self.frame_advanced)
        self.frame_graph.place(relx=0.037, rely=0.708, relheight=0.262
                , relwidth=0.92)
        self.frame_graph.configure(relief='groove')
        self.frame_graph.configure(borderwidth="2")
        self.frame_graph.configure(relief="groove")
        self.frame_graph.configure(bg="#d9d9d9")

    def setupconfig(self):
        config.currency = variables.dd_currency.get()
        config.coin = (variables.dd_coin.get()).split()[0]
        valid = True

        if(variables.var_cb_limit.get() == 1):
            temp = self.e_limit.get().strip()
            if len(temp)>0:
                try:
                    temp = float(temp)
                    config.limit = temp
                except ValueError:
                    config.limit = defaults.LIMIT
                    valid = False
                    return valid
            else:
                config.limit = defaults.LIMIT
                variables.var_cb_limit.set(0)
        else:            
            config.limit = defaults.LIMIT

        if(variables.var_cb_notify.get() == 1):
            temp = self.e_notify_interval.get().strip()
            if len(temp)>0:
                try:
                    temp = int(temp)
                    config.notify = temp
                except ValueError:
                    config.notify = defaults.NOTIFY
                    valid = False
                    return valid
            else:
                config.notify = defaults.NOTIFY_CONSTANT
            
            if(variables.var_cb_twitter.get() == 1):
                temp = self.e_twitter.get().strip()
                if len(temp)>0:
                    try:
                        temp = str(temp)
                        config.twitter = temp
                    except ValueError:
                        config.twitter = defaults.TWITTER
                        valid = False
                        return valid
                else:
                    config.twitter = defaults.TWITTER
                    variables.var_cb_twitter.set(0)
            else:            
                config.twitter = defaults.TWITTER

            if(variables.var_cb_email.get() == 1):
                temp = self.e_email.get().strip()
                if len(temp)>0:
                    try:
                        temp = str(temp)
                        config.email = temp
                    except ValueError:
                        config.email = defaults.EMAIL
                        valid = False
                        return valid
                else:
                    config.email = defaults.EMAIL
                    variables.var_cb_email.set(0)
            else:            
                config.email = defaults.EMAIL

            if(variables.var_cb_text_msg.get() == 1):
                temp = self.e_text_msg.get().strip()
                if len(temp)>0:
                    try:
                        temp = int(temp)
                        config.sms = temp
                    except ValueError:
                        config.sms = defaults.SMS
                        valid = False
                        return valid
                else:
                    config.sms = defaults.SMS
                    variables.var_cb_text_msg.set(0)
            else:            
                config.sms = defaults.SMS
        else:
            config.notify = defaults.NOTIFY
            config.twitter = defaults.TWITTER
            config.email = defaults.EMAIL
            config.sms = defaults.SMS
        return valid

    def infinite_hack(self):
        if (self.btn_run['state'] == 'normal'):
            root.after_cancel(self.timetraveler)
            return
        response = pinger.fetch_new_price()
        if 'error' in response:
            #Show Error Message and stop the service
            print(response['error'])
            self.stopservice()
            return
        print(response)
        
        newRate = round(response['rate'], 2)
        if( float(self.l_coin_price['text']) > newRate):
            self.l_coin_price['bg'] = '#d50000'
        else:
            self.l_coin_price['bg'] = '#00c853'
            
        self.l_coin_price['fg'] = '#fff'
        self.l_coin_price['text'] = newRate
        
        selectCoin = variables.dd_coin.get()
        selectCoin = selectCoin.split(' - ', 1)[1]
        config.msg = 'Hey!\nThe Value of ' + selectCoin + ' is now ' + variables.dd_currency.get().strip() + ' ' + str(self.l_coin_price['text'])

        if(config.notify is not False):
            self.count += 15000
            if(config.limit is not False):
                if(newRate < config.limit):
                    pinger.send_notification()
                    self.count=0
            notifyAt = round(60000 * float(config.notify))
            if(self.count == notifyAt):
                pinger.send_notification()
                self.count = 0
        self.timetraveler = root.after(15000, self.infinite_hack) #15s
        return

    def startservice(self):
        if(self.setupconfig()):
            print('service started!')
            pinger.setup_connection()
            print(config.currency, config.coin, config.limit, config.notify, config.twitter, config.email, config.sms)
            self.freezeinputs(True)
            self.btn_run.config(state='disabled')
            self.btn_stop.config(state='normal')
            self.infinite_hack()
            
    def stopservice(self):
        print('service stopped!')
        self.freezeinputs(False)
        self.btn_stop.config(state='disabled')
        self.btn_run.config(state='normal')

    def freezeinputs(self, flag):
        state = 'disabled' if flag==True else 'normal'
        self.dd_currency.config(state=state)
        self.dd_coin.config(state=state)
        self.cb_limit.config(state=state)
        self.cb_notify_interval.config(state=state)
        self.e_limit.config(state='normal') if (variables.var_cb_limit.get() == 1 and not flag) else self.e_limit.config(state='disabled')
        self.freezenotifiers(variables.var_cb_notify, flag)

    def freezeentries(self, cb_state, entry):
        state = 'normal' if cb_state.get() == 1 else 'disabled'
        entry.config(state=state)
	
    def freezenotifiers(self, cb_state, flag):
        self.e_notify_interval.config(state='normal') if (variables.var_cb_notify.get() == 1 and not flag) else self.e_notify_interval.config(state='disabled')
        self.cb_twitter.config(state='normal') if (cb_state.get() == 1 and not flag) else self.cb_twitter.config(state='disabled')
        self.cb_email.config(state='normal') if (cb_state.get() == 1 and not flag) else self.cb_email.config(state='disabled')
        self.cb_text_msg.config(state='normal') if (cb_state.get() == 1 and not flag) else self.cb_text_msg.config(state='disabled')
        self.e_twitter.config(state='normal') if (cb_state.get() == 1 and variables.var_cb_twitter.get() == 1 and not flag) else self.e_twitter.config(state='disabled')
        self.e_email.config(state='normal') if (cb_state.get() == 1 and variables.var_cb_email.get() == 1 and not flag) else self.e_email.config(state='disabled')
        self.e_text_msg.config(state='normal') if (cb_state.get() == 1 and variables.var_cb_text_msg.get() == 1 and not flag) else self.e_text_msg.config(state='disabled')

if __name__ == '__main__':
    vp_start_gui()


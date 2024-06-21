"""
4D-STEM Viewer for FEMTUS 4DSTEM data set
Auther : Eiji Okunishi 
version : 1.0
Pyhton version : 3.10.0

Required Library : If you do not have these libraries installed, please install them
Pillow(PIL)--> image operation
tkinter-->GUI
matplotlib-->build graph
numpy --> calcuration
natsort --> file order control
os
glob --> file operation

"""

from PIL import Image
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import Tk, Checkbutton, BooleanVar, messagebox
import numpy as np
import os
import glob
import h5py
from tkinter import filedialog
from mpl_toolkits.axes_grid1 import make_axes_locatable
from tkinter import font
from natsort import natsorted

# load sequence for files
def loading_function():

    global tiff_4d_array
    folder_path = filedialog.askdirectory() # folder open
    print(f"Selected folder: {folder_path}")
    
    try:
        tiff_4d_array = load_tiff_files(folder_path)
        print(f"Loaded 4D array with shape: {tiff_4d_array.shape}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        
#Loading files :FEMTUS 4DSTEM data(multi tiff file) exchange to numpy list
#フォルダー内のマルチフレームTIFFファイルを4次元配列に変換する
def load_tiff_files(folder_path):
    
    #tiff_files = natsorted(glob.glob(os.path.join(folder_path, '*.tif' )))
    tiff_files = natsorted([file for file in glob.glob(os.path.join(folder_path, '*')) if file.endswith(('.tif', '.tiff'))])
    if not tiff_files:
        raise FileNotFoundError(f"No TIFF files found in folder: {folder_path}")

    with Image.open(tiff_files[0]) as img:
        frame_count = img.n_frames
        img.seek(0)
        frame_array = np.array(img)
        height, width = frame_array.shape

    file_count = len(tiff_files)
    tiff_4d_array = np.zeros((file_count, frame_count, height, width), dtype=frame_array.dtype)
    
    for f, tiff_file in enumerate(tiff_files):
        with Image.open(tiff_file) as img:
            for i in range(frame_count):
                
                img.seek(i)
                tiff_4d_array[f, i, :, :] = np.array(img)
       
    return tiff_4d_array

# file save function for hdf5
# hdf5形式でセーブします
def save_files_hdf5(): 

    #s_folder_path = r'C:\Users\emdevelopper2\Documents\okunishi_emdevelopper2\PyJEM_okunishi_emdevelopper2\Python_PyJEM関係\PyJEM_Script_okunishi_origin\PyJEM_okunishi_py38\FEMTUS_4D_data_access\SiAlON-FEMTUS_4D\output'
    s_folder_path = filedialog.asksaveasfilename(defaultextension=".h5",filetypes=[("HDF5 files", "*.h5")],title="Save HDF5 File")
    
    if s_folder_path:
        with h5py.File(s_folder_path, 'w') as hdf:
            hdf.create_dataset('dataset_1', data=tiff_4d_array)
        print(f"Data saved to {s_folder_path}")
    else:
        print("Save operation cancelled.")  

#file open function for hdf5
def open_file_hdf5():

    global tiff_4d_array,root,frame
    global sx , sy,sx_var,sy_var,var,dx_var,dy_var,ax1,ax2
    global canvas1,canvas2,fig1,fig2,log_scale_var
    global dx_entry,dy_entry,sx_entry,sy_entry
    global dx_slider,dy_slider,sx_slider,sy_slider
    global button2,button3,button4,button5
    global log_scale_checkbox
    global ini_dx,ini_dy,ini_sx,ini_sy
    

    open_file_path = filedialog.askopenfilename(filetypes=[("HDF5 files", "*.h5")],title="Open HDF5 File")
    
    # ファイルパスが選択された場合のみ読み込み
    if open_file_path:
        with h5py.File(open_file_path, 'r') as hdf:
            tiff_4d_array = hdf['dataset_1'][:]
        #print(f"Data loaded from {open_file_path}")
        #print(tiff_4d_array)
        #print(f"Loaded 4D array with shape: {tiff_4d_array.shape}")
        re_open2()
        
    else:
        print("Load operation cancelled.")
        
    return tiff_4d_array

# when open another data
# ほかのデータを呼ぶときの処理  
def re_open(): # for FEMTUS data
    global root
    
    root.destroy()
    main()
    create_gui()


def re_open2(): # for HDF5
    global root
    
    root.destroy()
    root = tk.Tk()
    root.title("FEMTUS 4D-STEM Viewer")
    root.geometry("1570x1000")
    
    ini_sy = int((tiff_4d_array.shape[0])/2)
    ini_sx = int((tiff_4d_array.shape[1]/2))

    ini_dy =int(((tiff_4d_array.shape[2]/2))-1)
    ini_dx = int(((tiff_4d_array.shape[3]/2))-1)
 
    create_gui()    
    
    
# display : STEM image from selected position of diffraction
# 4次元配列から指定されたインデックスのスライスをプロットする--> Scan image
def plot_scan_image(array, sx, sy, dx, dy):
    
    try:
        ax1.clear()
        scan_image = array[:, :, dy, dx]
        img_scan = ax1.imshow(scan_image, cmap='viridis', interpolation='none')
        ax1.set_title('Virtual STEM Image')
        ax1.xaxis.tick_top()
        draw_cross2(ax1, sx, sy)
        
        if hasattr(plot_scan_image, 'cbar') and plot_scan_image.cbar:
            try:
                plot_scan_image.cbar.remove()
            except AttributeError:
                pass  # カラーバーの削除に失敗しても処理を続行
         # カラーバーの軸を設定
        divider2 = make_axes_locatable(ax1)
        cax2 = divider2.append_axes("right", size="5%", pad=0.1 )
            
        # 新しいカラーバーを追加
        plot_scan_image.cbar = fig1.colorbar(img_scan, cax = cax2  )
        #plot_scan_image.cbar = fig1.colorbar(img_scan   )
        plot_scan_image.cbar.set_label('Intensity')  # カラーバーのラベルを設定
           
        canvas1.draw()

    except IndexError:
        messagebox.showerror("Error", "Invalid slice index")
    
plot_scan_image.cbar = None          

# display : Diffraction pattern from selected position of STEM image
# 4次元配列から指定されたインデックスのスライスをプロットし、指定された座標にマークを表示する
def plot_diffraction(array, sx, sy, dx, dy):
    
    try:
        ax2.clear()
        diffraction = array[sy, sx, :, :]
        #diffraction = np.log1p(diffraction) 
        if log_scale_var.get():
            diffraction = np.log1p(diffraction)  # 対数スケールに変換
            
        img_diff = ax2.imshow(diffraction, cmap='viridis', interpolation='none')
        ax2.set_title('Diffraction from Selected Region')
        ax2.xaxis.tick_top()
        draw_cross(ax2, dx, dy) 
        
        if hasattr(plot_diffraction, 'cbar') and plot_diffraction.cbar:
            try:
                plot_diffraction.cbar.remove()
            except AttributeError:
                pass  # カラーバーの削除に失敗しても処理を続行
         # カラーバーの軸を設定
        divider = make_axes_locatable(ax2)
        cax = divider.append_axes("right", size="5%", pad=0.1)
            
        # 新しいカラーバーを追加
        plot_diffraction.cbar = fig2.colorbar(img_diff, cax = cax)
        plot_diffraction.cbar.set_label('Intensity')  # カラーバーのラベルを設定
   
        canvas2.draw()
        
    except IndexError:
        messagebox.showerror("Error", "Invalid slice index")
        
plot_diffraction.cbar = None        

# drawing marker on STEM image on scan image
# 指定された座標に十字マークを描く scan image上
def draw_cross(ax1, x, y, color='red'):

    ax1.plot([x - 2, x + 2], [y, y], color=color)
    ax1.plot([x, x], [y - 2, y + 2], color=color)

# drawing marker on Diff   
# 指定された座標に十字マークを描く Diffraction上 
def draw_cross2(ax2, x, y, color='red'):

    ax2.plot([x - 2, x + 2], [y, y], color=color)
    ax2.plot([x, x], [y - 2, y + 2], color=color)    

#display update
def update_plot(*args):
    global sx,sy,dx,dy
    sx = int(sx_var.get())
    sy = int(sy_var.get())
    dx = int(dx_var.get())
    dy = int(dy_var.get())
    plot_scan_image(tiff_4d_array, sx, sy, dx, dy)
    update_plot2()  # Update the diffraction plot as well with new dx, dy
    intensity2 = tiff_4d_array[sy,sx,dy,dx]
    var.set(f"intensity: {intensity2:.3f}")   


def update_plot2(*args):
    global sx,sy,dx,dy
    sx = int(sx_var.get())
    sy = int(sy_var.get())
    dx = int(dx_var.get())
    dy = int(dy_var.get())
    plot_diffraction(tiff_4d_array, sx, sy, dx, dy)
    draw_cross2(ax1, sx, sy)
    plot_scan_image(tiff_4d_array, sx, sy, dx, dy)
    intensity2 = tiff_4d_array[sy,sx,dy,dx]
    var.set(f"intensity: {intensity2:.3f}")  

# action of Slifer bar
# スライダーのアクション
def on_slider_change_dx(value):
    dx_var.set(int(float(value)))
    update_plot()
    
    
def on_slider_change_dy(value):
    dy_var.set(int(float(value)))
    update_plot()

def on_slider_change_sx(value):
    sx_var.set(int(float(value)))
    update_plot2()

def on_slider_change_sy(value):
    sy_var.set(int(float(value)))
    update_plot2()

# Mouse click function on STEM image
# Scan像上のマウスクリック"""canvas1(scan image)上でクリックされた位置に十字マークを描画し、その位置をsx, syに反映する"""
def on_canvas1_click(event):
    
    x2, y2 = int(event.xdata), int(event.ydata)
    sx_var.set(x2)
    sy_var.set(y2)
    update_plot()
    intensity2 = tiff_4d_array[sy,sx,dy,dx]
    var.set(f"intensity: {intensity2:.3f}")  
    
# Mouse click function on Diff
# 電子回折上のマウスクリック"""canvas2(Diffraction)上でクリックされた位置に十字マークを描画し、その位置をdx, dyに反映する"""
def on_canvas2_click(event):
    
    x, y = int(event.xdata), int(event.ydata)
    dx_var.set(x)
    dy_var.set(y)
    update_plot()
    intensity2 = tiff_4d_array[sy,sx,y,x]
    var.set(f"intensity: {intensity2:.3f}")  


    
def plot_ini_disp() :

    update_plot()   


        
#create new display with another folder      

        
def main():    
    
    global tiff_4d_array,root,frame
    global sx , sy,sx_var,sy_var,var,dx_var,dy_var,ax1,ax2,dx,dy
    global canvas1,canvas2,fig1,fig2,log_scale_var
    global dx_entry,dy_entry,sx_entry,sy_entry
    global dx_slider,dy_slider,sx_slider,sy_slider
    global button2,button3,button4,button5
    global log_scale_checkbox,root
    global ini_dx,ini_dy,ini_sx,ini_sy
      
    
    root = tk.Tk()
    root.title("FEMTUS 4D-STEM Viewer")
    font2 = font.Font(family='helvetica', size=12)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x = screen_width / 2 - window_width /2
    y = screen_height / 2 - window_height / 2
    x1 = 300
    y1 = 100
    root.geometry("+%d+%d" % (x1, y1))
    root.geometry("340x250")
    label_open_file = tk.Label(root, text="--Select your FEMTUS 4DSTEM data folder--", font=font2)
    label_open_file.place(x=10, y=10)
    
    loading_function() 
    
    root.geometry("1570x1080")
   
    ini_sy = int((tiff_4d_array.shape[0])/2)
    ini_sx = int((tiff_4d_array.shape[1]/2))

    ini_dy =int(((tiff_4d_array.shape[2]/2))-1)
    ini_dx = int(((tiff_4d_array.shape[3]/2))-1)

    
def main2():    

    global tiff_4d_array,root,frame
    global sx , sy,sx_var,sy_var,var,dx_var,dy_var,ax1,ax2,dx,dy
    global canvas1,canvas2,fig1,fig2,log_scale_var
    global dx_entry,dy_entry,sx_entry,sy_entry
    global dx_slider,dy_slider,sx_slider,sy_slider
    global button2,button3,button4,button5
    global log_scale_checkbox,root
    global ini_dx,ini_dy,ini_sx,ini_sy
    
    shape = (32,32,32,32)
    tiff_4d_array =np.zeros(shape)

    root = tk.Tk()
    root.title("FEMTUS 4D-STEM Viewer")
    font2 = font.Font(family='helvetica', size=12)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x = screen_width / 2 - window_width /2
    y = screen_height / 2 - window_height / 2
    x1 = 300
    y1 = 100
    root.geometry("+%d+%d" % (x1, y1))
    root.geometry("340x250")
    label_open_file = tk.Label(root, text="--Select your FEMTUS 4DSTEM data folder--", font=font2)
    label_open_file.place(x=10, y=10)
    
    #loading_function()
    
    root.geometry("1570x1050")
       
    ini_sy = int((tiff_4d_array.shape[0])/2)
    ini_sx = int((tiff_4d_array.shape[1]/2))

    ini_dy =int(((tiff_4d_array.shape[2]/2))-1)
    ini_dx = int(((tiff_4d_array.shape[3]/2))-1)


    
    
#create_gui()       
def create_gui():
    
    
    global tiff_4d_array,root,frame
    global sx , sy,sx_var,sy_var,var,dx_var,dy_var,ax1,ax2
    global canvas1,canvas2,fig1,fig2,log_scale_var
    global dx_slider,dy_slider,sx_slider,sy_slider
    global button3,button4
    global log_scale_checkbox
    global ini_dx,ini_dy,ini_sx,ini_sy
    
    # create menu bar
    # メニューバーの作成
    font_menu = ("Helvetica", 12)
    menubar=tk.Menu()    #メニューバーの生成
    root.config(menu=menubar)    #メニューバーをウィンドウに設置

    filemenu=tk.Menu(menubar)   #menubarを引数にして [ファイル] メニューを作成
    menubar.add_cascade(label="File",menu=filemenu)    # [ファイル] タブの設置

    #ファイルメニューに表示させるコマンドの追加
    filemenu.add_command(label="open data" , command=re_open , font=font_menu)
    filemenu.add_command(label="open HDF5" , command=open_file_hdf5 , font=font_menu)
    filemenu.add_command(label="save HDF5" , command=save_files_hdf5 , font=font_menu)
    #filemenu.add_command(label="閉じる")
    
    #GUI_position
    scan_axis_x = tiff_4d_array[1]
    scan_axis_y = tiff_4d_array[0]
    
    diff_axis_x = tiff_4d_array[3]
    diff_axis_y = tiff_4d_array[2]
    
    frame = tk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH)
    
    length1 = 300
    position_y = 100
    
    sx1 = 80
    sx2 = 810
    sy1 = position_y + 730
    sy2 = position_y + 730 + 90
    
    s_width = 680
    
    font_setting = ("Helvetica", 12)
    
    font2 = font.Font(family='helvetica', size=16)  
    font_CKB = font.Font(family='helvetica', size=12)  

    intensity2 = 0
    var = tk.StringVar()
    var.set(f"Intensity: {intensity2}")

    # 数値入力フィールドとスライダーの作成(Scan_image)
    dx_var = tk.IntVar(value=ini_dx)
    dy_var = tk.IntVar(value=ini_dy)

    dx_slider = tk.Scale(frame, from_=0, to=tiff_4d_array.shape[3]-1, orient=tk.HORIZONTAL, variable=dx_var, command=on_slider_change_dx, tickinterval=20 ,   font=font_setting, label="Position_Diff_X").place(x=sx2,y=sy1 , width=s_width)
    dy_slider = tk.Scale(frame, from_=0, to=tiff_4d_array.shape[2]-1, orient=tk.HORIZONTAL, variable=dy_var, command=on_slider_change_dy ,tickinterval=20, font=font_setting, label="Position_Diff_Y").place(x=sx2,y=sy2 , width=s_width)
    

    # 数値入力フィールドとスライダーの作成(Diffraction)
    sx_var = tk.IntVar(value=ini_sx)
    sy_var = tk.IntVar(value=ini_sy)

    sx_slider = tk.Scale(frame, from_=0, to=tiff_4d_array.shape[1]-1, orient=tk.HORIZONTAL, variable=sx_var, command=on_slider_change_sx ,tickinterval=25, font=font_setting, label="Position_Scan_X").place(x=sx1,y=sy1 , width=s_width)
    sy_slider = tk.Scale(frame, from_=0, to=tiff_4d_array.shape[0]-1, orient=tk.HORIZONTAL, variable=sy_var, command=on_slider_change_sy ,tickinterval=25, font=font_setting,label="Position_Scan_Y").place(x=sx1, y=sy2 , width=s_width)

    font_button = ("Helvetica", 12)

    button_pos_x = 0
    button=pos_y = 0
    button_width = 120
    button_height = 35
    button_bkg_color = "#f5fffa"
    
    button_plot_Scan_image = tk.Button(frame, text="Plot Scan Image" , relief="ridge", font=font_button , command=lambda: plot_scan_image(tiff_4d_array, sx_var.get(), sy_var.get(), dx_var.get(), dy_var.get())).place(x=70 ,y=55, width=button_width, height=button_height)
    button_plot_diff = tk.Button(frame, text="Plot Diffraction", relief="ridge", font=font_button ,  command=lambda: plot_diffraction(tiff_4d_array, sx_var.get(), sy_var.get(), dx_var.get(), dy_var.get())).place(x=800,y=55, width=button_width, height=button_height)

    # 対数スケールを切り替えるチェックボックスの状態を保持する変数
    log_scale_var = BooleanVar(value=False)

    # 対数スケール切り替え用のチェックボックスを作成
    log_scale_checkbox = Checkbutton(root, text="Log Scale", variable=log_scale_var, command=update_plot2 , font=font_CKB).place(x=1100, y=70)
    #log_scale_checkbox.pack()

   
    label_intensity= tk.Label(frame, textvariable=var , font=font2)
    label_intensity.place(x=1300, y=65)
    
    label_dimension = tk.Label(frame, text=(f"Data_dimension : Scan X:{tiff_4d_array.shape[1]}, Y:{tiff_4d_array.shape[0]}      Diffraction X:{tiff_4d_array.shape[3]}, Y:{tiff_4d_array.shape[2]}"), font=font2)
    label_dimension.place(x=500, y=25)

    fig1, ax1 = plt.subplots()
    ax1.xaxis.tick_top()
    canvas1 = FigureCanvasTkAgg(fig1, master=frame)
    #canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas1.get_tk_widget().place(x=70,y=position_y, width=700,height=700)

    fig2, ax2 = plt.subplots()
    ax2.xaxis.tick_top()
    canvas2 = FigureCanvasTkAgg(fig2, master=frame)
    #canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas2.get_tk_widget().place(x=800, y=position_y, width=700,height=700)
    #canvas2.get_tk_widget().place(x=20,y=30 , relwidth=1.0, relheight=1.0)

    # canvas2のクリックイベントにバインド
    canvas2.mpl_connect('button_press_event', on_canvas2_click)
    canvas1.mpl_connect('button_press_event', on_canvas1_click)
 
    root.mainloop()

    
if __name__ == '__main__':
    
    #open_window()  
    main() 
    create_gui() 
   
    
     
    

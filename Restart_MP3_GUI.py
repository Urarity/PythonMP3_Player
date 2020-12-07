import os
from tkinter import *
import pygame
from pygame import mixer
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import tkinter.messagebox
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
import time
import threading

index = 0

playlist = []

paused = FALSE


def music_charm():
    window = Tk()

    mixer.init()  # Initiate mixer

    # Colors for GUI
    green_color = "#5BB36A"
    pink_color = "#FFB7C5"

    # Window background
    image = Image.open("cherry_blossom.jpg")
    background_image = ImageTk.PhotoImage(image)

    background_label = Label(window, image=background_image, bg=pink_color)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # width_value = window.winfo_screenwidth()
    # height_value = window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (1000, 650))
    window.title("MusicCharm")  # Window title
    window.iconbitmap("music_player_icon.ico")  # Insert icon

    # Welcome sign
    welcome = Label(window, text='Welcome to MusicCharm', font=('Times New Roman', 20), bg=green_color, fg='black',
                    relief='raised')
    welcome.pack(padx=(50, 0), pady=(0, 90))

    # Photos for the buttons
    play_photo = PhotoImage(file="play.png")  # Play Button Picture
    stop_photo = PhotoImage(file="stop.png")  # Stop Button Picture
    pause_photo = PhotoImage(file="pause.png")  # Pause Button Picture
    rewind_photo = PhotoImage(file="rewind.png")  # Rewind Button Picture
    # mute_photo = PhotoImage(file="mute.png")  # Mute Button Picture

    # ********************************** Functions **********************************************

    # Function to add to the playlist
    def add_to_playlist_folder():
        directory = askdirectory()
        os.chdir(directory)
        for files in os.listdir(directory):
            if files.endswith(".mp3"):
                playlist.append(files)
                list_box.insert(0, files)

    def add_to_playlist_single(filename):
        global index
        global playlist
        global filename_path
        filename = os.path.basename(filename)
        list_box.insert(index, filename)
        playlist.insert(index, filename_path)
        index += 1

    # Function to delete songs from playlist
    def del_song():
        selected_song = list_box.curselection()
        selected_song = int(selected_song[0])
        list_box.delete(selected_song)
        playlist.pop(selected_song)

    # Function to play music / Restart music
    def next_music():
        try:
            global index
            index += 1
            pygame.mixer.music.load(playlist[index])
            pygame.mixer.music.play()
            status_bar['text'] = "Playing Music " + "" + os.path.basename(playlist[index])
        except IndexError:
            tkinter.messagebox.showerror("End of Playlist", "You have reached the end of the playlist")

    # Function to stop music
    def stop_music():
        mixer.music.stop()
        status_bar['text'] = "Stopped Music"

    # Function to play the previous song
    def previous_song():
        try:
            global index
            index -= 1
            pygame.mixer.music.load(playlist[index])
            pygame.mixer.music.play()
            status_bar['text'] = "Playing Music " + "" + os.path.basename(playlist[index])
        except IndexError:
            tkinter.messagebox.showinfo("End of Playlist", "You can't go any further back")

    def pause_music():
        global paused
        paused = TRUE
        mixer.music.pause()
        status_bar['text'] = "Music Paused"

    # Function to set volume
    def set_vol(val):
        volume = int(val) / 100
        mixer.music.set_volume(volume)  # Set volume of mixer takes value only from 0 to 1.
        # Example 0.0, 0.1, 0.55, 0.54, 0.99

    def play_music():
        global paused

        if paused:
            mixer.music.unpause()
            status_bar['text'] = "Music Resumed"
            paused = FALSE
        else:
            try:
                global play_it
                stop_music()
                selected_song = list_box.curselection()
                selected_song = int(selected_song[0])
                play_it = playlist[selected_song]
                mixer.music.load(play_it)
                mixer.music.play()
                status_bar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
                time_song()
            except:
                tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')

    # Function to look through file
    def browse_file(choice):
        if choice == "Folder":
            add_to_playlist_folder()
        elif choice == "Single":
            global filename_path
            filename_path = filedialog.askopenfilename()
            add_to_playlist_single(filename_path)
        # mixer.music.queue(filename_path)

    # Restart function
    def restart():
        window.destroy()
        music_charm()

    # About me
    def about_me():
        tkinter.messagebox.showinfo('MusicCharm ',
                                    """
        Creater: Patricia Rivera
        Created: 12/04/2019
        """)
        status_bar['text'] = "About the Program"

    def info():
        tkinter.messagebox.showinfo('How to use MusicCharm',
                                    """
        Add Folder: Add a music folder to playlist
        Add Single: Add a single music file to playlist
       -Del: Deletes a music file from playlist
        Play: Plays file you click from the playlist
        Note: If you don't click a file from the playlist you will get
        an error
        Rewind: Restarts the music you played
        Pause: Pauses the music you played
        Stop: Stops the music you played
        Mute: Mute music
        Next: Go to the next song
        Previous: Go to the previous song
        Clear List: Clears all the songs in the playlist
        """)

    # Rewind function
    def rewind_music():
        status_bar['text'] = "Music Rewinded"
        play_music()

    # Mute Function
    global muted
    muted = FALSE

    def mute_music():
        global muted
        global play_it

        if muted:  # Unmute the music
            mixer.music.set_volume(0.7)
            mute_btn.configure(text="Mute")
            scale.set(25)
            status_bar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            muted = FALSE
        else:  # mute the music
            mixer.music.set_volume(0)
            mute_btn.configure(text="Unmute")
            scale.set(0)
            status_bar['text'] = "Muted music" + ' - ' + os.path.basename(play_it)
            muted = TRUE

    def clear_listbox():
        list_box.delete(0, 'end')

    # MiddleFrame
    middle_frame = Frame(window, bg=green_color, relief='ridge')
    middle_frame.pack()

    # ********************************** Drop Down **********************************************

    string_var = StringVar(window)

    choices = {"Folder", "Single"}  # Dictionary with options
    string_var.set('+ How to add')  # set the default option

    variable = StringVar(window)
    variable.set("+ How to add")

    w = OptionMenu(middle_frame, variable, *choices, command=browse_file)
    w.config(bg=pink_color, fg='black', relief='raised')

    w.grid(row=2, column=0, padx=(0, 100), pady=(10, 25))

    # ********************************** Buttons **********************************************
    # image = play_photo
    # image = stop_photo
    # image = pause_photo
    # image = rewind_photo
    # image = mute_photo

    next_button = Button(middle_frame, text="Next", command=next_music, bg=pink_color, relief='raised')
    next_button.config(font=("Times New Roman", 10))  # Play Button
    next_button.grid(row=2, column=1)

    previous_button = Button(middle_frame, text="Previous", command=previous_song, bg=pink_color,
                             relief='raised')
    previous_button.config(font=("Times New Roman", 10))  # Previous Button
    previous_button.grid(row=2, column=2)

    play_btn = Button(middle_frame, image=play_photo, command=play_music, bg=pink_color, relief='raised')
    play_btn.grid(row=1, column=1)

    stop_btn = Button(middle_frame, image=stop_photo, command=stop_music, bg=pink_color, relief='raised')  # Stop Button
    stop_btn.grid(row=1, column=3, padx=(0, 105))

    pause_btn = Button(middle_frame, image=pause_photo, command=pause_music, bg=pink_color, relief='raised')  # Pause Button
    pause_btn.grid(row=1, column=2)

    rewind_btn = Button(middle_frame, image=rewind_photo, command=rewind_music, bg=pink_color, relief='raised')  # Restart Button
    rewind_btn.grid(row=1, column=3, padx=(60, 25))

    mute_btn = Button(middle_frame, text="Mute", command=mute_music, bg=pink_color, relief='raised')  # Mute Button
    mute_btn.grid(row=2, column=3)

    clear_box = Button(middle_frame, text="Clear list", command=clear_listbox, bg=pink_color, relief='raised')  # Clear listbox
    clear_box.grid(row=2, column=0, padx=(200, 0), pady=(10, 25))
    
    # add_btn = Button(middle_frame, text="+ Add", command=browse_file, bg=pink_color, relief='raised')  # Add Button
    # add_btn.grid(row=2, column=0, padx=(0, 83), pady=(10, 25))

    delete_btn = Button(middle_frame, text="-Del", command=del_song, bg=pink_color, relief='raised')  # Delete Button
    delete_btn.grid(row=2, column=0, padx=(85, 0), pady=(10, 25))

    # add_folder = Button(middle_frame, text="Add Folder", command=add_to_playlist, bg=pink_color,
    #                     relief='raised')  # add folder Button
    # add_folder.grid(row=2, column=0, padx=(0, 200), pady=(10, 25))

    # Lower and raise volume
    scale = Scale(window, from_=0, to=100, orient=HORIZONTAL, command=set_vol, bg=green_color, fg='black',
                  relief='raised')
    scale.config(font=("Times New Roman", 15))
    scale.set(25)
    mixer.music.set_volume(0.25)
    scale.pack(padx=(0, 0), pady=(25, 0))

    # ********************************** Menu **********************************************

    menu = Menu(window)
    window.config(menu=menu)

    sub_menu = Menu(menu)  # Sub menu not used but can be used
    menu.add_cascade(label="Information", menu=sub_menu)
    menu.add_command(label="Exit", command=window.destroy)
    menu.add_command(label="Restart", command=restart)
    sub_menu.add_command(label="Creator", command=about_me)
    sub_menu.add_command(label="Controls", command=info)
    # menu.add_command(label="Open", command=file_search)

    # ****************************** Status Bar **********************************************

    status_bar = Label(window, text="MusicCharm Home Page", relief=SUNKEN, anchor=W, bg=green_color)
    status_bar.pack(side=BOTTOM, fill=X)

    # ****************************** List Box **********************************************
    list_box = Listbox(middle_frame)  # List box

    # # Scroll Ball
    # scroll_bar = Scrollbar(window)
    # scroll_bar.pack(padx=(50, 125))
    #
    # # attach listbox to scrollbar
    # list_box.config(yscrollcommand=scroll_bar.set)
    # scroll_bar.config(command=list_box.yview)

    list_box.config(width=40, height=10, borderwidth=10, relief='raised', highlightthickness=0, background=pink_color)
    list_box.grid(row=1, column=0, padx=(25, 25), pady=(25, 0))

    # ****************************** Time **********************************************

    # MiddleFrame
    # top_frame = Frame(window)
    # top_frame.pack()

    time_label_song = Label(window, text="Total length: --:--", bg=green_color, fg='black', relief='raised')
    time_label_song.config(width=15, height=0, font=("Times New Roman", 15))
    time_label_song.pack(padx=(0, 0), pady=(25, 0))

    # playing_what = Label(window, text="Playing: ", bg=green_color, fg='black', relief='raised')
    # playing_what.pack(padx=(0, 0), pady=(25, 0))

    time_label_now = Label(window, text="Current length: --:--", bg=green_color, fg='black', relief='raised')
    time_label_now.config(width=15, height=0, font=("Times New Roman", 12))
    time_label_now.pack(padx=(0, 0), pady=(25, 0))

    # time function
    def time_song():
        global play_it, length
        # playing_what['text'] = "Playing:" + ' - ' + os.path.basename(play_it)

        data = os.path.splitext(play_it)
        print(data)

        # Goes through the data to check if file is .mp3 if so it continues else it will give you an error
        if data[1] == ".mp3":
            music = MP3(play_it)
            length = music.info.length

            minutes, seconds = divmod(length, 60)
            minutes = round(minutes)
            seconds = round(seconds)
            time_area = "{:02d}:{:02d}".format(minutes, seconds)
            time_label_song['text'] = "Total length" + ' - ' + time_area
        else:
            tkinter.messagebox.showinfo("Won't play", "The file you put in is not a mp3 file so it won't play."
                                                      "Please delete the file you put in and put in a mp3 file.")

        # Threading in python is used to run multiple threads (tasks, function calls) at the same time
        thread = threading.Thread(target=time_now, args=(length,))
        thread.start()

    def time_now(song_length):
        global paused

        # mixer.music.get_busy() returns false when the music stops so the timer doesn't continue
        while song_length and mixer.music.get_busy():
            if paused:
                continue
            else:
                minutes, seconds = divmod(song_length, 60)
                minutes = round(minutes)
                seconds = round(seconds)
                time_area = "{:02d}:{:02d}".format(minutes, seconds)
                time_label_now['text'] = "Current length" + ' - ' + time_area
                time.sleep(1)
                song_length -= 1  # You can also song_length += 1 to add seconds from 0 instead of from the start

    window.mainloop()


music_charm()

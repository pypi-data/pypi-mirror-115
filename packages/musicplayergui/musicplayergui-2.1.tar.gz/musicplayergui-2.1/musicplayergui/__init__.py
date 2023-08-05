def launch():
	global pauset
	pauset = False
	import pygame #used to create video games
	import tkinter as tkr #used to develop GUI
	from tkinter.filedialog import askdirectory #it permit to select dir
	import os #it permits to interact with the operating system
	font = "Helvetica 12 bold"
	music_player = tkr.Tk() 
	music_player.title("Please get yourself a VLC media player so you don't stick with lame functionality thing") 
	music_player.geometry("800x600")
	while True:
		directory = askdirectory()
		if not directory:
			pass
		else:
			break
	os.chdir(directory) #it permits to chenge the current dir
	song_list = os.listdir() #it returns the list of files song
	play_list = tkr.Listbox(music_player, font=font, bg="yellow", selectmode=tkr.SINGLE)
	pos = 0
	for item in song_list:
		if ".mp3" in item:
			play_list.insert(pos, item)
			pos += 1
		if ".wav" in item:
			play_list.insert(pos,item)
			pos += 1
		if ".ogg" in item:
			play_list.insert(pos,item)
			pos += 1
		else:
			continue
	pygame.init()
	pygame.mixer.init()
	var = tkr.StringVar() 
	song_title = tkr.Label(music_player, font=font, textvariable=var)
	def play():
		pygame.mixer.music.load(play_list.get(tkr.ACTIVE))
		var.set(play_list.get(tkr.ACTIVE))
		pygame.mixer.music.play()
	def stop():
		pygame.mixer.music.stop()
	def pause():
		global pauset
		pauset = not pauset
		if pauset:
			return pygame.mixer.music.pause()
		return pygame.mixer.music.unpause()
	def setvol(_=None):
		pygame.mixer.music.set_volume(float(vols.get()) / 100)
	Button1 = tkr.Button(music_player, width=5, height=3, font=font, text="PLAY", command=play, bg="blue", fg="white")
	Button2 = tkr.Button(music_player, width=5, height=3, font=font, text="STOP", command=stop, bg="red", fg="white")
	Button3 = tkr.Button(music_player, width=5, height=3, font=font, text="PAUSE", command=pause, bg="purple", fg="white")
	vols = tkr.Scale(music_player, label='Volume', from_=0, to=100, orient=tkr.HORIZONTAL, length=200, showvalue=100,tickinterval=10, resolution=1, command=setvol)
	song_title.pack()
	Button1.pack(fill="x")
	Button2.pack(fill="x")
	Button3.pack(fill="x")
	play_list.pack(fill="both", expand="yes")
	vols.pack()
	vols.set(pygame.mixer.music.get_volume())
	music_player.mainloop()
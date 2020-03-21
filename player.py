import subprocess
import re
import time

server_cmd = 'cmd'
player_cmd = 'mpc'

class SpotifyPlayer():
 def __init__(self):
  self.status = "Initiated"
  self.current_song = None
  self.mpc_status = None

 @staticmethod
 def run(cmd, *args):
  full_cmd = [cmd]
  for arg in args:
   full_cmd.append(arg)
  print(full_cmd)
  out = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  output = out.communicate()
  return output

 def update_status(self, out):
 # play/pause output looks like:
 #  Bebe Rexha;Asketa & Natan Chaim;The Chainsmokers - Call You Mine - Asketa & Natan Chaim Remix
 #  [playing] #22/36   2:47/3:03 (91%)
 #  volume: 25%   repeat: off   random: off   single: off   consume: off
  output = out[0].decode('utf-8').splitlines()
  # First time playing/pausing doesn't have status returned? 
  if isinstance(output, list) and len(output) == 3:
  	# Don't think I can individually parse artist, song, album, as '-' in any of these would break things
  	playing = output[0]
  	song_status = output[1]
  	mpc_status = output[2]

  	# Update current song
  	self.current_song = playing

  	# Get status of song
  	status = re.search(r"\[(.*?)\]",song_status).group(1)
  	self.status = status

  	# MPC status
  	self.mpc_status = mpc_status

#  print(playing)
#  print(song_status, status)
#  print(mpc_status)

 def get_status(self):
  output = self.run(player_cmd, 'status')
  return self.status

 def play(self):
  output = self.run(player_cmd, 'play')
  self.update_status(output)

 def pause(self):
  output = self.run(player_cmd, 'pause')
  self.update_status(output)

 def toggle(self):
  # TODO, change to 'mpc toggle'
  # For now, we assume
  if self.status == "paused":
   self.play()
  elif self.status == "playing":
   self.pause()
  else:
   print("Unkown status state")

 def clear(self):
  output = self.run(player_cmd, 'clear')

 def add_playlist(self, playlist="2wEdMantM5JEHCt01A6y64"):
  str = "spotify:playlist:"+playlist
  output = self.run(player_cmd, 'add', str)

 def shuffle(self):
  output = self.run(player_cmd, 'shuffle')

 def set_volume(self, val):
  output = self.run(player_cmd, 'volume', str(val))

 def wait_for_connection(self):
  max_time_to_wait = 30
  t = 0
  while True:
   output = self.run(player_cmd, 'status')
   status = output[0].decode('utf-8')
   if status != "mpd error: Connection refused\n":
    break
   elif t > max_time_to_wait:
    print(f"Waited max {max_time_to_wait} seconds")
    break
   print("Waiting for mpc to initialize...")
   t += 1
   time.sleep(1)

 def idle(self):
  print("Starting Idle")
  output = self.run(player_cmd, 'idle')
  print(f"Done Idling: {output}")


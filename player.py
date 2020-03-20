import subprocess
import re

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
  out = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  output = out.communicate()
  return output

 def update_status(self, out):
 # play/pause output looks like:
 #  Bebe Rexha;Asketa & Natan Chaim;The Chainsmokers - Call You Mine - Asketa & Natan Chaim Remix
 #  [playing] #22/36   2:47/3:03 (91%)
 #  volume: 25%   repeat: off   random: off   single: off   consume: off

  output = out[0].decode('utf-8').splitlines()

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


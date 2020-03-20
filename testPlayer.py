from player import SpotifyPlayer
import time

server = SpotifyPlayer()

#print(server.get_status())


print(server.status)
print("Pausing")
server.pause()
print(server.status)
time.sleep(3)
print("Playing")
server.play()
print(server.status)

from open_gopro.api import HttpCommands
from open_gopro.interface import HttpMessage, HttpMessages
from open_gopro.constants import CmdId
from open_gopro.interface import GoProHttp


# client = GoProHttp()
# http_gopro = HttpCommands(client)
http_gopro = HttpCommands(HttpMessages[HttpMessage, CmdId])

http_gopro.get_camera_state()
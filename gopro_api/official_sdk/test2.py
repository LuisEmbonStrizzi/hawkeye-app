import time
from open_gopro import WirelessGoPro, Params

with WirelessGoPro() as gopro:
    gopro.ble_command.load_preset(Params.Preset.CINEMATIC)
    gopro.ble_setting.resolution.set(Params.Resolution.RES_4K)
    gopro.ble_setting.fps.set(Params.FPS.FPS_30)
    gopro.ble_command.set_shutter(Params.Shutter.ON)
    time.sleep(2) # Record for 2 seconds
    gopro.ble_command.set_shutter(Params.Shutter.OFF)

    # Download all of the files from the camera
    media_list = [x["n"] for x in gopro.wifi_command.get_media_list().flatten]
    for file in media_list:
        gopro.wifi_command.download_file(camera_file=file)
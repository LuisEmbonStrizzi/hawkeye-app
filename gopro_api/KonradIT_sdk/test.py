from gopro_api import WirelessGoPro, Params
with WirelessGoPro() as gopro:
    gopro.ble_command.set_shutter(Params.Toggle.ENABLE)
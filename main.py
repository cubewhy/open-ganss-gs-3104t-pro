from typing import Literal
import usb
import sys


def find_keyboard() -> usb.core.Device | None:
    devices = usb.core.find(find_all=True)
    if devices is None:
        return None
    for dev in devices:
        try:
            if isinstance(dev, usb.core.Device):
                if dev.product == "GS3104T-PRO 2.4G":
                    return dev
        except ValueError:
            pass


def parse_payload(bytes_string: str) -> bytes:
    print(bytes_string)
    return bytes.fromhex(bytes_string)


def control(device: usb.core.Device, payload: bytes):
    device.write(0x05, payload)


def int_to_hex_color(n: int) -> str:
    if 0 <= n <= 0xFFFFFF:
        return f"{n:06X}".lower()
    raise ValueError("n should in the range 0 ~ 0xFFFFFF")


def turn_off_rgb(
    device: usb.core.Device,
):
    control(
        device,
        bytes.fromhex(
            "0510000000000000000000000000000000aa5500000000000000000000000014"
        ),
    )


def rgb_single_on(
    device: usb.core.Device,
    lighting_brightness: int = 5,
    lighting_speed: int = 3,
    colorful_flag: bool = True,
    color: int = 0xFFFFFF,
):
    pass


def set_rgb_mode(
    device: usb.core.Device,
    mode: int,
    lighting_brightness: int = 5,
    lighting_speed: int = 3,
    colorful_flag: bool = True,
    color: int = 0xFFFFFF,
    lighting_direction: Literal["upward", "downward"] = "downward",
):
    color_hex = int_to_hex_color(color)
    mode_hex = format(mode, "x")
    op_code = mode_hex[-1]
    if mode < 10:
        mode_str = f"0{mode}"
    else:
        mode_str = str(mode)
    lighting_direction_bit = 2 if lighting_direction == "upward" else 3
    colorful_flag_bit = 1 if colorful_flag else 0
    control(
        device,
        parse_payload(
            f"0510000{op_code}a{color_hex}00000000{colorful_flag_bit}0{lighting_brightness}0{lighting_speed}0{lighting_direction_bit}0000aa55000000000000000000000000{mode_str}"
        ),
    )


def handle_device(dev: usb.core.Device):
    set_rgb_mode(
        dev,
        26,
        lighting_brightness=5,
        color=0xFFFFFF,
        colorful_flag=True,
        lighting_direction="downward",
    )
    # turn_off_rgb(dev)


def main():
    # find the device
    dev = find_keyboard()
    if dev is None:
        print("Please connect your keyboard")
        sys.exit(1)

    intf_nums = []
    for cfg in dev:
        for intf in cfg:
            b_interface_number = getattr(intf, "bInterfaceNumber")
            if dev.is_kernel_driver_active(b_interface_number):
                dev.detach_kernel_driver(b_interface_number)
                intf_nums.append(b_interface_number)

    dev.set_configuration()

    try:
        handle_device(dev)
    finally:
        for intf_num in intf_nums:
            # release interface
            usb.util.release_interface(dev, intf_num)
            try:
                dev.attach_kernel_driver(intf_num)
            except usb.core.USBError as e:
                print(f"Could not reattach kernel driver for interface {intf_num}: {e}")


if __name__ == "__main__":
    main()

# Open Source Driver for GANSS GS3104T Pro Keyboard

## Workaround for Linux

Execute following command and restart your computer

```shell
echo options hid_apple fnmode=2 | sudo tee -a /etc/modprobe.d/hid_apple.conf

sudo mkdir -p /etc/udev/hwdb.d
sudo tee /etc/udev/hwdb.d/90-custom-applehid.hwdb >/dev/null <<'EOF'
evdev:input:*
 KEYBOARD_KEY_7009c=unknown
EOF
sudo systemd-hwdb update
sudo udevadm trigger -s input
```

## Features

- Control RGB lighting

## Road Map

- [ ] Switch RGB lighting mode
- [ ] Custom key mapping
- [ ] Custom RGB light for single keys
- [ ] Rewrite with Rust

## Usage

- Install uv
- Clone the repository
- Execute `uv sync` under the project dir
- Execute the script

<!-- ## RGB Modes -->
<!---->
<!-- | Name | Code | -->
<!-- | -------------- | --------------- | -->
<!-- | static | 0x1d | -->
<!-- | Single On | 0x1e | -->
<!-- | Single Off | 0x1f | -->
<!-- | Glitting | 0x20 | -->
<!-- | Falling | 0x21 | -->
<!-- | Colorful | 0x22 | -->

## License

This work is licensed under GPLv3

You're allowed to use, share and modify this work.

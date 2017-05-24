import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('http://192.168.0.4:8081/infces/')
qr.make(fit=True)

img = qr.make_image()
img.save("advanceduse.png")

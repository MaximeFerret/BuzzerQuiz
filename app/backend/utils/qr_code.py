import qrcode


def generate_qr_code(data):
    qr = qrcode.make(data)
    qr.save("qr_code.png")

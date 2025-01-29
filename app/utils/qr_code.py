import base64
from io import BytesIO

import qrcode


def generate_qr_code(link):
    """
    Génère un QR Code à partir d'un lien et le retourne sous forme de base64.

    :param link: Lien vers lequel le QR Code doit pointer.
    :return: Image du QR Code encodée en base64.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Sauvegarde en mémoire sous forme de base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return qr_base64

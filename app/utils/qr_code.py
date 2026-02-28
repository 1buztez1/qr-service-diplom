import io
import base64
import qrcode
from PIL import Image

def generate_qr_base64(data: str, box_size: int = 10, border: int = 4) -> str:
    qr = qrcode.QRCode(box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode('ascii')




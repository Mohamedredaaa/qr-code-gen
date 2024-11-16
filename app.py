import logging
import qrcode
import re  # Import regular expressions
import cairosvg  # For SVG to PNG conversion
from PIL import Image, ImageOps, ImageDraw
from PIL.Image import Resampling
from flask import Flask, render_template, request, flash, redirect, url_for
from io import BytesIO
import os

app = Flask(__name__)

# Use environment variable for secret key
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

logging.basicConfig(level=logging.INFO)

def remove_background(logo_img):
    """Removes the background of the logo image."""
    logo_img = logo_img.convert("RGBA")
    data = logo_img.getdata()
    new_data = []
    for item in data:
        if item[3] < 100:  # If alpha is less than 100 (transparent)
            new_data.append((255, 255, 255, 0))  # Make transparent pixels white
        else:
            new_data.append(item)
    logo_img.putdata(new_data)
    return logo_img

def add_logo_with_border(qr_img, logo_img, border_color="#FFFFFF", border_width=10):
    """Adds a logo with a border to the center of the QR code."""
    qr_width, qr_height = qr_img.size
    logo_width, logo_height = logo_img.size

    pos_x = (qr_width - logo_width) // 2
    pos_y = (qr_height - logo_height) // 2

    border_img = Image.new("RGBA", (logo_width + 2 * border_width, logo_height + 2 * border_width), border_color)
    border_img.paste(logo_img, (border_width, border_width), logo_img)

    qr_img.paste(border_img, (pos_x - border_width, pos_y - border_width), border_img)
    return qr_img

def hex_to_rgb(hex_color):
    """Converts a hex color to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles QR code generation."""
    try:
        qr_image_path = None

        if request.method == "POST":
            data = request.form.get("data")
            logo = request.files.get("logo")
            color = request.form.get("color", "#000000")
            size = int(request.form.get("size", 300))
            border_color = request.form.get("border_color", "#FFFFFF")
            border_width = int(request.form.get("border_width", 10))

            logging.info(f"Data received: {data}, Logo: {logo}, Color: {color}, Size: {size}, Border Color: {border_color}, Border Width: {border_width}")

            if not data or (not re.match(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", data) and not re.match(r"^[a-zA-Z0-9\s]+$", data)):
                flash("Invalid URL or text format", "danger")
                return redirect(url_for("index"))

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            fill_rgb = hex_to_rgb(color)
            back_rgb = (255, 255, 255)

            img = qr.make_image(fill_color=fill_rgb, back_color=back_rgb).convert("RGBA")
            logging.info(f"QR Code image created with color: {fill_rgb}")

            if logo:
                try:
                    if logo.filename.lower().endswith('.svg'):
                        svg_bytes = logo.read()
                        png_bytes = BytesIO()
                        cairosvg.svg2png(bytestring=svg_bytes, write_to=png_bytes)
                        png_bytes.seek(0)
                        logo_img = Image.open(png_bytes)
                    else:
                        logo_img = Image.open(logo)

                    logo_img = remove_background(logo_img)
                    logo_size = int(size * 0.2)
                    logo_img = logo_img.resize((logo_size, logo_size), Resampling.LANCZOS)

                    img = add_logo_with_border(img, logo_img, border_color=border_color, border_width=border_width)
                    logging.info("Logo with border added to QR code")

                except Exception as e:
                    flash(f"Error adding logo: {e}", "danger")
                    logging.error(f"Error adding logo: {e}")
                    return redirect(url_for("index"))

            qr_image_path = "static/qr_code.png"
            img.save(qr_image_path)
            logging.info("QR code saved successfully")

        return render_template("index.html", qr_image=qr_image_path)

    except Exception as e:
        logging.error(f"Error processing QR code: {e}")
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for("index"))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

 

from flask import Flask, render_template, request, make_response, redirect, url_for
import qrcode
from PIL import Image
from PIL.Image import Resampling as ImageResampling
import os

# Initialize Flask app
app = Flask(__name__)

# Set upload folder for QR codes and temporary logos
UPLOAD_FOLDER = 'static/qr_codes'
LOGO_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOGO_FOLDER, exist_ok=True)

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to add an image to the QR code
def add_image_to_qr(qr_img, logo_path, size):
    """
    Add an image/logo to the center of the QR code.
    """
    logo = Image.open(logo_path).convert("RGBA")

    # Resize logo dynamically based on the QR code size
    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width * size)  # Logo size is a percentage of QR code size
    logo = logo.resize((logo_size, logo_size), ImageResampling.LANCZOS)

    # Position the logo at the center of the QR code
    logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    qr_img.paste(logo, logo_pos, mask=logo)

    return qr_img

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_text = request.form.get("text")
        fg_color = request.form.get("fg_color", "black")  # Default foreground color is black
        bg_color = request.form.get("bg_color", "white")  # Default background color is white
        logo_size = float(request.form.get("logo_size", 0.2))  # Default logo size is 20%
        qr_size = int(request.form.get("qr_size", 10))  # Default QR code box size is 10
        logo_file = request.files.get("logo")

        if not input_text:
            return render_template("index.html", error="Please enter text or URL to generate QR code.")

        try:
            # Generate QR code with custom colors and size
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
                box_size=qr_size,
                border=4,
            )
            qr.add_data(input_text)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert("RGBA")

            # Handle logo upload if provided
            if logo_file and logo_file.filename:
                if allowed_file(logo_file.filename):
                    logo_path = os.path.join(LOGO_FOLDER, logo_file.filename)
                    logo_file.save(logo_path)

                    # Add logo to the QR code
                    qr_img = add_image_to_qr(qr_img, logo_path, logo_size)
                else:
                    return render_template("index.html", error="Unsupported file format. Allowed formats: PNG, JPG, JPEG, BMP, GIF.")

            # Save the QR code image
            qr_filename = f"qr_code_{hash(input_text)}.png"
            qr_filepath = os.path.join(UPLOAD_FOLDER, qr_filename)
            qr_img.save(qr_filepath)

            return render_template("index.html", qr_code=qr_filename)
        except Exception as e:
            return render_template("index.html", error=f"Error generating QR code: {e}")

    return render_template("index.html")

@app.route("/download/<filename>")
def download_qr(filename):
    """
    Serve the QR code file directly for download in the browser.
    """
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    try:
        with open(filepath, "rb") as f:
            response = make_response(f.read())
            response.headers["Content-Type"] = "image/png"
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
            return response
    except FileNotFoundError:
        return redirect(url_for("index", error="File not found."))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

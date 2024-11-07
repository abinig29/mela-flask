UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
MAX_CV_SIZE = 5 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

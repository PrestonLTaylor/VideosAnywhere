from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class VideoUploadForm(FlaskForm):
    """
    A `FlaskForm` instance for supporting a user uploading a raw mp4 video through a form.
    """

    # TODO: For now we will only support mp4, but support for other file formats should be implemented
    # TODO: Maybe better validation with mime-type inspection etc. to check if the file uploaded is a video.
    raw_video: FileField = FileField(label="Video File (.mp4): ", validators=[
        FileRequired(),
        FileAllowed(["mp4"], "Only mp4 files are currently supported.")
    ])
    submit: SubmitField = SubmitField("Upload")
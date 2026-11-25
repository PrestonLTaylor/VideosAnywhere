from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, HiddenField
from wtforms.validators import InputRequired

class VideoChunkUploadForm(FlaskForm):
    """
    A `FlaskForm` instance for supporting a video uploading by chunking a raw mp4 video identified by the server using `video_upload_id`.
    """

    # TODO: For now we will only support mp4, but support for other file formats should be implemented
    # TODO: Maybe better validation with mime-type inspection etc. to check if the file uploaded is a video.
    video_chunk: FileField = FileField(label="Video File (.mp4): ", validators=[
        FileRequired(),
        FileAllowed(["mp4"], "Only mp4 files are currently supported.")
    ])

    video_upload_id: HiddenField = HiddenField(validators=([InputRequired()]))

    submit: SubmitField = SubmitField("Upload")
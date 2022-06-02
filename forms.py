from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError


class ContactForm(FlaskForm):
    value_input = IntegerField("Input: ")
    char_in = StringField()
    submit = SubmitField("Submit")
    value_output = IntegerField("Output: ")
    char_out = StringField()

    # def validate_input(self):
    #     need_chars = "0123456789"
    #     for char in self.value_input.data:
    #         if char not in need_chars:
    #             raise ValidationError(
    #                 f"Character {char} is not allowed in username.")
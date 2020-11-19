# @Time    : 2020/11/19 21:26 
# @Author  : 孙北晨 
# @Version : V 0.1
# @Int     :
from flask_wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField("openid",validators=[DataRequired()])
    remember_me = BooleanField("remember_me",default = False)

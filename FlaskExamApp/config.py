class Config() :
    SECRET_KEY = "4398cf5c355c410ccaa5b58856b98372"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "edtest.noreply@gmail.com"
    MAIL_PASSWORD = "thisisanoreplyemail"
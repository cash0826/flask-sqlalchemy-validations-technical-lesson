from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class EmailAddress(db.Model):
    __tablename__ = 'emailaddress'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    backup_email = db.Column(db.String)

    @validates('email', 'backup_email')
    def validate_email(self, key, address):
        # check for presence and not empty string
        if not address:
            raise ValueError("Email must be present")
        
        # check for type using isistance Python function
        if not isinstance(address, str):
            raise ValueError("Email must be a string")
        
        # check for uniqueness (duplicates)
        duplicate_email = db.session.query(EmailAddress.id).filter_by(email = address).first
        if duplicate_email is not None:
            raise ValueError("Email must be unique")
        
        # returning valueError because seed file added duplicates. The DB currently has duplicate values and the code stops here.
        
        # check that email does not exceed character length. Standard is 254
        if len(address) > 20:
            raise ValueError("Email too long")
        
        # Reject hotmail and yahoo domains
        
        if address.split("@")[1] in ["hotmail.com", "yahoo.com"]:
            raise ValueError("Email cannot be a hotmail or yahoo address.")
        
        if '@' not in address:
            raise ValueError("Email must have an '@' in the address")

        return address
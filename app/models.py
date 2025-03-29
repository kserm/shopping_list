from datetime import datetime
from app import db

class ShoppingList(db.Model):
    __tablename__ = 'shopping_list'
    
    id = db.Column(db.Integer, primary_key=True)
    entries = db.Column(db.Text, nullable=False)
    checked_states = db.Column(db.Text)  # Store which items are checked
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ShoppingList {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'entries': self.entries,
            'checked_states': self.checked_states,
            'created_at': self.created_at
        }
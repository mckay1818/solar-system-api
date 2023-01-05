#get db access
from app import db

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet", back_populates="moons")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "description": self.description,
            "planet": self.planet
        }


    @classmethod
    def from_dict(cls, moon_data):
        new_moon = Moon(
                    name = moon_data["name"],
                    size = moon_data["size"],
                    description = moon_data["description"],
                    planet = moon_data["planet"]
                    )
        return new_moon
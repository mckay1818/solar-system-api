import pytest
from app import create_app, db
from flask.signals import request_finished
from app.models.planet import Planet
from app.models.moon import Moon

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
    
    with app.app_context():
        db.create_all()
        yield app
    
    with app.app_context():
        db.drop_all()
        

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def saved_two_planets(app):
    #Arrange
    planet_1 = Planet(
                name = "Mercury",
                color = "gray",
                description = "is the smallest planet in the Solar System",
                )
    planet_2 = Planet(
                name = "Earth",
                color = "blue",
                description = "The planet that we live on"
                )
    

    db.session.add(planet_1)
    db.session.add(planet_2)
    db.session.commit()
    db.session.refresh(planet_1, ["id"])
    db.session.refresh(planet_2, ["id"])


@pytest.fixture
def saved_one_moon(app):
    #Arrange
    moon_1 = Moon(
                name = "Earth's moon",
                size = 1079,
                description = "the only place beyond Earth where humans have set foot",
                planet_id = 2
                )

    db.session.add(moon_1)
    db.session.commit()
    db.session.refresh(moon_1, ["id"])



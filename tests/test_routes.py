from werkzeug.exceptions import HTTPException
from app.routes.planet_routes import validate_model
from app.models.planet import Planet
from app.models.moon import Moon
import pytest



####################
# Test get_planet  #
####################

def test_get_planets_optional_query_empty_db_returns_empty_list(client):
    # Act
    response = client.get("/planets")

    # Assert 
    assert response.status_code == 200
    assert response.get_json() == []
    
    
    
# GET /planets/1 returns a 200 with a response 
# body that matches our fixture
def test_get_one_planet(client, saved_two_planets):
    #Act
    response = client.get("/planets/1")
    response_body = response.get_json()
    
    #Assert
    assert response.status_code == 200
    assert response_body == {
                                "id" : 1,
                                "name" : "Mercury",
                                "color" : "gray",
                                "description" : "is the smallest planet in the Solar System",
                                "moons" : []
                            }

# GET /planets/1 with no data in test database 
# (no fixture) returns a 404
def test_get_one_no_data_planet(client):
    #Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 404
    assert response_body == {'message': ' Planet 1 not found.'}


# GET /planets with valid test data (fixtures) 
# returns a 200 with an array including appropriate test data
def test_get_all_planets_with_valid_data(client, saved_two_planets):
    #Act
    response = client.get("/planets")
    response_body = response.get_json()
    
    #Assert
    assert response.status_code == 200
    assert response_body ==[
                        {
                            "id" : 1,
                            "name" : "Mercury",
                            "color" : "gray",
                            "description" : "is the smallest planet in the Solar System",
                            "moons" : []
                        },
                                                {
                            "id" : 2,
                            "name" : "Earth",
                            "color" : "blue",
                            "description" : "The planet that we live on",
                            "moons" : []
                        }
            ]

#######################     
# Test create_planet  #
#######################

def test_create_one_planet(client):
    #Act
    response = client.post("/planets", json={
        "name": "Mercury",
        "description": "is the smallest planet in the Solar System",
        "color": "gray",
        "moons":[]
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    assert response_body == "Planet Mercury created."


#######################     
# Test update_planet  #
#######################

def test_replace_one_planet(client, saved_two_planets):
    #Arrange
    test_data = {
        "name": "Mars",
        "description": "Still a planet in our hearts",
        "color" : "Red"
    }

    #Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated."


def test_replace_planet_id_not_found(client, saved_two_planets):
    #Arrange
    test_data = {
        "name": "Mars",
        "description": "Still a planet in our hearts"
    }

    #Act
    response = client.put("/planets/9", json=test_data)
    response_body = response.get_json()

    #Assert 
    assert response.status_code == 404
    assert response_body == {'message': ' Planet 9 not found.'}


#######################     
# Test delete_planet  #
#######################

def test_delete_one_planet(client, saved_two_planets):
    #Act
    response = client.delete("/planets/1")
    response_body = response.get_json()

    #Assert 
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully deleted."


def test_delete_planet_id_not_found(client, saved_two_planets):
    #Act
    response = client.delete("/planets/5")
    response_body = response.get_json()

    #Assert 
    assert response.status_code == 404
    assert response_body == {"message": " Planet 5 not found."}


def test_delete_planet_invalid(client, saved_two_planets):
    #Act
    
    response = client.delete("/planets/cat")
    response_body = response.get_json()
    # response_body = response.get_data(as_text=True) 

    #Assert 
    assert response.status_code == 400
    assert response_body == {'message': ' Planet cat invalid.'}


########################     
# Test validate_planet #
########################

def test_validate_planet(saved_two_planets):
    # Act
    result_planet = validate_model(Planet, 1)

    # Assert
    assert result_planet.id == 1
    assert result_planet.name == "Mercury"
    assert result_planet.color == "gray"
    assert result_planet.description == "is the smallest planet in the Solar System"

def test_validate_planet_missing_record(saved_two_planets):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_planet = validate_model(Planet, "3")
    
def test_validate_planet_invalid_id(saved_two_planets):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_planet = validate_model(Planet, "cat")
        
####################        
# Test Moon routes #
####################

def test_create_one_moon_by_create_new_moon_to_planet(client, saved_two_planets):
    # Act
    response = client.post("/planets/2/moons", json = {
        "name": "Earth's moon",
        "size": 1079,
        "description": "the only place beyond Earth where humans have set foot",
        "planet_id": 2
        })

    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 201
    assert response_body == "Moon Earth's moon created and connected with Earth."

    new_moon = Moon.query.get(1)
    assert new_moon
    assert new_moon.name == "Earth's moon"
    assert new_moon.size == 1079
    assert new_moon.description == "the only place beyond Earth where humans have set foot"
    assert new_moon.planet_id == 2



def test_get_all_moons_with_empty_db_return_empty_list(client):
    # Act
    response = client.get("/moons")

    # Assert 
    assert response.status_code == 200
    assert response.get_json() == []
    
    


def test_get_moons_by_planet_id_with_vlaid_id(client, saved_one_moon):
    # Act
    response = client.get("/planets/2/moons")
    
    
    # Assert 
    assert response.status_code == 200
    assert response.get_json() == [{
        "name": "Earth's moon",
        "size": 1079,
        "description": "the only place beyond Earth where humans have set foot",
        "planet_id": 2
        }]



def test_get_all_moons(client):
    pass


def test_get_one_moon_by_id_with_vlaid_id(client):
    pass
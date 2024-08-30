from pydantic import BaseModel, ConfigDict

######################################
# 4. Définition des schémas


# Validateur intermédiaire à l'entrée request schema
class UserBase(BaseModel):
    username: str
    email: str
    password: str

# sortie de l'api schéma response


class UserDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str

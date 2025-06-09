# src/models/usuario.py
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

from src.extensions import db

class Usuario:
    def __init__(self, username, password, name, _id=None):
        self.username = username
        self.password = password # Já deve estar hashed ao ser passado, ou será hashed por set_password
        self.name = name
        self._id = _id # Para carregar usuários existentes do DB

    # Opcional: Propriedade para acessar a coleção, embora db.users seja mais direto
    # @property
    # def collection(self):
    #     return db.users

    # --- NOVO MÉTODO: CONVERTER INSTÂNCIA PARA DICIONÁRIO ---
    def to_dict(self):
        """
        Retorna uma representação de dicionário da instância do usuário
        adequada para inserção/atualização no MongoDB.
        """
        user_data = {
            "username": self.username,
            "password": self.password, # Este já deve ser o hash da senha
            "name": self.name
        }
        # Se o _id existir, inclua-o, mas insert_one() geralmente gera um novo
        # para novas inserções. Para atualizações, você o usaria na query.
        if self._id:
            user_data["_id"] = self._id
        return user_data
    # --- FIM DO NOVO MÉTODO ---

    def save(self):
        # O método save() agora deve usar to_dict() para obter os dados
        user_data_to_save = self.to_dict()
        if self._id:
            # Se o usuário já tem um _id, é uma atualização
            # Remover _id de $set para evitar erro se ele estiver presente
            update_data = user_data_to_save.copy()
            update_data.pop('_id', None) 
            self.collection.update_one({"_id": self._id}, {"$set": update_data})
        else:
            # Se não tem _id, é uma nova inserção
            result = db.users.insert_one(user_data_to_save)
            self._id = result.inserted_id # Atribui o _id gerado à instância
        return self

    @staticmethod
    def find_by_username(username):
        user_data = db.users.find_one({"username": username})
        if user_data:
            return Usuario(
                username=user_data['username'],
                password=user_data['password'], # Assume que é o hash
                name=user_data.get('name'),
                _id=user_data['_id']
            )
        return None

    @staticmethod
    def find_by_id(user_id):
        try:
            user_data = db.users.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return Usuario(
                    username=user_data['username'],
                    password=user_data['password'],
                    name=user_data.get('name'),
                    _id=user_data['_id']
                )
            return None
        except Exception:
            return None

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # Certifique-se de que self.password é o hash armazenado
        return check_password_hash(self.password, password)
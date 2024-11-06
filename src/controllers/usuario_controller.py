from fastapi import HTTPException
from database.mongodb import usuarios_collection, parse_usuario
from models.usuario import Usuario
from bson.objectid import ObjectId
from datetime import datetime

async def criar_usuario(usuario: Usuario):
    usuario.nome_usuario = f"{usuario.nome.lower()}.{usuario.nome.split()[-1].lower()}"
    usuario.data_criacao = usuario.data_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")
    novo_usuario = await usuarios_collection.insert_one(usuario.dict())
    return await obter_usuario_por_id(novo_usuario.inserted_id)

async def obter_usuario_por_id(usuario_id: str):
    usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
    if usuario:
        return parse_usuario(usuario)

async def atualizar_usuario(usuario_id: str, dados: dict):
    dados["data_atualizacao"] = datetime.now()
    await usuarios_collection.update_one({"_id": ObjectId(usuario_id)}, {"$set": dados})
    return await obter_usuario_por_id(usuario_id)

async def deletar_usuario(usuario_id: str):
    await usuarios_collection.delete_one({"_id": ObjectId(usuario_id)})
    return {"msg": "Usuário deletado com sucesso"}

async def obter_usuario_por_nome_usuario(nome_usuario: str):
    usuario = await usuarios_collection.find_one({"nome_usuario": nome_usuario})
    if usuario:
        return parse_usuario(usuario)
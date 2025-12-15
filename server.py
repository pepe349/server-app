import os, json, asyncio, websockets

# Diccionario para guardar las conexiones
CLIENTS = {"emisor": None, "receptor": None}

async def handler(websocket):
    role = None
    try:
        async for message in websocket:
            data = json.loads(message)
            
            # Registro de quién es quién
            if data.get("type") == "register":
                role = data["role"]
                CLIENTS[role] = websocket
                print(f"Sistema: {role} conectado.")

            # Si la PC manda un CONTROL, se lo pasamos al Celular
            elif data.get("type") == "CONTROL":
                if CLIENTS["emisor"]:
                    await CLIENTS["emisor"].send(message)

            # Si el Celular manda DATA (Video), se lo pasamos a la PC
            elif data.get("type") == "DATA":
                if CLIENTS["receptor"]:
                    await CLIENTS["receptor"].send(message)
    except:
        pass
    finally:
        if role:
            CLIENTS[role] = None
            print(f"Sistema: {role} desconectado.")

async def main():
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 8080))
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
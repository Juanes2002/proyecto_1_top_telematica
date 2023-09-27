import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
import os
import random
import uuid

# Lista de DataNodes

def send_file():
    # Especifica la ruta completa o relativa al archivo que deseas enviar
    current_directory = os.getcwd()
    file_path = current_directory + "/file.txt"
    
    # Lee el archivo y obtén su tamaño
    with open(file_path, "rb") as f:
        file_contents = f.read()
    file_size = len(file_contents)
    
    channel = grpc.insecure_channel('localhost:50051')
    name_node_stub = file_transfer_pb2_grpc.NameNodeStub(channel)
    
    unique_filename = str(uuid.uuid4()) + ".txt"

    # Solicita al NameNode la asignación de DataNodes para el archivo
    allocation_request = file_transfer_pb2.FileRequest(filename=unique_filename, size=file_size)
    file_metadata = name_node_stub.AllocateFile(allocation_request)
    
    # Obtén una ubicación de DataNode aleatoria
    random_data_node = random.choice(file_metadata.locations)
    
    data_node_stub = file_transfer_pb2_grpc.DataNodeStub(channel)
    
    # Divide el archivo en chunks y envía cada chunk al DataNode seleccionado
    chunk_size = 1024  # Tamaño del chunk
    offset = 0
    while offset < file_size:
        chunk_data = file_contents[offset:offset + chunk_size]
        chunk = file_transfer_pb2.Chunk(data=chunk_data)
        data_node_stub.UploadChunk(chunk)
        offset += chunk_size
    
    print("Archivo enviado correctamente")

if __name__ == '__main__':
    send_file()
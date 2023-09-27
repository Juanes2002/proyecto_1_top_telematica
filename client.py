import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc


def send_file():
    # Especifica la ruta completa o relativa al archivo que deseas enviar
    file_path = "C:/Users/user/OneDrive/Escritorio/Reto2/proyecto1/file_to_send.txt"

    # Lee el archivo
    with open(file_path, "rb") as f:
        file_contents = f.read()
    
    channel = grpc.insecure_channel('localhost:50051')
    stub = file_transfer_pb2_grpc.FileTransferStub(channel)
    
    # Crea un generador de chunks a partir del archivo
    chunk_generator = generate_chunks(file_contents)
    
    # Envía el archivo por chunks
    response = stub.SendFile(chunk_generator)
    
    print(response.message)

def generate_chunks(data, chunk_size=1024):
    for i in range(0, len(data), chunk_size):
        yield file_transfer_pb2.Chunk(data=data[i:i+chunk_size])

if __name__ == '__main__':
    send_file()
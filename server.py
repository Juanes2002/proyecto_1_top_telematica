import grpc
import os
from concurrent import futures
import file_transfer_pb2
import file_transfer_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class FileTransferServicer(file_transfer_pb2_grpc.FileTransferServicer):
    def SendFile(self, request_iterator, context):
        file_path = "server_received_file.txt"  # Nombre del archivo en el servidor
        with open(file_path, "wb") as f:
            for chunk in request_iterator:
                f.write(chunk.data)
        return file_transfer_pb2.Response(message="Archivo recibido correctamente")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC en ejecución en el puerto 50051...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

def split_file(input_file, output_directory, block_size):
    try:
        with open(input_file, 'rb') as source_file:
            block_number = 0
            while True:
                block_data = source_file.read(block_size)
                if not block_data:
                    break  # Fin del archivo
                block_filename = f"block{block_number}.bin"
                block_file_path = os.path.join(output_directory, block_file_name)
                with open(block_file_path, 'wb') as block_file:
                    block_file.write(block_data)
                block_number += 1
    except Exception as e:
        print(f"Error al dividir el archivo: {str(e)}") 

if __name__ == '__main__':
    serve()
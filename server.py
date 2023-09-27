import grpc
import os
from concurrent import futures
import file_transfer_pb2
import file_transfer_pb2_grpc
import random

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

data_nodes = ["data_node1", "data_node2", "data_node3"]

class NameNode(file_transfer_pb2_grpc.NameNodeServicer):
    def __init__(self):
        self.file_metadata = {}  # Un diccionario para rastrear la ubicación de los archivos y sus réplicas.
        self.data_nodes = data_nodes  # Un diccionario para rastrear la ubicación de los archivos y sus réplicas.

    def AllocateFile(self, request, context):
        # Lógica para asignar un archivo a dos DataNodes de manera aleatoria.
        file_name = request.filename

        if file_name in self.file_metadata:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(f"El archivo '{file_name}' ya existe.")
            return file_transfer_pb2.FileMetadata(locations=self.file_metadata[file_name])

        # Seleccione aleatoriamente dos DataNodes para almacenar el archivo.
        allocated_data_nodes = random.sample(self.data_nodes, 2)

        # Actualice el registro de ubicación del archivo.
        self.file_metadata[file_name] = allocated_data_nodes

        return file_transfer_pb2.FileMetadata(locations=allocated_data_nodes)

    def GetFileLocation(self, request, context):
        # Lógica para obtener la ubicación de las réplicas de un archivo.
        file_name = request.filename

        if file_name in self.file_metadata:
            replica_locations = self.file_metadata[file_name]
            return file_transfer_pb2.FileLocation(location=replica_locations[0])  # Devuelve la ubicación de la primera réplica
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Archivo '{file_name}' no encontrado.")
            return file_transfer_pb2.FileLocation(location="")

class DataNode(file_transfer_pb2_grpc.DataNodeServicer):
    def __init__(self, data_node_name):
        self.data_node_name = data_node_name
        self.storage_directory = f"data_node_storage/{data_node_name}"  # Directorio de almacenamiento del DataNode
        os.makedirs(self.storage_directory, exist_ok=True)

    def UploadChunk(self, request, context):
        # Lógica para almacenar los datos del chunk en el DataNode.
        try:
            chunk_data = request.data
            file_name = "received_chunk.bin"  # Puedes cambiar el nombre o usar un sistema de nombres único
            file_path = os.path.join(self.storage_directory, file_name)

            with open(file_path, "ab") as f:
                f.write(chunk_data)

            return file_transfer_pb2.Response(message="Chunk recibido correctamente")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error al recibir el chunk: {str(e)}")
            return file_transfer_pb2.Response(message="Error al recibir el chunk")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Crea una lista de DataNodes
    data_nodes = ["data_node1", "data_node2", "data_node3"]
    
    # Pasa la lista de DataNodes al constructor de NameNode
    name_node = NameNode()
    name_node.data_nodes = data_nodes
    
    # Agrega los DataNodes al servidor
    file_transfer_pb2_grpc.add_NameNodeServicer_to_server(name_node, server)
    file_transfer_pb2_grpc.add_DataNodeServicer_to_server(DataNode("data_node1"), server)
    file_transfer_pb2_grpc.add_DataNodeServicer_to_server(DataNode("data_node2"), server)
    file_transfer_pb2_grpc.add_DataNodeServicer_to_server(DataNode("data_node3"), server)
    
    server.add_insecure_port('[::]:50051')  # Puerto común para NameNode y DataNodes
    server.start()
    print("Servidor gRPC en ejecución en el puerto 50051...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
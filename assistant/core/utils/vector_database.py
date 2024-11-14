from pymilvus import MilvusClient


class VectorDatabase:
    def __init__(self, uri, user, password) -> None:
        self.client = MilvusClient(
            uri=uri, 
            token=f"{user}:{password}"
        )

    # def 


if __name__ == "__main__":
    import os
    import dotenv
    dotenv.load_dotenv()

    client = MilvusClient(
        uri=os.getenv("MILVUS_URI"),
        token=f"{os.getenv("MILVUS_USER")}:{os.getenv("MILVUS_PASSWORD")}"
    )

    print(client.list_databases())

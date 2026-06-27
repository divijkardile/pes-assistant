import json

import boto3

from app.config.settings import get_settings
from app.llm.interfaces.embedding_provider import (
    EmbeddingProvider,
)


class BedrockEmbeddingProvider(
    EmbeddingProvider,
):

    def __init__(self) -> None:
        settings = get_settings()

        self._model_id = (
            settings.bedrock_embedding_model
        )

        self._client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            aws_session_token=settings.aws_session_token,
        )

    async def embed(
        self,
        text: str,
    ) -> list[float]:

        body = json.dumps(
            {
                "inputText": text,
            }
        )

        response = self._client.invoke_model(
            modelId=self._model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        payload = json.loads(
            response["body"].read()
        )

        return payload["embedding"]
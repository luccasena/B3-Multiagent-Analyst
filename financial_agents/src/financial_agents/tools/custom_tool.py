
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import  utils.vector_storage as vector_storage

class RAGInput(BaseModel):
    """Schema de entrada da tool (validado pelo Pydantic do CrewAI)."""
    query: str = Field(description="Pergunta a ser buscada no índice FAISS")

class FAISSRAGTool(BaseTool):
    """
    Tool compatível com CrewAI que consulta um índice FAISS já persistido.
    Carrega o vectorstore uma única vez e usa retriever k=3 por padrão.
    """
    name: str = "search_financial_data"
    description: str = (
        "Busca e retorna dados fundamentalistas e informações financeiras "
        "de um banco vetorial FAISS previamente indexado."
    )

    # schema dos argumentos aceitos pela tool
    args_schema: type = RAGInput

    # Campos internos (não expostos) para manter o retriever em memória
    _vectorstore = None
    _retriever = None

    # Pydantic v2: inicialização pós-construção do modelo
    def model_post_init(self, __context) -> None:  # type: ignore[override]

        if self._vectorstore is None:
            self._vectorstore = vector_storage.load()

        if self._retriever is None:
            # ajuste seus kwargs aqui (similarity / mmr)
            self._retriever = self._vectorstore.as_retriever(
                search_type="similarity", search_kwargs={"k": 3}
            )

    # Método síncrono chamado pelo CrewAI quando a tool é usada
    def _run(self, query: str) -> str:  # CrewAI chama _run para execução síncrona
        if not query or not query.strip():
            return "Query vazia. Forneça uma pergunta clara para a busca."

        try:
            docs = self._retriever.get_relevant_documents(query)  # type: ignore[attr-defined]
        except Exception as e:
            return f"Falha ao consultar o índice FAISS: {e}"

        # Concatena o conteúdo básico dos documentos; ajuste conforme seu caso
        return "\n\n".join(d.page_content for d in docs)

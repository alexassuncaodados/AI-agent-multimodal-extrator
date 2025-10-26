from pydantic import BaseModel, Field
from datetime import date

# Modelo de dados desejado para saída da extração de informações de nota fiscal
class ExtracaoOutput(BaseModel):
    descricao_servico: str = Field(description="Descrição detalhada dos serviços prestados.")
    valor_servico: float = Field(description="Valor do serviço a ser pago.")
    numero_nf: int = Field(description="Número da Nota Fiscal de Serviço.")
    data_emissao: date = Field(description="Data em que a nota fiscal foi emitida.")
    valor_total: float = Field(description="Valor total da nota fiscal (bruto).")
    cnpj: str = Field(description="CNPJ da empresa, contendo apenas números.")

class Valida_nota(BaseModel):
    validado: bool = Field(description='valida se o documento enviado é um nota fiscal ou não')
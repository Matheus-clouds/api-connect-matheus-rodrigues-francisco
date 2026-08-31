# API Connect — Gerenciamento de Usuários

API REST de MVP para cadastro e administração de usuários. Foi desenvolvida com **Python 3 e Flask**, escolhidos pela simplicidade, curva de aprendizado curta e capacidade de criar serviços HTTP organizados rapidamente.

## Arquitetura

```
api-connect-usuarios/
├── app/
│   ├── routes/          # Mapeamento HTTP das rotas
│   ├── controllers/     # Manipulação de requisições e respostas
│   ├── services/        # Regras de negócio e validações
│   ├── repositories/    # Persistência temporária em memória
│   ├── errors.py        # Contrato centralizado de erros
│   └── __init__.py      # Factory do Flask
├── tests/               # Testes automatizados
├── run.py               # Ponto de entrada
├── requirements.txt     # Dependências
└── README.md
```

Os dados ficam em um array na memória; por isso, voltam ao estado inicial quando o servidor é reiniciado. A separação em repositório permite trocar essa implementação por banco de dados posteriormente sem mudar as rotas.

## Tecnologias

- Python 3.14
- Flask 3.1.3
- Git e GitHub
- unittest

## Inicialização do projeto

```powershell
git clone https://github.com/Matheus-clouds/api-connect-matheus-rodrigues-francisco.git
cd api-connect-matheus-rodrigues-francisco
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` instala o Flask. Os testes usam o `unittest` da biblioteca padrão, portanto não exigem outra dependência.

Caso a política do PowerShell impeça a ativação do ambiente virtual, execute somente nesta sessão:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Execução e testes

```powershell
python run.py
python -m unittest discover -s tests -v
```

O servidor fica disponível em `http://127.0.0.1:5000`. Para confirmar que está ativo, acesse `GET /health`.

## Endpoints

| Método | Rota | Finalidade | Sucesso |
|---|---|---|---|
| GET | `/api/usuarios` | Lista todos os usuários | 200 |
| GET | `/api/usuarios/{id}` | Busca um usuário | 200 |
| POST | `/api/usuarios` | Cria um usuário | 201 |
| PUT/PATCH | `/api/usuarios/{id}` | Atualiza um usuário | 200 |
| DELETE | `/api/usuarios/{id}` | Remove um usuário | 204 |

### Exemplo de cadastro

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/api/usuarios   -ContentType 'application/json'   -Body '{"nome":"Maria Oliveira","email":"maria@exemplo.com","idade":31}'
```

Campos aceitos: `nome` (obrigatório no cadastro), `email` (obrigatório no cadastro e único) e `idade` (opcional, inteiro entre 0 e 130). No `PATCH`, envie somente os campos a modificar. No `PUT`, envie uma representação completa, contendo ao menos `nome` e `email`.

## Contratos HTTP

Todas as respostas de sucesso são JSON, por exemplo:

```json
{
  "data": {
    "id": 3,
    "nome": "Maria Oliveira",
    "email": "maria@exemplo.com",
    "idade": 31
  },
  "message": "Usuario criado com sucesso."
}
```

Erros seguem uma estrutura previsível:

```json
{
  "error": {
    "status": 400,
    "message": "Dados de entrada invalidos.",
    "details": {
      "email": "Informe um e-mail valido."
    }
  }
}
```

Status empregados: `200` para leitura/atualização, `201` para criação, `204` para remoção (sem corpo, como determina o protocolo), `400` para JSON malformado ou falha de validação, `404` para recurso inexistente, `409` para e-mail já utilizado e `415` para `Content-Type` incorreto.

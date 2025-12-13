# Sistema de Gestão de Estoque - Moto Peças (v2.0) 🏍️

Sistema completo de gerenciamento de inventário (CRUD) desenvolvido em Python. O projeto simula um ambiente real de autopeças, focado em persistência de dados e integridade das informações.

## ⚙️ Funcionalidades Técnicas
O sistema foi refatorado para seguir princípios de **Clean Code** e **Modularização**, incluindo:

- **CRUD Completo via SQL**: Criação, Leitura, Atualização e Exclusão de registros em banco de dados SQLite.
- **Tratamento de Exceções (`try/except`)**: Blindagem do sistema contra entradas inválidas (ex: usuário digitar letras em campos numéricos).
- **Controle de Transações**: Uso de `commit` para garantir a integridade dos dados no banco.
- **Interface de Texto (CLI)**: Menu interativo com loops e validação de input.
- **Regras de Negócio**: Lógica dedicada para controle de entradas e saídas de estoque (não apenas substituição de valores).

## 🛠️ Tecnologias
- **Linguagem**: Python 3.x
- **Banco de Dados**: SQLite3 (Nativo)
- **Paradigma**: Procedural Modularizado

## 🚀 Como Executar
1. Certifique-se de ter o Python instalado.
2. Clone o repositório ou baixe o arquivo `main.py`.
3. Execute no terminal:
   ```bash
   python main.py

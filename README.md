# Sistema de Vendas com controle de Estoque

### Criando o arquivo binário (executável) com o PyInstaller

O PyInstaller é uma ferramenta poderosa para converter scripts Python em executáveis standalone, facilitando a distribuição de suas aplicações. Neste Passo-a-Passo, você aprenderá desde a instalação do PyInstaller até a criação de executáveis, incluindo a inclusão de arquivos adicionais e a utilização de scripts com extensão `.pyw`.

#### Passo 1: Instalar o PyInstaller

Para instalar o PyInstaller, você pode usar o `pip`:

```bash
pip install pyinstaller
```

#### Passo 2: Criar um Executável Simples

Suponha que você tenha um script Python chamado `main.py`. Para criar um executável simples, use o comando:

```bash
pyinstaller --onefile main.py
```

Este comando gera um único arquivo executável a partir do `main.py`.

#### Passo 3: Incluir um Arquivo de Banco de Dados

Se o seu script utiliza um banco de dados (por exemplo, `estoque.db`), você pode incluir este arquivo no executável. Use a opção `--add-data` para adicionar o arquivo de banco de dados:

```bash
pyinstaller --onefile --add-data 'estoque.db:.' main.py
```

Neste comando:
- `--add-data 'estoque.db:.'`: Adiciona o arquivo `estoque.db` ao executável. A sintaxe é `source:destination`, onde `source` é o caminho para o arquivo e `destination` é o caminho onde ele será extraído quando o executável for executado. O ponto (.) indica que o arquivo será extraído no mesmo diretório do executável.

#### Passo 4: Usar Scripts com Extensão `.pyw` (Somente Windows)

Para criar um executável que não abre uma janela de console (útil para aplicações GUI), use um script com extensão `.pyw`. Suponha que você tenha um script `main.pyw`. O comando para criar o executável é:

```bash
pyinstaller --onefile main.pyw
```

#### Passo 5: Resumo de Comandos

- **Criar um executável simples**:
  ```bash
  pyinstaller --onefile main.py
  ```

- **Incluir um arquivo de banco de dados**:
  ```bash
  pyinstaller --onefile --add-data 'estoque.db:.' main.py
  ```

- **Criar um executável que não abre console (somente Windows)**:
  ```bash
  pyinstaller --onefile main.pyw
  ```

### Considerações Finais

1. **Estrutura de Diretórios**:
   Após executar o PyInstaller, você verá novos diretórios e arquivos:
   - **build/**: Diretório temporário usado durante a criação do executável.
   - **dist/**: Contém o executável gerado.
   - **main.spec**: Arquivo de especificação usado pelo PyInstaller. Você pode editá-lo para configurações avançadas.

2. **Distribuição**:
   - O arquivo executável estará localizado no diretório `dist/`.
   - Distribua este arquivo para seus usuários finais. Eles não precisarão de uma instalação do Python para executar sua aplicação.

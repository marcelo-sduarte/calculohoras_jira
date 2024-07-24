# Calculadora de Horas do Jira

# Visão Geral
A Calculadora de Horas do Jira é um projeto em Python projetado para otimizar o processo de rastreamento de horas de trabalho para funcionários em vários squads utilizando dados do Jira e arquivos de funcionários. Aproveitando o poder da biblioteca Pandas, esta ferramenta lê eficientemente arquivos Excel contendo dados do Jira e informações dos funcionários, realiza cálculos para determinar as horas trabalhadas por cada funcionário dentro de seus respectivos squads e entrega resultados abrangentes ao cliente.

# Estrutura de Pastas
    - env
    - input
    - output
        - files
        - logs
    - src
        -libs
        

# Instalação
Para usar a Calculadora de Horas do Jira, siga estes passos:

1. Clone este repositório em sua máquina local:
git clone http://10.10.15.53/sabia/vortx
Instale as dependências necessárias:

2. Instale as bibliotecas necessárias:
pip install -r requirements.txt

3. Configure o repositorio virtual.
python -m venv env

4. Certifique que seus arquivos Excel contendo dados do Jira e informações dos funcionários estejam na pasta [input] e garantindo que sigam o formato especificado.

5. Use as funcao save_credential que consta na lib_process.py para salvar no cofre de senha do windows as senhas que serão utilizadas ou salve manualmente usando teclas Windows + R e digitando  “control.exe keymgr.dll”.

6. Execute o script principal [src/main.py]:
python main.py

7. Revise file [gvars.py] e ajustes os diretorios que serão utilizados no projeto.

8. Todas as bibliotecas usadas no python constam no file [pieces.py]


# Licença
Este projeto é licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter mais detalhes.

Copyright © 2024 Cadmus by Marcelo Duarte. Todos os direitos reservados.
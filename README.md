# BRAMON - site template para estações

Template para criação de site para listagem de capturas das estações associadas a [BRAMON](https://www.bramonmeteor.org).
Você pode ver um exemplo de site rodando visitando o [Meteoros Floripa](https://meteoros.floripa.br) mantido pelo 
operador [Thiago Paes](https://www.mrprompt.com.br).

## Iniciando

Antes de ter o site em funcionamento, você precisa configurar alguns passos

- [GitHub](#GitHub)
- [Git](#Git)
- [Python](#Python)
- [FFMpeg](#Ffmpeg)
- [Simple Form](#Simple_Form)

#### GitHub

Para iniciar, é necessário uma conta no [GitHub](https://github.com) para que possamos utilizar o 
[Github Pages](https://help.github.com/pt/github/working-with-github-pages).

Caso você não possua uma, crie agora para utilizar este recurso ou configure o Jekyll localmente. Efetuando um build
local, você pode publicar diretamente o diretório `_site` em seu servidor.

#### Git

Você precisa ter o [Git](https://git-scm.com/download/win) instalado e configurado em sua máquina.

#### Python 

Para iniciar, você precisa ter o [Python 3.7+](https://www.python.org/) instalado em sua máquina e com o `PATH` 
corretamente configurado. Após isso, entre no diretório `bin` do projeto e instale as dependências com:

```console
pip install -r requirements.txt 
```

#### Simple Form

Para receber emails do site, você precisa gerar um token no [Simple Form](https://getsimpleform.com/) e 
atualizar o arquivo `_config.yml` com seu novo token.

#### FFMpeg

As estações BRAMON possuem por padrão, o [ffmpeg]() instalado no diretório `tools`, geralmente `C:\bramon\tools`,
configure sua variável de ambiente para incluir este diretório em seu *PATH*.

## Configurando o site

Edite o arquivo `_config.yml` para inserir os dados de suas estações, o arquivo contém comentários sobre cada 
configuração necessária.

## Publicando

Para efetuar a publicação do site, você precisa apenas rodar o script `make-posts.py` localizado no diretório `bin` do 
projeto, o mesmo irá atualizar os arquivos necessários, efetuar um commit e um push para o repositório, em alguns minutos
seu site estará publicado - dependendo do número de capturas e etc, o tempo do build pode variar bastante.

## Rodando localmente

Caso você possua o `Docker` instalado, você pode utilizar o container pronto para ver seu site rodando localmente.

```console
docker-compose up
```

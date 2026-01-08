# Assistente Pessoal com Ollama

Assistente pessoal com reconhecimento de voz (STT), síntese de voz (TTS) e processamento de linguagem natural usando Ollama.

## Pré-requisitos

- Python 3.12 ou superior
- Ollama instalado e configurado
- Microfone configurado no sistema
- Placa de áudio funcionando

### Dependências do Sistema (Linux)

```bash
# Para PyAudio (reconhecimento de voz)
sudo apt-get install portaudio19-dev python3-pyaudio

# Para pygame (reprodução de áudio)
sudo apt-get install python3-pygame
```

## Instalação

### 1. Instalar o Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Baixar o modelo base

O projeto usa o modelo `gemma3:270m` como base:

```bash
ollama pull gemma3:270m
```

### 3. Criar o modelo personalizado "servo"

O projeto inclui um modelo personalizado. Para criá-lo:

```bash
ollama create servo -f model/servo.Modelfile
```

Isso criará um modelo chamado "servo" baseado no gemma3:270m com personalidade configurada.

### 4. Executar o servidor Ollama

Em um terminal separado, execute:

```bash
ollama serve
```

Mantenha este terminal aberto enquanto usa o assistente.

### 5. Instalar dependências Python

**Usando Poetry (recomendado):**

```bash
# Instalar Poetry se ainda não tiver
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependências do projeto
poetry install
```

**Usando pip:**

```bash
pip install -r requirements.txt
```

## Execução

### Executar o Assistente

**Com Poetry:**

```bash
poetry run python main.py
```

**Com pip/virtualenv:**

```bash
python main.py
```

### Como Usar

1. O assistente iniciará e mostrará "Escutando..." no console
2. Fale no microfone - o assistente gravará até detectar silêncio
3. Aguarde o reconhecimento e a resposta do assistente
4. A resposta será reproduzida em áudio automaticamente
5. Para sair, diga "sair", "exit" ou "quit"

### Funcionalidades

- **Reconhecimento de Voz**: Captura áudio do microfone até detectar silêncio
- **Síntese de Voz**: Reproduz as respostas em áudio usando Edge TTS
- **Memória Persistente**: Aprende e armazena respostas quando você usa palavras-chave como "aprenda", "escute", "leia", "veja", "treine"
- **Personalidade Configurável**: O modelo tem uma personalidade definida no `servo.Modelfile`

## Estrutura do Projeto

```
ASSISTENTE_PESSOAL/
├── main.py                 # Arquivo principal para executar o assistente
├── src/
│   ├── stt.py             # Reconhecimento de voz (Speech-to-Text)
│   ├── tts.py             # Síntese de voz (Text-to-Speech)
│   ├── servo.py           # Classe principal do assistente com Ollama
│   ├── memory.py          # Gerenciamento de memória persistente
│   └── memory.json        # Arquivo de memória do assistente
├── model/
│   └── servo.Modelfile    # Configuração do modelo Ollama personalizado
├── pyproject.toml         # Configuração do projeto (Poetry)
└── requirements.txt       # Dependências do projeto
```

## Configuração

### Voz TTS

Você pode alterar a voz do TTS editando o arquivo `main.py`:

```python
tts = TTS("pt-BR-ThalitaMultilingualNeural")  # Altere para outra voz
```

Para ver todas as vozes disponíveis, consulte a documentação do Edge TTS.

### Personalidade do Assistente

A personalidade do assistente pode ser modificada editando o arquivo `model/servo.Modelfile` e recriando o modelo:

```bash
ollama create servo -f model/servo.Modelfile
```

## Solução de Problemas

### Erro ao instalar PyAudio

Se tiver problemas ao instalar PyAudio, instale as dependências do sistema primeiro (veja Pré-requisitos).

### Ollama não encontrado

Certifique-se de que o Ollama está instalado e o servidor está rodando:

```bash
ollama serve
```

### Microfone não detectado

Verifique se o microfone está funcionando no sistema e se as permissões estão corretas.

### Modelo "servo" não encontrado

Certifique-se de criar o modelo antes de executar:

```bash
ollama create servo -f model/servo.Modelfile
```
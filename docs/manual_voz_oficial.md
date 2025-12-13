# Manual Técnico: Voz_Oficial (Coqui TTS)

Este documento registra todas as informações técnicas necessárias para configurar, recuperar e utilizar a **Voz_Oficial** para a geração de áudio nos cards.

## 1. Identificação da Voz

*   **Nome:** Voz_Oficial
*   **Arquivo de Referência:** `f:\workspaces_gera_flascards\voice_samples\Voz_Oficial.wav`
*   **Origem:** Extraída do vídeo do YouTube (trecho 00:30-00:40).
*   **Tecnologia:** Coqui TTS (XTTS v2).

## 2. Ambiente de Execução

Devido a restrições do Coqui TTS, é **obrigatório** o uso de **Python 3.10**.

*   **Python Base:** `F:\python310_nuget\tools\python.exe` (Instalação local/portable existente).
*   **Virtual Environment:** `venv_xtts`
*   **Caminho do Venv:** `f:\workspaces_gera_flascards\venv_xtts`

### Como recriar o ambiente (em caso de perda):

```powershell
# 1. Criar o ambiente virtual usando o Python 3.10 específico
F:\python310_nuget\tools\python.exe -m venv venv_xtts

# 2. Ativar o ambiente (opcional, se for rodar comandos manuais)
.\venv_xtts\Scripts\Activate.ps1

# 3. Instalar o Coqui TTS
f:\workspaces_gera_flascards\venv_xtts\Scripts\pip install coqui-tts
```

## 3. Script de Geração

O script responsável pela geração é: `f:\workspaces_gera_flascards\scripts\tts_worker.py`

### Como executar:

O script aceita um arquivo JSON como argumento contendo os parâmetros de geração.

**Comando:**
```powershell
f:\workspaces_gera_flascards\venv_xtts\Scripts\python.exe scripts/tts_worker.py args_xtts.json
```

**Estrutura do JSON (args_xtts.json):**
```json
{
    "text": "Texto que será falado pela voz clonada.",
    "output_path": "caminho/para/arquivo_saida.wav",
    "ref_audio_path": "f:\\workspaces_gera_flascards\\voice_samples\\Voz_Oficial.wav",
    "language": "pt"
}
```

## 4. Notas Importantes

*   **Split de Texto:** O modelo XTTS v2 tem um limite de caracteres (~200 chars) por inferência para garantir qualidade. Para textos longos, é ideal dividir o texto em sentenças e gerar em partes, ou implementar um split automático no worker.
*   **GPU:** O script tentará usar CUDA (GPU NVIDIA) automaticamente se disponível.
*   **Dependência:** O arquivo `Voz_Oficial.wav` **não deve ser deletado**, pois é a "alma" da voz clonada.

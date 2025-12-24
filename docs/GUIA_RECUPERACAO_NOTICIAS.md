# 📰 Guia Completo: Formas de Recuperar Notícias

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Métodos de Recuperação](#métodos-de-recuperação)
4. [Scrapers Disponíveis](#scrapers-disponíveis)
5. [Fluxo de Trabalho](#fluxo-de-trabalho)
6. [Exemplos Práticos](#exemplos-práticos)

---

## 🎯 Visão Geral

O sistema possui **duas formas principais** de recuperar notícias:

### 1️⃣ **Extração Manual via Dashboard** (Recomendado)
- Interface visual intuitiva
- Seleção de fonte e manchetes
- Processamento em fila otimizado
- Controle total sobre o que é processado

### 2️⃣ **Processamento Direto via API** (Programático)
- Uso do `WorkflowManager` diretamente
- Ideal para automação e scripts
- Processamento em lote

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    DASHBOARD (UI)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Extração │  │  Fila de │  │ Galeria  │              │
│  │  Manual  │  │ Rascunhos│  │  Final   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
└───────┼─────────────┼─────────────┼─────────────────────┘
        │             │             │
        ▼             ▼             ▼
┌─────────────────────────────────────────────────────────┐
│              WORKFLOW MANAGER (Orquestrador)             │
│  ┌──────────────────────────────────────────────────┐   │
│  │ • list_headlines()      - Lista manchetes        │   │
│  │ • save_draft_quick()    - Salva rascunho rápido  │   │
│  │ • process_draft_content() - Processa conteúdo    │   │
│  │ • generate_images()     - Gera imagens           │   │
│  │ • generate_video()      - Gera vídeo             │   │
│  └──────────────────────────────────────────────────┘   │
└───────┬─────────────┬─────────────┬─────────────────────┘
        │             │             │
        ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ SCRAPERS │  │ SERVICES │  │   DATA   │
│          │  │          │  │          │
│ • G1     │  │ Ollama   │  │ JSON     │
│ • UOL    │  │ Image    │  │ Images   │
│ • CNN    │  │ Video    │  │ Videos   │
│ • Terra  │  │ Prompt   │  │          │
│ • +11    │  │ Summary  │  │          │
└──────────┘  └──────────┘  └──────────┘
```

---

## 🔄 Métodos de Recuperação

### Método 1: Dashboard - Extração Manual (RECOMENDADO)

#### **Passo a Passo:**

1. **Abrir Dashboard**
   ```bash
   python dashboard.py
   ```

2. **Aba "1. Nova Extração"**
   - Clique em uma fonte de notícias (ex: G1, UOL, CNN Brasil)
   - O sistema busca automaticamente as manchetes mais recentes

3. **Selecionar Manchetes**
   - Marque as notícias que deseja processar
   - Clique em "Salvar Rascunhos"
   - ⚡ **RÁPIDO**: Apenas 2-5 segundos por notícia!

4. **Aba "2. Fila de Rascunhos"**
   - Veja todos os rascunhos pendentes
   - Selecione quais processar
   - Clique em "Gerar Conteúdo"
   - Sistema processa: resumo + prompts + imagens + vídeo

5. **Aba "3. Galeria"**
   - Visualize todos os cards finalizados
   - Clique em um card para ver detalhes
   - Opções: Regenerar imagens, Gerar vídeo, Excluir

#### **Vantagens:**
- ✅ Interface visual intuitiva
- ✅ Controle total sobre seleção
- ✅ Processamento otimizado em fila
- ✅ Feedback visual em tempo real
- ✅ Não bloqueia a UI

---

### Método 2: API Programática

#### **Uso Básico:**

```python
from services.workflow_manager import WorkflowManager

# Inicializar
workflow = WorkflowManager()

# 1. Listar manchetes de uma fonte
headlines = workflow.list_headlines("G1")
# Retorna: [(titulo1, url1), (titulo2, url2), ...]

# 2. Salvar rascunho rápido (apenas scraping)
json_path = workflow.save_draft_quick(
    source_name="G1",
    url="https://g1.globo.com/politica/noticia/...",
    progress_callback=lambda msg: print(msg)
)

# 3. Processar conteúdo do rascunho (resumo + prompts)
data = workflow.process_draft_content(
    json_path=json_path,
    progress_callback=lambda msg: print(msg)
)

# 4. Gerar imagens
workflow.generate_images_for_article(
    json_path=json_path,
    data=data,
    progress_callback=lambda msg: print(msg)
)

# 5. Gerar vídeo
video_path = workflow.generate_video_for_article(
    json_path=json_path,
    data=data,
    progress_callback=lambda msg: print(msg)
)

# 6. Publicar no site
workflow.update_site_and_deploy()
```

#### **Processamento em Lote:**

```python
# Processar múltiplas notícias automaticamente
sources = ["G1", "UOL", "CNN Brasil"]

for source in sources:
    headlines = workflow.list_headlines(source)
    
    # Pegar as 5 primeiras manchetes
    for title, url in headlines[:5]:
        print(f"Processando: {title}")
        
        # Salvar rascunho
        json_path = workflow.save_draft_quick(source, url)
        
        if json_path:
            # Processar conteúdo
            data = workflow.process_draft_content(json_path)
            
            if data:
                # Gerar imagens e vídeo
                workflow.generate_images_for_article(json_path, data)
                workflow.generate_video_for_article(json_path, data)

# Atualizar site uma vez no final
workflow.update_site_and_deploy()
```

---

## 📡 Scrapers Disponíveis

O sistema possui **15 scrapers especializados**:

| Fonte | Classe | Características |
|-------|--------|-----------------|
| **G1** | `G1Scraper` | Portal Globo, cobertura ampla |
| **UOL** | `UOLScraper` | Notícias gerais, política, economia |
| **Terra** | `TerraScraper` | Portal tradicional brasileiro |
| **Brasil 247** | `Brasil247Scraper` | Foco em política progressista |
| **CNN Brasil** | `CNNBrasilScraper` | Notícias internacionais e nacionais |
| **Estadão** | `EstadaoScraper` | Jornalismo tradicional |
| **Folha** | `FolhaScraper` | Folha de S.Paulo |
| **Metrópoles** | `MetropolesScraper` | Notícias de Brasília e Brasil |
| **R7 Notícias** | `R7Scraper` | Portal Record |
| **Veja** | `VejaScraper` | Revista semanal |
| **Valor Econômico** | `ValorScraper` | Foco em economia e negócios |
| **Exame** | `ExameScraper` | Negócios e tecnologia |
| **IstoÉ** | `IstoeScraper` | Revista semanal |
| **CartaCapital** | `CartaCapitalScraper` | Política e sociedade |
| **Correio Braziliense** | `CorreioBrazilienseScraper` | Notícias de Brasília |

### **Características dos Scrapers:**

Cada scraper implementa:

1. **`list_headlines()`** - Busca manchetes da página principal
   - Filtra apenas notícias reais (não entretenimento, esportes, etc.)
   - Remove duplicatas
   - Limita a 20 manchetes mais relevantes

2. **`scrape(url)`** - Extrai conteúdo completo de uma notícia
   - Título
   - Conteúdo (parágrafos)
   - Autor/Fonte
   - URL original

3. **Filtros Inteligentes:**
   - ✅ Apenas URLs de notícias válidas
   - ❌ Exclui: entretenimento, esportes, blogs, vídeos
   - ✅ Títulos com mínimo de 20-30 caracteres
   - ✅ Conteúdo com parágrafos substanciais

---

## 🔄 Fluxo de Trabalho Completo

### **Fluxo Otimizado (Sistema Atual):**

```
1. EXTRAÇÃO RÁPIDA (2-5s por notícia)
   └─> list_headlines(fonte)
   └─> save_draft_quick(url)
       ├─> Scraping do conteúdo
       ├─> Salva JSON com status "draft_pending"
       └─> Retorna imediatamente

2. PROCESSAMENTO EM LOTE (60-90s por notícia)
   └─> process_draft_content(json_path)
       ├─> Gera resumo jornalístico (Ollama)
       ├─> Gera prompts para imagens (Ollama)
       ├─> Valida qualidade do conteúdo
       └─> Atualiza JSON com status "draft_ready"

3. GERAÇÃO DE MÍDIA (30-60s por notícia)
   └─> generate_images_for_article()
       ├─> Gera 4 imagens (ComfyUI/SDXL)
       └─> Aplica overlays de texto
   └─> generate_video_for_article()
       ├─> Gera áudios (Edge TTS)
       ├─> Combina imagens + áudio
       └─> Cria vídeo final (MoviePy)

4. PUBLICAÇÃO
   └─> update_site_and_deploy()
       ├─> Atualiza index.html
       ├─> Copia arquivos para site
       └─> Deploy automático
```

### **Estrutura de Dados:**

```json
{
  "title": "Título da Notícia",
  "source": "G1",
  "url": "https://...",
  "author": "Nome do Autor",
  "content": "Conteúdo completo...",
  "status": "draft_pending | draft_ready | published",
  "summary": {
    "introduction": "...",
    "development": "...",
    "conclusion": "..."
  },
  "prompts": {
    "general_summary": "...",
    "introduction": "...",
    "development": "...",
    "conclusion": "..."
  },
  "tiktok_summary": "Resumo curto para vídeo"
}
```

---

## 💡 Exemplos Práticos

### **Exemplo 1: Adicionar Notícias Manualmente**

```python
# Via Dashboard (RECOMENDADO)
# 1. Abra dashboard.py
# 2. Aba "1. Nova Extração"
# 3. Clique em "G1"
# 4. Selecione 5 manchetes
# 5. Clique "Salvar Rascunhos"
# 6. Vá para aba "2. Fila de Rascunhos"
# 7. Selecione todas
# 8. Clique "Gerar Conteúdo"
```

### **Exemplo 2: Script de Automação Diária**

```python
#!/usr/bin/env python
"""
Script para coletar notícias automaticamente
Executar diariamente via cron/task scheduler
"""
from services.workflow_manager import WorkflowManager
import datetime

def coletar_noticias_diarias():
    workflow = WorkflowManager()
    
    # Fontes prioritárias
    fontes = ["G1", "UOL", "CNN Brasil", "Folha"]
    
    print(f"[{datetime.datetime.now()}] Iniciando coleta diária...")
    
    total_processadas = 0
    
    for fonte in fontes:
        print(f"\n=== Processando {fonte} ===")
        
        # Buscar manchetes
        headlines = workflow.list_headlines(fonte)
        
        # Pegar as 3 primeiras
        for title, url in headlines[:3]:
            print(f"  → {title[:50]}...")
            
            # Salvar rascunho rápido
            json_path = workflow.save_draft_quick(fonte, url)
            
            if json_path:
                total_processadas += 1
    
    print(f"\n✅ Total de notícias coletadas: {total_processadas}")
    print("Use o dashboard para processar os rascunhos.")

if __name__ == "__main__":
    coletar_noticias_diarias()
```

### **Exemplo 3: Processar Rascunhos Pendentes**

```python
import glob
import json
from services.workflow_manager import WorkflowManager

def processar_rascunhos_pendentes():
    workflow = WorkflowManager()
    
    # Buscar todos os JSONs
    json_files = glob.glob("data/*/*.json")
    
    pendentes = []
    for json_path in json_files:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Verificar se está pendente
        if data.get('status') == 'draft_pending':
            pendentes.append(json_path)
    
    print(f"Encontrados {len(pendentes)} rascunhos pendentes")
    
    for i, json_path in enumerate(pendentes, 1):
        print(f"\n[{i}/{len(pendentes)}] Processando {json_path}")
        
        # Processar conteúdo
        data = workflow.process_draft_content(json_path)
        
        if data:
            # Gerar imagens
            workflow.generate_images_for_article(json_path, data)
            
            # Gerar vídeo
            workflow.generate_video_for_article(json_path, data)
    
    # Atualizar site
    workflow.update_site_and_deploy()
    print("\n✅ Processamento completo!")

if __name__ == "__main__":
    processar_rascunhos_pendentes()
```

---

## 🎯 Recomendações

### **Para Uso Diário:**
1. ✅ Use o **Dashboard** para seleção manual
2. ✅ Adicione rascunhos rapidamente (aba 1)
3. ✅ Processe em lote quando tiver tempo (aba 2)
4. ✅ Revise na galeria antes de publicar (aba 3)

### **Para Automação:**
1. ✅ Use `save_draft_quick()` para coleta rápida
2. ✅ Execute processamento em horários de baixo uso
3. ✅ Monitore logs para detectar erros
4. ✅ Faça backup dos JSONs regularmente

### **Melhores Práticas:**
- 📌 Colete notícias pela manhã (conteúdo fresco)
- 📌 Processe em lote à noite (menos carga)
- 📌 Revise manualmente antes de publicar
- 📌 Mantenha diversidade de fontes
- 📌 Evite duplicatas (mesmo assunto, fontes diferentes)

---

## 🔧 Troubleshooting

### **Problema: Scraper não retorna manchetes**
```python
# Solução: Verificar se o site mudou estrutura
scraper = workflow.scrapers["G1"]
soup = scraper.get_soup(scraper.base_url)
print(soup.prettify()[:1000])  # Inspecionar HTML
```

### **Problema: Timeout do Ollama**
```python
# Solução: Aumentar timeout ou usar modelo menor
# Em workflow_manager.py, linha ~25:
self.model_name = "llama3.2:3b"  # Modelo mais rápido
```

### **Problema: Imagens não são geradas**
```python
# Solução: Verificar ComfyUI
# 1. ComfyUI está rodando?
# 2. Modelos estão carregados?
# 3. Verificar logs em services/image_service.py
```

---

## 📚 Referências

- **Código Principal:** `services/workflow_manager.py`
- **Scrapers:** `scrapers/optimized_scrapers.py`
- **Dashboard:** `dashboard.py`
- **Documentação Adicional:** `docs/GUIA_CRIAR_CARD.md`

---

**Última Atualização:** 24/12/2024
**Versão:** 2.0

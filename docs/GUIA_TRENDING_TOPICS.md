# 🔥 Guia: Buscar Notícias Trending (Mais Quentes)

## 📋 O que são Trending Topics?

O sistema agora pode **analisar múltiplas fontes simultaneamente** para identificar os **assuntos mais falados do momento**!

### Como Funciona:

1. **Coleta** manchetes de 6 fontes principais (G1, UOL, CNN Brasil, Folha, Estadão, Metrópoles)
2. **Analisa** palavras-chave mais frequentes
3. **Identifica** notícias relacionadas aos temas quentes
4. **Classifica** por relevância (score baseado em keywords trending)

---

## 🚀 3 Formas de Usar

### 1️⃣ Via Dashboard (MAIS FÁCIL)

**Passo a Passo:**

1. Abra o dashboard:
   ```bash
   python dashboard.py
   ```

2. Vá para **Aba "1. Nova Extração"**

3. Clique no botão **🔥 TRENDING TOPICS** (laranja, grande)

4. Aguarde a análise (15-30 segundos)

5. Veja as **top 20 notícias mais quentes** com:
   - Fonte original
   - Título completo
   - Palavras-chave trending marcadas com 🔥

6. Selecione as notícias desejadas

7. Clique em **"Salvar Rascunhos"**

8. Processe na **Aba "2. Fila de Rascunhos"**

**Vantagens:**
- ✅ Interface visual
- ✅ Vê as palavras-chave trending
- ✅ Seleciona manualmente quais salvar
- ✅ Feedback em tempo real

---

### 2️⃣ Via Script Interativo (RÁPIDO)

```bash
python buscar_noticias_quentes.py
```

**O que faz:**
1. Busca trending topics automaticamente
2. Mostra top 15 palavras-chave mais quentes
3. Mostra top 20 notícias mais relevantes
4. Pergunta quantas você quer salvar
5. Salva como rascunhos automaticamente

**Exemplo de saída:**
```
🔥 PALAVRAS-CHAVE MAIS QUENTES
1. lula               ████████████ (12)
2. governo            ██████████ (10)
3. brasil             █████████ (9)
4. presidente         ████████ (8)
5. economia           ███████ (7)

📰 NOTÍCIAS MAIS RELEVANTES (TOP 20)
1. [G1] Score: 45
   Lula anuncia novo pacote econômico para o Brasil
   🔥 lula, governo, economia

💾 Quantas notícias deseja salvar? (0-20): 5
```

---

### 3️⃣ Via Script Avançado (CONTROLE TOTAL)

```bash
# Apenas visualizar (não salva)
python scripts/buscar_trending_topics.py

# Salvar as top 10 automaticamente
python scripts/buscar_trending_topics.py --save 10

# Buscar mais manchetes por fonte
python scripts/buscar_trending_topics.py --max-per-source 30 --save 15
```

**Parâmetros:**
- `--save N`: Salva as top N notícias como rascunhos
- `--max-per-source N`: Máximo de manchetes por fonte (padrão: 20)

---

## 📊 Como o Score é Calculado

Cada notícia recebe um **score de relevância** baseado em:

```python
Score = Σ (frequência de cada keyword trending na notícia)
```

**Exemplo:**

Se a notícia contém:
- "lula" (aparece 12x em outras manchetes) → +12
- "governo" (aparece 10x) → +10
- "economia" (aparece 7x) → +7
- **Score total = 29**

Quanto **maior o score**, mais **relevante** é a notícia para os trending topics!

---

## 🎯 Casos de Uso

### Caso 1: Cobertura de Última Hora

**Situação:** Aconteceu algo importante e você quer cobrir rapidamente.

**Solução:**
```bash
python buscar_noticias_quentes.py
# Salva as top 5-10 notícias
# Processa no dashboard
```

### Caso 2: Curadoria Diária

**Situação:** Todo dia você quer pegar as notícias mais relevantes.

**Solução:**
1. Dashboard → 🔥 TRENDING TOPICS
2. Revisa manualmente as top 20
3. Seleciona as mais interessantes
4. Salva e processa

### Caso 3: Automação Completa

**Situação:** Quer automatizar tudo via cron/scheduler.

**Solução:**
```bash
# Cron diário às 8h
0 8 * * * cd /path/to/projeto && python scripts/buscar_trending_topics.py --save 10
```

---

## 🔍 Fontes Analisadas

O sistema analisa **6 fontes principais**:

1. **G1** - Portal Globo
2. **UOL** - Portal UOL
3. **CNN Brasil** - CNN Brasil
4. **Folha** - Folha de S.Paulo
5. **Estadão** - O Estado de S.Paulo
6. **Metrópoles** - Portal Metrópoles

**Por que essas fontes?**
- ✅ Alta frequência de atualização
- ✅ Cobertura ampla de temas
- ✅ Scrapers otimizados e confiáveis
- ✅ Representam diferentes linhas editoriais

---

## 🛠️ Personalização

### Adicionar Mais Fontes

Edite `scripts/buscar_trending_topics.py`:

```python
self.priority_sources = [
    "G1",
    "UOL", 
    "CNN Brasil",
    "Folha",
    "Estadão",
    "Metrópoles",
    "Veja",        # Adicionar
    "R7 Notícias"  # Adicionar
]
```

### Ajustar Stopwords

Adicione palavras a ignorar:

```python
self.stopwords = {
    'de', 'da', 'do', # ... existentes
    'nova',  # Adicionar
    'novo',  # Adicionar
}
```

### Mudar Número de Resultados

```python
# No dashboard (linha ~233)
trending_news = results['trending_news'][:30]  # Era 20

# No script
python scripts/buscar_trending_topics.py --save 20  # Era 10
```

---

## 📈 Exemplos de Output

### Dashboard:
```
🔥 Encontradas 20 notícias quentes! 
Palavras-chave: lula, governo, brasil, economia, presidente

☑ [G1] Lula anuncia pacote econômico 🔥 lula, governo, economia
☑ [UOL] Governo estuda novas medidas 🔥 governo, brasil
☑ [CNN Brasil] Presidente fala sobre economia 🔥 presidente, economia
...
```

### Script:
```
🔥 PALAVRAS-CHAVE MAIS QUENTES
1. lula               ████████████ (12)
2. governo            ██████████ (10)
3. brasil             █████████ (9)
4. presidente         ████████ (8)
5. economia           ███████ (7)
6. congresso          ██████ (6)
7. senado             █████ (5)
8. câmara             █████ (5)
9. reforma            ████ (4)
10. tributária        ████ (4)

📰 NOTÍCIAS MAIS RELEVANTES (TOP 20)
1. [G1] Score: 45
   Lula anuncia novo pacote econômico para o Brasil
   🔥 lula, governo, economia
   🔗 https://g1.globo.com/...

2. [UOL] Score: 38
   Governo apresenta reforma tributária no Congresso
   🔥 governo, reforma, tributária
   🔗 https://www.uol.com.br/...
```

---

## ⚡ Performance

### Tempo de Execução:

- **Coleta de manchetes**: ~15-20 segundos (6 fontes)
- **Análise de keywords**: ~1-2 segundos
- **Classificação**: Instantâneo
- **Total**: ~20-25 segundos

### Otimizações:

- Scrapers paralelos (futuro)
- Cache de manchetes (futuro)
- Análise incremental (futuro)

---

## 🐛 Troubleshooting

### Problema: "Nenhuma notícia trending encontrada"

**Causas:**
- Fontes fora do ar
- Mudança na estrutura HTML dos sites
- Problemas de conexão

**Solução:**
```bash
# Testar fontes individualmente
python dashboard.py
# Clicar em cada fonte para ver qual funciona
```

### Problema: Palavras-chave irrelevantes

**Solução:**
Adicione às stopwords em `buscar_trending_topics.py`:

```python
self.stopwords.update({
    'palavra_irrelevante_1',
    'palavra_irrelevante_2',
})
```

### Problema: Script muito lento

**Solução:**
Reduza o número de manchetes por fonte:

```bash
python scripts/buscar_trending_topics.py --max-per-source 10
```

---

## 💡 Dicas Pro

### 1. Combine com Fontes Específicas

```python
# Primeiro: Trending topics gerais
# Depois: Fonte específica para aprofundar
```

### 2. Use Horários Estratégicos

- **Manhã (8h-10h)**: Notícias do dia anterior
- **Tarde (14h-16h)**: Notícias do dia
- **Noite (20h-22h)**: Resumo do dia

### 3. Monitore Palavras-chave

Crie um log das palavras-chave trending:

```bash
python scripts/buscar_trending_topics.py > trending_$(date +%Y%m%d).log
```

### 4. Automação Inteligente

```bash
#!/bin/bash
# Script diário
python scripts/buscar_trending_topics.py --save 10
sleep 3600  # Aguardar 1h
python dashboard.py  # Processar rascunhos
```

---

## 📚 Referências

- **Script Principal**: `scripts/buscar_trending_topics.py`
- **Script Rápido**: `buscar_noticias_quentes.py`
- **Dashboard**: `dashboard.py` (botão 🔥 TRENDING TOPICS)
- **Documentação Geral**: `docs/GUIA_RECUPERACAO_NOTICIAS.md`

---

**Última Atualização:** 24/12/2024
**Versão:** 1.0

# 🔧 Guia: Recuperar Cards com Erros (ComfyUI Desligado)

## 🎯 Problema Comum

Você tentou gerar cards mas **esqueceu de ligar o ComfyUI**?

**Resultado:**
- ✅ Resumos gerados (Ollama)
- ✅ Prompts gerados (Ollama)
- ❌ **Imagens NÃO geradas** (ComfyUI estava off)
- ❌ Vídeos não gerados (dependem das imagens)

---

## 🔍 Passo 1: Verificar Status dos Cards

```bash
python verificar_cards.py
```

**O que mostra:**
```
📊 VERIFICAÇÃO DE STATUS DOS CARDS
===================================

✅ CARDS COMPLETOS
1. Notícia sobre economia
2. Notícia sobre política
Total: 2 cards completos

🖼️ CARDS SEM IMAGENS (ComfyUI estava desligado?)
1. Lula anuncia pacote econômico
   ❌ Faltam: general_summary.png, introduction.png, development.png, conclusion.png
2. Governo estuda reforma
   ❌ Faltam: general_summary.png, introduction.png, development.png, conclusion.png
Total: 2 cards sem imagens

💡 SOLUÇÃO:
   1. Ligue o ComfyUI
   2. Execute: python reprocessar_imagens.py
```

---

## 🚀 Passo 2: Ligar o ComfyUI

### **Opção A: Manual**
```bash
# Ir para pasta do ComfyUI
cd C:\path\to\ComfyUI

# Executar
python main.py
```

### **Opção B: Via Dashboard (NOVO!)**
```
Dashboard → Indicador de status do ComfyUI
→ Se estiver vermelho, clique para ligar
```

---

## 🔄 Passo 3: Reprocessar Imagens

```bash
python reprocessar_imagens.py
```

**Fluxo interativo:**
```
⚠️ IMPORTANTE: Certifique-se que o ComfyUI está LIGADO!
ComfyUI está rodando? (s/n): s

📊 Encontrados 2 cards sem imagens completas:
 1. Lula anuncia pacote econômico
    ❌ Faltam: general_summary.png, introduction.png, ...
 2. Governo estuda reforma
    ❌ Faltam: general_summary.png, introduction.png, ...

Reprocessar 2 cards? (s/n): s

🚀 INICIANDO REPROCESSAMENTO
================================

[1/2] Processando: Lula anuncia pacote econômico...
    🎨 Gerando imagem: general_summary
    🎨 Gerando imagem: introduction
    🎨 Gerando imagem: development
    🎨 Gerando imagem: conclusion
    ✅ Imagens geradas com sucesso!

[2/2] Processando: Governo estuda reforma...
    🎨 Gerando imagem: general_summary
    🎨 Gerando imagem: introduction
    🎨 Gerando imagem: development
    🎨 Gerando imagem: conclusion
    ✅ Imagens geradas com sucesso!

📊 RESUMO DO REPROCESSAMENTO
================================
✅ Sucesso:  2/2
❌ Erros:    0/2
```

---

## ✅ Passo 4: Verificar Novamente

```bash
python verificar_cards.py
```

**Agora deve mostrar:**
```
✅ CARDS COMPLETOS
1. Lula anuncia pacote econômico
2. Governo estuda reforma
3. Notícia sobre economia
4. Notícia sobre política
Total: 4 cards completos
```

---

## 🎬 Passo 5: Gerar Vídeos (Opcional)

### **Via Dashboard:**
```
1. Aba 3: Galeria
2. Clicar no card
3. Botão "Gerar Vídeo"
```

### **Via Script:**
```bash
python generate_all_videos.py
```

---

## 📋 Checklist de Prevenção

Antes de processar cards, verifique:

```
☐ Ollama está rodando?
   → Dashboard mostra status
   → Ou: ollama serve

☐ ComfyUI está rodando?
   → Dashboard mostra status (NOVO!)
   → Ou: cd ComfyUI && python main.py

☐ Modelos carregados?
   → SDXL Turbo
   → VAE
   → LoRAs (se usar)
```

---

## 🔧 Troubleshooting

### **Problema: "ComfyUI não responde"**

**Solução:**
```bash
# Verificar se está rodando
curl http://localhost:8188

# Se não responder, reiniciar
# Fechar ComfyUI
# Abrir novamente
cd ComfyUI
python main.py
```

---

### **Problema: "Imagens geradas mas estão pretas"**

**Causa:** VAE incorreto

**Solução:**
```python
# Verificar em services/image_service.py
# Deve usar: sdxl_vae.safetensors
```

---

### **Problema: "Erro de memória no ComfyUI"**

**Solução:**
```
1. Fechar outros programas
2. Usar --lowvram no ComfyUI
3. Reduzir batch size
4. Processar cards um por vez
```

---

### **Problema: "Script diz que faltam imagens mas elas existem"**

**Solução:**
```bash
# Verificar nomes dos arquivos
# Devem ser exatamente:
- general_summary.png
- introduction.png
- development.png
- conclusion.png

# Verificar no diretório do card
cd data/nome_do_card
ls *.png
```

---

## 💡 Dicas Pro

### **1. Sempre verifique antes**
```bash
python verificar_cards.py
```

### **2. Processe em lotes pequenos**
```
5-10 cards por vez
Evita sobrecarga
```

### **3. Use o dashboard**
```
Mostra status em tempo real
Indica quando há erro
```

### **4. Mantenha logs**
```bash
python reprocessar_imagens.py > reprocess.log 2>&1
```

---

## 🎯 Resumo Rápido

```
ERRO: Cards sem imagens (ComfyUI estava off)

SOLUÇÃO:
1. python verificar_cards.py          # Ver quais faltam
2. Ligar ComfyUI                       # Manual ou dashboard
3. python reprocessar_imagens.py       # Reprocessar
4. python verificar_cards.py           # Confirmar
5. Gerar vídeos (opcional)             # Dashboard ou script
```

---

## 📊 Fluxo Visual

```
Cards com Erro
     ↓
Verificar Status
     ↓
Ligar ComfyUI
     ↓
Reprocessar Imagens
     ↓
Verificar Novamente
     ↓
Gerar Vídeos
     ↓
Publicar
```

---

## 🚨 Prevenção Futura

### **Adicionar ao Workflow:**

```
ANTES de processar cards:

1. ✅ Verificar Ollama
   Dashboard → Indicador verde

2. ✅ Verificar ComfyUI
   Dashboard → Indicador verde (NOVO!)

3. ✅ Processar
   Aba 2 → Gerar Conteúdo

4. ✅ Verificar
   python verificar_cards.py
```

---

## 📚 Scripts Disponíveis

| Script | Função |
|--------|--------|
| `verificar_cards.py` | Verifica status de todos os cards |
| `reprocessar_imagens.py` | Reprocessa apenas imagens faltantes |
| `generate_all_videos.py` | Gera vídeos para todos os cards |

---

## 🎊 Conclusão

**Não se preocupe!** 

Esquecer de ligar o ComfyUI é comum. Com estes scripts, você pode:

✅ **Identificar** rapidamente quais cards falharam  
✅ **Reprocessar** apenas o que faltou  
✅ **Economizar** tempo (não precisa refazer tudo)  
✅ **Prevenir** no futuro com checklist  

---

**Última Atualização:** 24/12/2024
**Versão:** 1.0

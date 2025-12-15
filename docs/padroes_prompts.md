# Padrões de Geração de Prompts (FlashCards AI)

Este documento define as normas para criação de prompts para geração de imagens do Lula (e outros temas) utilizando o modelo **Cheyenne v2.2** e **LoRA**.

## 1. Estrutura do Prompt

O prompt deve seguir rigorosamente a seguinte estrutura sequencial:

`[TRIGGER] + [AÇÃO/SUJEITO] + [CONTEXTO/CENÁRIO] + [DETALHES VISUAIS] + [SUFIXO DE ESTILO]`

### Componentes:

*   **TRIGGER (Obrigatório):** `lula`
    *   Deve ser sempre a primeira palavra para ativar o LoRA.
*   **AÇÃO/SUJEITO:** Descrição do que ele está fazendo.
    *   *Ex:* `sitting at desk`, `speaking at podium`, `shaking hands`.
*   **CONTEXTO/CENÁRIO:** Onde ele está ou elementos de fundo.
    *   *Ex:* `presidential office background`, `brazilian flag in background`, `political rally crowd`.
*   **DETALHES VISUAIS:** Iluminação, expressão, enquadramento.
    *   *Ex:* `serious expression`, `warm lighting`, `cinematic lighting`, `close up`.
*   **SUFIXO DE ESTILO (Congelado):**
    *   `, detailed, sharp, HD, HDR, best quality, best resolution, 2D, colored Graphic Novel illustration, By Gibrat, hatching, lineart, sketch, hyper illustration, vibrant, saturated`

## 2. Prompt Negativo (Padrão)

Deve ser usado em todas as gerações para garantir limpeza e evitar deformações.

`simple background, cartoon, anime, distorted, low quality, blurry, text, watermark, signature, bad anatomy, bad hands, missing fingers`

## 3. Diretrizes de Conteúdo

1.  **Tradução Visual:** Não tente descrever conceitos abstratos complexos. Transforme o texto da notícia em uma cena visual concreta.
    *   *Ruim:* "Democracia e liberdade"
    *   *Bom:* "Lula casting a vote in a ballot box, smiling"
2.  **Sem Texto:** Evite pedir para escrever palavras na imagem (o modelo não sabe escrever bem).
3.  **Foco no Sujeito:** O LoRA foi treinado com foco no rosto/pessoa. Mantenha o sujeito em destaque.

## 4. Configurações Técnicas (Cheyenne + LoRA)

*   **Steps:** `10` a `20` (Para Cheyenne v2.2) ou `30` (Para Alta Fidelidade).
*   **CFG Scale:** `3.5` (Ideal para liberdade criativa mantendo coerência).
*   **Resolution:** `1024x1024` (SDXL Native).

## 5. Melhores Práticas e Correções (Aprendizado)

Baseado em testes, as seguintes práticas garantem melhor consistência:

1.  **Reforço de Identidade:** O LoRA pode falhar em prompts casuais. Sempre adicione `man` ou `male` logo após o trigger se o sujeito estiver ambíguo.
    *   *Ex:* `lula, man, holding a tablet...`
2.  **Conceitos Aprovados (Bom Desempenho):**
    *   *Escritório/Mesa:* `sitting at presidential desk, writing...`
    *   *Tech/Comunicação:* `holding a phone`, `holding a tablet` (com reforço de gênero).
    *   *Diplomacia:* `shaking hands`, `flanked by flags`.
3.  **Evitar:**
    *   Backgrounds genéricos que confundem a escala (ex: Mapas gigantes mal integrados).
    *   Poses onde o rosto fica obstruído ou muito distante sem reforço de identidade.

4.  **Contexto e Relevância (CRITICIDADE ALTA)**
    *   **Não force o personagem:** Se a notícia não for sobre o Lula, **NÃO** use o trigger `lula` nem carregue no visual dele. Use descrições genéricas (`brazilian government official`, `minister`, `judge`).
    *   *Ex:* Notícia sobre Economia/Bancos -> Use `bank executive`, `financial graphs`.
    *   *Ex:* Notícia sobre STF -> Use `judge in court`, `scales of justice`.

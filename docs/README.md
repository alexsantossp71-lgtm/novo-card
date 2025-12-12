# FlashCards News Gallery - GitHub Pages Guide

Este site foi gerado automaticamente para ser hospedado no GitHub Pages.

## Como colocar no ar (Deploy)

1.  **Suba os arquivos para o GitHub:**
    Certifique-se de que a pasta `docs/` foi enviada para o seu repositório (comitar e dar push).

2.  **Configure o GitHub Pages:**
    *   Vá na página do seu repositório no GitHub.
    *   Clique em **Settings** (Configurações) > **Pages** (no menu lateral esquerdo).
    *   Em **Build and deployment** > **Source**, escolha "Deploy from a branch".
    *   Em **Branch**, selecione `main` (ou `master`) e na pasta selecione `/docs`.
    *   Clique em **Save**.

3.  **Acesse:**
    O GitHub vai gerar um link (ex: `https://seu-usuario.github.io/nome-do-repo/`).
    Aguarde alguns minutos e acesse.

## Atualizando o Site
Sempre que gerar novas imagens com o dashboard:
1.  Rode `python build_site.py` localmente.
2.  Faça o commit e push das mudanças na pasta `docs/`.
3.  O site será atualizado automaticamente pelo GitHub.

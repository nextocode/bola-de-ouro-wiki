# Como contribuir

Obrigado por ajudar a manter esta wiki correta e atualizada! Existem dois tipos principais de contribuição: **corrigir dados** e **atualizar após a cerimônia**.

## Como funciona o repositório

Os dados ficam em `data/*.csv`, que são a **fonte única de verdade**. As páginas `docs/vencedores-masculino.md`, `docs/vencedoras-feminino.md` e `docs/ranking.md`, e os arquivos `data/*.json`, são **geradas** pelo script `scripts/build_docs.py`. Nunca edite essas páginas à mão: altere o CSV e rode o script.

Páginas escritas à mão (podem ser editadas diretamente): `README.md`, `docs/historia.md`, `docs/perfis.md`, `docs/recordes-e-curiosidades.md` e `docs/brasileiros.md`.

## Corrigir um dado

1. Abra o CSV correspondente em `data/`.
2. Corrija a linha. Colunas: `ano`, `jogador`, `nacionalidade` (texto exibido), `paises` (usado nos rankings; separe dupla nacionalidade com `;`), `clube` e `observacao`.
3. Rode `python3 scripts/build_docs.py`.
4. Faça commit do CSV **e** dos arquivos regenerados, e abra um pull request citando uma fonte confiável.

## Como atualizar após a cerimônia

A cerimônia de 2026 (70ª edição) está marcada para **26 de outubro de 2026**, em Londres. Depois dela:

1. Acrescente uma linha ao final de `data/vencedores-masculino.csv` e outra em `data/vencedoras-feminino.csv`, por exemplo:

   ```csv
   2026,Nome do Jogador,Nacionalidade,País,Clube,
   ```

   Use o **clube do jogador na época da premiação**. Se o jogador já venceu antes, repita exatamente o mesmo nome para que a contagem de títulos funcione.
2. Rode `python3 scripts/build_docs.py`.
3. Atualize à mão os trechos que citam "até 2025":
   - `README.md`: tabela de resumo (edições concedidas, jogadores diferentes, vencedor mais recente), aviso de "próxima edição" e o texto "até a edição 2025";
   - `docs/historia.md`: seção "2026: a 70ª edição";
   - `docs/recordes-e-curiosidades.md` e `docs/perfis.md`: recordes, sequências e a seção "Quem nunca ganhou";
   - `docs/brasileiros.md`: número de edições desde o último brasileiro e eventuais brasileiros no pódio.
4. Confira o resultado em o site da _France Football_ (https://www.francefootball.fr/) antes de publicar.

## Estilo

- Português do Brasil, texto objetivo e factual.
- Cite números e nomes apenas quando tiver segurança; na dúvida, abra uma issue.
- Mantenha a convenção de nomes dos clubes e países já usada nos CSVs.

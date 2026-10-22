# 🏆 Wiki da Bola de Ouro

> Tudo sobre os vencedores do prêmio de **melhor jogador do mundo**: a lista completa de 1956 a 2025, rankings, recordes, perfis dos maiores campeões e curiosidades.

A **Bola de Ouro** (_Ballon d'Or_) é concedida pela revista francesa _France Football_ desde 1956. Esta wiki reúne os dados em português e mantém tudo em arquivos simples (Markdown + CSV/JSON), fáceis de ler, corrigir e reaproveitar.

> ⏳ **Próxima edição:** a cerimônia de 2026 (70ª edição) está marcada para **26 de outubro de 2026, em Londres**, a primeira vez que o prêmio sai de Paris. Este repositório cobre as edições **até 2025**. Veja [como atualizar](CONTRIBUTING.md#como-atualizar-após-a-cerimônia) quando o resultado sair.

---

## 📌 Resumo rápido (até a edição 2025)

| | |
|---|---|
| **Primeira edição** | 1956, vencida por Stanley Matthews |
| **Edições masculinas concedidas** | 69 (a de 2020 foi cancelada pela pandemia) |
| **Jogadores diferentes premiados** | 47 |
| **Maior vencedor** | Lionel Messi, com **8** títulos |
| **Segundo maior** | Cristiano Ronaldo, com **5** títulos |
| **Vencedor mais recente (masc.)** | Ousmane Dembélé (2025, Paris Saint-Germain) |
| **Vencedora mais recente (fem.)** | Aitana Bonmatí (2025, Barcelona), tricampeã consecutiva |
| **Último brasileiro vencedor** | Kaká (2007) |

---

## 📚 Índice

| Página | O que você encontra |
|---|---|
| [🏅 Vencedores (masculino)](docs/vencedores-masculino.md) | Tabela completa de 1956 a 2025, com clube, nacionalidade e número do título |
| [🏅 Vencedoras (feminino)](docs/vencedoras-feminino.md) | Todas as vencedoras desde a criação, em 2018 |
| [📊 Ranking de vencedores](docs/ranking.md) | Por jogador, país, clube e década |
| [⭐ Perfis dos grandes campeões](docs/perfis.md) | Quem são os multicampeões e os vencedores que marcaram época |
| [📜 História e regras](docs/historia.md) | Origem, critérios, votação, fusão com a FIFA e troféus paralelos |
| [🎯 Recordes e curiosidades](docs/recordes-e-curiosidades.md) | Mais jovem, mais velho, sequências, quem nunca ganhou e mais |
| [🇧🇷 Brasileiros na Bola de Ouro](docs/brasileiros.md) | Ronaldo, Rivaldo, Ronaldinho, Kaká e os que chegaram perto |

---

## 🗂️ Estrutura do repositório

```text
.
├── README.md                      # esta página (home da wiki)
├── CONTRIBUTING.md                # como corrigir dados e atualizar após cada cerimônia
├── LICENSE
├── data/
│   ├── vencedores-masculino.csv   # fonte única de verdade (masculino)
│   ├── vencedoras-feminino.csv    # fonte única de verdade (feminino)
│   └── *.json                     # mesmos dados em JSON, para uso em projetos
├── docs/
│   ├── vencedores-masculino.md    # gerada a partir do CSV
│   ├── vencedoras-feminino.md     # gerada a partir do CSV
│   ├── ranking.md                 # gerada a partir do CSV
│   ├── perfis.md
│   ├── historia.md
│   ├── recordes-e-curiosidades.md
│   └── brasileiros.md
├── scripts/
│   └── build_docs.py              # regenera as páginas geradas e os JSONs
└── .github/ISSUE_TEMPLATE/
    └── correcao-de-dados.md
```

As páginas marcadas como **geradas** são produzidas pelo script `scripts/build_docs.py` a partir dos CSVs. Para alterar uma tabela ou um ranking, edite o CSV e rode:

```bash
python3 scripts/build_docs.py
```

## ⚖️ Aviso

Projeto independente e sem fins lucrativos, **sem qualquer vínculo** com a _France Football_, o Groupe Amaury ou a FIFA. "Ballon d'Or" é marca de seus respectivos titulares. As informações são factuais e podem conter imprecisões; se encontrar algum erro, abra uma [issue](../../issues/new/choose) ou envie um pull request.

## 📄 Licença

Código e conteúdo sob licença [MIT](LICENSE).

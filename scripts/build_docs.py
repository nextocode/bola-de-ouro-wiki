#!/usr/bin/env python3
"""Regenera as páginas geradas da wiki a partir dos CSVs em data/.

Uso (a partir da raiz do repositório):

    python3 scripts/build_docs.py

Gera:
    docs/vencedores-masculino.md
    docs/vencedoras-feminino.md
    docs/ranking.md
    data/vencedores-masculino.json
    data/vencedoras-feminino.json

Depende apenas da biblioteca padrão do Python 3.8+.
"""
import csv
import json
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

AVISO = (
    "<!-- ATENÇÃO: página gerada por scripts/build_docs.py a partir dos CSVs em data/. "
    "Não edite à mão: altere o CSV e rode o script novamente. -->\n\n"
)


def ler(nome):
    with open(DATA / nome, encoding="utf-8", newline="") as f:
        linhas = list(csv.DictReader(f))
    for l in linhas:
        l["ano"] = int(l["ano"])
    return sorted(linhas, key=lambda l: l["ano"])


def ordinal(n):
    return f"{n}º"


def vencedores_validos(linhas):
    return [l for l in linhas if l["jogador"].strip()]


def tabela_vencedores(linhas):
    contagem = Counter()
    out = ["| Ano | Jogador | Nacionalidade | Clube | Título nº | Observação |",
           "|:---:|---|---|---|:---:|---|"]
    for l in linhas:
        if not l["jogador"].strip():
            out.append(f"| {l['ano']} | _—_ | _—_ | _—_ | _—_ | _{l['observacao']}_ |")
            continue
        contagem[l["jogador"]] += 1
        n = contagem[l["jogador"]]
        nome = f"**{l['jogador']}**" if n > 1 else l["jogador"]
        out.append(
            f"| {l['ano']} | {nome} | {l['nacionalidade']} | {l['clube']} | "
            f"{ordinal(n)} | {l['observacao']} |"
        )
    return "\n".join(out)


def pagina_masculina(linhas):
    v = vencedores_validos(linhas)
    ult = v[-1]
    c = Counter(l["jogador"] for l in v)
    top = c.most_common(1)[0]
    txt = AVISO
    txt += "# Vencedores da Bola de Ouro (masculino)\n\n"
    txt += (
        f"Lista completa dos vencedores do prêmio de **melhor jogador do mundo** concedido pela "
        f"_France Football_, de {linhas[0]['ano']} a {linhas[-1]['ano']}.\n\n"
    )
    txt += (
        f"- **Edições concedidas:** {len(v)} (a de 2020 não aconteceu)\n"
        f"- **Jogadores diferentes premiados:** {len(c)}\n"
        f"- **Maior vencedor:** {top[0]} ({top[1]} títulos)\n"
        f"- **Vencedor mais recente:** {ult['jogador']} ({ult['ano']}, {ult['clube']})\n\n"
    )
    txt += "> **Como ler:** nomes em **negrito** indicam que o jogador já havia vencido antes. "
    txt += "A coluna _Clube_ mostra o clube do jogador na época da premiação. "
    txt += "Para dois jogadores de dupla nacionalidade, as duas aparecem separadas por barra.\n\n"
    txt += tabela_vencedores(linhas) + "\n\n"
    txt += "---\n\n[← Voltar ao início](../README.md) · [Ranking de vencedores →](ranking.md) · "
    txt += "[Vencedoras (feminino) →](vencedoras-feminino.md)\n"
    return txt


def pagina_feminina(linhas):
    v = vencedores_validos(linhas)
    ult = v[-1]
    c = Counter(l["jogador"] for l in v)
    top = c.most_common(1)[0]
    txt = AVISO
    txt += "# Vencedoras da Bola de Ouro (feminino)\n\n"
    txt += (
        "A Bola de Ouro feminina foi criada pela _France Football_ em "
        f"{linhas[0]['ano']}, depois de mais de seis décadas de prêmio masculino.\n\n"
    )
    txt += (
        f"- **Edições concedidas:** {len(v)}\n"
        f"- **Maior vencedora:** {top[0]} ({top[1]} títulos)\n"
        f"- **Vencedora mais recente:** {ult['jogador']} ({ult['ano']}, {ult['clube']})\n\n"
    )
    txt += tabela_vencedores(linhas) + "\n\n"
    txt += "---\n\n[← Voltar ao início](../README.md) · "
    txt += "[Vencedores (masculino) →](vencedores-masculino.md)\n"
    return txt


def ranking_jogadores(v):
    por_jogador = OrderedDict()
    for l in v:
        d = por_jogador.setdefault(l["jogador"], {"anos": [], "clubes": []})
        d["anos"].append(l["ano"])
        if l["clube"] not in d["clubes"]:
            d["clubes"].append(l["clube"])
    itens = sorted(por_jogador.items(), key=lambda kv: (-len(kv[1]["anos"]), kv[1]["anos"][0]))
    return itens


def pagina_ranking(masc, fem):
    v = vencedores_validos(masc)
    jogadores = ranking_jogadores(v)
    multi = [(n, d) for n, d in jogadores if len(d["anos"]) >= 2]

    txt = AVISO + "# Ranking de vencedores\n\n"
    txt += f"Estatísticas calculadas sobre as **{len(v)} edições concedidas** do prêmio masculino "
    txt += f"({masc[0]['ano']}–{masc[-1]['ano']}).\n\n"

    # Jogadores com 2+ títulos
    txt += "## Jogadores com dois ou mais títulos\n\n"
    txt += "| # | Jogador | Títulos | Anos | Clubes nas conquistas |\n|:---:|---|:---:|---|---|\n"
    pos = 0
    ultimo = None
    for i, (n, d) in enumerate(multi, 1):
        q = len(d["anos"])
        if q != ultimo:
            pos = i
            ultimo = q
        txt += f"| {pos}º | **{n}** | {q} | {', '.join(map(str, d['anos']))} | {' → '.join(d['clubes'])} |\n"
    txt += "\n"

    # Países
    por_pais = defaultdict(list)
    for l in v:
        for p in l["paises"].split(";"):
            por_pais[p].append(l)

    def excl_comp(ls):
        e = [l for l in ls if ";" not in l["paises"]]
        c = [l for l in ls if ";" in l["paises"]]
        return e, c

    itens_pais = sorted(
        por_pais.items(),
        key=lambda kv: (-len(excl_comp(kv[1])[0]), -len(kv[1]), kv[0]),
    )
    txt += "## Títulos por país\n\n"
    txt += "| # | País | Títulos | + Compartilhados* | Jogadores distintos | Vencedores |\n"
    txt += "|:---:|---|:---:|:---:|:---:|---|\n"
    pos = 0
    ultimo = None
    for i, (p, ls) in enumerate(itens_pais, 1):
        e, c = excl_comp(ls)
        chave = (len(e), len(c))
        if chave != ultimo:
            pos = i
            ultimo = chave
        nomes = OrderedDict()
        for l in ls:
            nomes[l["jogador"]] = nomes.get(l["jogador"], 0) + 1
        lista = ", ".join(f"{n} ({q}x)" if q > 1 else n for n, q in nomes.items())
        txt += f"| {pos}º | {p} | {len(e)} | {len(c) if c else '—'} | {len(nomes)} | {lista} |\n"
    txt += (
        "\n> **Notas:** (1) \\*_Compartilhados_ são títulos de jogadores com dupla nacionalidade "
        "(Alfredo Di Stéfano e Omar Sívori), que contam para os dois países e por isso ficam fora "
        "da coluna principal, que define a ordem da tabela. "
        "(2) Alemanha inclui os títulos da Alemanha Ocidental. "
        "(3) União Soviética e Tchecoslováquia são contadas à parte de Rússia/Ucrânia e "
        "República Tcheca, respectivamente.\n\n"
    )

    # Clubes
    por_clube = defaultdict(list)
    for l in v:
        por_clube[l["clube"]].append(l)
    itens_clube = sorted(por_clube.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    txt += "## Títulos por clube (clube do jogador na premiação)\n\n"
    txt += "| # | Clube | Títulos | Vencedores |\n|:---:|---|:---:|---|\n"
    pos = 0
    ultimo = None
    for i, (cl, ls) in enumerate(itens_clube, 1):
        q = len(ls)
        if q < 2:
            break
        if q != ultimo:
            pos = i
            ultimo = q
        nomes = OrderedDict()
        for l in ls:
            nomes[l["jogador"]] = nomes.get(l["jogador"], 0) + 1
        lista = ", ".join(f"{n} ({c}x)" if c > 1 else n for n, c in nomes.items())
        txt += f"| {pos}º | {cl} | {q} | {lista} |\n"
    txt += "\n_Clubes com apenas um título não aparecem na tabela; veja a lista completa na página de vencedores._\n\n"

    # Por década
    txt += "## Títulos por década\n\n"
    por_decada = defaultdict(list)
    for l in v:
        por_decada[(l["ano"] // 10) * 10].append(l)
    txt += "| Década | Edições concedidas | Maior vencedor da década |\n|:---:|:---:|---|\n"
    for dec in sorted(por_decada):
        ls = por_decada[dec]
        c = Counter(l["jogador"] for l in ls)
        mx = max(c.values())
        if mx == 1:
            lideres = "_ninguém repetiu o título na década_"
        else:
            lideres = ", ".join(f"{n} ({mx}x)" for n, q in c.items() if q == mx)
        txt += f"| {dec}s | {len(ls)} | {lideres} |\n"
    txt += "\n"

    # Feminino
    vf = vencedores_validos(fem)
    cf = Counter(l["jogador"] for l in vf)
    txt += "## Feminino\n\n| Jogadora | Títulos |\n|---|:---:|\n"
    for n, q in sorted(cf.items(), key=lambda kv: (-kv[1], kv[0])):
        txt += f"| {n} | {q} |\n"
    txt += "\n---\n\n[← Voltar ao início](../README.md) · [Vencedores →](vencedores-masculino.md)\n"
    return txt


def main():
    masc = ler("vencedores-masculino.csv")
    fem = ler("vencedoras-feminino.csv")

    (DOCS / "vencedores-masculino.md").write_text(pagina_masculina(masc), encoding="utf-8")
    (DOCS / "vencedoras-feminino.md").write_text(pagina_feminina(fem), encoding="utf-8")
    (DOCS / "ranking.md").write_text(pagina_ranking(masc, fem), encoding="utf-8")

    for nome, linhas in (("vencedores-masculino", masc), ("vencedoras-feminino", fem)):
        with open(DATA / f"{nome}.json", "w", encoding="utf-8") as f:
            json.dump(
                [
                    {
                        "ano": l["ano"],
                        "jogador": l["jogador"] or None,
                        "nacionalidade": l["nacionalidade"] or None,
                        "clube": l["clube"] or None,
                        "observacao": l["observacao"] or None,
                    }
                    for l in linhas
                ],
                f,
                ensure_ascii=False,
                indent=2,
            )
            f.write("\n")

    print("Páginas e JSONs regenerados com sucesso.")


if __name__ == "__main__":
    main()

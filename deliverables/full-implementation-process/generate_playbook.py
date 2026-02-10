#!/usr/bin/env python3
"""
generate_playbook.py — Gerador reutilizável de playbooks padronizados.

Uso:
    python generate_playbook.py --config config.yaml
    python generate_playbook.py --config config.yaml --output ./output/
    python generate_playbook.py --config config.yaml --format markdown
    python generate_playbook.py --config config.yaml --only prompt
    python generate_playbook.py --config config.yaml --only checklist
    python generate_playbook.py --config config.yaml --only template
    python generate_playbook.py --config config.yaml --only playbook

Dependências:
    pip install pyyaml

Autor: Thiago Rodrigues + Claude Opus 4.6
Versão: 1.0 (2026-02-10)
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERRO: PyYAML não instalado. Rode: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════
# CORE: Carrega config
# ═══════════════════════════════════════════════════

def load_config(config_path: str) -> dict:
    """Carrega e valida o arquivo de configuração YAML."""
    path = Path(config_path)
    if not path.exists():
        print(f"ERRO: Arquivo não encontrado: {config_path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    required_keys = ["process_name", "phases", "roles"]
    for key in required_keys:
        if key not in config:
            print(f"ERRO: Chave obrigatória ausente no config: '{key}'")
            sys.exit(1)

    return config


# ═══════════════════════════════════════════════════
# GERADOR 1: Prompt completo para Claude
# ═══════════════════════════════════════════════════

def generate_prompt(config: dict) -> str:
    """Gera um prompt completo para Claude Code baseado na config."""
    name = config["process_name"]
    description = config.get("description", f"Processo padrão de {name}")
    roles = config["roles"]
    phases = config["phases"]
    tools = config.get("tools", [])
    sources = config.get("sources", [])
    stakeholders = config.get("stakeholders", roles)

    roles_list = "\n".join(f"- **{r['name']}**: {r['description']}" for r in roles)
    phases_list = "\n".join(
        f"- Fase {i}: {p['name']} ({p.get('duration', 'TBD')})"
        for i, p in enumerate(phases)
    )
    tools_list = "\n".join(f"- {t['name']}: {t['purpose']}" for t in tools) if tools else "- Definir conforme necessidade"
    sources_list = "\n".join(f"- {s}" for s in sources) if sources else "- Fontes internas do projeto"
    stakeholder_names = ", ".join(s["name"] for s in stakeholders)

    prompt = f"""Você é o Claude Code operando como múltiplos agentes especializados para construir o processo padronizado de "{name}".

## CONTEXTO
{description}

## ROLES ENVOLVIDOS
{roles_list}

## FASES DO PROCESSO
{phases_list}

## FERRAMENTAS INTEGRADAS
{tools_list}

## FONTES A CONSULTAR
{sources_list}

## MÉTODO
1. INVENTÁRIO: Liste todas as fontes acessíveis e mapeie o conhecimento existente.
2. EXTRAÇÃO: Para cada fase, extraia padrões de projetos anteriores (GANTTs, tickets, threads).
3. MULTI-AGENTE: Crie memos de {stakeholder_names} com:
   - O que precisa existir para assinar embaixo
   - Perguntas para quebrar o processo
   - Riscos identificados
4. SABATINA CRUZADA: Cada agente questiona 2 outros. Compile requisitos.
5. PESQUISA EXTERNA: Busque best practices para cada fase e triangule com o interno.
6. CONSTRUÇÃO: Monte o processo com RACI, gates, DoD, checklists, templates.
7. AUDITORIA: Rode auditoria como "chefe chato" até passar em TODOS os quality gates:
   - G1 Ação: executável sem perguntar ao autor
   - G2 Rastreabilidade: fontes citadas
   - G3 Coerência: não contradiz documentos existentes
   - G4 Cobertura: todos os roles representados
   - G5 Auditável: checklists, templates, gates, métricas
   - G6 Pragmatismo: sem burocracia inútil

## ENTREGÁVEIS
A) Texto final para documentação (markdown)
B) Checklists por fase
C) Templates (tickets, mensagens, páginas)
D) Quality Report (riscos, gaps, decisões, métricas)

## REGRAS
1. NÃO invente fatos. Marque "NÃO ENCONTRADO" + plano de obtenção.
2. Cada etapa com fonte (interna ou externa).
3. Trabalho cíclico: coletar → sintetizar → auditar → refinar.
4. Saídas em PT-BR, linguagem operacional, sem enfeite.
"""
    return prompt


# ═══════════════════════════════════════════════════
# GERADOR 2: Esqueleto do playbook em markdown
# ═══════════════════════════════════════════════════

def generate_playbook(config: dict) -> str:
    """Gera o esqueleto do playbook em markdown."""
    name = config["process_name"]
    roles = config["roles"]
    phases = config["phases"]
    description = config.get("description", "")
    metrics = config.get("metrics", [])
    risks = config.get("risks", [])

    # Header
    lines = [
        f"# {name}",
        "",
        "---",
        "",
        "## Informações do Documento",
        "",
        "| Campo | Valor |",
        "|:------|:------|",
        f"| **Owner** | {config.get('owner', 'TBD')} |",
        f"| **Versão** | 1.0 |",
        f"| **Última Atualização** | {datetime.now().strftime('%Y-%m-%d')} |",
        f"| **Status** | Draft |",
        "",
        "---",
        "",
        "## Visão Geral",
        "",
        description if description else f"[Descrever o processo de {name}]",
        "",
        "---",
        "",
    ]

    # RACI
    lines.extend([
        "## Papéis e Responsabilidades (RACI)",
        "",
        "| Fase | " + " | ".join(r["name"] for r in roles) + " |",
        "|:-----|" + "|".join(":---:" for _ in roles) + "|",
    ])
    for i, phase in enumerate(phases):
        raci_row = phase.get("raci", {})
        cells = []
        for role in roles:
            cell = raci_row.get(role["name"], "-")
            cells.append(cell)
        lines.append(f"| {i}. {phase['name']} | " + " | ".join(cells) + " |")
    lines.extend(["", "**Legenda**: R=Responsável · A=Accountable · C=Consultado · I=Informado", "", "---", ""])

    # Fases
    lines.append("## Fases do Processo")
    lines.append("")
    for i, phase in enumerate(phases):
        lines.extend([
            f"### FASE {i}: {phase['name']}",
            "",
            "| Campo | Valor |",
            "|:------|:------|",
            f"| **Objetivo** | {phase.get('objective', '[Definir]')} |",
            f"| **Owner** | {phase.get('owner', '[Definir]')} |",
            f"| **Duração típica** | {phase.get('duration', '[Definir]')} |",
            f"| **Onde acontece** | {phase.get('where', '[Definir]')} |",
            f"| **Por que existe** | {phase.get('why', '[Definir]')} |",
            "",
            "**O que fazer:**",
        ])
        for step in phase.get("steps", ["[Definir passos]"]):
            lines.append(f"1. {step}")
        lines.extend([
            "",
            f"**Inputs:** {phase.get('inputs', '[Definir]')}",
            f"**Outputs:** {phase.get('outputs', '[Definir]')}",
            "",
            "**Critérios de Aceite (DoD):**",
        ])
        for dod in phase.get("dod", ["[Definir critério]"]):
            lines.append(f"- [ ] {dod}")
        lines.extend([
            "",
            f"**Gate {i}: {phase['name']} Complete** → Avança para Fase {i+1}",
            "",
            "**Falhas comuns:**",
        ])
        for fail in phase.get("common_failures", ["[Identificar]"]):
            lines.append(f"- {fail}")
        lines.extend(["", "---", ""])

    # Métricas
    if metrics:
        lines.extend([
            "## Métricas e KPIs",
            "",
            "| Métrica | O que mede | Target |",
            "|:--------|:-----------|:-------|",
        ])
        for m in metrics:
            lines.append(f"| {m['name']} | {m['measures']} | {m.get('target', 'TBD')} |")
        lines.extend(["", "---", ""])

    # Riscos
    if risks:
        lines.extend([
            "## Risk Register",
            "",
            "| Risco | Probabilidade | Impacto | Mitigação |",
            "|:------|:-------------|:--------|:----------|",
        ])
        for r in risks:
            lines.append(f"| {r['description']} | {r.get('probability', 'TBD')} | {r.get('impact', 'TBD')} | {r.get('mitigation', 'TBD')} |")
        lines.extend(["", "---", ""])

    return "\n".join(lines)


# ═══════════════════════════════════════════════════
# GERADOR 3: Checklists
# ═══════════════════════════════════════════════════

def generate_checklists(config: dict) -> str:
    """Gera checklists para cada fase."""
    name = config["process_name"]
    phases = config["phases"]

    lines = [
        f"# Checklists — {name}",
        "",
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "---",
        "",
    ]

    for i, phase in enumerate(phases):
        lines.extend([
            f"## Checklist Fase {i}: {phase['name']}",
            "",
            "### Entrada",
        ])
        for pre in phase.get("prerequisites", ["Gate anterior aprovado"]):
            lines.append(f"- [ ] {pre}")
        lines.extend(["", "### Execução"])
        for step in phase.get("steps", ["[Definir]"]):
            lines.append(f"- [ ] {step}")
        lines.extend(["", "### Saída (Gate)"])
        for dod in phase.get("dod", ["[Definir critério]"]):
            lines.append(f"- [ ] {dod}")
        lines.extend(["", "---", ""])

    # DoR/DoD checklist
    lines.extend([
        "## Definition of Ready (DoR) — Por Ticket",
        "",
        "- [ ] Título segue convenção do processo",
        "- [ ] Descrição com Acceptance Criteria mensuráveis",
        "- [ ] Endereça necessidade de negócio rastreável",
        "- [ ] Critérios mensuráveis (YES/NO, não subjetivo)",
        "- [ ] Tamanho adequado (≤ 5 dias; se maior, quebrar)",
        "- [ ] Sem dependências bloqueantes",
        "",
        "## Definition of Done (DoD) — Por Ticket",
        "",
        "- [ ] Trabalho concluído e verificado",
        "- [ ] Validação executada com zero erros críticos",
        "- [ ] Evidência capturada (screenshot, log, report)",
        "- [ ] Documentação atualizada",
        "- [ ] Ticket atualizado e fechado",
        "",
        "---",
        "",
    ])

    # Audit checklist
    lines.extend([
        "## Checklist de Auditoria",
        "",
        "### Qualidade do Processo",
        "- [ ] Cada fase tem owner definido",
        "- [ ] Cada fase tem DoD mensurável",
        "- [ ] Gates são verificados (não são teatro)",
        "- [ ] RACI não tem 2 Accountables na mesma fase",
        "- [ ] Templates existem para artefatos recorrentes",
        "- [ ] Métricas são coletáveis sem esforço extra",
        "",
        "### Completude",
        "- [ ] Todos os roles representados no RACI",
        "- [ ] Todos os stakeholders contemplados",
        "- [ ] Risk register populado",
        "- [ ] Cadências definidas",
        "- [ ] Escalonamento documentado",
        "",
        "### Pragmatismo",
        "- [ ] Cada artefato existe por um motivo claro",
        "- [ ] Nenhuma burocracia sem valor",
        "- [ ] Processo adaptável a projetos Small/Medium/Large",
        "",
    ])

    return "\n".join(lines)


# ═══════════════════════════════════════════════════
# GERADOR 4: Templates
# ═══════════════════════════════════════════════════

def generate_templates(config: dict) -> str:
    """Gera templates reutilizáveis."""
    name = config["process_name"]
    roles = config["roles"]
    templates = config.get("templates", [])

    lines = [
        f"# Templates — {name}",
        "",
        f"Gerado em: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "---",
        "",
    ]

    # Template de ticket
    lines.extend([
        "## Template: Ticket Padrão",
        "",
        "```markdown",
        "## Objective",
        "[UMA frase — o que este ticket entrega e por que importa]",
        "",
        "## Overview",
        "[2-3 parágrafos de contexto]",
        "",
        "## Key Tasks",
        "| Task | Owner | Why |",
        "|:-----|:------|:----|",
        "| [Ação] | [Role] | [Razão] |",
        "",
        "## Validation",
        "| Check | Method | Owner |",
        "|:------|:-------|:------|",
        "| [O que verificar] | [Como] | [Quem] |",
        "",
        "## Risks",
        "| Risk | Impact | Mitigation |",
        "|:-----|:-------|:-----------|",
        "| [Risco] | [Impacto] | [Mitigação] |",
        "```",
        "",
        "---",
        "",
    ])

    # Template de kick-off
    lines.extend([
        "## Template: Mensagem de Kick-off",
        "",
        "```",
        f"@here Kick-off: [PROJECT NAME]",
        "",
        f"Estamos iniciando [PROJECT]. Overview:",
        "",
        "Escopo:",
        "- [N] deliverables conforme SOW",
        "- Timeline: [INÍCIO] → [GO-LIVE]",
        "",
        "Time:",
    ])
    for role in roles:
        lines.append(f"- {role['name']}: [Nome]")
    lines.extend([
        "",
        "Artefatos:",
        "- GANTT: [LINK]",
        "- Tickets: [LINK]",
        "",
        "Cadências:",
        "- Daily async: [canal]",
        "- Weekly sync: [dia/hora]",
        "",
        "Riscos:",
        "- [Risco 1]: [Mitigação]",
        "",
        "Próximos passos:",
        "1. [Ação] — [Owner] — ETA [Data]",
        "```",
        "",
        "---",
        "",
    ])

    # Template de página de documentação
    lines.extend([
        "## Template: Página de Documentação",
        "",
        "```markdown",
        "# [PROJECT NAME] — Hub",
        "",
        "## Info",
        "| Campo | Valor |",
        "|:------|:------|",
        "| Owner | [Nome] |",
        "| Status | [Active/Complete/Hold] |",
        "| Updated | [Data] |",
        "",
        "## Timeline",
        "| Phase | Start | End | Status |",
        "|:------|:------|:----|:-------|",
    ])
    for phase in config["phases"]:
        lines.append(f"| {phase['name']} | [date] | [date] | [status] |")
    lines.extend([
        "",
        "## Team",
        "| Role | Person |",
        "|:-----|:-------|",
    ])
    for role in roles:
        lines.append(f"| {role['name']} | [name] |")
    lines.extend([
        "",
        "## Key Links",
        "| Resource | Link |",
        "|:---------|:-----|",
        "| Tickets | [url] |",
        "| GANTT | [url] |",
        "| SOW | [url] |",
        "",
        "## Decisions Log",
        "| Date | Decision | Context |",
        "|:-----|:---------|:--------|",
        "```",
        "",
    ])

    # Change Request template
    lines.extend([
        "---",
        "",
        "## Template: Change Request",
        "",
        "```markdown",
        "## Change Request: [Descrição curta]",
        "",
        "| Campo | Valor |",
        "|:------|:------|",
        "| CR ID | CR-[PROJECT]-[NNN] |",
        "| Solicitante | [Nome + Role] |",
        "| Data | [YYYY-MM-DD] |",
        "| Categoria | [ ] Escopo [ ] Timeline [ ] Técnico [ ] Budget |",
        "",
        "### Descrição da Mudança",
        "[O que está sendo pedido e por quê]",
        "",
        "### Impact Assessment",
        "| Dimensão | Impacto |",
        "|:---------|:--------|",
        "| Escopo | [O que muda] |",
        "| Timeline | [Dias a mais] |",
        "| Esforço | [Horas adicionais] |",
        "| Risco | [Novos riscos] |",
        "",
        "### Decisão",
        "| Status | Aprovador | Data |",
        "|:-------|:----------|:-----|",
        "| [ ] Aprovado [ ] Rejeitado [ ] Adiado | [Nome] | [Data] |",
        "```",
        "",
    ])

    # Retrospective template
    lines.extend([
        "---",
        "",
        "## Template: Retrospectiva (Keep/Stop/Start)",
        "",
        "```markdown",
        "# Retrospectiva — [PROJECT NAME]",
        "Data: [YYYY-MM-DD] | Participantes: [Nomes]",
        "",
        "## Dados do Projeto",
        "| Métrica | Planejado | Real | Delta |",
        "|:--------|:---------|:-----|:------|",
        "| Lead Time | [X] sem | [Y] sem | [+/-] |",
        "| Total Tickets | [X] | [Y] | [+/-] |",
        "",
        "## KEEP (Continuar fazendo)",
        "1. [Item]",
        "",
        "## STOP (Parar de fazer)",
        "1. [Item + root cause]",
        "",
        "## START (Começar a fazer)",
        "1. [Item + benefício]",
        "",
        "## Action Items",
        "| Ação | Owner | Deadline |",
        "|:-----|:------|:---------|",
        "| [ação] | [nome] | [data] |",
        "```",
        "",
    ])

    # Custom templates from config
    for tmpl in templates:
        lines.extend([
            f"## Template: {tmpl['name']}",
            "",
            "```",
            tmpl.get("content", "[Conteúdo do template]"),
            "```",
            "",
            "---",
            "",
        ])

    return "\n".join(lines)


# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Gerador reutilizável de playbooks padronizados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python generate_playbook.py --config implementation.yaml
  python generate_playbook.py --config sales.yaml --output ./sales/
  python generate_playbook.py --config implementation.yaml --only prompt
        """,
    )
    parser.add_argument(
        "--config", required=True, help="Caminho do arquivo YAML de configuração"
    )
    parser.add_argument(
        "--output",
        default="./output/",
        help="Diretório de saída (default: ./output/)",
    )
    parser.add_argument(
        "--only",
        choices=["prompt", "playbook", "checklist", "template", "all"],
        default="all",
        help="Gerar apenas um tipo de artefato",
    )

    args = parser.parse_args()

    # Load config
    config = load_config(args.config)
    name_slug = config["process_name"].lower().replace(" ", "_").replace("/", "_")

    # Create output dir
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = []

    # Generate requested artifacts
    if args.only in ("prompt", "all"):
        content = generate_prompt(config)
        path = output_dir / f"{name_slug}_PROMPT.md"
        path.write_text(content, encoding="utf-8")
        generated.append(("Prompt", path))

    if args.only in ("playbook", "all"):
        content = generate_playbook(config)
        path = output_dir / f"{name_slug}_PLAYBOOK.md"
        path.write_text(content, encoding="utf-8")
        generated.append(("Playbook", path))

    if args.only in ("checklist", "all"):
        content = generate_checklists(config)
        path = output_dir / f"{name_slug}_CHECKLISTS.md"
        path.write_text(content, encoding="utf-8")
        generated.append(("Checklists", path))

    if args.only in ("template", "all"):
        content = generate_templates(config)
        path = output_dir / f"{name_slug}_TEMPLATES.md"
        path.write_text(content, encoding="utf-8")
        generated.append(("Templates", path))

    # Summary
    print(f"\n{'='*60}")
    print(f"  PLAYBOOK GENERATOR — {config['process_name']}")
    print(f"{'='*60}")
    print(f"  Config: {args.config}")
    print(f"  Output: {output_dir.resolve()}")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    for artifact_type, path in generated:
        print(f"  [{artifact_type:12s}] {path}")
    print(f"{'='*60}")
    print(f"  Total: {len(generated)} artifacts")
    print()


if __name__ == "__main__":
    main()

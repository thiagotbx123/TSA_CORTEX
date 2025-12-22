# /consolidar - Consolidação de Sessão TSA_CORTEX

Execute esta rotina ao FINAL de cada sessão de trabalho para preservar conhecimento.

## PASSOS OBRIGATÓRIOS

### PASSO 1: Análise da Sessão
Analise o que foi feito nesta sessão:
- Arquivos TypeScript criados/modificados
- Tipos adicionados
- Testes implementados
- Bugs corrigidos
- Features completadas
- Decisões arquitetônicas

### PASSO 2: Criar Arquivo de Sessão
Crie arquivo em `sessions/YYYY-MM-DD_HH-MM.md` usando o template `sessions/_template.md`

### PASSO 3: Atualizar Knowledge Base
Atualize os arquivos relevantes em `knowledge-base/`:
- `api/` - Documentação de APIs usadas (Slack, Linear, Drive)
- `troubleshooting/` - Problemas encontrados e soluções
- `decisions/` - Decisões arquitetônicas importantes

### PASSO 4: Atualizar Memory
Atualize `.claude/memory.md` com:
- Estado atual de cada módulo
- Últimas ações realizadas
- Novos bloqueios identificados
- Próximos passos sugeridos

### PASSO 5: Commit e Push
Execute:
```bash
git add .
git commit -m "consolidar: [resumo breve da sessão]"
git push
```

### PASSO 6: Relatório Final
Apresente ao usuário:

```
✅ SESSÃO CONSOLIDADA
━━━━━━━━━━━━━━━━━━━━

📝 Resumo: [o que foi feito]

📁 Arquivos Atualizados:
- sessions/YYYY-MM-DD_HH-MM.md
- .claude/memory.md
- knowledge-base/[arquivos]

🔄 Git:
- Commit: [hash curto]
- Mensagem: [mensagem]
- Push: [sucesso/falha]

🎯 Próxima Sessão:
1. [sugestão 1]
2. [sugestão 2]
3. [sugestão 3]
```

---

**IMPORTANTE:** Esta rotina garante que nenhum conhecimento seja perdido entre sessões.

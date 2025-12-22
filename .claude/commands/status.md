# /status - Status do Projeto TSA_CORTEX

Execute para obter visão geral do estado atual do projeto.

## O QUE VERIFICAR

### 1. Estado do Projeto
Leia `.claude/memory.md` e apresente:
- Fase atual
- Módulos implementados
- Bloqueios conhecidos

### 2. Knowledge Base
Liste arquivos em `knowledge-base/`:
- Quantidade de documentos
- Última atualização

### 3. Sessões
Verifique `sessions/`:
- Total de sessões registradas
- Última sessão (data e resumo)

### 4. Dependências
Execute e apresente:
```bash
# Verificar se node_modules existe
ls node_modules 2>NUL || echo "Dependências não instaladas - execute: npm install"
```

### 5. Git Status
Execute e apresente:
```bash
git status
git log --oneline -5
```

### 6. Configuração
Verifique:
- `.env` existe?
- `config/default.json` válido?

### 7. Próximas Ações
Baseado no contexto, sugira 3 próximas ações prioritárias.

---

## FORMATO DE SAÍDA

```
📊 STATUS DO PROJETO: TSA_CORTEX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Fase Atual: [fase]
📅 Última Sessão: [data]
📚 Knowledge Base: [X] documentos
🔄 Git: [X] commits, branch [nome]

📦 Módulos:
- collectors/   [status]
- normalizer/   [status]
- clustering/   [status]
- worklog/      [status]
- linear/       [status]
- cli/          [status]

⚠️ Bloqueios:
- [bloqueio 1]
- [bloqueio 2]

✅ Últimas Ações:
- [ação 1]
- [ação 2]

🎯 Próximos Passos:
1. [ação prioritária 1]
2. [ação prioritária 2]
3. [ação prioritária 3]
```

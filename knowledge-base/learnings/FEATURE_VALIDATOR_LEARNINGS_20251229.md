# Feature Validator - Aprendizados Consolidados
## Sessao: 2025-12-29

---

## CONTEXTO

Sessao de refinamento do processo de validacao de features do QBO Winter Release FY26.
Problemas identificados nos screenshots anteriores levaram a revisao completa do metodo.

---

## APRENDIZADOS CRITICOS

### 1. TEMPO DE ESPERA

**Problema:** Screenshots capturando loading spinners (4 pontos azuis)

**Causa:** Tempo de espera de 10 segundos insuficiente para QBO carregar

**Solucao:**
```python
WAIT_TIME_MIN = 30   # Minimo 30 segundos
WAIT_TIME_MAX = 60   # Maximo antes de investigar
```

**Regra:** Se apos 30s ainda tiver spinner, investigar se feature existe no ambiente.

---

### 2. NUNCA REJEITAR, APENAS MARCAR

**Problema:** Usuario nao sabia quando captura falhava

**Orientacao do usuario:**
> "negar é perigoso, pois eu preciso saber se foi negado"

**Solucao:** Sistema de FLAGS
```python
class ValidationFlags:
    LOGIN_PAGE = "LOGIN_PAGE"
    LOADING_DETECTED = "LOADING_DETECTED"
    ERROR_CONTENT = "ERROR_CONTENT"
    VERY_SMALL_FILE = "VERY_SMALL_FILE"  # < 50KB
    SMALL_FILE = "SMALL_FILE"            # 50-100KB
    ERROR_PAGE_404 = "ERROR_PAGE_404"
    NOT_AVAILABLE = "NOT_AVAILABLE"
```

**Regra:** Sempre capturar, sempre salvar, sempre marcar com flags.

---

### 3. EVIDENCE NOTES TECNICAS

**Problema:** Notes genericas como "Screenshot capturado" nao passam confianca

**Orientacao do usuario:**
> "as anotacoes tem q passar confianca de quem foi evidenciado que a feature solicitada ta funcionando"

**Solucao:** Template tecnico estruturado
```
FEATURE: WR-014 - Benchmarking
ENVIRONMENT: TCO (Apex Tire)
URL: https://qbo.intuit.com/app/reports
PAGE_TITLE: Intuit Enterprise Suite
FILE_SIZE: 113KB
QUALITY: ACCEPTABLE
FLAGS: NONE
VISIBLE_HEADERS: Reports & Analytics, Performance center
VALIDATION: PASS - Feature captured successfully
```

---

### 4. 404 = NOT_AVAILABLE (Nao tentar mais)

**Problema:** Tentar recapturar infinitamente URLs que nao existem

**Descoberta:** URL /app/workflowautomation retorna 404 em Construction

**Solucao:**
1. Detectar pagina 404 ("We're sorry, we can't find")
2. Marcar como NOT_AVAILABLE
3. Buscar na web para confirmar se feature deveria existir
4. Documentar no tracker com justificativa
5. NAO tentar recapturar

---

### 5. FEATURES DE DOCUMENTACAO

**Problema:** Tentar capturar features que nao sao UI

**Descoberta:** WR-023 (Feature Compatibility) e documentacao, nao pagina

**Solucao:**
1. Identificar features que sao "N/A - Documentation"
2. Marcar como N/A no tracker
3. Referenciar onde a informacao pode ser encontrada

---

### 6. LOGIN AUTOMATICO

**Problema:** Sessao expira e captura pagina de login

**Descoberta:** Browser pode ter conta errada salva

**Solucao:**
1. Usar layer1_login.py com tratamento de multi-conta
2. Clicar em "Utilize uma conta diferente" se necessario
3. Detectar LOGIN_PAGE flag e alertar

---

### 7. QUALIDADE POR TAMANHO

**Thresholds definidos:**
```python
SIZE_EXCELLENT = 250  # KB - Screenshot rico
SIZE_GOOD = 150       # KB - Adequado
SIZE_ACCEPTABLE = 100 # KB - Minimo aceitavel
SIZE_WEAK = 50        # KB - Requer investigacao
SIZE_ERROR_PAGE = 139 # KB - Tamanho tipico de 404
```

**Regra:** Se < 100KB, investigar. Se = 139KB, provavelmente 404.

---

## METODO PADRONIZADO v2.0

```
1. LOGIN AUTOMATICO
   - layer1_login.py
   - Tratar multi-conta
   - Verificar empresa correta

2. NAVEGACAO
   - URL primaria
   - Timeout: 60s
   - Fallback URL se erro

3. ESPERA
   - Minimo: 30s
   - Maximo: 60s
   - Se spinner persistir: investigar

4. CAPTURA
   - Screenshot viewport
   - Timeout: 60s
   - Salvar sempre

5. ANALISE
   - Detectar flags
   - Verificar tamanho
   - Extrair headers

6. EVIDENCE NOTES
   - Template tecnico
   - URL, size, headers
   - Flags e validacao

7. DECISAO
   - PASS: >= 100KB, sem erros
   - REVIEW: < 100KB ou com flags
   - NOT_AVAILABLE: 404 confirmado
   - N/A: Feature de documentacao
```

---

## ARQUIVOS CRIADOS

| Arquivo | Proposito |
|---------|-----------|
| qbo_checker/feature_validator.py | Metodo padronizado v2.0 |
| docs/PROCESSO_REFINADO_WINTER_RELEASE.md | Documentacao do processo |
| docs/RECAPTURE_TCO_FINAL_20251229.md | Resultados TCO |
| docs/RECAPTURE_CONSTRUCTION_FINAL_20251229.md | Resultados Construction |
| WINTER_RELEASE_TRACKER_UPDATED_20251229.xlsx | Tracker atualizado |

---

## PROXIMAS EVOLUCOES

1. **Detectar spinner visualmente** - Usar analise de imagem para confirmar
2. **Retry inteligente** - Se loading, esperar mais automaticamente
3. **Cache de sessao** - Manter login por mais tempo
4. **Parallelizacao** - Capturar multiplas features simultaneamente

---

## COMANDOS UTEIS

```bash
# Rodar feature validator
python -c "from qbo_checker.feature_validator import capture_feature; ..."

# Login automatico
python -c "from layer1_login import login; pw, browser, page = login('TCO', 'apex')"

# SpineHub collect
cd C:\Users\adm_r\Projects\TSA_CORTEX && npx ts-node src/cli/index.ts collect --all
```

---

*Documento gerado automaticamente*
*Sessao: 2025-12-29*
*Claude Code + Feature Validator v2.0*

# Guía de Revisión Periódica de Cumprimento Normativo

Este protocolo define a lista de comprobacións (*checklist*) que a tripulación de Noutrora debe executar ante calquera cambio de versión, modificación da web ou adición de novas funcións.

---

## 📋 Lista de Verificación Periódica (*Checklist*)

### 1. Auditoría de Protección de Datos (RGPD / LOPD-GDD)
- [ ] **Cero CDNs e Fontes Externas:** `index.html` non contén ligazóns a `fonts.googleapis.com`, `fonts.gstatic.com` nin `cdn.tailwindcss.com`. Todo o código CSS e JS é autónomo e local.
- [ ] **Cero Cookies na Web:** Comprobar que a web non deposita cookies nin garda identificadores de seguimento.
- [ ] **Cero Rexistro de IPs:** A web oficial resólvese de xeito estático en GitHub Pages protexida por Cloudflare, sen servidores dinámicos nin captura de IPs de persoas visitantes.
- [ ] **Historial Desactivado no Navegador:** Confirmar en `config/noutrora.cfg` que `places.history.enabled = false` permanece bloqueado (`lockPref`).
- [ ] **Telemetría e Estudos Bloqueados:** Confirmar que `policies.template.json` e `noutrora.cfg` manteñen toda a telemetría en `false`.

### 2. Auditoría LSSI-CE e Comunitaria
- [ ] **Contacto Visible e Titularidade:** O pé de páxina de `index.html` e o modal de aviso legal identifican o proxecto como iniciativa veciñal sen ánimo de lucro e conteñen o correo `intelixenciaaxusta@gmail.com`.
- [ ] **Explicación Transparente de Privacidade:** O modal `#privacy-modal` explica o cumprimento estrito do principio de minimización de datos.

### 3. Auditoría de Licenzas e Marcas (MPL-2.0)
- [ ] **Integridade de `omni.ja`:** A construción de Noutrora faise mediante superposición externa limpa sen alterar os arquivos centrais do motor.
- [ ] **Separación de Marca:** O proxecto preséntase como Noutrora e recoñece con claridade a súa base técnica de Firefox sen usurpar a marca nin inducir a erro.
- [ ] **Avisos de Copyright e Licenza Aberta:** Consérvase a mención á licenza Mozilla Public License 2.0 (MPL-2.0).

---

## 🛠️ Execución Automatizada de Probas Obrigatorias

Antes de calquera commit ou empaquetado, é obrigatorio executar a batería completa:

```bash
python3 scripts/run_tests.py
```

O test `tests/test_normativa.py` audita automaticamente estes puntos clave para impedir que ningún cambio inadvertido vulnere a normativa.


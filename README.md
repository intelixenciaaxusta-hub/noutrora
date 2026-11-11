# Navegador Noutrora (v2.0 «Atlántico»)

**Noutrora** é un navegador web persoal e soberano, construído sobre o motor de Firefox con identidade propia inspirada no Océano Atlántico e no espírito da web libre de 1994 (*N’94*). 

Deseñado baixo o principio de **intimidade blindada e acougo psicolóxico**: sen historial de páxinas visitadas (`places.history.enabled = false`), pero conservando as sesións iniciadas para evitar o ruído de autenticarse a diario. Cero ventás emerxentes, cero telemetría, cun conxunto de extensións respectuosas integradas de serie (**uBlock Origin**, **TWP** en galego, **I Still Don't Care About Cookies** e **SponsorBlock**) e un **Porto Base** cultural diario de 6 cartas.

---

## Documentación do Proxecto

| Ficheiro | Propósito |
| :--- | :--- |
| [`CONSTITUCION.md`](./CONSTITUCION.md) | As 5 Leis Fundamentais e o manifesto ético innegociable de Noutrora. |
| [`SPEC.md`](./SPEC.md) | Especificación técnica do Porto Base, Catálogo Vivo e distribución consciente. |
| [`CATALOGO.md`](./CATALOGO.md) | Inventario polo miúdo de cada personalización activa (que fai e por que) e Folla de Ruta (*Backlog*). |
| [`AGENTS.md`](./AGENTS.md) | Regras e fluxo de traballo paso a paso para o axente asistente de desenvolvemento. |
| [`decalogo.txt`](./decalogo.txt) | Declaración pública de principios e compromisos en 10 puntos directos. |
| [`formadeserepensar.txt`](./formadeserepensar.txt) | Ensaio sobre a economía do don, a rede libre e a resistencia fronte á *enshittification*. |

---

## Fluxo de Traballo Paso a Paso

Calquera mudanza ou axuste segue sempre este ciclo de 4 pasos:

1. **Analizar e Acordar:** Revisar que preferencia interna (`noutrora.cfg`), política (`policies.template.json`) ou estilo CSS controla o comportamento desexado.
2. **Compilar e Probar en Laboratorio:**
   - Compilar a superposición externa sobre o motor:
     ```bash
     python3 scripts/build.py
     ```
   - Probar na contorna illada de probas:
     ```bash
     ./run.sh
     ```
3. **Documentar en `CATALOGO.md`:** Rexistrar calquera novidade ou axuste no catálogo técnico para saber sempre o motivo de cada liña de configuración.
4. **Control de Versións (Git):** Realizar un *commit* limpo e atómico en canto a mudanza estea verificada polo usuario.

---

## Ordes Rápidas

- **Execución da batería de probas técnicas (TDD):**
  ```bash
  python3 scripts/run_tests.py
  ```
- **Execución en probas de Noutrora:**
  ```bash
  ./run.sh
  ```
- **Recompilar a configuración externa:**
  ```bash
  python3 scripts/build.py
  ```
- **Xerar o paquete web oficial:**
  ```bash
  python3 scripts/package_web.py
  ```
- **Instalar/actualizar o lanzador no escritorio Linux:**
  ```bash
  ./install-linux.sh
  ```

---

## Estrutura de Cartafoles

```text
Noutrora/
├── CONSTITUCION.md               # As 5 Leis Fundamentais e manifesto ético
├── SPEC.md                       # Especificación técnica e editorial do Porto Base
├── CATALOGO.md                   # Rexistro vivo de personalizacións activas e backlog
├── AGENTS.md                     # Regras operativas do axente
├── README.md                     # Este manual
├── decalogo.txt                  # Decálogo de principios
├── formadeserepensar.txt         # Ensaio sobre a economía do don
├── normativa/                    # Marco legal español e licenzas (LOPD-GDD, RGPD, LSSI, MPL-2.0)
│   ├── LOPD_GDD_RGPD.md          # Adaptación veciñal e dereitos de privacidade
│   ├── LICENZAS_FIREFOX_MPL.md   # Mozilla Public License 2.0 e política de marcas
│   └── GUIA_REVISION_PERIODICA.md# Protocolo e checklist de revisión periódica
├── config/                       # Capa de personalización limpa (versionada en Git)
│   ├── home.html                 # O Porto Base (6 cartas culturais en cuadrícula 3×2)
│   ├── exploracion.json          # Catálogo cultural e mariñeiro offline
│   ├── bookmarks.json            # Fonte de verdade da Bitácora
│   ├── policies.template.json    # Políticas (uBlock, TWP, sen telemetría nin popups)
│   ├── noutrora.cfg              # Axustes internos de motor, estilos Atlántico e JS
│   └── branding/                 # Compás de Noutrora e iconas vectoriais da interface
├── scripts/
│   ├── bootstrap.py              # Descarga e aprovisionamento do motor oficial
│   ├── build.py                  # Inxecta a configuración externa sen tocar omni.ja
│   ├── package_web.py            # Xeración do paquete web para noutrora.es
│   └── package_native.py         # Empaquetado consciente para sistemas de escritorio
├── base/firefox/                 # Motor binario Gecko oficial (ignorado en Git)
└── upstream/                     # Proxectos de referencia (Betterfox, LibreWolf)
```

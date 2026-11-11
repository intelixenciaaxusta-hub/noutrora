# Regras do Axente — Proxecto Noutrora (v2.0)

Cando operes dentro deste repositorio (raíz de Noutrora), cumpre sempre estas directrices:

1. **Respecto Absoluto á Constitución e ao Spec:**
   - Le e respecta os principios de [`CONSTITUCION.md`](./CONSTITUCION.md) e a arquitectura de [`SPEC.md`](./SPEC.md) antes de propoñer ou realizar calquera cambio.
   - **Regra de Ouro:** Silencio, soberanía e intimidade total. Cero roubo nin recolección de datos, sen gardar historial de páxinas visitadas (`places.history.enabled = false`), pero conservando as sesións iniciadas (cookies activas + uBlock Origin) para evitar o *ruído psicolóxico* de volver iniciar sesión. Cero ventás emerxentes nin consumo innecesario de RAM/CPU.
2. **Estilo de Comunicación e Fluxo de Traballo en Tripulación (Obrigatorio):**
   - **Goberno da Nave (Roles Especializados):**
     - **O Capitán (Orquestrador / Axente Principal):** Goberna o rumbo, define a estratexia, delega tarefas nos subaxentes axeitados, sintetiza as conclusións de forma escueta para o usuario e toma a decisión final de commit tras recibir confirmación.
     - **O Construtor (*Builder*):** Executa cambios técnicos en código e probas dentro do ámbito illado.
     - **O Auditor (*Reviewer*):** Verifica conformidade estrita coa Constitución, Spec, integridade de arquivos e ausencia de ruído ou telemetría.
     - **O Crítico (*Critic / Red Team*):** Busca activamente puntos de rotura (multiplataforma Windows/Mac/Linux, caídas de rede, parénteses, rutas con espazos, consumo).
   - **Mensaxes curtas e cousa a cousa:** Non envíes textos longos nin abafantes. Vai punto por punto con brevidade e claridade.
   - **Paso 1 — Analizar e Acordar antes de tocar:** Explica brevemente que compoñente se vai tocar e agarda confirmación se hai varias opcións.
   - **Paso 2 — Probas Técnicas Obrigatorias (TDD):** Ningún avance se dá por bo sen executar `python3 scripts/run_tests.py` e acadar o 100% dos test en verde.
   - **Paso 3 — Documentar:** Todo axuste ou función nova debe quedar reflectido en [`CATALOGO.md`](./CATALOGO.md) (e en [`SPEC.md`](./SPEC.md) se muda a arquitectura).
   - **Paso 4 — Compilar e probar:** Executa `python3 scripts/build.py` e valida a execución.
   - **Paso 5 — Control de versións limpo:** Realiza commits atómicos e descritivos en Git trala aprobación expresa do usuario.
3. **Estrutura do Proxecto e Documentación:**
   - `CONSTITUCION.md`: Manifesto asinado e as 5 Leis Fundamentais de Noutrora.
   - `SPEC.md`: Especificación técnica e editorial (as 6 cartas do Porto Base, Catálogo Vivo e Caderno do Capitán).
   - `CATALOGO.md`: Rexistro vivo de todas as personalizacións activas e Folla de Ruta (*Backlog*).
   - `README.md`: Manual de uso e mantemento.
   - `decalogo.txt` e `formadeserepensar.txt`: Declaración de principios e ensaio filosófico sobre a economía do don e a rede libre.
   - `normativa/`: Cadro regulador español e licenzas (`LOPD_GDD_RGPD.md`, `LICENZAS_FIREFOX_MPL.md`, `GUIA_REVISION_PERIODICA.md`) para o proxecto veciñal sen ánimo de lucro.
   - `config/home.html` e `config/exploracion.json`: O Porto Base (`3×2`: *Perder o norte*, *Terra á vista*, *Mergullar*, *O Libro do día*, *Atracar* e *Fondear*) e o seu catálogo cultural/mariñeiro.
   - `config/bookmarks.json`: Fonte única de verdade para a **Bitácora**.
   - `config/policies.template.json` e `config/noutrora.cfg`: Políticas, privacidade sen historial pero con sesión activa, bloqueo de popups e paleta cromática Océano Atlántico.
   - `scripts/bootstrap.py`: Descarga e aprovisiona o binario base de Firefox.
   - `scripts/build.py`: Inxecta a configuración e a superposición externa sobre `base/firefox/` sen tocar `omni.ja`.
   - `scripts/package_web.py`, `scripts/package_native.py` e `scripts/package_mac.py`: Xeración do paquete web para `noutrora.es` e dos empaquetados.
   - `run.sh` e `install-linux.sh`: Execución en contorna de probas illada e instalación local.
   - `scripts/capitan.py` (e `capitan.sh`) *(planificado / en especificación)*: Panel visual privado (**«O Caderno do Capitán»**) para engadir/editar portos, filmes, libros e ligazóns sen tocar código.
4. **Control de Versións e Política de Commits:**
   - Nunca subas `base/`, `dist/`, `upstream/`, `profile-test/` nin `profile-lab/` ao repositorio Git.
   - **Formato de Mensaxes (*Conventional Commits*):** `feat:`, `bookmark:`, `fix:`, `docs:`, `chore:`.
5. **Arquitectura e Despregamento (Web Oficial e Instaladores):**
   - **Web Pública (`noutrora.es`):** Aloxada de forma estática en **GitHub Pages** con protección de **Cloudflare DNS** (rexistros A e CNAME en Solo DNS / Proxy). Garante dispoñibilidade 24/7, cero consumo da rede doméstica e anonimato total da IP residencial (Lei 1). A web nunca se publica nun NAS nin servidor privado.
   - **Instaladores e Paquetes:** Distribución pública mediante **GitHub Releases** con sumas de control SHA-256 e descarga dende `noutrora.es/downloads/`.
   - **Automatización de Publicación:** A publicación efectúase de xeito automatizado a través de GitHub Actions (`.github/workflows/pages.yml`) en cada commit validado en `main`.

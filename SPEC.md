# Especificación Técnica e Editorial — Noutrora v2.0 (`SPEC.md`)

Este documento define a arquitectura técnica, o modelo de datos cultural e o sistema de posta a punto e distribución de **Noutrora**.

---

## 1. Arquitectura Xeral («Noutrora Core»)

1. **Motor Base Intacto (`base/firefox/`):**
   - Motor Gecko oficial de Mozilla con `omni.ja` sen modificar para garantir o 100 % de compatibilidade bancaria, vídeo (DRM), velocidade e seguridade.
2. **Capa de Soberanía e Privacidade (`config/noutrora.cfg` + `config/policies.template.json`):**
   - **Sen historial de páxinas (`places.history.enabled = false`):** Non almacena ningún rexistro das páxinas visitadas polo navegante.
   - **Sesións conservadas (`privacy.clearOnShutdown.cookies = false`):** Conserva as cookies de inicio de sesión lexítimas para evitar o «ruído psicolóxico» de volver autenticarse cada día.
   - **Extensións integradas de serie:** uBlock Origin fixado e activo dende o primeiro arranque (con listas anti-cookies reforzadas), I Still Don't Care About Cookies, SponsorBlock e Traduzir Páxinas Web (TWP) preconfigurado ao galego en segundo plano.
   - **Identidade Atlántica v2.0:** Paleta `#1B3644` (Abismo Atlántico), `#FAF9F5` (Espuma de Sal), `#D6D3C9` (Area de Baixamar), `#7A9E9F` (Bruma Costeira), `#0F232E` (Noite de Temporal), icona de ventá co compás na segunda «o» e marcadores renomeados como **«Bitácora»**.

---

## 2. Especificación do «Porto Base» (`config/home.html` — Cuadrícula `3×2`)

| Carta | Nome | Comportamento na Carta | Acción ao Premer |
| :--- | :--- | :--- | :--- |
| **`01`** | **Perder o norte** | Botón de exploración creativa + botón `+` para engadir webs propias en local. | Abre ao chou unha experiencia interactiva, visual ou sonora da colección sen mapa. |
| **`02`** | **Terra á vista** | Botón de exploración cultural + botón `+` para engadir webs propias en local. | Abre ao chou un ensaio, arquivo cultural ou artigo de música, cine ou literatura. |
| **`03`** | **Mergullar** | Amosa o **Filme ou Serie do día** (título, ano e xénero) + botón de compás **«Cambiar punto cardinal»**. | Abre a **Ficha Cultural Noutrora** (modal limpo dentro do Porto Base) con cartel/imaxe, sinopse sen spoilers, nota do Capitán, botón **«Cambiar punto cardinal»** e botón **«Ler análise a fondo»**. |
| **`04`** | **O Libro do día** | Amosa o **Libro do día** (título e autor) + botón de compás **«Cambiar punto cardinal»**. | Abre a **Ficha Literaria Noutrora** con portada/imaxe, historia da obra, por que lelo, botón **«Cambiar punto cardinal»** e ligazón a reseña ou fragmento. |
| **`05`** | **Atracar** | Amosa na propia carta a **fotografía en miniatura do porto do día**, o seu nome, **localidade e provincia** (percorrendo en orde a Costa da Morte -> resto de Galicia -> Asturias -> Cantabria -> resto da costa). | Abre a **Ficha Mariñeira Noutrora** coa foto en grande, localidade, provincia, coordenadas, historia mariñeira do porto e opcións para navegar polos portos da costa. |
| **`06`** | **Fondear** | O **Fondeadoiro persoal**: carta libre e editable polo navegante para gardar o seu enderezo habitual de uso diario. Cero publicidade e cero patrocinios. | Abre o enderezo configurado por quen navega. |

---

## 3. Modelo de Datos do Catálogo Vivo (`config/exploracion.json` e `https://noutrora.es/exploracion.json`)

O navegador inclúe `config/exploracion.json` de fábrica (para funcionar 100 % sen conexión) e ao abrir o Porto Base consulta de forma silenciosa e en só lectura `https://noutrora.es/exploracion.json`, gardando en caché local as novidades culturais que publique o Capitán.

Estrutura do JSON:
```json
{
  "version": "2.0",
  "updated_at": "2026-11-09",
  "perder_o_norte": [
    { "title": "...", "url": "..." }
  ],
  "terra_a_vista": [
    { "title": "...", "url": "..." }
  ],
  "mergullar": [
    {
      "id": "halt-and-catch-fire",
      "title": "Halt and Catch Fire",
      "year": "2014–2017",
      "kind": "Serie · 4 tempadas",
      "creator": "Christopher Cantwell & Christopher C. Rogers",
      "image": "https://...",
      "summary": "Dende os primeiros clónicos de IBM nos anos 80 ata o nacemento dos navegadores web en 1994...",
      "captain_note": "Unha obra mestra sobre a amizade, o fracaso e a paixón por construír o futuro.",
      "article_title": "Ler análise en Jot Down: «A estafa do transaccional»",
      "article_url": "https://www.jotdown.es/2026/02/la-estafa-de-lo-transaccional/"
    }
  ],
  "libros": [
    {
      "id": "en-el-camino-kerouac",
      "title": "No camiño (On the Road)",
      "author": "Jack Kerouac",
      "year": "1957",
      "image": "https://...",
      "summary": "Escrita en tres semanas sobre un rolo continuo de papel de teletipo...",
      "captain_note": "O latexo fundacional da Xeración Beat e da viaxe sen mapa.",
      "article_title": "Explorar dossier e contexto literario",
      "article_url": "https://..."
    }
  ],
  "puertos": [
    {
      "day_order": 1,
      "name": "Porto de Caión",
      "locality": "A Laracha",
      "province": "A Coruña",
      "region": "Costa da Morte · Galicia",
      "coords": "43°19′17″N 8°36′27″O",
      "image": "https://...",
      "history": "Antigo porto baleeiro dende o século XVI e porta de entrada oriental á Costa da Morte...",
      "more_url": "https://..."
    }
  ]
}
```

---

## 4. «O Caderno do Capitán» (`scripts/capitan.py` + Interfaz Visual)

Para que quen xestiona Noutrora poida actualizar todos os contidos sen ter que editar código nin JSON a man:
- Ao executar `./capitan.sh` (ou `python3 scripts/capitan.py`), ábrese unha interface web local no propio navegador Noutrora.
- Permite ver e engadir cun formulario visual:
  - Novos **Portos** (Nome, Localidade, Provincia, Foto, Historia).
  - Novos **Filmes / Series** para *Mergullar*.
  - Novos **Libros do día**.
  - Novas ligazóns para **Perder o norte** e **Terra á vista**.
- Conta cun botón **«Gardar e Empaquetar para noutrora.es»** que actualiza `config/exploracion.json`, recompila o navegador local e deixa lista a carpeta `dist/noutrora.es/` para o seu despregamento no servidor.

---

## 5. Distribución Consciente e Instalación con Esforzo Propio (Lei 5)

En cumprimento da **Lei 5 da Constitución** (*A Liberdade Ten un Prezo*), Noutrora fuxe expressamente dos instaladores comerciais opacos de «un clic»:
1. **Instalación transparente e con amor propio:**
   - A instalación faise mediante scripts claros e verificables (`install-linux.sh`, `./run.sh`), onde quen navega sabe exactamente onde se colocan os ficheiros (`/opt/noutrora` ou o perfil local illado), sen procesos ocultos en segundo plano nin telemetría invasiva.
2. **Empaquetado honesto (`scripts/package_native.py` e `scripts/package_web.py`):**
   - Paquetes lexibles (`.deb`, `.AppImage`, `.dmg`, `.zip`) deseñados para seren inspeccionados e postos a punto polo usuario en tres pasos conscientes.
3. **Web oficial con instrucións claras (`https://noutrora.es`):**
   - A páxina web oficial non engana nin camufla a instalación: explica con honestidade o proceso paso a paso, lembrando que poñer a punto o teu propio barco leva cinco minutos e é un exercicio de dignidade e soberanía dixital.

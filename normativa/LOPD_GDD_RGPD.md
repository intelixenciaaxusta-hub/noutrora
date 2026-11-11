# Cadro Normativo de Protección de Datos — Proxecto Noutrora
**Marco Xurídico:** Regulamento Xeral de Protección de Datos (RGPD - Regulamento UE 2016/679) e Lei Orgánica 3/2018 de Protección de Datos Persoais e garantía dos dereitos dixitais (LOPD-GDD).

---

## 1. Natureza Xurídica e Finalidade Comunitaria

* **Proxecto:** Noutrora Browser (`noutrora.es`).
* **Titularidade e Natureza:** Iniciativa comunitaria de código aberto, cultural e sen ánimo de lucro, **desenvolvida no seo dunha asociación de veciños de Galicia e ofrecida como ben comunal público para que a use quen queira**, sen restricións xeográficas, sen cotas, sen rexistro e sen peaxes.
* **Espírito:** Economía do don, ben común veciñal aberto ao mundo, privacidade sen concesións e respecto á tradición do hipertexto libre de 1994.
* **Ausencia de Explotación Comercial:** O proxecto non comercializa servizos, non insire publicidade, non monetiza o tráfico nin intercambia datos persoais con terceiros baixo ningún concepto.

---

## 2. Principios Fundamentais Aplicados (Art. 5 RGPD)

### A. Principio de Minimización e Cero Recolección (Privacy by Design)
1. **No Navegador Noutrora:**
   - Desactivación estrutural e por política do historial de páxinas visitadas (`places.history.enabled = false`).
   - Bloqueo total de telemetría de Mozilla, estudos Shield, Normandy, informes de fallos (`crashreporter`) e peticións en segundo plano a servidores externos.
   - Conservación local de cookies e sesións unicamente no equipo do usuario para garantir a comodidade sen ruído psicolóxico de inicios de sesión reiterados, protexidas polo illamento estrito de *Total Cookie Protection* e a extensión *uBlock Origin*.
2. **Na Web Oficial (`noutrora.es`):**
   - **Cero Cookies:** A web non xera nin deposita cookies técnicas, de sesión nin de seguimento.
   - **Cero CDNs e Fontes Externas:** Todo o deseño e estilos nútrense de ficheiros propios aloxados no servidor local (`tailwind.js`, `style.css`), sen ligazóns a Google Fonts nin servizos que poidan capturar ou filtrar o enderezo IP das persoas visitantes.
   - **Logs Anónimos de Servidor:** O servidor web non almacena enderezos IP nin pegadas dixitais (*browser fingerprints*). As peticións polo túnel rexístranse exclusivamente baixo o identificador local de loopback `127.0.0.1`.

---

## 3. Rexistro de Actividades de Tratamento (RAT) e DPO

* **Aplicabilidade do Rexistro de Actividades (Art. 30 RGPD):** Ao tratarse dun proxecto sen ánimo de lucro veciñal sen tratamento masivo nin continuado de datos persoais, e que non trata datos sensibles (categorías especiais do Art. 9 RGPD), opera baixo o réxime de exención ao non existir tratamento sistemático nin recolección.
* **Delegado de Protección de Datos (DPO - Art. 37 RGPD):** Non resulta preceptivo o nomeamento dun DPO polo tipo de entidade e a ausencia de tratamento de datos a gran escala.

---

## 4. Canle Oficial para o Exercicio de Dereitos (Dereitos ARSULIPO)

Calquera persoa pode solicitar información, consultar dúbidas ou formular peticións relativas á privacidade a través da canle oficial:

* **Correo electrónico de contacto veciñal:** `intelixenciaaxusta@gmail.com`
* **Tempo de resposta estimado:** Máximo de 30 días naturais segundo a normativa vixente.


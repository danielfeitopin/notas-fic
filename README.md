# Notas FIC

📊 NotasFIC é un proxecto de código aberto que ofrece unha plataforma para visualizar datos históricos de resultados dos diferentes graos da Facultade de Informática da Universidade da Coruña. O proxecto ten como obxectivo proporcionar unha ferramenta útil para estudantes e calquera persoa interesada en analizar a evolución dos resultados académicos ao longo do tempo.

## Como xordeu esta idea?

ℹ️ O portal de estudos da UDC só amosa os datos dos últimos 3 cursos académicos (e ás veces nin sequera xa que están repetidos). Quen non quere revivir vellos tempos e ver como evolucionaron os resultados dos seus graos ao longo dos anos? Ademais, a información histórica é esencial para identificar tendencias, avaliar o rendemento académico e tomar decisións informadas sobre a educación superior.

❓Por outra banda, o formato no que aparecen os datos no portal de estudos dificulta a visualización áxil de preguntas que todos nos facemos, como pode ser *Cal é a asignatura con menor taxa de aprobados do grao?*. Actualmente habería que ir vendo a ollo ata onde alcanza cada barra verde ou mesmo calcular as porcentaxes de aprobados "a man" para todas as asignaturas do grao.

🤔 Se quixeramos comparar os diferentes graos entre si, ou mesmo comparar os resultados de cada grao ao longo dos anos, a tarefa sería aínda máis ardua. No primeiro caso, teríamos que acceder ao portal de estudos para cada grao e comparar os datos visualmente. No segundo caso, teríamos que mudar de lapela entre os anos académicos constantemente.

💡 Polo tanto, o noso proxecto trata de resolver estas limitacións proporcionando unha plataforma centralizada onde os usuarios poden acceder tanto a datos históricos que xa non están dispoñibles no portal de estudos oficial, como a datos de varias titulacións ao mesmo tempo.

## Portal de estudos VS NotasFIC

| Característica                 | Portal de estudos oficial | NotasFIC |
| ------------------------------ | ------------------------- | -------- |
| Datos históricos               | 3 anos (como máximo)                 | Histórico completo      |
| Comparación entre graos        | Manual            | A unha soa ollada |
| Evolución temporal dos resultados | A demasiados clicks de distancia  | Gráficas moi chulas |
| Visualización de métricas fundamentais | Ármate de paciencia | Instantáneo e ao teu gusto |

## As nosas armas ⚒️

| Ferramenta        | Uso no proxecto                         |
| ----------------- | --------------------------------------- |
| Python            | Scrapping, análise de datos e API       |
| Flask             | Framework para a API                    |
| SQLAlchemy        | ORM para a xestión da base de datos     |
| BeautifulSoup     | Scrapping web                           |
| HTML/CSS/JS       | Frontend                                |
| Chart.js          | Biblioteca para gráficos interactivos   |  

## Licencia

📃 Este proxecto está licenciado baixo a [GNU General Public License version 3](<https://opensource.org/license/gpl-3-0>). Pódese atopar unha copia desta licencia no arquivo [LICENSE], e na carpeta [LICENSES].

<div align="center">

| Permisos      | Condicións                     | Limitacións |
| ---------------- | ------------------------------ | ----------- |
| 🟢 Uso Comercial | 🔵 Revelar a fonte              | 🔴 Fiabilidade |
| 🟢 Distribución   | 🔵 Aviso de licenza e "copyright" | 🔴 Garantías  |
| 🟢 Modificación   | 🔵 Mesma licenza                 |             |
| 🟢 Uso de patente  | 🔵 Cambios de estado                |             |
| 🟢 Uso privado    |                                 |             |   

_Táboa baseada en [choosealicense.com](<https://choosealicense.com/licenses/gpl-3.0/>)_

</div>

<details>
<summary> Por que esta licencia? </summary>
 
___
 
- Proteccións xurídicas melloradas
- Consideracións éticas
- Sostenibilidade a longo prazo
 

___

</details>

<details>
<summary> Dependencias empregadas e as súas licencias</summary>

___

<div align="center">

Paquetes de terceiros:

|                  Compoñente                   |               Licencia                |
| :------------------------------------------: | :----------------------------------: |
| [![beautifulsoup4_img]][beautifulsoup4_link] | [![beautifulsoup4_license_badge]](#) |
|          [![Flask_img]][Flask_link]          |     [![Flask_license_badge]](#)      |
|       [![requests_img]][requests_link]       |    [![requests_license_badge]](#)    |
|     [![SQLAlchemy_img]][SQLAlchemy_link]     |   [![SQLAlchemy_license_badge]](#)   |
 
</div>
 
<!-- LINKS -->
[beautifulsoup4_img]: <https://img.shields.io/badge/4.14.3-grey?label=beautifulsoup4&labelColor=blue>
[beautifulsoup4_link]: <https://www.crummy.com/software/BeautifulSoup/bs4/>
[beautifulsoup4_license_badge]: <https://img.shields.io/badge/MIT-green?label=license>

[Flask_img]: <https://img.shields.io/badge/3.1.3-grey?label=Flask&labelColor=blue>
[Flask_link]: <https://flask.palletsprojects.com/en/stable/>
[Flask_license_badge]: <https://img.shields.io/pypi/l/Flask>

[requests_img]: <https://img.shields.io/badge/2.32.5-grey?label=requests&labelColor=blue>
[requests_link]: <https://requests.readthedocs.io/>
[requests_license_badge]: <https://img.shields.io/pypi/l/requests>

[SQLAlchemy_img]: <https://img.shields.io/badge/2.0.47-grey?label=SQLAlchemy&labelColor=blue>
[SQLAlchemy_link]: <https://www.sqlalchemy.org/>
[SQLAlchemy_license_badge]: <https://img.shields.io/pypi/l/SQLAlchemy>

___

</details>

## Limitacións do proxecto

⚠️ Aínda que estamos cheos de boas intencións, o tempo é limitado e o proxecto non é perfecto. Algunhas limitacións a ter en conta:

- Os datos históricos poden non estar completamente actualizados ou poden conter erros, xa que non están dispoñibles no portal de estudos oficial.
- Os gráficos son limitados de momento, pero esperamos que sirvan de exemplo para que outras persoas podan melloralo e adaptalo ás súas necesidades.
- Actualmente só traballamos con datos de 2 graos (GCED e GIA), a modo de exemplo.
- A visualización é fundamentalmente de datos sobre resultados de asignaturas, mais non se inclúen outros datos que poden resultar interesantes e que tamén están dispoñibles no portal de estudos.

## Traballo futuro

🚀 O proxecto está en constante evolución e temos moitas ideas para mellorar e ampliar as funcionalidades. Algúns dos plans futuros inclúen:

- Incluír datos do GEI, que ten moitas máis asignaturas e máis anos académicos.
- Mellorar e ampliar os gráficos para ofrecer unha visualización máis completa e interactiva dos datos.
- Incorporar datos sobre as taxas a nivel de titulación e de centro (se pescudas polo noso código verás que xa dimos algúns pasiños nesa dirección).

## Un chisquiño sobre nós

<div align="center">

**Daniel Feito** (GEI + MUNICS)

Backend (scrapping) e dirección do proxecto.

[![GitHub](https://img.shields.io/badge/GitHub-%23181717?style=for-the-badge&logo=github&logoColor=%23181717&color=white)](<https://github.com/danielfeitopin>)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-white?style=for-the-badge&logo=linkedin&logoColor=white&color=%230A66C2)](<https://www.linkedin.com/in/danielfeitopin/>)

**Lúa Rico** (GCED)

Backend (base de datos e API).

[![GitHub](https://img.shields.io/badge/GitHub-%23181717?style=for-the-badge&logo=github&logoColor=%23181717&color=white)](<https://github.com/l1911>)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-white?style=for-the-badge&logo=linkedin&logoColor=white&color=%230A66C2)](<https://www.linkedin.com/in/lua-rico/>)

**Mario Ozón** (GEI)

Frontend e API.

[![GitHub](https://img.shields.io/badge/GitHub-%23181717?style=for-the-badge&logo=github&logoColor=%23181717&color=white)](<https://github.com/marioozon>)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-white?style=for-the-badge&logo=linkedin&logoColor=white&color=%230A66C2)](<https://www.linkedin.com/in/mario-oz%C3%B3n-casais-42241b273/>)

</div>

## Agradecementos

🫂Este proxecto non tería sido posible sen a colaboración de pequenas persoas anónimas que capturaron os datos do portal de estudos no momento correcto e o compartiron de xeito público no gran [Arquivo de Internet](<https://web.archive.org/>). Grazas a eles, é posible (non sen traballo) recuperar estes datos históricos tan valiosos (sobre todo para os nostálxicos).

## Apoia este proxecto

⭐ Se atopas que este proxecto é útil ou interesante, por favor, considera darlle unha estrela no [repositorio de GitHub]. O teu  apoio axúdanos a mellorar e manter o proxecto!

<!-- LINKS -->
[repositorio de GitHub]: <https://github.com/danielfeitopin/notas-fic>
[LICENSE]: <LICENSE>
[LICENSES]: <./LICENSES>
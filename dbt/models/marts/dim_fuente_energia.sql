{{ config(materialized='table') }}

select distinct
    "EnerSource" as fuente_energia
from {{ source('plata', 'xm_listado_recursos') }}
where "EnerSource" is not null

union

select 'No informado' as fuente_energia

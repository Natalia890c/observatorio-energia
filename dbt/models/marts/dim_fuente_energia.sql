{{ config(materialized='table') }}

select distinct
    fuente_energia
from {{ source('plata', 'xm_listado_recursos') }}
where fuente_energia is not null

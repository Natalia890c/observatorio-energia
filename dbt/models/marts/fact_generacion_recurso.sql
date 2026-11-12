{{ config(materialized='table') }}

select
    g."Date"::date as fecha,
    g.hora,
    g.code as codigo_recurso,
    r.nombre_recurso,
    r.tipo_recurso,
    r.fuente_energia,
    g.valor as generacion
from {{ source('plata', 'xm_generacion') }} g
left join {{ source('plata', 'xm_listado_recursos') }} r
    on g.code = r.codigo_recurso

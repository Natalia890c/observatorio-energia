{{ config(materialized='table') }}

select
    g.fecha::date as fecha,
    g.hora,
    g.code as codigo_recurso,
    r.nombre_recurso,
    r.tipo_recurso,
    r.fuente_energia,
    g.valor as generacion
from {{ source('plata', 'xm_generacion') }} g
left join {{ ref('dim_recurso') }} r
    on g.code = r.codigo_recurso
where g.valor is not null

{{ config(materialized='table') }}

with codigos as (
    select codigo_recurso
    from {{ source('plata', 'xm_listado_recursos') }}
    where codigo_recurso is not null

    union

    select code as codigo_recurso
    from {{ source('plata', 'xm_generacion') }}
    where code is not null
),
catalogo as (
    select
        codigo_recurso,
        max(nombre_recurso) as nombre_recurso,
        max(tipo_recurso) as tipo_recurso,
        max(tipo_despacho) as tipo_despacho,
        max(tipo_recurso_operativo) as tipo_recurso_operativo,
        max(codigo_empresa) as codigo_empresa,
        max(fuente_energia) as fuente_energia,
        max(estado) as estado
    from {{ source('plata', 'xm_listado_recursos') }}
    where codigo_recurso is not null
    group by codigo_recurso
)
select
    c.codigo_recurso,
    r.nombre_recurso,
    r.tipo_recurso,
    r.tipo_despacho,
    r.tipo_recurso_operativo,
    r.codigo_empresa,
    r.fuente_energia,
    r.estado
from codigos c
left join catalogo r
    on c.codigo_recurso = r.codigo_recurso

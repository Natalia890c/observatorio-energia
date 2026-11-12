{{ config(materialized='table') }}

with codigos as (
    select "Code" as codigo_recurso
    from {{ source('plata', 'xm_listado_recursos') }}
    where "Code" is not null

    union

    select code as codigo_recurso
    from {{ source('plata', 'xm_generacion') }}
    where code is not null
),
catalogo as (
    select
        "Code" as codigo_recurso,
        max("Name") as nombre_recurso,
        max("Type") as tipo_recurso,
        max("Disp") as tipo_despacho,
        max("RecType") as tipo_recurso_operativo,
        max("CompanyCode") as codigo_empresa,
        max("EnerSource") as fuente_energia,
        max("State") as estado
    from {{ source('plata', 'xm_listado_recursos') }}
    where "Code" is not null
    group by "Code"
)
select
    c.codigo_recurso,
    r.nombre_recurso,
    r.tipo_recurso,
    r.tipo_despacho,
    r.tipo_recurso_operativo,
    r.codigo_empresa,
    coalesce(r.fuente_energia, 'No informado') as fuente_energia,
    r.estado
from codigos c
left join catalogo r
    on c.codigo_recurso = r.codigo_recurso

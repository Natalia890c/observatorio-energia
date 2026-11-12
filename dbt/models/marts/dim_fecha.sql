{{ config(materialized='table') }}

with fechas as (
    select try_strptime(periodo || '-01', '%Y-%m-%d')::date as fecha
    from {{ source('plata', 'enerandes_ventas') }}

    union

    select fecha::date
    from {{ source('plata', 'xm_precio_bolsa') }}

    union

    select fecha::date
    from {{ source('plata', 'xm_generacion') }}

    union

    select fecha::date
    from {{ source('plata', 'noaa_oni') }}
)
select
    cast(strftime(f.fecha, '%Y%m%d') as integer) as fecha_id,
    f.fecha,
    extract(year from f.fecha)::integer as anio,
    extract(month from f.fecha)::integer as mes,
    strftime(f.fecha, '%B') as nombre_mes,
    extract(quarter from f.fecha)::integer as trimestre,
    extract(day from f.fecha)::integer as dia,
    extract(dow from f.fecha)::integer as dia_semana,
    coalesce(n.fase_enso, 'No informado') as fase_enso,
    n.anomalia_oni
from fechas f
left join {{ source('plata', 'noaa_oni') }} n
    on date_trunc('month', f.fecha) = date_trunc('month', n.fecha)
where f.fecha is not null

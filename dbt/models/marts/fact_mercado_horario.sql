{{ config(materialized='table') }}

with precio as (
    select fecha::date as fecha, hora, valor as precio_bolsa
    from {{ source('plata', 'xm_precio_bolsa') }}
),
demanda as (
    select fecha::date as fecha, hora, valor as demanda_mwh
    from {{ source('plata', 'xm_demanda') }}
)
select
    cast(precio.fecha as date) as fecha,
    precio.hora,
    precio.precio_bolsa,
    demanda.demanda_mwh
from precio
inner join demanda
    on precio.fecha = demanda.fecha
   and precio.hora = demanda.hora

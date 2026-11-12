-- Consulta 1. Evolución mensual del precio de bolsa y la demanda.
select
    date_trunc('month', fecha)::date as mes,
    round(avg(precio_bolsa), 2) as precio_promedio,
    round(avg(demanda_mwh), 2) as demanda_promedio,
    count(*) as registros_horarios
from fact_mercado_horario
group by 1
order by 1;

SELECT 
    Dzielnica, 
    COUNT(ID_oferty) AS Liczba_Ofert,
    ROUND(AVG(Cena_R$), 2) AS Srednia_Cena_Reale,
    ROUND(AVG(Ocena_lokalizacji), 2) AS Srednia_Ocena_Lokalizacji
FROM 
    Tabela_Oferty
GROUP BY 
    Dzielnica
HAVING 
    Liczba_Ofert > 50
ORDER BY 
    Srednia_Cena_Reale DESC
LIMIT 10;
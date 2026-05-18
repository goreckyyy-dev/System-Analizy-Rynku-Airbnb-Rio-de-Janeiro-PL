SELECT 
    Czy_Superhost, 
    COUNT(ID_oferty) AS Liczba_Ofert,
    ROUND(AVG(Cena_R$), 2) AS Srednia_Cena_Reale,
    ROUND(AVG(Ocena_ogolna), 2) AS Srednia_Ocena
FROM 
    Tabela_Oferty
GROUP BY 
    Czy_Superhost;
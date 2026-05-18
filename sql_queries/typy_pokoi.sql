SELECT 
    Typ_pokoju,
    COUNT(ID_oferty) AS Liczba_Ofert,
    ROUND((COUNT(ID_oferty) * 100.0) / (SELECT COUNT(*) FROM Tabela_Oferty), 2) AS Udział_Procentowy,
    ROUND(AVG(Cena_R$), 2) AS Srednia_Cena_R$,
    ROUND(AVG(Minimalna_liczba_nocy), 1) AS Srednia_Min_Nocy
FROM 
    Tabela_Oferty
GROUP BY 
    Typ_pokoju
ORDER BY 
    Liczba_Ofert DESC;
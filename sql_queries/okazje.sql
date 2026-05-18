create view poszukiwanie_okazji as
SELECT 
    Nazwa_oferty,
    Dzielnica,
    Cena_R$,
    Ocena_ogolna,
    Liczba_recenzji
FROM 
    Tabela_Oferty
WHERE 
    Cena_R$ < (SELECT AVG(Cena_R$) FROM Tabela_Oferty) -- Cena poniżej średniej w całym Rio
    AND Ocena_ogolna >= 4.9                             -- Ekstremalnie wysoka ocena gości
    AND Liczba_recenzji >= 10                           -- Oferta sprawdzona przez wielu gości
    AND Dzielnica IN ('Copacabana', 'Ipanema', 'Leblon') -- Najbardziej pożądane turystycznie strefy
ORDER BY 
    Cena_R$ ASC
LIMIT 15;
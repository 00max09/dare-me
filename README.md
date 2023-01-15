# dare-me

## Opis projektu
Zaimplemenotwaliśmy część funkcjonalności naszej strony.
Administratorzy mogą stworzyć challenge i dodać do niego opis, oraz film instruktażowy.
Użytkownicy mogą przeglądać wszystkie filmy, lub tylko filimy pogrupowane po kategorii lub użytkowniku, który je dodał posortowane po liczbie polubień. Użytkownik może polubić dany film. Możliwe jest również zobaczenie 'Hall of fame', w którym wylistowani są użytkownicy z największą sumaryczną liczbą polubień pod ich filmami.

## Aspekty Techniczne
Projekt został napisany przy pomocy biliblioteki 'flask' do pythona, aby uruchomić projekt należy najpierw aktywować virtualEnv (polecenie `x`) a następnie uruchomić aplikację (polecenie `x`). Do przesłanego pliku `.zip` dodaliśmy kilka filmów przykładowych oraz bazę danych z przykładowymi wyzwaniami i użytkownikami. admina
Pod endpointem `/upload_challenge` jest formularz dostępny tylko dla konta admina (konto o loginie "a" oraz haśle "a") w którym admin jest w stanie stworzyć challenge dla określonej kategorii
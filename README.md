# Lukko_ja_Ovikello
Korjasin sysipaskan ruotsalaisen Glue-merkkisen ulko-oven lukon

Lukko otti yhteyttä johonkin serveriin Kiinassa ja se kesti minuutteja.
Kerran se avasi oven ominpäin. Se saattoi myös jumittua, koska moottori
ei saanut tarpeeksi tehoja.

Purin koko paskan ja jäljelle jäi vain moottori ja kotelo.

Ohjaan moottoria 4 releen ESP-01 kortilla ja 12 voltilla
mutta 10 ohmin vastuksen kautta (korjaus: lisäsin siihen toisen 10 ohmin vastuksen sarjaan, koska ulisi rasittavasti). Lukossa oli jonkinlainen anturi, joka
havaitsi millon jumittaa. Minä ajan sitä vain voimalla auki 2 sekunttia ja
kiinni 1 sekunttia, jolloin akseli asemoituu keskelle, ja nuppia
voi käyttää.

Kytkin myös ovikellon optoisolaattorin kautta ESP-01 kortille.
Menusta on mahdollista valita OVIKELLO, jolloinka ovi avautuu heti
kun ovikelloa painaa. Mutta vain kerran. Sisäovi on lukittavissa,
eli tätä voivat käyttää pakettien tuojat. Muuten ovikelloa
pitää rämpyttää tasan 9 kertaa, tai "HEH", jos on viestimies.

Lisäksi yksi rele (3) ohjaa ovitilassa olevaa tuuletinta, mikä
pitää rapusta tulevat käryt rapussa. Hetikohta keksin miten rele (4)
lämäyttä Abloy-oven takas kiinni, mutta pelkkä magneetti ei näytä riittävän.

Lukkoa avatessa pitää ensiksi valita "AU-" ja sitten "KI", jotteivat 
satunnaisesti pingailevat verkkokonnat availe ovea, koska se myös
näkyy tarvittaessa yleisessä internetissä, mikä on huisin kätevää.  Turvallisuus
säilyy sikäli, että lukkoserveri saa virtaa vain jos eteisen
tuulikaapissa on valot.

Parannus: "curl Lukko | grep ring" havaitsee ovikellon, jos esmes on kuullokeet päässä.

<img src=lukko.png>
<img src=screen.png>

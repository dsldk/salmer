Installationsvejledning
=======================

Denne vejledning forklarer, hvordan man får en ny udviklingsmaskine op
at køre med salme-sitet.

Vi antager i det følgende, at dit udgangspunkt er en bruger med
sudo-rettigheder på en helt nyinstalleret maskine, f.eks. en ny KVM-VM,
med Ubuntu Server Edition 18.04. Mutatis mutandis for andre
konfigurationer.

Systemafhængigheder
+++++++++++++++++++

::

    sudo apt update && sudo apt upgrade

    sudo apt install build-essential python-dev python3-venv git  memcached openjdk-8-jre ruby-full gettext postgresql python3 python3-venv davfs2

    # Det sker, at der ikke er dansk locale installeret fra starten.
    sudo locale-gen da_DK.UTF-8

    # Compass
    sudo gem install compass

Under installationen bliver du spurgt, om almindelige brugere skal kunne
mounte WebDAV-mapper. Det er ligemeget, hvad du svarer, eftersom du er
nødt til at mounte som root (fordi vi skal kunne skrive til eXist).

Installér ``eXist``
+++++++++++++++++++

Sitet virker p.t. med ``eXist`` 2.2. Der er ikke gjort noget forsøg på
at få det til at virke på en senere version. Install by whatever means -
en hurtig metode til udvikling er at kopiere ``eXist``-installationen
fra et site, som man har adgang til.

F.eks::

    scp -r salmer.magenta.dk:/srv/dsl/eXist-db .

``eXist`` vil nu kunne startes::

    cd eXist-db
    export EXIST_HOME=$PWD
    bin/startup.sh &
    cd ..

Dette vil sende output til ``stdout`` - send det evt. til en fil i
stedet, eller brug ``byobu`` e.l. til at have flere vinduer åbne i
terminalen.

Du kan nu mounte ``eXist``'s ``apps``-mappe for at oprette en database
til salmesitet, hvis der ikke allerede er en::

    mkdir xml-dbs
    sudo mount -w -t davfs http://localhost:8080/exist/webdav/db/apps ./xml-dbs && sudo chown -R ubuntu:ubuntu xml-dbs && sudo -R chmod a+w ./xml-dbs

Hvis din bruger og gruppe ikke hedder "ubuntu" (hvilket er standard i
``uvtool``), skal du skrive dit eget bruger- og gruppenavn i stedet.

Installér Django og Pyramid
+++++++++++++++++++++++++++

Opret og aktiver virtualenv
---------------------------

::

    git clone git@git.magenta.dk:dsldk/salmer
    cd salmer
    python3 -m venv venv
    source venv/bin/activate


Installér Django-site
---------------------

::

    cd literature_database
    python setup.py develop
    python manage.py makemigrations
    python manage.py migrate

Dette sætter databasen op med en SQLite-database. I koden
(``literature_database/settings.py``) er der et udkommenteret eksempel
på, hvordan det kan sættes op med PostgreSQL, hvis du hellere vil det.

Du kan nu køre admin-sitet med kommandoen::

    python manage.py runserver 0.0.0.0:8000

Hvis du gerne vil logge ind, skal du lave en superbruger til det med
``python manage.py createsuperuser``. Hvis du ikke tilgår sitet via
``localhost``, skal du tilføje hostnavnet i URL'en til ``ALLOWED_HOSTS``
i settings.

Installér Pyramid
-----------------

Hvis du stadig er nede i databasemappen, skal du gå et skridt op og
derefter ned i mappen med Pyramid-sitet::

    cd ..
    cd generic_literature_site/generic_literature_site
    git clone git@git.magenta.dk:dsldk/exist_api.git
    cd ..
    python setup.py develop
    compass compile generic_literature_site/scss
    cd ..


Pyramid-sitet er nu installeret, men før du kan køre det, skal du have
installeret den tilhørende ``eXist``-database::

    sudo cp -r eXist-dbs/salmer ../xml-dbs

Dette skal udføres i roden af mappen ``dsl_site_template``. Du er nu
færdig med selve installationen.

Kør sitet
---------

Du burde nu være klar til at køre sitet::

    cd generic_literature_site
    export DJANGO_SETTINGS_MODULE=literature_database.settings
    pserve development.ini

Du skulle gerne se linjen "Serving on http://0.0.0.0:6543", og du skulle
derfor gerne kunne gå ind på den tilsvarende URL og se sitet.

Konfiguration - eXist og facsimiles
-----------------------------------

Filen ``development.ini`` indeholder defaults, der egner sig til udvikling.

I filen ``production.ini`` er der et eksempel på en mere produktionsegneti
indstilling.

I alle tilfælde skal disse to linjer rettes til den korrekte værdi for din
opsætning::

    exist_server = http://localhost:8080/exist/rest/db/apps/salmer/
    facsimiles = /srv/dsl/facsimiles

Hvis du kører eXist et andet sted end på ``localhost``, skal du
(naturligvis) angive den rigtige URL.

Facsimile-mappen skal pege på, hvor du vælger at lægge facsimiles.

Mappen skal have denne struktur::

    /sti/til/facsimiles
        /<xml_id>
           001.jpg
           002.jpg
           ...

Værdierne af JPEG-filnavnene skal svare til attributten ``facs`` i
XML-teksternes ``<pb>``-tag, altså fx ``facs="001"``.


Appendix: Fix permissions i ``eXist``
+++++++++++++++++++++++++++++++++++++

Du *burde* nu være færdig, som jeg skrev herover, men hvis databasen til
salmesitet er nyoprettet i ``eXist``, får du en fejl, som skyldes at der
ikke er sat execute-permissions på xQuery-scripts.

Dette er muligvis en fejl i ``eXist``, eftersom filerne ligger med
execute-permissions i Git. For at ordne det er vi nødt til at gå ind i
``eXist``'s kommandolinjeklient::

    cd ../../eXist-db
    bin/client.sh -s -u <brugernavn> -P <password>
    cd apps
    cd salmer
    cd xqueries
    chmod check_header_chapters.xquery user=+execute,group=+execute,other=+execute
    # Gentag ovenstående linje for alle de xqueries, du skal bruge
    quit


Hvis du har kopieret data fra et eksisterende salme-site, er dette nok
allerede på plads, men hvis du senere opdaterer med et helt nyt
xQuery-script, kan det igen være nødvendigt at følge ovenstående
procedure.

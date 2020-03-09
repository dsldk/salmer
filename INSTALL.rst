Installationsvejledning
=======================

Denne vejledning forklarer, hvordan man får en ny udviklingsmaskine op at køre med det generiske website baseret på Brandessitet. Når den er afprøvet og vi ved, at alt virker, som det skal, kan den flyttes til kildekoden.

Vi antager i det følgende, at dit udgangspunkt er en bruger med sudo-rettigheder på en helt nyinstalleret maskine, f.eks. en ny KVM-VM, med Ubuntu Server Edition 18.04. Mutatis mutandis for andre konfigurationer.

h2. Systemafhængigheder

<pre>
sudo apt update && sudo apt upgrade

sudo apt install build-essential python-dev python3-venv git  memcached openjdk-8-jre ruby-full gettext postgresql python3 python3-venv davfs2

# Det sker, at der ikke er dansk locale installeret fra starten.
sudo locale-gen da_DK.UTF-8

# Compass
sudo gem install compass
</pre>
Under installationen bliver du spurgt, om almindelige brugere skal kunne mounte WebDAV-mapper. Det er ligemeget, hvad du svarer, eftersom du er nødt til at mounte som root (fordi vi skal kunne skrive til eXist).

h2. Installér @eXist@

Sitet virker p.t. med @eXist@ 2.2. Der er ikke gjort noget forsøg på at få det til at virke på en senere version. Install by whatever means - en hurtig metode til udvikling er at kopiere @eXist@-installationen fra Brandes-sitet.

F.eks 

<pre>
scp -r brandes:/srv/brandes/eXist-db .
</pre>

@eXist@ vil nu kunne startes:
<pre>
cd eXist-db
export EXIST_HOME=$PWD
bin/startup.sh &
cd ..
</pre>

Dette vil sende output til @stdout@ - send det evt. til en fil i stedet, eller brug @byobu@ e.l. til at have flere vinduer åbne i terminalen.

Du kan nu mounte @eXist@'s @apps@-mappe for at oprette en database til det nye site (mere om det nedenunder):
<pre>
mkdir xml-dbs
sudo mount -w -t davfs http://localhost:8080/exist/webdav/db/apps ./xml-dbs && sudo chown -R ubuntu:ubuntu xml-dbs && sudo -R chmod a+w ./xml-dbs
</pre>

Hvis din bruger og gruppe ikke hedder "ubuntu" (hvilket er standard i "@uvtool@":https://help.ubuntu.com/lts/serverguide/cloud-images-and-uvtool.html), skal du skrive dit eget bruger- og gruppenavn i stedet.

h2. Installér Django og Pyramid

h3. Opret og aktiver virtualenv

<pre>
git clone git@git.magenta.dk:dsldk/dsl_site_template
cd dsl_site_template
python3 -m venv venv
source venv/bin/activate
</pre>

h3. Installér Django-site

<pre>
cd literature_database
python setup.py develop
python manage.py makemigrations
python manage.py migrate
</pre>

Dette sætter databasen op med en SQLite-database. I koden (@literature_database/settings.py@) er der et udkommenteret eksempel på, hvordan det kan sættes op med PostgreSQL, hvis du hellere vil det.

Du kan nu køre admin-sitet med kommandoen
<pre>
python manage.py runserver 0.0.0.0:8000
</pre>
Hvis du gerne vil logge ind, skal du lave en superbruger til det med @python manage.py createsuperuser@. Hvis du ikke tilgår sitet via @localhost@, skal du tilføje hostnavnet i URL'en til @ALLOWED_HOSTS@ i settings.

h3. Installér Pyramid

Hvis du stadig er nede i databasemappen, skal du gå et skridt op og derefter ned i mappen med Pyramid-sitet:
<pre>
cd ..
cd generic_literature_site/generic_literature_site
git clone git@git.magenta.dk:dsldk/exist_api.git
cd ..
python setup.py develop
compass compile generic_literature_site/scss
cd ..
</pre>

Pyramid-sitet er nu installeret, men før du kan køre det, skal du have installeret den tilhørende @eXist@-database:

<pre>
sudo cp -r generic-eXist-data ../xml-dbs
</pre>

Dette skal udføres i roden af mappen @dsl_site_template@. Du er nu færdig med selve installationen.

h2. Kør sitet

Du burde nu være klar til at køre sitet:

<pre>
cd generic_literature_site
export DJANGO_SETTINGS_MODULE=literature_database.settings
pserve development.ini
</pre>

Du skulle gerne se linjen "Serving on http://0.0.0.0:6543", og du skulle derfor gerne kunne gå ind på den tilsvarende URL og se sitet.

h2. Appendix: Fix permissions i @eXist@

Du _burde_ nu være færdig, som jeg skrev herover, men faktisk får du en fejl, som skyldes at der ikke er sat execute-permissions på xQuery-scripts i @eXist@.

Dette er muligvis en fejl i @eXist@, eftersom filerne ligger med execute-permissions i Git. For at ordne det, er vi nødt til at gå ind i @eXist@'s kommandolinjeklient:
<pre>
cd ../../eXist-db
bin/client.sh -s -u <brugernavn> -P <password>
cd apps
cd generic-eXist-data
cd xqueries
chmod check_header_chapters.xquery user=+execute,group=+execute,other=+execute
# Gentag ovenstående linje for alle de xqueries, du skal bruge
quit
</pre>

For at køre det helt basale generiske site, som det ser ud i dag, er det kun nødvendigt at ændre betingelser på det ene script, der vises i eksemplet, men lige så snart vi skal manipulere tekster (i et ikke-template-site), skal der sættes på hvert enkelt script, vi får brug for (hvilket er mange af dem, omend ikke dem alle sammen - dette kan vi rydde op i en anden gang).

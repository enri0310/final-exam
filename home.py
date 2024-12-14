import streamlit as st
import utils as utl

utl.setup_page(
    title="Olimpiadi",
    icon="🏅",
    layout="centered",
    css_file="styles.css"
)


col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    st.image(
        "images/logo.svg",
        use_container_width = True
    )

st.markdown(
    "<h1>Gloria e medaglie: scopri le prestazioni olimpiche delle nazioni</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3>Un viaggio attraverso i successi delle nazioni nelle Olimpiadi estive, dal passato glorioso al presente</h3>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p>
    Benvenuto! Questa piattaforma è dedicata a esplorare i medaglieri delle Olimpiadi estive, 
    una celebrazione dello sport che unisce atleti e nazioni da tutto il mondo.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.markdown("""<h3> 📚 Definizione di 'Olimpiade' </h3>""",
            unsafe_allow_html = True)
st.markdown("""
    <div>
    <strong>Olimpìade</strong>  s. f. [dal lat. <em>Olympias -iădis</em>, gr. <em>᾿Ολυμπιάς -άδος</em>] -
        <span style="color: #808080;">1. In età antica: a. Complesso di gare (ginniche, atletiche, ippiche) che si celebravano ogni quattro anni 
            nella città greca di Olimpia, nell’Elide, in occasione delle feste olimpie, a partire dal 776 a. C. e fino al 393 d. C. b. Periodo di 
            tempo di quattro anni che intercorreva fra due successive celebrazioni delle feste e delle gare olimpie; usata fin dal sec. 5° come punto 
            di riferimento cronologico, l’olimpiade fu adottata come base di computo per la datazione ufficiale dallo storico Timeo e divulgata da 
            Eratostene (per es.: la prima o., il 776 a. C.; la seconda o., il 772 a. C., ecc.). </span>
    2. In età moderna (per lo più al plur., le olimpiadi, e spesso con iniziale maiuscola), la più importante manifestazione sportiva per atleti 
            non professionisti, consistente in un complesso di gare internazionali, ispirate agli antichi giochi olimpici, che dal 1896 si svolgono 
            ogni quattro anni in sede diversa: le O. di Atene, di Roma, di Monaco, di Mosca, di Pechino. Dal 1924 si svolgono inoltre le o. invernali,
            anch’esse ogni quattro anni, che sono dedicate agli sport della neve e del ghiaccio e hanno luogo in un paese diverso da quello che 
            organizza i giochi olimpici, con uno scarto di due anni rispetto a questi ultimi.
    <div style="text-align: right;"> - 
    <a href="https://www.treccani.it/vocabolario/olimpiade/">Enciclopedia Treccani</a>
    </div>
    </div>
    """, 
    unsafe_allow_html = True)

st.markdown("---")

st.markdown("""<h3> 🌍 Esplora i medaglieri </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Scopri le sezioni principali per analizzare i dati delle Olimpiadi Estive.
    </p>
    """,
    unsafe_allow_html = True
)

col1, col2, col3 = st.columns(3)
with col1:
    st.image("images/medal_table.png", use_container_width = False)
    if st.button("Vai a medaglie nel Mondo"):
        st.switch_page("app_pages/an_world.py")

with col2:
    st.image("images/europe.png", use_container_width = False)
    if st.button("Vai a Medaglie in Europa"):
        st.switch_page("app_pages/an_eu.py")

with col3:
    st.image("images/medal.webp", use_container_width = False)
    if st.button("Vai a medaglie in Italia"):
        st.switch_page("app_pages/an_italy.py")

st.markdown("---")

st.markdown("""<h3>❓ Il problema delle Nazioni</h3>""", 
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Nel corso della storia delle Olimpiadi, diverse nazioni hanno cambiato nome o subito trasformazioni politiche significative. 
    Questi cambiamenti, visibili nei medaglieri olimpici, non solo riflettono evoluzioni geografiche, ma anche contesti politici e sociali particolari delle epoche in cui sono avvenuti.
    </p>

    <p>
    Uno dei primi casi emblematici riguarda l'<a href="https://en.wikipedia.org/wiki/Australasia_at_the_Olympics">Australasia</a>, una squadra che 
    rappresentava l’unione di <a href="https://en.wikipedia.org/wiki/Australia_at_the_Olympics">Australia</a> e 
     <a href="https://en.wikipedia.org/wiki/New_Zealand_at_the_Olympics">Nuova Zelanda</a>. Successivamente, si è deciso di separare questa rappresentanza, 
    con l’Australia che ha adottato il proprio nome e la Nuova Zelanda che ha partecipato come nazione indipendente, riflettendo così una chiara 
    distinzione tra i due paesi.
    </p>

    <p>
    Altre modifiche hanno riguardato cambiamenti interni o relazioni internazionali che hanno influenzato la partecipazione olimpica di interi gruppi 
    di nazioni. Un caso significativo è quello della <a href="https://en.wikipedia.org/wiki/Bohemia_at_the_Olympics">Boemia</a>, storica regione 
    dell’attuale Repubblica Ceca. Dopo la creazione della <a href="https://en.wikipedia.org/wiki/Czechoslovakia_at_the_Olympics">Cecoslovacchia</a>, 
    il nuovo nome ha rappresentato l’unione con la Slovacchia. Negli anni ’90,  la separazione pacifica dei due paesi ha portato alla nascita di due 
    entità distinte: la <a href="https://en.wikipedia.org/wiki/Czech_Republic_at_the_Olympics">Repubblica Ceca</a> e la 
    <a href="https://en.wikipedia.org/wiki/Slovakia_at_the_Olympics">Slovacchia</a>, ognuna con la propria rappresentanza olimpica.
    </p>

    <p>
    Il caso di <a href="https://en.wikipedia.org/wiki/Republic_of_China_(Formosa)_at_the_1960_Summer_Olympics#:~:text=The%20Republic%20of%20China%20(ROC,Western%20name%20for%20the%20island).">Formosa</a> 
    (l’antico nome di Taiwan) riflette le complesse dinamiche politiche internazionali. Per evitare conflitti diplomatici con la Repubblica Popolare Cinese, 
    Taiwan ha adottato il nome <a href=https://en.wikipedia.org/wiki/Chinese_Taipei_at_the_Olympics">Tapei Cinese</a>, una denominazione neutrale che ha 
    permesso la sua partecipazione alle Olimpiadi.
    </p>

    <p>
    Un esempio peculiare è quello delle <a href="https://simple.wikipedia.org/wiki/British_West_Indies_at_the_Olympics">Federazione delle Indie Occidentali</a>, 
    una federazione di paesi caraibici sotto la corona britannica che partecipò insieme alle Olimpiadi di Roma del 1960 dove conquistò due bronzi provenienti dalla
    delegazione giamaicana.
    </p>
    
    <p> Un altro esempio significativo riguarda il <a href="https://en.wikipedia.org/wiki/Sri_Lanka_at_the_Olympics">Ceylon</a>, 
    nome con cui l'attuale <a href="https://en.wikipedia.org/wiki/Sri_Lanka_at_the_Olympics">Sri Lanka</a> partecipò alle prime edizioni delle Olimpiadi, 
    prima di adottare il nuovo nome dopo la proclamazione della Repubblica nel 1972. 
    Questo cambiamento riflette non solo l'indipendenza del paese dal dominio coloniale britannico, 
    ma anche la volontà di riaffermare un'identità nazionale più radicata nella cultura e nella storia locale. 
    Da allora, il paese ha gareggiato con il nome Sri Lanka, segnando una netta transizione rispetto al passato coloniale. 
    </p>

    <p> 
    La <a href="https://en.wikipedia.org/wiki/Germany_at_the_Olympics">Germania</a> ha una storia olimpica complessa, passando da una delegazione 
    unificata durante la Guerra Fredda come
    <a href="https://en.wikipedia.org/wiki/United_Team_of_Germany_at_the_Olympics">Squadra Unificata Tedesca</a> 
    due comitati separati dal 1968 al 1988 (<a href="https://en.wikipedia.org/wiki/East_Germany_at_the_Olympics">Germania East</a> e 
    <a href="https://en.wikipedia.org/wiki/West_Germany_at_the_Olympics">Germania Ovest</a>). 
    Dopo la riunificazione, la Germania ha partecipato come un'unica nazione, riportando così una rappresentazione olimpica comune.
    </p>

    <p>
    La storia olimpica della <a href="https://en.wikipedia.org/wiki/Russia_at_the_Olympics">Russia</a> 
    e dell'<a href="https://en.wikipedia.org/wiki/Soviet_Union_at_the_Olympics">Unione Sovietica</a> riflette i profondi cambiamenti politici che 
    hanno influenzato la partecipazione olimpica di questi paesi. L'Unione Sovietica ha partecipato alle Olimpiadi dal 1952 al 1991 e, dopo il suo crollo, 
    gli ex sovietici, ad esclusione di Estonioa Lettonia e Lituania, parteciparono insieme con il nome di 
    <a href="https://en.wikipedia.org/wiki/Unified_Team_at_the_Olympics ">Squadra Unificata</a>(CIO)
    alle Olimpiadi del 1992. Successivamente, la Russia ha formato il proprio Comitato Olimpico, ma a Tokyo 2020, a causa delle sanzioni internazionali 
    per il doping di Stato, ha dovuto partecipare come <a href="https://en.wikipedia.org/wiki/Russian_Olympic_Committee#:~:text=On%2019%20February%202021%2C%20it,of%20the%20Russian%20Olympic%20Committee.">Comitato Olimpico Russo</a> (ROC). 
    Questa struttura neutrale è stata creata per consentire agli atleti russi di partecipare sotto una bandiera neutrale, senza simboli nazionali.
    </p>

    <p>
    La <strong>Serbia</strong> e il <strong>Montenegro</strong> hanno una storia olimpica che riflette le loro complesse relazioni politiche e storiche. 
    Entrambi i paesi facevano parte della <a href="https://en.wikipedia.org/wiki/Yugoslavia_at_the_Olympics">Jugoslavia</a> (1920-1992), 
    che partecipò alle Olimpiadi come un'unica nazione. Dopo lo scioglimento della Jugoslavia, formarono insieme la 
    <a href="https://en.wikipedia.org/wiki/Serbia_and_Montenegro_at_the_Olympics">Repubblica Federale di Jugoslavia</a> e 
    parteciparono come "FR Jugoslavia" alle Olimpiadi di Atlanta 1996 e Sydney 2000. Con il cambiamento del nome in 
    <a href="https://en.wikipedia.org/wiki/Serbia_and_Montenegro_at_the_Olympics">Serbia and Montenegro</a> nel 2003, 
    il paese gareggiò insieme nelle Olimpiadi di Atene 2004. Dopo la separazione nel 2006, 
    <a href="https://en.wikipedia.org/wiki/Serbia_at_the_Olympics">Serbia</a> e 
    <a href="https://en.wikipedia.org/wiki/Montenegro_at_the_Olympics">Montenegro</a> hanno partecipato separatamente alle Olimpiadi.
    </p>

    <p>
    Un altro caso interessante è quello della <a href="https://en.wikipedia.org/wiki/Unified_Team_at_the_Olympics">Squadra Unificata</a>, 
    formata dagli atleti provenienti dagli Stati ex-sovietici, che parteciparono alle Olimpiadi del 1992. Dopo il crollo dell'Unione Sovietica nel 1991, 
    i paesi che ne facevano parte non formarono immediatamente comitati olimpici nazionali separati. Pertanto, un gruppo di atleti sovietici gareggiò 
    insieme sotto la bandiera olimpica, senza simboli nazionali, come segno di unità temporanea, mentre i nuovi stati indipendenti, come Estonia, 
    Lettonia e Lituania, parteciparono separatamente.
    </p>
    <p>
    Infine, il cambio di nome della <strong>Macedonia</strong> in <a href="https://en.wikipedia.org/wiki/North_Macedonia_at_the_Olympics">Macedonia del Nord</a> 
    è il risultato di un lungo processo di negoziazione con la Grecia, che contestava l’uso del nome “Macedonia”, associato a una regione storica greca. 
    Questo nuovo nome ha risolto una disputa diplomatica che influenzava anche la partecipazione olimpica del paese.
    </p>

    <p>
    In sintesi, i cambiamenti nei nomi delle nazioni e nelle loro delegazioni olimpiche sono specchio di trasformazioni 
    politiche e sociali che hanno avuto un impatto profondo sul panorama delle competizioni internazionali. 
    Questi eventi continuano a testimoniare l'evoluzione della politica mondiale e la ridefinizione delle identità nazionali.
    </p>
    """,
    unsafe_allow_html = True
)

st.markdown("---")

# Selettore per cambiare nazione tramite slidebar
st.markdown("""<h3>🔧 Modifica Nazione</h3>""", 
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Ai fini dell'analisi, sono state apportate alcune modifiche al dataset originale. In particolare, in accordo con quanto precedentemente spiegato, 
    le seguenti nazioni sono state aggiornate:
    <ul>
        <li><strong>Australasia</strong> è stata unita con <strong>Australia</strong></li>
        <li><strong>Bohemia</strong> è stata integrata in <strong>Cecoslovacchia</strong></li>
        <li><strong>Formosa</strong> è stata sostituita con <strong>Chinese Taipei</strong></li>
        <li><strong>ROC</strong> è stata unificata con <strong>Russia</strong></li>
        <li><strong>Czechoslovakia</strong> è stata lasciata così
        <li>Il nome di <strong>Ceylon</strong> è stato sostituito con <strong>Sri Lanka</strong></li>
        <li><strong>British West Indies</strong> è stata rappresentata da <strong>Jamaica</strong></li>
        <li><strong>FR Jugoslavia</strong> è stata unita con <strong>Serbia and Montenegro</strong></li>
        <li><strong>United Team of Germany</strong> è stata sostituita con <strong>Germany</strong></li>
        <li>Il nome della <strong>Macedonia</strong> è stato cambiato in <strong>North Macedonia</strong>, come riconosciuto a livello internazionale</li>
        <li><strong>Unified Team</strong> è stata sostituita con <strong>Soviet Union</strong></li>
    </ul>
    </p>

    <p>
    Per quanto riguarda altri casi particolari, come quelli dell'Unione Sovietica e dell'ex Jugoslavia, sono stati approfonditi separatamente durante 
    l'analisi del dataset. Inoltre, nel caso della Germania, è stata lasciata la possibilità all'utente di decidere se considerare la nazione 
    come un'unica entità anche durante il periodo della divisione in Geramina Est ed Ovest.
    </p>


    <p>
    Sempre ai fini dell'analisi, alcune delegazioni non riconducibili a una singola nazione sono state escluse dal dataset originale. 
    Questo è stato fatto per mantenere coerenza nei confronti dei medaglieri e delle rappresentanze nazionali. 
    Di seguito sono elencate le delegazioni escluse:
    <ul>
        <li><a href="https://en.wikipedia.org/wiki/Mixed_team_at_the_Olympics">Mixed team</a>: 
            squadre composte da atleti di diverse nazioni, partecipanti alle prime edizioni dei Giochi Olimpici.
        </li>
        <li><a href="https://en.wikipedia.org/wiki/Independent_Olympic_Participants">Independent Olympic Participants</a>: 
            atleti che hanno gareggiato sotto una bandiera neutrale a causa di problemi geopolitici o sanzioni internazionali.
        </li>
        <li><a href="https://en.wikipedia.org/wiki/Refugee_Olympic_Team">Refugee Olympic Team</a>: una delegazione speciale 
            formata da atleti rifugiati, introdotta per la prima volta alle Olimpiadi di Rio 2016.
        </li>
        <li><a href="https://en.wikipedia.org/wiki/Individual_Neutral_Athletes">Individual Neutral Athletes</a>: atleti 
            che hanno partecipato senza rappresentare il loro paese per ragioni politiche o disciplinari.
        </li>
        <li><a href="https://en.wikipedia.org/wiki/Independent_Olympic_Athletes">Independent Olympic Athletes</a>: simile ai 
            partecipanti neutrali, include atleti di nazioni prive di un comitato olimpico attivo o riconosciuto.
        </li>
    </ul>
    </p>
    <p>
    Queste esclusioni sono state effettuate per focalizzarsi sulle prestazioni delle nazioni tradizionali e moderne, garantendo un'analisi coerente 
    del medagliere.
    </p>

    """,
    unsafe_allow_html = True
)

st.markdown("---")

st.markdown("""<h3>💬 Esplora, scopri, condividi</h3>""", 
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Questa piattaforma è il punto di partenza per scoprire storie e curiosità sulle Olimpiadi. 
    Naviga tra i dati, approfondisci i successi delle nazioni e lasciati ispirare dal mondo dello sport.
    </p>
    """,
    unsafe_allow_html = True)

st.markdown("---")

# Sezione Fonti e Crediti
st.markdown("""<h3>📌 Fonti</h3>""",
            unsafe_allow_html=True)
st.markdown(
    """
    <p>
        Le informazioni sui medaglieri sono state raccolte da dati pubblici disponibili su 
        <a href="https://en.wikipedia.org/wiki/Main_Page">
        Wikipedia</a>.
        <br>
        Per trasparenza e per permettere ulteriori analisi, puoi scaricare tutti i file CSV utilizzati in un unico archivio.
    </p>
    """,
    unsafe_allow_html = True
)

'''col1, col2, col3 = st.columns([2, 2, 2])  # Tre colonne, la centrale più larga
with col2:
    with open("dataframes/dataframes.zip", "rb") as fp:
        btn = st.download_button(
            label = "📂 Scarica i dati",
            data = fp,
            file_name = "dataframes.zip",
            mime = "application/zip",
            use_container_width = True
        )'''


# Footer
st.markdown(
    """
    <div class="footer">
        © 2024 - Creato usando <a href="https://streamlit.io/">Streamlit</a> 
        <br>Created by <b>Enrico Sorgato</b>
    </div>
    """,
    unsafe_allow_html = True
)

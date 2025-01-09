import streamlit as st
import utils as utl

utl.setup_page(
    title = "Dataset",
    icon = "🗂️",
    layout = "centered"
)

st.title("Informazioni utili sui dataset utilizzati 🚀")

st.markdown(
    """
    <hr style = "margin-top: 0; margin-bottom: 0; height: 2px; border: none; background-color: #1f77b4;">
    <br>
    """, 
    unsafe_allow_html = True
)

#SEZIONE ORIGINE DATASET
st.markdown(
    """
    <div style="background-color: #f0f8ff; border-radius: 10px;">
    <h2> Origine dei dataset </h2>
    </div>
    <br>
    """,
    unsafe_allow_html = True
)


st.markdown("""<h3> 🔍 Dataset delle medaglie olimpiche </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Questo dataset è stato creato estraendo i dati relativi alle nazioni membri dell'Unione Europea da 
    <a href = "https://en.wikipedia.org/wiki/Member_state_of_the_European_Union">Wikipedia</a>. 
    Dopo aver rimosso le note e tutti i riferimenti aggiuntivi per rendere i dati tidy e aver uniformato i nomi delle nazioni per garantire coerenza 
    con gli altri dataset utilizzati, si ottiene un dataset pulito e pronto per l'analisi dei dati europei.
    </p>
    """, 
    unsafe_allow_html = True
)


st.markdown("""<h3> 🏙️ Dataset delle città ospitanti </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Il dataset delle città ospitanti delle Olimpiadi è stato creato partendo dalla tabella presente su 
    <a href = "https://en.wikipedia.org/wiki/List_of_Olympic_Games_host_cities">Wikipedia</a>. 
    Sono state selezionate le colonne rilevanti per l'analisi e i dati sono stati ripuliti per eliminare eventuali ambiguità. 
    Il risultato finale è un dataset che offre una panoramica chiara delle città e delle nazioni che hanno ospitato 
    le edizioni estive dei giochi olimpici.
    </p>
    """, 
    unsafe_allow_html = True
)


st.markdown("""<h3> 🌍 Dataset dei Paesi Europei </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Questo dataset è stato creato estraendo i dati relativi alle nazioni membri dell'Unione Europea da 
    <a href = "https://en.wikipedia.org/wiki/Member_state_of_the_European_Union">Wikipedia</a>. 
    Dopo aver rimosso le note e tutti i riferimenti aggiuntivi per rendere i dati tidy e aver uniformato i nomi delle nazioni per garantire 
    coerenza con gli altri dataset utilizzati, si ottiene un dataset pulito e pronto per l'analisi dei dati europei.
    </p>
    """, 
    unsafe_allow_html=True
)


st.markdown("""<h3> 🏅 Dataset delle medaglie italiane a Parigi 2024 </h3>""",
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Questo dataset è stato creato a partire dalle informazioni contenute nell'articolo di
    <a href = "https://www.eurosport.it/olimpiadi/olimpiadi-parigi-2024/2024/giochi-olimpici-italia-da-quali-regioni-arrivano-le-40-medaglie_sto20028615/story.shtml" target="_blank">Eurosport</a>. 
    L'articolo descrive la provenienza degli atleti italiani che hanno vinto almeno una medaglia durante le Olimpiadi di Parigi 2024 specificando per 
    ciascuno il tipo di medaglia conquistata e ulteriori dettagli sulla città di appartenenza. Per consentire l'estrazione dei dati, l'articolo è stato
    salvato in un file chiamato 'italy2024.txt'. Grazie alla sua struttura organizzata per regione, è stato possibile ricavare il dataset
    finale il quale include le seguenti informazioni: nome dell'atleta, città e regione di nascita, numero di medaglie d'oro, argento, bronzo e il 
    totale delle medaglie conquistate.
    </p>
    """, 
    unsafe_allow_html = True
)



st.markdown(
    """
    <hr style = "margin-top: 0; margin-bottom: 0; height: 2px; border: none; background-color: #1f77b4;">
    <br>
    """, 
    unsafe_allow_html = True
)



#SEZIONE PROBLEMI
st.markdown(
    """
    <div style="background-color: #f0f8ff; border-radius: 10px;">
    <h2> Problematiche riscontrate </h2>
    </div>
    <br>
    """,
    unsafe_allow_html = True
)


st.markdown("""<h3>❓ Il problema delle nazioni</h3>""", 
            unsafe_allow_html = True)
st.markdown(
    """
    <p>
    Nel corso della storia delle Olimpiadi diverse nazioni hanno cambiato nome o subito trasformazioni politiche significative. 
    Questi cambiamenti visibili nei medaglieri olimpici non solo riflettono evoluzioni geografiche, ma anche contesti politici e sociali particolari 
    delle epoche in cui sono avvenuti.
    </p>

    <p>
    Uno dei primi casi emblematici riguarda l'<a href = "https://en.wikipedia.org/wiki/Australasia_at_the_Olympics">Australasia</a>, una squadra che 
    rappresentava l’unione di <a href = "https://en.wikipedia.org/wiki/Australia_at_the_Olympics">Australia</a> e 
    <a href = "https://en.wikipedia.org/wiki/New_Zealand_at_the_Olympics">Nuova Zelanda</a>. Successivamente si è deciso di separare questa rappresentanza: 
    l’Australia che ha adottato il proprio nome, mentre la Nuova Zelanda ha partecipato come nazione indipendente, riflettendo così una chiara 
    distinzione tra i due paesi.
    </p>

    <p>
    Altre modifiche hanno riguardato cambiamenti interni o relazioni internazionali che hanno influenzato la partecipazione olimpica di interi gruppi 
    di nazioni. Un caso significativo è quello della <a href = "https://en.wikipedia.org/wiki/Bohemia_at_the_Olympics">Boemia</a>, storica regione 
    dell’attuale Repubblica Ceca. Dopo la creazione della <a href = "https://en.wikipedia.org/wiki/Czechoslovakia_at_the_Olympics">Cecoslovacchia</a>, 
    il nuovo nome ha rappresentato l’unione con la Slovacchia. Negli anni ’90  la separazione pacifica dei due paesi ha portato alla nascita di due 
    entità distinte: la <a href = "https://en.wikipedia.org/wiki/Czech_Republic_at_the_Olympics">Repubblica Ceca</a> e la 
    <a href = "https://en.wikipedia.org/wiki/Slovakia_at_the_Olympics">Slovacchia</a>, ognuna con la propria rappresentanza olimpica.
    </p>

    <p>
    Il caso di <a href = "https://en.wikipedia.org/wiki/Republic_of_China_(Formosa)_at_the_1960_Summer_Olympics#:~:text=The%20Republic%20of%20China%20(ROC,Western%20name%20for%20the%20island).">Formosa</a> 
    (l’antico nome di Taiwan) riflette le complesse dinamiche politiche internazionali. Per evitare conflitti diplomatici con la Repubblica Popolare Cinese, 
    Taiwan ha adottato il nome <a href = https://en.wikipedia.org/wiki/Chinese_Taipei_at_the_Olympics">Tapei Cinese</a>, una denominazione neutrale che ha 
    permesso la sua partecipazione alle Olimpiadi.
    </p>

    <p>
    Un esempio peculiare è quello delle <a href = "https://simple.wikipedia.org/wiki/British_West_Indies_at_the_Olympics">Federazione delle Indie Occidentali</a>, 
    una federazione di paesi caraibici sotto la corona britannica che partecipò insieme alle Olimpiadi di Roma del 1960 dove conquistò due bronzi provenienti dalla
    delegazione giamaicana.
    </p>
    
    <p> Un altro esempio significativo riguarda il <a href = "https://en.wikipedia.org/wiki/Sri_Lanka_at_the_Olympics">Ceylon</a>, 
    nome con cui l'attuale <a href = "https://en.wikipedia.org/wiki/Sri_Lanka_at_the_Olympics">Sri Lanka</a> partecipò alle prime edizioni delle Olimpiadi 
    prima di adottare il nuovo nome dopo la proclamazione della Repubblica nel 1972. 
    Questo cambiamento riflette non solo l'indipendenza del paese dal dominio coloniale britannico, 
    ma anche la volontà di riaffermare un'identità nazionale più radicata nella cultura e nella storia locale. 
    Da allora il paese ha gareggiato con il nome Sri Lanka, segnando una netta transizione rispetto al passato coloniale. 
    </p>

    <p> 
    La <a href = "https://en.wikipedia.org/wiki/Germany_at_the_Olympics">Germania</a> ha una storia olimpica complessa passando da una delegazione 
    unificata durante la Guerra Fredda come
    <a href = "https://en.wikipedia.org/wiki/United_Team_of_Germany_at_the_Olympics">Squadra Unificata Tedesca</a> 
    due comitati separati dal 1968 al 1988 (<a href = "https://en.wikipedia.org/wiki/East_Germany_at_the_Olympics">Germania East</a> e 
    <a href = "https://en.wikipedia.org/wiki/West_Germany_at_the_Olympics">Germania Ovest</a>). 
    Dopo la riunificazione la Germania ha partecipato come un'unica nazione riportando così una rappresentazione olimpica comune.
    </p>

    <p>
    La storia olimpica della <a href = "https://en.wikipedia.org/wiki/Russia_at_the_Olympics">Russia</a> e 
    dell'<a href = "https://en.wikipedia.org/wiki/Soviet_Union_at_the_Olympics">Unione Sovietica</a> riflette i profondi cambiamenti politici che hanno 
    influenzato la loro partecipazione ai giochi olimpici. Prima della Rivoluzione del 1917, la Russia partecipò come 
    <a href = "https://en.wikipedia.org/wiki/Russian_Empire_at_the_Olympics">Impero Russo</a>. Dal 1952 al 1991, invece, prese parte alle Olimpiadi come Unione Sovietica, 
    dominando spesso il medagliere. Dopo il crollo dell'URSS, gli atleti delle ex repubbliche sovietiche, ad eccezione di Estonia, Lettonia e Lituania, 
    gareggiarono insieme come <a href = "https://en.wikipedia.org/wiki/Unified_Team_at_the_Olympics">Squadra Unificata</a> (Unified Team) alle Olimpiadi del 1992. 
    Successivamente, la Russia costituì il proprio Comitato Olimpico e partecipò come nazione indipendente. Tuttavia, a causa delle sanzioni internazionali 
    per il doping di Stato, agli atleti russi fu imposto di competere sotto una bandiera neutrale ai Giochi di Tokyo 2020, rappresentando il 
    <a href = "https://en.wikipedia.org/wiki/Russian_Olympic_Committee#:~:text=On%2019%20February%202021%2C%20it,of%20the%20Russian%20Olympic%20Committee.">Comitato Olimpico Russo</a> (ROC). 
    Questa struttura neutrale è stata creata per consentire agli atleti russi di partecipare senza utilizzare simboli o bandiere nazionali ufficiali.
    </p>

    <p>
    La <strong>Serbia</strong> e il <strong>Montenegro</strong> hanno una storia olimpica che riflette le loro complesse relazioni politiche e storiche. 
    Entrambi i paesi facevano parte della <a href = "https://en.wikipedia.org/wiki/Yugoslavia_at_the_Olympics">Jugoslavia</a> (1920-1992), 
    che partecipò alle Olimpiadi come un'unica nazione. Dopo lo scioglimento della Jugoslavia, formarono insieme la 
    <a href = "https://en.wikipedia.org/wiki/Serbia_and_Montenegro_at_the_Olympics">Repubblica Federale di Jugoslavia</a> e 
    parteciparono come "FR Jugoslavia" alle Olimpiadi di Atlanta 1996 e Sydney 2000. Con il cambiamento del nome in 
    <a href = "https://en.wikipedia.org/wiki/Serbia_and_Montenegro_at_the_Olympics">Serbia and Montenegro</a> nel 2003, 
    il paese gareggiò insieme nelle Olimpiadi di Atene 2004. Dopo la separazione nel 2006, 
    <a href = "https://en.wikipedia.org/wiki/Serbia_at_the_Olympics">Serbia</a> e 
    <a href = "https://en.wikipedia.org/wiki/Montenegro_at_the_Olympics">Montenegro</a> hanno partecipato separatamente alle Olimpiadi.
    </p>

    <p>
    Infine il cambio di nome della <strong>Macedonia</strong> in <a href = "https://en.wikipedia.org/wiki/North_Macedonia_at_the_Olympics">Macedonia del Nord</a> 
    è il risultato di un lungo processo di negoziazione con la Grecia che contestava l’uso del nome 'Macedonia' associato a una regione storica greca. 
    Questo nuovo nome ha risolto una disputa diplomatica che influenzava anche la partecipazione olimpica del paese.
    </p>

    <p>
    In sintesi i cambiamenti nei nomi delle nazioni e nelle loro delegazioni olimpiche sono specchio di trasformazioni 
    politiche e sociali che hanno avuto un impatto profondo sul panorama delle competizioni internazionali. 
    Questi eventi continuano a testimoniare l'evoluzione della politica mondiale e la ridefinizione delle identità nazionali.
    </p>
    """,
    unsafe_allow_html = True
)


st.markdown("""<h3>🔧 Modifica nazione</h3>""", 
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
        <li><strong>ROC</strong> e <strong>Russian Empire</strong> son stati unificati con la <strong>Russia</strong></li>
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
    Il caso dell'Unione Sovietica è stato trattato in modo approfondito in una sezione separata dell'analisi del dataset, mentre nel caso della Germania 
    è stata lasciata la possibilità all'utente di decidere se considerare la nazione come un'unica entità anche durante il periodo della divisione in 
    Geramina Est ed Ovest.
    </p>

    <p>
    Sempre ai fini dell'analisi alcune delegazioni non riconducibili a una singola nazione sono state escluse dal dataset originale. 
    Questo è stato fatto per mantenere coerenza nei confronti dei medaglieri e delle rappresentanze nazionali. 
    Di seguito sono elencate le delegazioni escluse:
    <ul>
        <li><a href = "https://en.wikipedia.org/wiki/Mixed_team_at_the_Olympics">Mixed team</a>: 
            squadre composte da atleti di diverse nazioni, partecipanti alle prime edizioni dei Giochi Olimpici.
        </li>
        <li><a href = "https://en.wikipedia.org/wiki/Independent_Olympic_Participants">Independent Olympic Participants</a>: 
            atleti che hanno gareggiato sotto una bandiera neutrale a causa di problemi geopolitici o sanzioni internazionali.
        </li>
        <li><a href = "https://en.wikipedia.org/wiki/Refugee_Olympic_Team">Refugee Olympic Team</a>: una delegazione speciale 
            formata da atleti rifugiati, introdotta per la prima volta alle Olimpiadi di Rio 2016.
        </li>
        <li><a href = "https://en.wikipedia.org/wiki/Individual_Neutral_Athletes">Individual Neutral Athletes</a>: atleti 
            che hanno partecipato senza rappresentare il loro paese per ragioni politiche o disciplinari.
        </li>
        <li><a href = "https://en.wikipedia.org/wiki/Independent_Olympic_Athletes">Independent Olympic Athletes</a>: simile ai 
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


st.markdown(
    """
    <hr style = "margin-top: 0; margin-bottom: 0; height: 2px; border: none; background-color: #1f77b4;">
    <br>
    """, 
    unsafe_allow_html = True
)


#footer
st.markdown(
    """
    <div class = "footer">
    Creato con ❤️ da <b>Enrico Sorgato</b> © 2025
    </div>
    """,
    unsafe_allow_html = True
)
# REALIZZAZIONE DI UN DATABASE CON RELATIVO SITO WEB PER LA RACCOLTA DI SEQUENQUE DI RNA

Il progetto si pone come obiettivo l'implementazione di un database dove mantenere le informazioni relative alle molecole di RNA,
e la realizzazione di un sito web che consenta agli utenti di accedere ad esse, con la possibilità di scaricare: oltre alle informazioni sulle molecole,
i file ad esse relative.

Per l'implementazione del db si è scelto un approccio NoSQL con [MongoDB](https://www.mongodb.com/home), e per questo sono stati realizzati degli script in Python per creare 
i documenti delle molecole di rna da caricarvi. Gli script sono gestiti da un menu che permette di effettuare diverse scelte tra cui: l'inserimento dei file su mongodb
realizzando un JSON a partire da un file .txt (con valori separati da tabulazione) contenente le informazioni da inserire, la modifica di un singolo campo di un
documento, l'eliminazione di un solo documento o dell'intera collection. 

Per l'implementazione del sito web si è utilizzato [Flask](https://flask.palletsprojects.com/en/2.2.x/), un framework per realizzare siti web con Python.
Per collegare il sito web al db ed effettuare operazioni di ricerca dei dati, sono stati usati i "tools" [pandas](https://pandas.pydata.org/) e [PyMongo](https://pymongo.readthedocs.io/en/stable/).  


## Installation

Per far funzionare gli script per la gestione del db è necessario installare tramite [pip](https://pip.pypa.io/en/stable/) il tool PyMongo.

```bash
pip install pymongo
```

Per far far funzionare il codice del sito web bisogna installare tutti i tools presenti nel file requirements.txt.

## Usage

Per poter utilizzare gli script per la creazione e l'inserimento di sequenze di rna nel db bisogna passare allo script un file txt (separato da tab) contenente le
sequenze di molecole, con relative informazioni nel seguente ordine: Db name, Organism name, Length, Unpaired bases, Paired bases, Is Pseudoknotted, 
Pseudoknot order, Rna Type, Benchmark ID, Genus, Core, Core plus, Shape, Is validated, Link db.
Nel caso in cui una sequenza presenti uno o più campi che non hanno valore (rimane vuoto), inserire la stringa di caratteri: --
Per poter prendere il campo del db relativo all'accession number bisogna mettere nella cartella ct_files del progetto i files ct (con header) delle molecole.

Per poter utilizzare correttamente il sito web bisogna configurare, nel file config.py, i path delle cartelle contenenti i file con le varie estensioni 
(dbn, ct, bpseq e fasta).

## Update Taxonomy files

Per fare l'aggiornamento dei file con le varie tassonomie (SILVA, ENA, GTDB, LTP, NCBI), bisogna: 
  - andare sul sito di [SILVA](https://www.arb-silva.de/), da qui selezionare Download Archive e andare all'utltima release (ad oggi, 12/12/2022, è la release_138.1);
    da qui andare in Exports e poi in taxonomy, dove troviamo i file per le tassonomie:
      - SILVA: taxmap_slv_lsu_ref_#numeroultimarelease.txt.gz e taxmap_slv_ssu_ref_#numeroultimarelease.txt.gz
      - NCBI: da qui entrare nella cartella ncbi e prendere: taxmap_ncbi_lsu_ref_#numeroultimarelease.txt.gz e taxmap_ncbi_ssu_ref_#numeroultimarelease.txt.gz
      - ENA: da qui entrare nella cartella ncbi e prendere: taxmap_embl-ebi_ena_lsu_ref_#numeroultimarelease.txt.gz e 
        taxmap_embl-ebi_ena_ssu_ref_#numeroultimarelease.txt.gz
    Dentro la cartella ncbi in taxonomy si trovano anche i file utilizzati per associare ad ogni singolo taxa il proprio rank. 
    I file si chiamano: tax_ncbi_lsu_ref_#numeroultimarelease.txt.gz e tax_ncbi_ssu_ref_#numeroultimarelease.txt.gz
  - andare sul sito di [LTP](https://imedea.uib-csic.es/mmg/ltp/#Downloads) e selezionare il file (es. LTP database in csv format)
  - andare sul sito di [GTDB](https://gtdb.ecogenomic.org/downloads), cliccare il link sotto la colonna Primary nella tabella chiamata GTDB data files; 
    da qui selezionare releases -> latest -> ar53_taxonomy.tsv e bac120_taxonomy.tsv
  Tutti i file presi devono essere in formato csv e devono avere 2 colonne, con questi nomi e nel seguente ordine: taxonomy (stringa con la tassonomia dove i taxa
  sono divisi da ;) e organism name. 
  Ottenuti i file in csv va eseguito lo script: remove_duplicates.py per rimuovere tutti i duplicati, e successivamente il merge_file.py per unire i file con lsu nel
  nome con i rispettivi ssu, per ogni tassonomia.
  Alla fine bisogna avere solo 5 file per le tassonomie (dovranno chiamarsi: silva_taxonomy.csv, ena_taxonomy.csv, e così via per tutte e 5 le tassonomie)
  che andranno messi nella cartella files/taxonomy del progetto.
  
  Infine, per il file contente i taxa e il loro rank, bisogna: 
    - prendere il file come specificato sopra;
    - rimuovere la colonna centrale (column 2);
    - della prima colonna, separare da tutta la stringa l'ultima parola (corrispondente al taxa); 
      es. root;cellular organisms;Archaea;Euryarchaeota;Diaforarchaea group;Thermoplasmata;Thermoplasmatales;Thermoplasmataceae;Thermoplasma; -> Thermoplasma 
    - il file finale, deve avere come prima colonna il taxa e come seconda colonna il rank, deve chiamarsi: TaxaName_TaxaRank.txt (con valori separati da tab) e andrà
      messo nella cartella files del progetto.

## License

[MIT](https://choosealicense.com/licenses/mit/)

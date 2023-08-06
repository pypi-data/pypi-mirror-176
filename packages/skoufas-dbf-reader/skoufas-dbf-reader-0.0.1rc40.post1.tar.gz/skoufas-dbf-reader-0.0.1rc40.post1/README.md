# Skoufas Library DBF Reader

Functions to read and convert from the DBF file used to track books in the Skoufas library

## Columns in DBF file

| Column | Name (english) | Name (Greek) |
|--------|----------------|--------------|
| A01 | Author surname, name, language | ΕΠΩΝΥΜΟ,ΟΝΟΜΑ ΣΥΓΓΡΑΦΕΑ |
| A02 | title | Τιτλος |
| A03 | subtitle | Υποτιτλος |
| A04 | Dewey | Ταξινομικος αριθμος |
| A05 | entry_number | αριθμος εισαγωγης |
| A06 | translator, edition, entry_number | μεταφραστης, εκδοση, αριθμος εισαγωγης |
| A07 | edition | εκδοση |
| A08 | editor | εκδοτης |
| A09 | edition place | τοπος εκδοσης |
| A10 | edition date | ετος εκδοσης |
| A11 | pages | σελιδες |
| A12 | topics | θεμα 1 |
| A13 | topics | θεμα 2 |
| A14 | topics | θεμα 3 |
| A15 | topics | θεμα 4 |
| A16 | curator | επιμελητης |
| A17 | notes | σημειωσεις (συνηθως αν είναι δωρεες) |
| A18 | material | συνοδευτικο υλικο |
| A19 | isbn | |
| A20 | Notes | σημειωσεις |
| A21 | series | Σειρα |
| A22 | | θεσεις κλειδια |
| A23 | | θεσεις κλειδια |
| A24 | | θεσεις κλειδια |
| A25 | | θεσεις κλειδια |
| A26 | | θεσεις κλειδια |
| A27 | | θεσεις κλειδια |
| A28 | | θεσεις κλειδια |
| A29 | | θεσεις κλειδια |
| A30 | | θεσεις κλειδια |

## Checks required

- Duplicated Entry Numbers (~800)
- Non-numeric entry numbers (~130)
- Missing entry numbers (~200)
- Weird author names
    - 12760EZ,GABRIEL GARCIA
    - 15767ΗΓΟΠΟΥΛΟΣ,ΧΡΗΣΤΟΣ
- Weird deweys and replacements (~300)
- Loan -> Book Entry or Entry number?
- Translator corrections

## Columns required

### BookEntry

- Title
- Subtitle
- DeclaredAuthors
- Dewey
- Edition
- EditionDate
- EditorId (FK: Editor)
- CuratorId (FK: Curator)
- Pages
- PagesText
- Volumes
- Notes
- Material
- HasCD
- HasDVD
- ISBN

### Author

- Name
- Surname
- Middlename
- Fullname

### Authorship (Many-to-Many)

- AuthorId (FK: Author)
- BookEntryId (FK: BookEntry)

### Translator

- Name
- Surname
- Middlename
- Fullname

### Curator

- Name
- Surname
- Middlename
- Fullname

### Editor

- Name
- Place

### Translation

- TranslatorId (FK: Translator)
- BookEntryId (FK: BookEntry)

### Entry Numbers (one-to-many)

- Number (unique)
- BookEntryId (FK: BookEntry)

### Topic

- Name

### BookInTopic (many-to-many)

- TopicId (FK: Topic)
- BookEntryId (FK: BookEntry)

### Donor

- Name
- Surname
- Middlename
- Fullname

### Donation (Many-to-Many)

- DonorId (FK: Donor)
- BookEntryId (FK: BookEntry)

### Customer

- Name
- Surname
- Middlename
- FullName
- IdNumber
- IdType
- PhoneNumber
- Email

### Loan

- CustomerId (FK: Customer)
- BookEntryId (FK: BookEntry)
- StartDateTime
- EndDateTime
- Note

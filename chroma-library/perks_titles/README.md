# earth_perks_titles.py in topic parts

The Library's titles and perks, cut by kind and volume (Token-saving step 5, 10-18). These parts are the source.
`python3 -B build.py earth` (the Library's build.py, in the shared folder) joins them in name order, byte for byte,
into ../earth_perks_titles.py, which the engine and the game read. Edit a part here, never the joined file. Read
00-head.py once for the field list; each other part is one kind (career, partner, skill, asset ...) of one volume.
